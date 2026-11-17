# Calibration Tool 🎯

**Sistema de Auxilio para Calibragem de Miras Ópticas.**

## 💡 A Ideia e o Problema
No tiro desportivo e tático, a "zeragem" (calibração) de lunetas, *red dots* e miras metálicas é tradicionalmente feita pelo método de tentativa e erro. O atirador efetua disparos, verifica o alvo manualmente e estima os ajustes angulares. Esse processo consome tempo de estande e **desperdiça munição**, um insumo de altíssimo custo no cenário brasileiro. Além disso, os sistemas eletrônicos que automatizam essa leitura costumam ser importados e financeiramente inacessíveis para a maioria do público.

## 🎯 O Objetivo
O **Calibration Tool** nasceu como Trabalho de Conclusão de Curso (TCC) em Ciência da Computação para democratizar a precisão balística, oferecendo uma solução nacional e de baixo custo. 

O software transforma a câmera de um smartphone comum (conectado via Wi-Fi local) em um sensor óptico inteligente. Utilizando marcadores ArUco e cálculos de homografia, o sistema estabiliza a visão do alvo, detecta automaticamente o furo do disparo no papel, calcula o desvio milimétrico e converte esse erro em **instruções exatas de cliques de correção** (em MOA ou MIL) para as torres da mira do atirador.

## ✨ Principais Funcionalidades
* **Visão Computacional Robusta:** Uso de OpenCV para retificação de perspectiva (*Top-Down*) e filtros morfológicos para detecção precisa de impactos, ignorando sombras e ruídos.
* **Cálculo Balístico Dinâmico:** Conversão exata do erro linear para frações angulares (1/2, 1/4, 1/8 MOA e 1/10 MIL) ajustável para qualquer distância de tiro informada (de 10m a 100m+).
* **Interface Focada em IHC:** Interface gráfica amigável, intuitiva e com Prevenção Ativa de erros, projetada para ser operada rapidamente no estande de tiro.
* **Histórico e Persistência:** Banco de dados local com SQLite que gerencia múltiplos perfis de atiradores, cadastra armamentos e salva o histórico de resultados de todas as sessões de calibração.

## 🛠️ Tecnologias Utilizadas
* **Back-end & Visão:** Python, OpenCV, NumPy, Math.
* **Front-end / UI:** PyWebView, Tailwind CSS, HTML/JS.
* **Banco de Dados:** SQLite.
