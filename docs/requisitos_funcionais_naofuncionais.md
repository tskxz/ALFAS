## 1. Requisitos Funcionais (F - Functionality)

### 1.1. Gestão de Contas e Autenticação
* **RF01 - Tipos de Acesso:** O sistema deve separar os conteúdos públicos (acessíveis a visitantes) dos conteúdos reservados (exclusivos para utilizadores registados).
* **RF02 - Consentimento Parental:** O registo de utilizadores menores de idade deve exigir a validação do consentimento do encarregado de educação antes da ativação da conta.
* **RF03 - Autenticação:** O sistema deve permitir o início de sessão (login) e a recuperação de palavra-passe.
* **RF04 - Gestão de Perfil:** O utilizador deve poder consultar e editar a sua informação pessoal (nome, género, ano de escolaridade e foto de perfil).
* **RF05 - Gestão Administrativa:** O Administrador deve gerir contas de utilizador, perfis de acesso (Roles: Convidado, Registado, Manager, Admin) e alterar estados de conta (ativo, inativo, pendente).

### 1.2. Gestão do Catálogo Formativo
* **RF06 - Inscrição em Formações:** O utilizador deve poder pesquisar e inscrever-se em workshops e webinars.
* **RF07 - Acesso a Materiais:** O utilizador inscrito deve ter acesso aos vídeos e ficheiros de apoio associados ao recurso formativo.
* **RF08 - Gestão de Conteúdos Formativos:** O Gestor de Conteúdos (Manager) e o Administrador devem poder criar, editar e remover workshops, webinars, categorias e áreas de saúde.

### 1.3. Questionários de Avaliação
* **RF09 - Questionário de Diagnóstico (Pré-teste):** O sistema deve exigir a resposta a um questionário de diagnóstico antes de dar acesso ao conteúdo do recurso formativo.
* **RF10 - Questionário Final (Pós-teste):** O sistema deve disponibilizar um questionário de avaliação no final da formação.
* **RF11 - Registo de Resultados:** O sistema deve guardar as respostas, a nota obtida e a data/hora de conclusão de cada questionário.
* **RF12 - Configuração de Questionários:** O Manager deve poder criar e editar perguntas, opções de resposta e soluções dos questionários.

### 1.4. Gamificação
* **RF13 - Atribuição de Recompensas:** O sistema deve emitir automaticamente um badge e um certificado digital quando o utilizador obtém uma pontuação igual ou superior a 85% no questionário final.
* **RF14 - Consulta de Recompensas:** O utilizador deve poder visualizar os badges e transferir os certificados guardados no seu perfil.

### 1.5. Biblioteca Virtual e Informação
* **RF15 - Consulta de Informação Pública:** A plataforma deve apresentar notícias, artigos, destaques semanais e a agenda de atividades.
* **RF16 - Gestão da Biblioteca:** O Manager deve poder publicar e editar notícias, eventos e artigos na área pública.

### 1.6. Módulo Estatístico
* **RF17 - Cálculo de Métricas de Aprendizagem:** O backend deve calcular o ganho de aprendizagem simples e o ganho normalizado $g = \frac{p\acute{o}s - pr\acute{e}}{m\acute{a}ximo - pr\acute{e}}$, juntamente com métricas descritivas (média, mediana, desvio-padrão, mínimos e máximos).
* **RF18 - Painel de Indicadores:** O backoffice deve apresentar gráficos sobre o número de utilizadores, taxa de conclusão e evolução das notas por recurso, área de saúde ou ano de escolaridade.
* **RF19 - Análise de Perguntas:** O sistema deve calcular a taxa de acerto por pergunta para apoiar a revisão das provas.
* **RF20 - Exportação de Dados:** O sistema deve permitir descarregar os registos de respostas em formato CSV.

---

## 2. Requisitos Não Funcionais (FURPS+)

### 2.1. Usabilidade (Usability)
* **RNF-U01 - Interface Responsiva:** A interface deve adaptar-se a diferentes tamanhos de ecrã (desktop e mobile), utilizando uma navegação adequada ao público jovem.
* **RNF-U02 - Suporte Multilingue:** A estrutura da aplicação deve estar preparada para suportar mais do que um idioma (Português e Inglês).
* **RNF-U03 - Mensagens do Sistema:** O sistema deve apresentar mensagens claras em caso de erro de preenchimento ou falha de operação.

### 2.2. Fiabilidade (Reliability)
* **RNF-R01 - Tratamento de Exceções:** O sistema deve tratar falhas de ligação à base de dados ou erros de validação sem interromper a execução do serviço.
* **RNF-R02 - Integridade dos Calculos:** Os dados estatísticos devem ser calculados diretamente a partir da base de dados no momento da consulta.

### 2.3. Desempenho (Performance)
* **RNF-P01 - Fluidade da Interface:** O carregamento das páginas do frontend deve ocorrer sem bloqueios visíveis na navegação.
* **RNF-P02 - Tempo de Resposta do Módulo Estatístico:** As consultas de processamento de dados e cálculo de métricas no backend devem responder dentro de prazos aceitáveis para o utilizador.

### 2.4. Suportabilidade (Supportability)
* **RNF-S01 - Separação de Camadas:** O projeto deve manter uma separação clara entre o frontend e o backend.
* **RNF-S02 - Organização do Código:** O código deve seguir os princípios de Programação Orientada a Objetos (POO) e incluir documentação interna.

### 2.5. Restrições (+)
* **RNF-+01 - Tecnologias de Frontend:** O frontend da aplicação deve ser construído em **React**.
* **RNF-+02 - Tecnologias de Backend:** A API e as regras de negócio devem ser desenvolvidas em **Python** com a framework **Flask**.
* **RNF-+03 - Sistema de Base de Dados:** O sistema deve utilizar **MySQL** ou **SQL Server**.
* **RNF-+04 - Proteção de Dados:** As palavras-passe devem ser guardadas com encriptação/hashing, garantindo a conformidade com as regras de proteção de dados de menores.