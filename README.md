# 🎯 Calibration Tool — Sistema de Auxílio para Calibragem de Miras Ópticas

> 🏆 **Projeto Premiado:** 1º Lugar na categoria Ciência da Computação no **INOVAFEI** (Centro Universitário FEI).

Sistema de visão computacional e engenharia de usabilidade desenvolvido como Trabalho de Conclusão de Curso (TCC). Projeto apresentado ao Centro Universitário [FEI](https://portal.fei.edu.br/), como parte dos requisitos necessários para aprovação na disciplina de Interface Humano-Computador (CC8122), e aprovação no curso de Ciencia da Computação, orientado pelo Prof. Dr. [Plinio Thomaz Aquino Junior](http://lattes.cnpq.br/6186413528999908). A aplicação automatiza e assiste o processo de zeragem (*zeroing*) de miras ópticas (lunetas) no tiro esportivo, convertendo desvios de impacto em instruções diretas de ajuste mecânico.

---

## 📌 Visão Geral e Problema Resolvido

Tradicionalmente, a calibragem de uma luneta exige múltiplos disparos de tentativa e erro, cálculos balísticos manuais (conversão de distância e unidades angulares como MOA/MIL) e deslocamentos constantes até o alvo. Esse processo consome tempo de pista e gera alto desperdício de munição.

O **Calibration Tool** resolve esse problema por meio de um fluxo assistido em tempo real:
1. **Captura Remota:** Utiliza um smartphone posicionado próximo ao alvo transmitindo vídeo via rede local (Câmera IP) para o notebook do atirador.
2. **Correção de Perspectiva:** Detecta quatro marcadores **ArUco** nos cantos do alvo e aplica **homografia planar** para corrigir distorções de ângulo da câmera.
3. **Detecção e Cálculo Balístico:** Identifica o Ponto de Impacto (**POI**) após o disparo, calcula a distância vetorial até o Ponto de Mira (**POA**) definido pelo usuário e converte o desvio em **cliques exatos** para as torres de elevação e lateralidade da luneta.

---

## 📂 Estrutura do Repositório

| Diretório | Conteúdo |
| :--- | :--- |
| **[`/src`](./src/sistema_calibracao)** | Código-fonte principal da aplicação em Python (OpenCV, NumPy), interface gráfica e requisitos de execução. |
| **[`/documentacao_ihc`](./documentacao_ihc)** | Documentação completa de Engenharia de Usabilidade: Personas, Análise de Tarefas (HTA, GOMS, CTT), MoLIC, Planejamento DECIDE, Inspeção Heurística e Avaliação Empírica. |
| **[`/documentos_tcc`](./documentos_tcc)** | Monografia final, apresentações de banca, referências bibliográficas e arquivos dos marcadores ArUco para impressão. |
| **[`/scripts_auxiliares`](./scripts_auxiliares)** | Scripts utilitários para teste isolado de conexão de câmera IP, validação de homografia e calibração intrínseca. |

---

## 🧠 Engenharia de Usabilidade (IHC) e Validação em Campo

Toda a interface do sistema foi projetada e avaliada para garantir acessibilidade tanto para atiradores iniciantes quanto experientes:

* **Inspeção Heurística (Nielsen):** Análise sistemática de todas as telas com classificação de severidade (0 a 4), identificação de boas práticas (*dark mode* técnico, prevenção de erros e feedback em linguagem natural) e levantamento de melhorias de navegação.
* **Teste Empírico em Estande de Tiro:** Avaliação por observação direta em ambiente real com disparos controlados. O sistema permitiu aproximar a calibragem em **apenas 2 disparos** — processo que tradicionalmente demandaria de **5 a 10 disparos** — validando a economia de insumos e a clareza do feedback em cliques.

👉 *Acesse o índice completo dos artefatos de IHC em [`/documentacao_ihc/README.md`](./documentacao_ihc/README.md).*

---

## 🛠️ Stack Tecnológica e Metodologia

* **Linguagem & Visão Computacional:** Python, OpenCV (`cv2.aruco`, transformações homográficas), NumPy.
* **Design de Interface & Prototipação:** Figma.
* **Engenharia de IHC & Documentação:** Molic, HTA, GOMS, CTT, Método DECIDE e Heurísticas de Nielsen.

---

## 👨‍💻 Autor

**Mateus Rocha** — Bacharel em Ciência da Computação pelo Centro Universitário FEI.
