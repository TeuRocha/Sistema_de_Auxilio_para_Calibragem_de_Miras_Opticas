# 💻 Código-Fonte — Calibration Tool

Este diretório contém o código-fonte e o executável da aplicação desktop responsável pelo processamento de vídeo em tempo real, detecção de marcadores ArUco, transformação homográfica e cálculo de correção balística em cliques (MOA/MIL), com interface gráfica construída em HTML/CSS/JS e executada nativamente via **PyWebView**.

---

## ▶️ Como Executar o Sistema

Você pode iniciar a aplicação de duas formas:

### Opção 1: Via Executável (Recomendado para Windows — sem necessidade de instalação)
Basta navegar até a pasta do executável e abrir o arquivo diretamente:
```text
src/dev_interface/dist/app/app.exe
```

---

### Opção 2: Via Código-Fonte (Python)

## 📋 Pré-requisitos

* **Python 3.10+** instalado no sistema.
* **Smartphone** com aplicativo de transmissão de vídeo via rede local (ex.: *IP Webcam* para Android) conectado na **mesma rede Wi-Fi** do computador.
* **Alvo impresso** contendo os 4 marcadores **ArUco** nos cantos (disponível na pasta [`documentos_tcc`](/documentos_tcc/marcadores_aruco)).

---

## ⚙️ Instalação das Dependências

Abra o terminal (Prompt de Comando, PowerShell ou Git Bash) dentro desta pasta (`src/`) e instale as bibliotecas necessárias:

```bash
pip install opencv-python numpy pywebview
```

## 🚀 Execução

No terminal (dentro de src/), execute o arquivo principal:

```bash
python app.py
```

🎯 Fluxo de Uso na Interface

1. Inicie o servidor de vídeo no aplicativo do smartphone e anote o endereço IP exibido na tela (ex.: http://0.0.0.0:8080/video)

2. Realize o login ou cadastro de usuário na aplicação.

3. No Setup de Calibração, informe a distância até o alvo (em metros), o valor do clique da luneta (ex.: 1/4 MOA) e a URL do stream da câmera IP.

4. Defina o Ponto de Mira (POA) clicando sobre o alvo na tela.

5. om os 4 marcadores ArUco detectados (badge verde), clique em Salvar Referência.

6. Efetue o disparo e clique em Confirmar POI para visualizar a correção recomendada em cliques para as torres de elevação e lateralidade.

🔧 Solução Rápida de Problemas

- Bloqueio de segurança no Windows ao abrir o app.exe: Caso o Windows Defender / Controle Inteligente de Aplicativos bloqueie a execução por ser um software independente sem assinatura comercial, clique em Mais informações > Executar assim mesmo.

- Erro ao conectar na câmera: Verifique se o computador e o smartphone estão na mesma rede Wi-Fi e se o endereço termina com /video. Você pode testar a conexão isoladamente usando o script conexao.py na pasta [scripts_auxiliares](/scripts_auxiliares).

- Marcadores ArUco não detectados: Certifique-se de que os 4 cantos do alvo estão totalmente visíveis no enquadramento da câmera e sem sombras fortes ou reflexos diretos sobre os marcadores. Seguindo a ordem e posicionamento padrão, que pode ser visualizado na imagem a seguir:

<img width="362" height="491" alt="formato_padrao_marcadores" src="https://github.com/user-attachments/assets/4a67833b-d592-47b0-b355-a4b8ca7f56c0" />
