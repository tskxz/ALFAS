## 1. Convidado (Utilizador Não Registado)
* **Descrição:** Qualquer visitante que acede à plataforma livremente por via da web, sem efetuar autenticação ou registo prévio.
* **Contexto de Atuação:** Frontoffice (Área Pública).
* **Principais Funcionalidades / Permissões:**
  * Consultar conteúdos públicos: áreas de informação de saúde, notícias, publicações e agenda de atividades da biblioteca virtual.
  * Iniciar o processo de registo para criação de conta de utilizador.

---

## 2. Utilizador Registado (Jovem / Formando)
* **Descrição:** Utilizador autenticado que concluiu com sucesso o registo na plataforma.
* **Contexto de Atuação:** Frontoffice (Área Reservada).
* **Principais Funcionalidades / Permissões:**
  * Pesquisar, consultar e inscrever-se em recursos formativos (workshops e webinars).
  * Aceder aos conteúdos formativos, gravações e materiais de apoio organizados por níveis.
  * Responder obrigatoriamente ao questionário de diagnóstico (pré) antes do acesso aos conteúdos.
  * Responder ao questionário final (pós) para avaliação do progresso de aprendizagem.
  * Visualizar a evolução pessoal e o ganho de aprendizagem obtido.
  * Obter *badges* e certificados digitais de conclusão (gerados quando a pontuação no questionário final é $\ge 85\%$).
  * Consultar e atualizar os seus dados pessoais de perfil.

---

## 3. Encarregado de Educação / Tutor
* **Descrição:** Ator responsável legal pelo menor de idade que pretende registar-se na plataforma. A sua intervenção é um requisito de proteção de dados e conformidade legal.
* **Contexto de Atuação:** Frontoffice (Fluxo Externo de Validação).
* **Principais Funcionalidades / Permissões:**
  * Receber a notificação eletrónica contendo o pedido de consentimento informado.
  * Validar e autorizar o registo do menor através de confirmação digital, ação indispensável para que o sistema ative a conta do jovem.

---

## 4. Formador / Profissional de Saúde (Dinamizador)
* **Descrição:** Profissional especializado (professor ou profissional de saúde) responsável por dinamizar as atividades, workshops e webinars disponibilizados na plataforma.
* **Contexto de Atuação:** Frontoffice / Produção de Conteúdos.
* **Principais Funcionalidades / Permissões:**
  * Dinamizar os eventos e sessões formativas.
  * *Nota de Arquitetura:* As suas ações operacionais na plataforma (como a submissão ou disponibilização de novos materiais) são geridas e publicadas através da área de administração pelos gestores de conteúdos (*Managers*).

---

## 5. Manager (Gestor de Conteúdos)
* **Descrição:** Utilizador registado com privilégios de acesso à área de administração (*Backoffice*), responsável pela curadoria, dinamização e gestão operacional de conteúdos e avaliações.
* **Contexto de Atuação:** Backoffice (Área de Gestão).
* **Principais Funcionalidades / Permissões:**
  * Gerir a Biblioteca Virtual: adicionar, editar e remover recursos formativos (webinars e workshops), áreas de saúde, categorias, atividades e notícias.
  * Gerir a Avaliação: criar, editar e configurar os questionários de diagnóstico e finais associados a cada recurso formativo.
  * Consultar o módulo de estatísticas: visualizar indicadores de utilização da plataforma (inscrições, taxa de conclusão) e indicadores estatísticos de aprendizagem (ganho médio normalizado, distribuições e análise de perguntas).
  * Exportar dados brutos das respostas e classificações (ex.: em formato CSV) para posterior análise externa detalhada.

---

## 6. Administrador (Admin)
* **Descrição:** Utilizador com privilégios máximos e acesso total a todas as vertentes do sistema informático.
* **Contexto de Atuação:** Backoffice (Área de Administração Geral).
* **Principais Funcionalidades / Permissões:**
  * Acumular todas as permissões e funcionalidades operacionais do *Manager*.
  * Gerir utilizadores, perfis de acesso (*roles*) e estados das contas (ex.: ativa, inativa, pendente).
  * Configurar permissões de segurança, políticas de privacidade e garantir o correto funcionamento e integridade global do sistema.

---