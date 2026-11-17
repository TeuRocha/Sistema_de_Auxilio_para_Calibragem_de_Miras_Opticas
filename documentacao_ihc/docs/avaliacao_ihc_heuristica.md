# Avaliação de IHC através de Inspeção Heurística

## Descrição da Avaliação

Avaliação heurística, definida por Nielsen e Molich (1994), é um método de avaliação de usabilidade onde um avaliador procura problemas de usabilidade numa interface com o usuário através da análise e interpretação de um conjunto de princípios ou heurísticas. Este método de avaliação é baseado no julgamento do avaliador.

**Avaliador:** Mateus Rocha (desenvolvedor do projeto)<br>
**Sistema avaliado:** Calibration Tool — Sistema de Auxilio para Calibragem de Miras Ópticas<br>
**Escopo:** Todas as telas do fluxo principal (Login, Cadastro, Menu Principal, Setup de Calibração, Definir POA, Salvar Referência, Confirmar POI, Consultar Feedback)

---

**Tabela \- Conjunto de heurísticas de Nielsen (1994)**

| **1\.Visibilidade do status do sistema:** |
| :---- |
| O sistema deve sempre manter os usuários informados sobre o que está acontecendo através de feedback apropriado, em um tempo razoável. |
| **2\.Compatibilidade entre sistema e mundo real:** |
| O sistema deve utilizar a linguagem do usuário, com palavras, frases e conceitos familiares para ele, ao invés de termos específicos de sistemas. Seguir convenções do mundo real, fazendo com que a informação apareça em uma ordem lógica e natural. |
| **3\.Controle e liberdade para o usuário:** |
| Estão relacionados à situação em que os usuários frequentemente escolhem as funções do sistema por engano e então necessitam de "uma saída de emergência” claramente definida para sair do estado não desejado sem ter que percorrer um longo diálogo, ou seja, é necessário suporte a *undo* e *redo*. |
| **4\.Consistência e padrões:** |
| Referem-se ao fato de que os usuários não deveriam ter acesso a diferentes situações, palavras ou ações representando a mesma coisa. A interface deve ter convenções não-ambíguas. |
| **5\.Prevenção de erros:** |
| Os erros são as principais fontes de frustração, ineficiência e ineficácia durante a utilização do sistema. |
| **6\.Reconhecimento em lugar de lembrança:** |
| Tornar objetos, ações, opções visíveis e coerentes. O usuário não deve ter que lembrar informações de uma parte do diálogo para outra. Instruções para o uso do sistema devem estar visíveis ou facilmente acessíveis. |
| **7\.Flexibilidade e eficiência de uso:** |
| A ineficiência nas tarefas pode reduzir a eficácia do usuário e causar-lhes frustração. O sistema deve ser adequado tanto para usuários inexperientes quanto para usuários experientes. |
| **8\.Projeto minimalista e estético:** |
| Os diálogos não devem conter informações irrelevantes ou raramente necessárias. Cada unidade extra de informação em um diálogo compete com unidades relevantes e diminui sua visibilidade relativa. |
| **9\.Auxiliar os usuários a reconhecer, diagnosticar e recuperar erros:** |
| Mensagens de erro devem ser expressas em linguagem natural (sem códigos), indicando precisamente o erro e sugerindo uma solução. |
| **10\.Ajuda e documentação:** |
| Mesmo que seja melhor que o sistema possa ser usado sem documentação, pode ser necessário fornecer ajuda e documentação. Tais informações devem ser fáceis de encontrar, ser centradas na tarefa do usuário, listar passos concretos a serem seguidos e não ser muito grandes. A ajuda deve estar facilmente acessível e on-line. |


## 1. Avaliação Heurística — Violações Identificadas

> **Nota:** Apenas heurísticas violadas são relatadas nesta seção.

### Tabela de Grau de Severidade

| Grau | Tipo | Descrição |
| :--: | :--- | :--- |
| 0 | Sem importância | Não afeta a operação da interface |
| 1 | Cosmético | Não há necessidade imediata de solução |
| 2 | Simples | Problema de baixa prioridade (pode ser reparado) |
| 3 | Grave | Problema de alta prioridade (deve ser reparado) |
| 4 | Catastrófico | Muito grave, deve ser reparado antes do lançamento |

---

### Violações

| # | Heurística Violada | Problema | Local | Gravidade | Solução Recomendada |
| :--: | :--- | :--- | :--- | :--: | :--- |
| 1 | **H3 — Controle e Liberdade do Usuário** | Ausência de botão "Voltar" em quase todas as etapas do fluxo de calibração. Uma vez que o usuário avança de uma tela para a próxima (ex.: de Definir POA para Salvar Referência), não há como retornar à etapa anterior sem reiniciar o fluxo completo. Após confirmar e avançar, a ação se torna irreversível. | Telas: Definir POA, Salvar Referência, Confirmar POI, Consultar Feedback | **3 — Grave** | Implementar botão "Voltar" em cada etapa do fluxo, permitindo ao usuário retornar à etapa imediatamente anterior sem perder todo o progresso. O retorno crítico deve ser acompanhado de modal de confirmação ("Tem certeza? O progresso desta etapa será perdido.") para evitar cliques acidentais. |
| 2 | **H4 — Consistência e Padronização** | O botão principal de avanço muda de posição em cada trecho do sistema, não tendo um posicionamento padronizado. | Telas: Definir POA, Salvar Referência | **1 — Cosmético** | Padronizar posicionamento dos botões, reduzindo carga cognitiva e tempo gasto utilizando o sistema, principalmente nas telas com foco em visão do alvo em tempo real. |
| 3 | **H5 — Prevenção de Erros** | Na tela "Setup de Calibração", o campo de entrada manual aceita qualquer valor numérico sem validação em tempo real. O usuário não recebe aviso após ligar a câmera, sem saber de antemão qual é a faixa de valores aceitos. | Tela: Setup de Calibração | **2 — Simples** | Não permitir valores negativos, impossibilitando o erro do usuário. |
| 4 | **H10 — Ajuda e Documentação** | O sistema não possui nenhuma seção de ajuda, guia de uso ou documentação acessível durante a interação. A ausência de ajuda contextual obriga o usuário iniciante a aprender por tentativa e erro. | Global — todas as telas | **2 — Simples** | Implementar um botão de ajuda (ícone "?") fixo no header, abrindo um painel com guia rápido da cena atual. Alternativamente, adicionar tooltips de instrução contextual descrevendo brevemente o que o usuário deve fazer. |

### Imagens das Heurísticas Violadas

#### H3 - Controle e Liberdade do Usuário
> Nota: Ausência do botão voltar em diversas telas.
> As telas seguem respectivamente: Definir POA, Salvar Referência, Confirmar POI, Consultar Feedback.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/25169788-5fd5-4805-9d9b-94015f2c4496" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/6ac07d2d-6108-4074-af17-179f8ceb351f" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/a5271b3e-161b-4501-a5d7-70aa8efa1003" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/4063ebf1-850f-4d2c-a276-9fa104cb7fc4" />

#### H4 - Consistência e Padronização
> Nota: Ausência de padronização nos botões que avançam etapas do sistema.
> As telas seguem respectivamente: Definir POA, Salvar Referência.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/aff0504d-6336-437d-9935-f449ceeae68a" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/6ac07d2d-6108-4074-af17-179f8ceb351f" />

#### H5 - Prevenção de Erros
> Nota: Ausência de limite para definir distância, permitindo valores negativos na tela Setup de Calibração.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/0845cc82-571b-40b3-8ed8-fd9b468aca11" />

#### H10 - Ajuda e Documentação
> Nota: Ausência de seção ajuda em todas as etapas de calibração do sistema.
> As telas seguem respectivamente: Setup de Calibração, Definir POA, Salvar Referência, Confirmar POI, Consultar Feedback.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/32d32ac1-5da6-4586-a65a-1de05aac925b" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/aff0504d-6336-437d-9935-f449ceeae68a" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/6ac07d2d-6108-4074-af17-179f8ceb351f" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/a5271b3e-161b-4501-a5d7-70aa8efa1003" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/4063ebf1-850f-4d2c-a276-9fa104cb7fc4" />

---

## 2. Boas Práticas de Heurística — Heurísticas Atendidas

> **Nota:** Esta seção tem caráter didático, registrando onde cada heurística foi satisfatoriamente aplicada. Algumas heurísticas (como H3 e H4) aparecem tanto como violação quanto como boa prática; nestes casos, o escopo de sucesso é pontual à tela mencionada, não faz parte de um sucesso dentro do fluxo global do sistema.

| # | Heurística | Exemplo de Aplicação no Sistema |
| :--: | :--- | :--- |
| H1 | **Visibilidade do Estado do Sistema** | Na tela "Definir POA", "Salvar Referência" e "Confirmar POI", o sistema exibe em tempo real o status de detecção dos marcadores ArUco com badge colorido ("ArUcos detectados" em verde), mantendo o usuário constantemente informado sobre sua detecção. |
| H2 | **Compatibilidade entre Sistema e Mundo Real** | O feedback de correção é apresentado em linguagem direta e familiar ao atirador: "4 cliques para Direita \| 7 cliques para Cima", em vez de valores técnicos em MOA ou MIL. Isso traduz o jargão balístico para instruções concretas de ajuste nas torres da luneta, linguagem já conhecida pelo público-alvo. |
| H3 | **Controle e Liberdade do Usuário** | Na tela "Definir POA", o usuário pode redefinir o ponto de mira quantas vezes quiser antes de confirmar. Na tela "Confirmar POI", o usuário pode verificar quantas vezes for necessário. O sistema não força um comprometimento prematuro com uma definição incorreta. |
| H4 | **Consistência e Padronização** | O sistema mantém identidade visual consistente em todas as telas: mesma paleta de cores, mesma tipografia, mesmo espaçamento e mesmo padrão de mensagens de erro com texto descritivo. |
| H5 | **Prevenção de Erros** | Na tela "Definir POA", o botão "Confirmar POA" permanece desabilitado enquanto nenhum ponto de mira tiver sido definido, impedindo que o usuário avance para a próxima etapa sem ter completado a ação necessária. |
| H6 | **Reconhecimento em Lugar de Lembrança** | Durante o fluxo de calibração, as configurações iniciais (como a distância definida na primeira etapa) são mantidas pelo sistema e aplicadas automaticamente no cálculo balístico final. Além disso, a marcação do Ponto de Mira (POA) permanece visível como referência durante a captura do Ponto de Impacto (POI), não obrigando memorização do usuário sobre suas ações anteriores. |
| H7 | **Flexibilidade e Eficiência de Uso** | Na tela "Setup de Calibração", o sistema oferece tanto botões de setas para cima e para baixo, quanto campo de entrada manual para valores personalizados, permitindo o usuário escolher como definir distância. |
| H8 | **Projeto Minimalista e Estético** | O design segue padrão dark mode com elementos técnicos e limpos, sem banners publicitários, animações desnecessárias ou informações irrelevantes. Cada elemento de interface presente na tela tem função direta na tarefa atual do usuário. |
| H9 | **Auxiliar os Usuários a Reconhecer, Diagnosticar e Recuperar Erros** | Na tela "Definir POA", o sistema exibe mensagem de falha específica descritiva para o problema de clicar fora da área limite de detecção dos marcadores, e informa como corrigir o problema. |

### Imagens das Boas Práticas de Heurísticas

#### H1 - Visibilidade do Estado do Sistema
> Nota: O sistema exibe status de detecção em tempo real como feedback visual de seu funcionamento.
> As telas seguem respectivamente: Definir POA, Salvar Referência, Confirmar POI.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/aff0504d-6336-437d-9935-f449ceeae68a" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/6ac07d2d-6108-4074-af17-179f8ceb351f" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/a5271b3e-161b-4501-a5d7-70aa8efa1003" />

#### H2 - Compatibilidade entre Sistema e Mundo Real
> Nota: O sistema retorna um feedback em linguagem direta e familiar ao atirador na tela Consultar Feedback.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/4063ebf1-850f-4d2c-a276-9fa104cb7fc4" />

#### H3 - Controle e Liberdade do Usuário
> Nota: O sistema permite liberdade para definir seu ponto de mira e verificar ponto de impacto quantas vezes quiser.
> As telas seguem respectivamente: Definir POA, Confirmar POI.
<img width="1256" height="784" alt="image" src="https://github.com/user-attachments/assets/25169788-5fd5-4805-9d9b-94015f2c4496" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/a5271b3e-161b-4501-a5d7-70aa8efa1003" />

#### H4 - Consistência e Padronização
> Nota: O sistema mantém identidade visual em todas as telas com relação à mesma paleta de cores, tipografia, espaçamento e mensagens de erro.
> As telas seguem respectivamente: Cadastrar Usuário, Efetuar Login, Menu Principal, Histórico de Calibração, Setup de Calibração, Definir POA, Salvar Referência, Confirmar POI, Consultar Feedback.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/738436d5-11e8-4607-996d-244394859ff2" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/e70975e0-df90-4f19-b827-1cdfa72d73ff" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/05408000-d84e-4a27-87b1-46ffb15d65a4" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/e422eab6-d8b4-4c9c-b35a-9fbdbafb16d0" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/0845cc82-571b-40b3-8ed8-fd9b468aca11" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/aff0504d-6336-437d-9935-f449ceeae68a" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/6ac07d2d-6108-4074-af17-179f8ceb351f" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/a5271b3e-161b-4501-a5d7-70aa8efa1003" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/4063ebf1-850f-4d2c-a276-9fa104cb7fc4" />

#### H5 - Prevenção de Erros
> Nota: O sistema mantém desabilitado o botão que avança no sistema quando o usuário há de realizar uma ação, ou na falta de detecção do alvo.
> As telas seguem respectivamente: Definir POA, Confirmar POI.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/aff0504d-6336-437d-9935-f449ceeae68a" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/3f58a503-d7de-45f8-9130-8982105cb086" />

#### H6 - Reconhecimento em Lugar de Lembrança
> Nota: O sistema não exige do atirador memorização sobre suas ações anteriores.
> As telas seguem respectivamente: Setup de Calibração, Confirmar POI
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/0845cc82-571b-40b3-8ed8-fd9b468aca11" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/a5271b3e-161b-4501-a5d7-70aa8efa1003" />

####  H7 - Flexibilidade e Eficiência de Uso
> Nota: O sistema oferece diversas maneiras para o usuário escolher como definir distância na tela Setup de Calibração.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/5638c7a5-d81b-4d73-8540-d945c44b8917" />

#### H8 - Projeto Minimalista e Estético
> Nota: O sistema segue padrão de design dark mode com visual técnico e limpo, sem informações desnecessárias em todas as telas.
> As telas seguem respectivamente: Cadastrar Usuário, Efetuar Login, Menu Principal, Histórico de Calibração, Setup de Calibração, Definir POA, Salvar Referência, Confirmar POI, Consultar Feedback.
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/738436d5-11e8-4607-996d-244394859ff2" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/e70975e0-df90-4f19-b827-1cdfa72d73ff" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/05408000-d84e-4a27-87b1-46ffb15d65a4" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/e422eab6-d8b4-4c9c-b35a-9fbdbafb16d0" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/0845cc82-571b-40b3-8ed8-fd9b468aca11" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/aff0504d-6336-437d-9935-f449ceeae68a" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/6ac07d2d-6108-4074-af17-179f8ceb351f" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/a5271b3e-161b-4501-a5d7-70aa8efa1003" />
<img width="1255" height="782" alt="image" src="https://github.com/user-attachments/assets/4063ebf1-850f-4d2c-a276-9fa104cb7fc4" />

####  H9 - Auxiliar os Usuários a Reconhecer, Diagnosticar e Recuperar Erros
> Nota: O sistema exibe mensagem de erro ao tentar marcar o POA onde não é possível, informando como corrigir o problema na tela Definir POA.
<img width="1262" height="790" alt="image" src="https://github.com/user-attachments/assets/fde5927a-38f3-40d8-b7a9-b46e77a35c12" />


---

## 3. Fluxograma do Processo de Avaliação Heurística

```
┌─────────────────────────────────────────────────────────┐
│         PREPARAÇÃO                                      │
│  • Familiarizar-se com as 10 heurísticas de Nielsen     │
│  • Familiarizar-se com o sistema/protótipo a avaliar    │
│  • Definir escopo: todas as telas do fluxo principal    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│         COLETA DE DADOS (avaliador individualmente)     │
│  • Executar cada tarefa do fluxo como um usuário        │
│  • Inspecionar cada tela contra a lista de heurísticas  │
│  • Anotar cada violação encontrada                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│         INTERPRETAÇÃO                                   │
│  • Para cada violação: identificar a heurística violada │
│  • Localizar exatamente em qual tela/elemento ocorre    │
│  • Classificar a gravidade (0 a 4)                      │
│  • Registrar justificativa do problema                  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│         CONSOLIDAÇÃO                                    │
│  • Revisar todos os problemas encontrados               │
│  • Verificar consistência das classificações            │
│  • Eliminar duplicatas                                  │
│  • Priorizar por gravidade                              │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│         RELATO DOS RESULTADOS                           │
│  • Produzir tabela consolidada de violações             │
│  • Registrar boas práticas identificadas                │
│  • Propor soluções para cada problema                   │
│  • Planejar reprojeto das telas afetadas                │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼ (fase iterativa)
              Retornar à Coleta de Dados
              após implementar correções
```
