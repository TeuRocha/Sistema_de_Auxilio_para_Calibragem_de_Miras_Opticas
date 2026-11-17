import numpy as np
import cv2
import math

with np.load('calibracao_camera.npz') as data:
    mtx = data['mtx']
    dist = data['dist']

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()

LARGURA_ALVO_CM = 47.0
ALTURA_ALVO_CM = 25.0
MOA_100M_CM = 2.9089
VALOR_CLIQUE_MOA = 1/4 
AGUARDANDO_POA = 0
AGUARDANDO_R = 1
AGUARDANDO_TIRO = 2
AGUARDANDO_S = 3

distancia_metros = float(input("Digite a distância do alvo em metros (ex: 10.0): "))

pontos_reais = np.array([
    [0, 0],
    [LARGURA_ALVO_CM, 0],
    [LARGURA_ALVO_CM, ALTURA_ALVO_CM],
    [0, ALTURA_ALVO_CM]
], dtype="float32")

H_td = None
img_topdown = None 
poa_pixel = None
poa_td_pixel = None # POA mapeado na imagem topdown
poa_real_cm = None
frame_referencia = None
estado_atual = AGUARDANDO_POA
pts_src = None

def clique_mouse(event, x, y, flags, param):
    global poa_pixel, poa_td_pixel, poa_real_cm, estado_atual, pts_src, H_td
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if pts_src is not None and H_td is not None:
            poligono = pts_src.astype(np.int32)
            is_inside = cv2.pointPolygonTest(poligono, (x, y), False)

            if is_inside >= 0:
                poa_pixel = (x, y)
                
                # Transforma o clique direto para a coordenada da imagem top-down
                ponto_clicado = np.array([[[x, y]]], dtype="float32")
                ponto_transformado = cv2.perspectiveTransform(ponto_clicado, H_td)
                
                px_td = ponto_transformado[0][0][0]
                py_td = ponto_transformado[0][0][1]
                
                poa_td_pixel = (int(px_td), int(py_td))
                poa_real_cm = (px_td / 10.0, py_td / 10.0) # img_topdown tem 10 pixels por cm
                
                print(f"[SUCESSO]: POA definido: {poa_real_cm} cm")
                estado_atual = AGUARDANDO_R
            else:
                print("[ERRO]: Clique fora da área do alvo! Clique entre os 4 ArUcos (dentro do bloco verde).")
        else:
            print("[ERRO]: Posicione os 4 ArUcos antes de clicar!")

def calcular_cliques(poa, poi, distancia):
    erro_x = poi[0] - poa[0]
    erro_y = poa[1] - poi[1]
    
    valor_1moa_dist = (distancia / 100.0) * MOA_100M_CM
    valor_clique_cm = valor_1moa_dist * VALOR_CLIQUE_MOA
    
    cliques_x = round(erro_x / valor_clique_cm)
    cliques_y = round(erro_y / valor_clique_cm)
    return cliques_x, cliques_y

cap = cv2.VideoCapture(1)
cv2.namedWindow("Alvo")
cv2.setMouseCallback("Alvo", clique_mouse)

while True:
    ret, frame = cap.read()
    if not ret: break

    frame_corrigido = cv2.undistort(frame, mtx, dist)
    corners, ids, rejected = cv2.aruco.detectMarkers(frame_corrigido, aruco_dict, parameters=aruco_params)
    img_topdown = None

    if estado_atual == AGUARDANDO_POA:
        mensagem = "Clique no centro do alvo para definir o POA."
        cor_msg = (255, 255, 255) # Branco
    elif estado_atual == AGUARDANDO_R:
        mensagem = "Pressione 'r' para salvar imagem de referencia."
        cor_msg = (0, 255, 0) # Verde
    elif estado_atual == AGUARDANDO_TIRO:
        mensagem = "Efetue o disparo e aproxime o alvo da camera."
        cor_msg = (0, 255, 255) # Amarelo
    elif estado_atual == AGUARDANDO_S:
        mensagem = "Pressione 's' para detectar o impacto."
        cor_msg = (255, 165, 0) # Laranja

    cv2.putText(frame_corrigido, mensagem, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_msg, 2)
    cv2.putText(frame_corrigido, "Pressione 'Q' para sair", (20, frame_corrigido.shape[0] - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    if ids is not None and len(ids) >= 4:
        centros_detectados = {}
        for i, marker_id in enumerate(ids.flatten()):
            if marker_id in [0, 1, 2, 3]:
                M = cv2.moments(corners[i][0])
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    centros_detectados[marker_id] = (cX, cY)
        
        if all(m in centros_detectados for m in [0, 1, 2, 3]):
            pts_src = np.array([centros_detectados[0], centros_detectados[1], 
                                centros_detectados[2], centros_detectados[3]], dtype="float32")
            
            cv2.polylines(frame_corrigido, [np.int32(pts_src)], True, (0, 255, 0), 2)

            largura, altura = int(LARGURA_ALVO_CM * 10), int(ALTURA_ALVO_CM * 10)
            pts_dst = np.array([[0,0], [largura-1, 0], [largura-1, altura-1], [0, altura-1]], dtype="float32")
            H_td, _ = cv2.findHomography(pts_src, pts_dst)
            img_topdown = cv2.warpPerspective(frame_corrigido, H_td, (largura, altura))
    
    # Exibe topdown em tempo real com o POA se estiver definido
    if img_topdown is not None:
        img_td_display = img_topdown.copy()
        if poa_td_pixel is not None:
            cv2.circle(img_td_display, poa_td_pixel, 5, (0, 0, 255), -1)
            cv2.putText(img_td_display, "POA", (poa_td_pixel[0]+10, poa_td_pixel[1]-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.imshow("Visao Top-Down (Estatica)", img_td_display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    
    if key == ord('r') and img_topdown is not None and estado_atual == AGUARDANDO_R:
        frame_referencia = img_topdown.copy()
        estado_atual = AGUARDANDO_TIRO
        print("[SISTEMA]: Imagem de referencia salva. Pode atirar! Depois do disparo pressione 's'.")

    if key == ord('s') and frame_referencia is not None and img_topdown is not None:
        diff = cv2.absdiff(frame_referencia, img_topdown)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        candidatos = []
        
        # Filtro de candidatos baseado em Área e Circularidade
        for c in contours:
            area = cv2.contourArea(c)
            if 5 <= area <= 200: # Ajuste o range de área esperado na imagem topdown
                perimetro = cv2.arcLength(c, True)
                if perimetro == 0: continue
                # Fórmula da circularidade: 4*pi*A / P² (1.0 é um círculo perfeito)
                circularidade = 4 * math.pi * area / (perimetro * perimetro)
                
                if circularidade > 0.4: # Aceita formas razoavelmente redondas (furos de projétil)
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        cX = int(M["m10"]/M["m00"])
                        cY = int(M["m01"]/M["m00"])
                        candidatos.append({
                            'pt': (cX, cY),
                            'area': area,
                            'circ': circularidade
                        })

        # Ordena para mostrar os mais prováveis (mais circulares) primeiro
        candidatos = sorted(candidatos, key=lambda x: x['circ'], reverse=True)

        poi_confirmado = False
        poi_real_cm = None

        for cand in candidatos:
            img_feedback = img_topdown.copy()
            
            # Desenha o POA (Vermelho)
            if poa_td_pixel:
                cv2.circle(img_feedback, poa_td_pixel, 5, (0, 0, 255), -1)
                cv2.putText(img_feedback, "POA", (poa_td_pixel[0]+10, poa_td_pixel[1]-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            # Desenha o candidato a POI (Azul)
            pt_candidato = cand['pt']
            cv2.circle(img_feedback, pt_candidato, 5, (255, 0, 0), -1) # AZUL
            cv2.putText(img_feedback, "POI?", (pt_candidato[0]+10, pt_candidato[1]-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            cv2.imshow("Visao Top-Down (Estatica)", img_feedback)
            cv2.waitKey(1) # Atualiza a janela da interface
            
            resposta = input("Está correto o POI detectado em azul? (s/n): ").strip().lower()
            
            if resposta == 's':
                poi_confirmado = True
                poi_real_cm = (pt_candidato[0] / 10.0, pt_candidato[1] / 10.0)
                print(f"Impacto confirmado em: {poi_real_cm} cm (Área: {cand['area']:.1f}, Circ: {cand['circ']:.2f})")
                
                # Exibe a imagem final confirmada
                cv2.putText(img_feedback, "POI Confirmado", (pt_candidato[0]+10, pt_candidato[1]+15), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                cv2.imshow("Visao Top-Down (Estatica)", img_feedback)
                cv2.waitKey(1)
                break

        if poi_confirmado and poa_real_cm:
            cx, cy = calcular_cliques(poa_real_cm, poi_real_cm, distancia_metros)
            dir_x = "Direita" if cx < 0 else "Esquerda"
            dir_y = "Baixo" if cy < 0 else "Cima"
            print(f"\n--- AJUSTE: {abs(cx)} cliques p/ {dir_x} | {abs(cy)} cliques p/ {dir_y} ---\n")
            
            resposta_acerto = input("Houve acerto no alvo da maneira desejada? O sistema pode ser encerrado? (s/n): ").strip().lower()
            if resposta_acerto == 's':
                print("[SISTEMA]: Encerrando o sistema. Ótimos tiros!")
                break
            else:
                print("[SISTEMA]: Retornando para definição de um novo POA.")
                estado_atual = AGUARDANDO_POA
                poa_pixel = None
                poa_td_pixel = None
                poa_real_cm = None
                frame_referencia = None
        else:
            print("[ALERTA]: Nenhum furo detectado na imagem (ou nenhum candidato validado). Verifique o alvo.")

    if poa_pixel is not None:
        cv2.circle(frame_corrigido, poa_pixel, 8, (0, 0, 255), -1)
        cv2.putText(frame_corrigido, "POA", (poa_pixel[0]+10, poa_pixel[1]-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

    cv2.imshow("Alvo", frame_corrigido)

cap.release()
cv2.destroyAllWindows()