## Agregados de Negócio

* **Utilizador**: Agregado responsável pela gestão de utilizadores, autenticação, controlo de perfis/roles (Admin, Manager, Utilizador Registado, Convidado), estados da conta e registo do consentimento parental para menores de idade.
* **Formação**: Agregado que reúne os recursos formativos (webinars e workshops), respetivas áreas de saúde, níveis de aprendizagem, tipos e estados dos conteúdos.
* **Diagnóstico**: Agregado responsável pela estrutura de questionários (diagnóstico pré e final pós), gestão de perguntas, opções de resposta e registo de classificações/desempenho dos utilizadores.
* **Gamificação**: Agregado focado nos elementos de recompensa e progressão, como a validação de critérios e atribuição automática de *badges* e certificados de conclusão.
* **Biblioteca Virtual**: Agregado que gere as publicações, notícias, agenda de atividades e destaques informativos disponibilizados na plataforma.

---

## Entidades de Domínio, Objetos de Valor e Atributos Essenciais

### Entidades e Agregados Principais
* **User (Entidade Raiz - Utilizador)**
  * **Atributos:** `id`, `name`, `email`, `birth_date`, `parental_consent`, `password`, `img_url`, `email_verified_at`, `remember_token`, `gender_id`, `schoolyear_id`, `userstate_id`
* **Resource (Entidade Raiz - Formação)**
  * **Atributos:** `id`, `name`, `description`, `img_url`, `badge_url`, `healtharea_id`, `resourcetype_id`, `resourcestate_id`
* **HealthArea (Entidade)**
  * **Atributos:** `id`, `title`, `subtitle`, `description`, `icon`, `img_url`, `video_url`, `resourcestate_id`
* **ResourceLevel (Entidade)**
  * **Atributos:** `id`, `level`, `title`, `description`, `video_url`, `pdf_url`, `resource_id`, `resourcestate_id`
* **Quiz (Entidade Raiz - Avaliação/Diagnóstico)**
  * **Atributos:** `id`, `name`, `description`, `resource_id`, `quiztype_id`, `qastate_id`
* **Question (Entidade)**
  * **Atributos:** `id`, `title`, `quiz_id`, `qastate_id`
* **Answer (Entidade)**
  * **Atributos:** `id`, `answer`, `correct`, `question_id`, `qastate_id`
* **QuizUser (Entidade de Associação / Histórico de Avaliação)**
  * **Atributos:** `id`, `grade`, `grade_date`, `user_id`, `quiz_id`
* **ResourceUser & ResourceLevelUser (Entidades de Associação / Gamificação e Progresso)**
  * **Atributos:** `id`, `user_id`, `resource_id` / `resourcelevel_id`, `favorite`, `progress`
* **News, Activity & Content (Entidades - Biblioteca Virtual)**
  * **Atributos:** `id`, `title`, `description`, `author`, `url`, `news_date` / `activity_datetime`, `healtharea_id`, `resourcestate_id`

### Objetos de Valor (Value Objects)
Entidades imutáveis representativas de estados, tipos ou tabelas de domínio auxiliar:
* `Gender`, `SchoolYear`, `UserState`, `ResourceType`, `ResourceState`, `QuizType`, `QAState`, `ContentType`

---

## Associações, Multiplicidades e Regras de Invariância

### Associações e Multiplicidades
* **Utilizador – Recurso Formativo ($1 \dots *$)**: Um `User` pode inscrever-se e associar-se a múltiplos `Resource` através de `ResourceUser`.
* **Recurso Formativo – Questionário ($1 \dots 2$)**: Cada `Resource` é enquadrado por até dois `Quiz` (diagnóstico pré-formação e avaliação final pós-formação).
* **Questionário – Pergunta ($1 \dots *$)**: Um `Quiz` é composto por uma ou mais `Question`.
* **Pergunta – Resposta ($1 \dots *$)**: Cada `Question` possui múltiplas opções de `Answer` (com indicação da resposta correta).
* **Área de Saúde – Conteúdos / Formações ($1 \dots *$)**: Uma `HealthArea` agrupa diversos `Resource`, `News`, `Activity` e `Content`.

### Regras de Invariância (Invariants)
1. **Consentimento Parental Obrigatorio:** O registo de utilizadores menores de idade exige que o atributo `parental_consent` seja explicitamente validado (`true`) antes da ativação e acesso à conta.
2. **Sequência do Percurso de Aprendizagem:** O acesso ao conteúdo formativo (`ResourceLevel`) e ao questionário final exige obrigatoriamente a resolução prévia do questionário de diagnóstico (pré).
3. **Atribuição de Certificados e Badges:** A emissão do certificado de conclusão e do *badge* do recurso só ocorre se a pontuação obtida no questionário final for igual ou superior a 85% ($grade \ge 85$).

---