import webview
import cv2
import numpy as np
import threading
import base64
import math
import sqlite3
import datetime

class PrecisionScopeAPI:
    def __init__(self):
        # Proteção contra o erro de limite de recursão do Windows
        self._window = None
        self._camera_thread = None
        self.running = False
        self.current_frame_base64 = None
        self.frame_shape = None
        
        # Banco de Dados
        self.db_path = "precision_scope.db"
        self._inicializar_banco()
        
        # Estado do Sistema
        self.usuario_atual = None
        self.distancia_metros = 10.0
        self.valor_clique_moa = 0.25 
        
        # Medidas Reais do Alvo
        self.LARGURA_ALVO_CM = 38.5
        self.ALTURA_ALVO_CM = 55.5
        
        # Variáveis de Visão Computacional
        self.poa_pixel = None
        self.poa_td_pixel = None
        self.poi_td_pixel = None
        self.pts_src = None
        self.H_td = None
        self.img_topdown = None
        self.frame_referencia = None
        self.frame_congelado = None
        self.pois_rejeitados = []
        self.estado_atual = "MENU"
        
        # Objetos do OpenCV protegidos
        self._aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self._aruco_params = cv2.aruco.DetectorParameters()

        try:
            with np.load('calibracao_camera.npz') as data:
                self._mtx = data['mtx']
                self._dist = data['dist']
        except:
            self._mtx, self._dist = None, None

    def set_window(self, window):
        self._window = window

    def iniciar_sistema(self):
        if not self.running:
            self.running = True
            self._camera_thread = threading.Thread(target=self.loop_captura_camera)
            self._camera_thread.daemon = True
            self._camera_thread.start()
            return {"status": "ok", "msg": "Iniciando conexão com a câmera..."}
        return {"status": "ok", "msg": "Sistema já em execução."}

    def _inicializar_banco(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, senha TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS historico 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, arma TEXT, 
            distancia REAL, clique TEXT, dir_h TEXT, cl_h INTEGER, 
            dir_v TEXT, cl_v INTEGER, data TEXT, 
            FOREIGN KEY(user_id) REFERENCES usuarios(id))''')
        conn.commit()
        conn.close()

    def cadastrar_usuario(self, nome, email, senha):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conn.commit()
            conn.close()
            return {"status": "sucesso", "msg": "Usuário cadastrado com sucesso!"}
        except Exception as e:
            return {"status": "erro", "msg": str(e)}

    def fazer_login(self, nome, senha):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
        user = cursor.fetchone()
        conn.close()
        if user:
            self.usuario_atual = {"id": user[0], "nome": user[1]}
            return {"status": "sucesso", "user": user[1]}
        return {"status": "erro", "msg": "Usuário ou senha incorretos."}

    def salvar_setup_sessao(self, distancia, clique_moa):
        self.distancia_metros = float(distancia)
        self.valor_clique_moa = float(clique_moa)
        self.estado_atual = "AGUARDANDO_POA"
        return {"status": "ok"}

    def buscar_historico(self):
        """Busca o histórico do usuário logado"""
        if not getattr(self, 'usuario_atual', None):
            return []
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Adicionamos a coluna 'arma' na busca (l[1])
            cursor.execute('''SELECT data, arma, distancia, clique, dir_h, cl_h, dir_v, cl_v 
                              FROM historico WHERE user_id = ? ORDER BY id DESC''', 
                           (self.usuario_atual['id'],))
            linhas = cursor.fetchall()
            conn.close()
            
            resultado = []
            for l in linhas:
                resultado.append({
                    "data": l[0],
                    "arma": l[1] if l[1] else "Não informada", # Pega a arma ou diz que não foi informada
                    "distancia": l[2],
                    "clique": l[3],
                    "dir_h": l[4],
                    "cl_h": l[5],
                    "dir_v": l[6],
                    "cl_v": l[7]
                })
            return resultado
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []

    def solicitar_frame(self):
        return self.current_frame_base64

    def registrar_clique_tela(self, norm_x, norm_y):
        if self.frame_shape is None:
            return {"status": "erro", "msg": "Câmera não iniciada."}
            
        h, w = self.frame_shape
        x_real = int(norm_x * w)
        y_real = int(norm_y * h)
        
        if self.pts_src is not None and self.H_td is not None:
            poligono = self.pts_src.astype(np.int32)
            is_inside = cv2.pointPolygonTest(poligono, (x_real, y_real), False)

            if is_inside >= 0:
                self.poa_pixel = (x_real, y_real)
                ponto_clicado = np.array([[[x_real, y_real]]], dtype="float32")
                ponto_transformado = cv2.perspectiveTransform(ponto_clicado, self.H_td)
                self.poa_td_pixel = (int(ponto_transformado[0][0][0]), int(ponto_transformado[0][0][1]))
                return {"status": "sucesso", "msg": "POA travado com sucesso!"}
            else:
                return {"status": "erro", "msg": "Clique fora do alvo! Clique dentro do bloco verde."}
        
        return {"status": "erro", "msg": "Aguarde a detecção dos ArUcos."}

    def salvar_referencia_atual(self):
        if self.poa_pixel is None:
            return {"status": "erro", "msg": "Defina o POA primeiro!"}
        if self.img_topdown is None:
            return {"status": "erro", "msg": "Alvo não detectado no momento do clique!"}

        self.frame_referencia = self.img_topdown.copy()
        self.estado_atual = "AGUARDANDO_TIRO"
        self.pois_rejeitados = [] 
        self.poi_td_pixel = None
        
        return {"status": "sucesso", "msg": "Referência estática salva! Sistema pronto."}

    def verificar_impacto(self):
        if self.frame_referencia is None or self.img_topdown is None:
            return {"status": "aguardando"}

        if getattr(self, 'poi_td_pixel', None) is not None:
            return {"status": "sucesso", "msg": "Furo detectado. Confirme na tela."}

        diff = cv2.absdiff(self.frame_referencia, self.img_topdown)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        candidatos = []
        for c in contours:
            area = cv2.contourArea(c)
            if 5 <= area <= 200: 
                perimetro = cv2.arcLength(c, True)
                if perimetro == 0: continue
                
                circularidade = 4 * math.pi * area / (perimetro * perimetro)
                if circularidade > 0.4:
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        cX = int(M["m10"]/M["m00"])
                        cY = int(M["m01"]/M["m00"])
                        
                        foi_rejeitado = False
                        for rx, ry in self.pois_rejeitados:
                            if math.hypot(cX - rx, cY - ry) <= 5: 
                                foi_rejeitado = True
                                break
                        
                        if not foi_rejeitado:
                            candidatos.append({'pt': (cX, cY), 'circ': circularidade})

        if len(candidatos) > 0:
            candidatos = sorted(candidatos, key=lambda x: x['circ'], reverse=True)
            self.poi_td_pixel = candidatos[0]['pt']
            return {"status": "sucesso", "msg": "Impacto Detectado! Aguardando confirmação."}
            
        return {"status": "aguardando"}

    def ignorar_impacto(self):
        if getattr(self, 'poi_td_pixel', None) is not None:
            self.pois_rejeitados.append(self.poi_td_pixel)
            self.poi_td_pixel = None
        return {"status": "reset", "msg": "Retomando varredura contínua..."}
    
    def calcular_correcao(self):
        if not getattr(self, 'poa_td_pixel', None) or not getattr(self, 'poi_td_pixel', None):
            return {"status": "erro", "msg": "Pontos não definidos."}

        poa_real_cm = (self.poa_td_pixel[0] / 10.0, self.poa_td_pixel[1] / 10.0)
        poi_real_cm = (self.poi_td_pixel[0] / 10.0, self.poi_td_pixel[1] / 10.0)

        erro_x = poi_real_cm[0] - poa_real_cm[0]
        erro_y = poa_real_cm[1] - poi_real_cm[1]

        # Desvio linear absoluto em milímetros
        desvio_mm = round(math.hypot(erro_x, erro_y) * 10, 1)

        # ==========================================
        # LOG DE DIAGNÓSTICO NO TERMINAL
        # ==========================================
        print("\n" + "="*45)
        print("=== DIAGNÓSTICO DE CÁLCULO BALÍSTICO ===")
        print(f"1. Distância definida (Setup): {self.distancia_metros} metros")
        print(f"2. Torre definida (Setup): {self.valor_clique_moa} MOA/MIL")
        print(f"3. Erro lido pela Câmera: X={erro_x:.4f} cm | Y={erro_y:.4f} cm")
        print(f"4. Desvio total do centro: {desvio_mm} mm")

        TOLERANCIA_MM = 8.0 

        if desvio_mm <= TOLERANCIA_MM:
            print("-> RESULTADO FINAL: Dentro da mosca (0 cliques).")
            cliques_x = 0
            cliques_y = 0
            dir_x = "Centro (Calibrado)"
            dir_y = "Centro (Calibrado)"
        else:
            if self.valor_clique_moa == 0.1: 
                valor_clique_cm = (self.distancia_metros / 100.0) * 1.0
                print("-> LÓGICA USADA: MIL (MRAD)")
            else:
                MOA_100M_CM = 2.9089
                valor_1moa_dist = (self.distancia_metros / 100.0) * MOA_100M_CM
                valor_clique_cm = valor_1moa_dist * self.valor_clique_moa
                print("-> LÓGICA USADA: MOA")
                print(f"Tamanho de 1 MOA nessa distância: {valor_1moa_dist:.4f} cm")

            print(f"5. Força de 1 Clique no Alvo: {valor_clique_cm:.4f} cm")

            if valor_clique_cm <= 0: 
                print("-> [ALERTA] Divisão por zero evitada!")
                valor_clique_cm = 0.01

            cliques_x = round(erro_x / valor_clique_cm)
            cliques_y = round(erro_y / valor_clique_cm)
            
            print(f"6. CONTA MATEMÁTICA REALIZADA:")
            print(f"   Cliques X: {erro_x:.4f} / {valor_clique_cm:.4f} = {cliques_x}")
            print(f"   Cliques Y: {erro_y:.4f} / {valor_clique_cm:.4f} = {cliques_y}")

            dir_x = "Direita" if cliques_x < 0 else "Esquerda"
            dir_y = "Cima" if cliques_y < 0 else "Baixo"

        print("="*45 + "\n")

        return {
            "status": "sucesso", "clx": abs(cliques_x), "dir_x": dir_x,
            "cly": abs(cliques_y), "dir_y": dir_y, "desvio": desvio_mm
        }
    
    def salvar_no_historico(self, nome_arma, dados):
        """Salva a sessão no banco apenas quando o usuário clica em concluir."""
        if not getattr(self, 'usuario_atual', None):
            return {"status": "erro", "msg": "Usuário não autenticado."}

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            import datetime
            agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            cursor.execute('''INSERT INTO historico 
                (user_id, arma, distancia, clique, dir_h, cl_h, dir_v, cl_v, data) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (self.usuario_atual['id'], nome_arma, float(dados['distancia']), 
                 dados['clique_tipo'], dados['dir_x'], dados['clx'], 
                 dados['dir_y'], dados['cly'], agora))
            
            conn.commit()
            conn.close()
            return {"status": "sucesso"}
        except Exception as e:
            return {"status": "erro", "msg": str(e)}
    
    def reiniciar_calibracao(self):
        self.estado_atual = "AGUARDANDO_POA"
        self.poa_pixel = None
        self.poa_td_pixel = None
        self.poi_td_pixel = None
        self.frame_referencia = None
        self.frame_congelado = None
        self.pois_rejeitados = []
        return {"status": "sucesso"}
    
    def recuperar_senha(self, email):
        """Simula a recuperação de senha buscando o e-mail no banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Em um cenário real, enviaríamos um e-mail. Aqui exibimos na interface.
            return {"status": "sucesso", "msg": f"Sua senha é: {user[0]}"}
        return {"status": "erro", "msg": "E-mail não encontrado na base de dados."}

    def preparar_novo_disparo(self):
        """Limpa o POI e as rejeições, mas MANTÉM o POA intacto para um tiro de confirmação."""
        self.estado_atual = "AGUARDANDO_POA" # Permite capturar uma nova referência
        self.poi_td_pixel = None
        self.frame_referencia = None
        self.frame_congelado = None
        self.pois_rejeitados = []
        return {"status": "sucesso"}

    def loop_captura_camera(self):
        # Conexão estrita revertida exatamente para a que funciona via Wi-Fi
        cap = cv2.VideoCapture(1)
        
        # Se a 1 falhar, o sistema te avisa corretamente, mas você confirmou que é a 1
        if not cap.isOpened():
            print("[ERRO] Falha ao abrir dispositivo (1)")
            if self._window:
                self._window.evaluate_js("alert('Erro: Dispositivo (1) não encontrado. Verifique o celular.')")
            self.running = False
            return

        while self.running:
            ret, frame = cap.read()
            if not ret: continue

            self.frame_shape = frame.shape[:2]

            if getattr(self, '_mtx', None) is not None and getattr(self, '_dist', None) is not None:
                frame_corrigido = cv2.undistort(frame, self._mtx, self._dist)
            else:
                frame_corrigido = frame.copy()

            corners, ids, rejected = cv2.aruco.detectMarkers(frame_corrigido, self._aruco_dict, parameters=self._aruco_params)
            self.pts_src = None 

            if ids is not None and len(ids) >= 4:
                centros_detectados = {}
                for i, marker_id in enumerate(ids.flatten()):
                    if marker_id in [0, 1, 2, 3]:
                        M = cv2.moments(corners[i][0])
                        if M["m00"] != 0:
                            centros_detectados[marker_id] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
                if all(m in centros_detectados for m in [0, 1, 2, 3]):
                    self.pts_src = np.array([
                        centros_detectados[0], centros_detectados[1], 
                        centros_detectados[2], centros_detectados[3]
                    ], dtype="float32")
                    
                    cv2.polylines(frame_corrigido, [np.int32(self.pts_src)], True, (0, 255, 0), 2)
                    
                    largura = int(self.LARGURA_ALVO_CM * 10)
                    altura = int(self.ALTURA_ALVO_CM * 10)
                    pts_dst = np.array([[0,0], [largura-1, 0], [largura-1, altura-1], [0, altura-1]], dtype="float32")
                    
                    self.H_td, _ = cv2.findHomography(self.pts_src, pts_dst)
                    self.img_topdown = cv2.warpPerspective(frame_corrigido, self.H_td, (largura, altura))
                else:
                    self.img_topdown = None
            else:
                self.img_topdown = None

            if self.poa_pixel is not None:
                cv2.circle(frame_corrigido, self.poa_pixel, 5, (0, 0, 255), -1)

            if self.estado_atual == "AGUARDANDO_TIRO" and getattr(self, 'poi_td_pixel', None) is not None and getattr(self, 'H_td', None) is not None:
                _, H_inv = cv2.invert(self.H_td)
                pt_topdown = np.array([[[self.poi_td_pixel[0], self.poi_td_pixel[1]]]], dtype="float32")
                pt_live = cv2.perspectiveTransform(pt_topdown, H_inv)
                
                cx_live = int(pt_live[0][0][0])
                cy_live = int(pt_live[0][0][1])
                
                cv2.circle(frame_corrigido, (cx_live, cy_live), 6, (255, 0, 0), -1)

            # 4. Envia para o HTML (Preservando proporção vertical ou horizontal)
            h_orig, w_orig = frame_corrigido.shape[:2]
            
            # Aumentamos a base para 1080 para manter a qualidade em tela cheia
            escala = 1080 / max(h_orig, w_orig)
            novo_w, novo_h = int(w_orig * escala), int(h_orig * escala)
            
            frame_display = cv2.resize(frame_corrigido, (novo_w, novo_h))
            _, buffer = cv2.imencode('.jpg', frame_display, [cv2.IMWRITE_JPEG_QUALITY, 85])
            self.current_frame_base64 = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
            
        cap.release()

if __name__ == '__main__':
    api = PrecisionScopeAPI()
    window = webview.create_window('CALIBRATION TOOL', url='frontend.html', js_api=api, width=1280, height=800)
    api.set_window(window)
    webview.start()