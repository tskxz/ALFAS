# ALFAS - Plataforma de Literacia em Saúde para Jovens

## Descrição do Projeto

O consórcio **ALFAS (Alfabetização em Saúde)** tem como missão disponibilizar uma plataforma web interativa orientada para jovens em idade escolar (3.º ciclo e ensino secundário), professores e profissionais de saúde, promovendo hábitos saudáveis e decisões informadas.

### Principais Funcionalidades

- **Recursos Formativos:** Oferta de webinars e workshops estruturados por temas de saúde, com acesso a vídeos e materiais de apoio.
- **Percurso e Avaliação de Aprendizagem:** Cada formação integra um questionário de diagnóstico inicial (pré-formação) e um questionário final (pós-formação), permitindo calcular e acompanhar o ganho de aprendizagem.
- **Gamificação:** Atribuição de badges e certificados de conclusão para os utilizadores que obtenham 85% ou mais no questionário final.
- **Biblioteca Virtual:** Espaço com publicações temáticas, notícias de saúde, agenda de atividades e destaques semanais geridos pelo backoffice.
- **Consentimento Parental:** Processo específico de verificação de idade e solicitação de autorização parental para utilizadores menores.

## Atores do Sistema

- **Convidado (Utilizador Não Registado):** Consulta informação pública, notícias, agenda e realiza o registo.
- **Utilizador Registado:** Inscreve-se em formações, acede aos recursos, responde a questionários e consulta o seu progresso e prémios.
- **Gestor de Conteúdos (Manager):** Faz a gestão de formações, questionários, notícias e analisa métricas de aprendizagem.
- **Administrador:** Efetua a gestão total da plataforma, perfis de acesso, utilizadores e integridade do sistema.

## Arquitetura e Tecnologias

A solução adota uma arquitetura em camadas com separação entre cliente e servidor:

- **Frontend:** React (interface intuitiva, responsiva e adaptada ao público jovem)
- **Backend:** Python com Flask (regras de negócio, rotas e tratamento estatístico)
- **Base de Dados:** MySQL / SQL Server (modelo relacional normalizado)
