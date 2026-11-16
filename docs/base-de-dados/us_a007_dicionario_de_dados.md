
## Tabela: users
**Descrição:** Guarda os dados de identificação e perfil dos utilizadores registados.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment | ID único do utilizador. |
| `name` | VARCHAR(255) | NOT NULL | Nome completo. |
| `gender_id` | INT Unsigned | NOT NULL | FK (genders.id) | Género do utilizador. |
| `schoolyear_id` | INT Unsigned | NOT NULL | FK (schoolyears.id) | Ano de escolaridade. |
| `birth_date` | DATE | NOT NULL | Data de nascimento (usado p/ menoridade). |
| `parental_consent` | BOOLEAN | NOT NULL | Default: 0 | Consentimento parental obtido. |
| `email` | VARCHAR(255) | NOT NULL | UNIQUE | Endereço de e-mail p/ login. |
| `img_url` | VARCHAR(500) | NULL | Default: NULL | URL da foto de perfil. |
| `email_verified_at` | TIMESTAMP | NULL | Default: NULL | Carimbo de verificação do email. |
| `password` | VARCHAR(255) | NOT NULL | Hash da palavra-passe. |
| `remember_token` | VARCHAR(100) | NULL | Default: NULL | Token de sessão ("Lembrar-me"). |
| `userstate_id` | INT Unsigned | NOT NULL | FK (userstates.id) | Estado da conta. |

**Regras de Validação & Integridade:**
- O campo `email` deve ter sintaxe válida de e-mail e ser único na base de dados.
- Se a idade calculada através de `birth_date` for inferior a 18 anos, `parental_consent` tem obrigatoriamente de registar o valor 1 (True) para a conta poder ser ativada (`userstate_id`).

---

## Tabela: roles
**Descrição:** Perfis/papéis de acesso (Admin, Manager, User, Guest).

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned | NOT NULL | PK | Auto-Increment | ID do perfil. |
| `name` | VARCHAR(50) | NOT NULL | UNIQUE | Nome do perfil. |

---

## Tabela: role_user
**Descrição:** Junção N:M entre utilizadores e perfis de acesso.

| Atributo | Tipo / Modificadores |
| :--- | :--- |
| `role_id` | INT Unsigned | NOT NULL | PK, FK (roles.id) |
| `user_id` | BIGINT Unsigned | NOT NULL | PK, FK (users.id) |

---

## Tabela: genders
**Descrição:** Tabela catalógica que armazena os géneros disponíveis para o perfil do utilizador.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned | NOT NULL | PK | Auto-Increment | Identificador único do género. |
| `gender` | VARCHAR(50) | NOT NULL | Designação do género. |

---

## Tabela: schoolyears
**Descrição:** Tabela catalógica que define os anos de escolaridade dos utilizadores.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned | NOT NULL | PK | Auto-Increment | Identificador único do ano de escolaridade. |
| `schoolyear` | VARCHAR(50) | NOT NULL | Designação do ano de escolaridade. |

---

## Tabela: userstates
**Descrição:** Tabela catalógica que representa os possíveis estados de uma conta de utilizador.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned | NOT NULL | PK | Auto-Increment | Identificador único do estado da conta. |
| `state` | VARCHAR(50) | NOT NULL | Designação do estado (ex: Ativo, Pendente, Bloqueado). |

---

## Tabela: resources
**Descrição:** Regista os recursos formativos (Workshops e Webinars).

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment | ID do recurso. |
| `name` | VARCHAR(255) | NOT NULL | Título do recurso. |
| `description` | TEXT | NULL | Descrição do recurso formativo. |
| `healtharea_id` | INT Unsigned | NOT NULL | FK (healthareas.id) | Área de saúde. |
| `resourcetype_id` | INT Unsigned | NOT NULL | FK (resourcetypes.id) | Tipo (Webinar/Workshop). |
| `resourcestate_id` | INT Unsigned | NOT NULL | FK (resourcestates.id) | Estado de publicação. |
| `img_url` | VARCHAR(500) | NULL | URL da imagem de capa. |
| `badge_url` | VARCHAR(500) | NULL | URL do badge atribuído no fim da formação. |

---

## Tabela: resourcelevels
**Descrição:** Níveis pedagógicos nos quais cada recurso se estrutura.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment | ID do nível. |
| `level` | INT Unsigned | NOT NULL | Default: 1 | Ordem/número do nível. |
| `title` | VARCHAR(255) | NOT NULL | Título do nível. |
| `description` | TEXT | NULL | Resumo pedagógico do nível. |
| `video_url` | VARCHAR(500) | NULL | URL do vídeo de apoio. |
| `pdf_url` | VARCHAR(500) | NULL | URL do PDF de apoio. |
| `resource_id` | BIGINT Unsigned | NOT NULL | FK (resources.id) | Recurso pai. |
| `resourcestate_id` | INT Unsigned | NOT NULL | FK (resourcestates.id) | Estado. |

---

## Tabela: resource_user
**Descrição:** Inscrições e favoritos dos utilizadores nos recursos formativos.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment | ID |
| `user_id` | BIGINT Unsigned | NOT NULL | FK (users.id) | Utilizador |
| `resource_id` | BIGINT Unsigned | NOT NULL | FK (resources.id) | Recurso |
| `favorite` | BOOLEAN | NOT NULL | Default: 0 | Registo de recurso favorito. |

---

## Tabela: resourcelevel_user
**Descrição:** Registo do progresso individual em cada nível de um recurso.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment | ID |
| `user_id` | BIGINT Unsigned | NOT NULL | FK (users.id) | Utilizador |
| `resourcelevel_id` | BIGINT Unsigned | NOT NULL | FK (resourcelevels.id) | Nível do recurso |
| `progress` | DECIMAL(5,2) | NOT NULL | Default: 0.00 | Percentagem de conclusão (0 a 100%). |

---

## Tabela: healthareas
**Descrição:** Tabela catalógica que armazena as áreas temáticas de literacia em saúde.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned \| NOT NULL \| PK \| Auto-Increment | ID da área de saúde. |
| `title` | VARCHAR(255) \| NOT NULL | Título da área de saúde. |
| `subtitle` | VARCHAR(255) \| NULL | Subtítulo descritivo. |
| `description` | TEXT \| NULL | Descrição detalhada da área temática. |
| `icon` | VARCHAR(255) \| NULL | Ícone representativo. |
| `img_url` | VARCHAR(500) \| NULL | URL da imagem de destaque. |
| `video_url` | VARCHAR(500) \| NULL | URL do vídeo introdutório. |
| `resourcestate_id` | INT Unsigned \| NOT NULL \| FK (resourcestates.id) | Estado de publicação da área. |

---

## Tabela: resourcetypes
**Descrição:** Tabela catalógica que classifica os tipos de recursos formativos (ex: Webinar, Workshop).

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned \| NOT NULL \| PK \| Auto-Increment | ID do tipo de recurso. |
| `type` | VARCHAR(50) \| NOT NULL | Designação do tipo de recurso. |

---

## Tabela: resourcestates
**Descrição:** Tabela catalógica que define os estados de publicação dos recursos e conteúdos.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned \| NOT NULL \| PK \| Auto-Increment | ID do estado do recurso. |
| `state` | VARCHAR(50) \| NOT NULL | Designação do estado (ex: Publicado, Rascunho, Arquivado). |

---

## Tabela: quizzes
**Descrição:** Questionários de diagnóstico (pré) ou finais (pós) associados aos recursos.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment | ID do quiz. |
| `name` | VARCHAR(255) | NOT NULL | Título do quiz. |
| `description` | TEXT | NULL | Instruções de preenchimento. |
| `resource_id` | BIGINT Unsigned | NOT NULL | FK (resources.id) | Recurso formativo. |
| `quiztype_id` | INT Unsigned | NOT NULL | FK (quiztypes.id) | Tipo (Diagnóstico / Final). |
| `qastate_id` | INT Unsigned | NOT NULL | FK (qastates.id) | Estado do quiz. |

---

## Tabela: questions
**Descrição:** Questões contidas num determinado questionário.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment | ID da pergunta. |
| `title` | TEXT | NOT NULL | Enunciado da pergunta. |
| `quiz_id` | BIGINT Unsigned | NOT NULL | FK (quizzes.id) | Questionário associado. |
| `qastate_id` | INT Unsigned | NOT NULL | FK (qastates.id) | Estado da pergunta. |

---

## Tabela: answers
**Descrição:** Opções de resposta para cada pergunta.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment | ID da resposta. |
| `answer` | TEXT | NOT NULL | Texto da opção de resposta. |
| `question_id` | BIGINT Unsigned | NOT NULL | FK (questions.id) | Pergunta associada. |
| `correct` | BOOLEAN | NOT NULL | Default: 0 | Indica se é a resposta correta (1 ou 0). |
| `qastate_id` | INT Unsigned | NOT NULL | FK (qastates.id) | Estado da opção. |

---

## Tabela: quiz_user
**Descrição:** Registo das submissões e notas obtidas pelos utilizadores.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment | ID do registo de avaliação. |
| `grade` | DECIMAL(5,2) | NOT NULL | Classificação obtida (0.00 a 100.00%). |
| `grade_date` | DATETIME | NOT NULL | Default: CURRENT_TIMESTAMP | Data/hora da submissão. |
| `user_id` | BIGINT Unsigned | NOT NULL | FK (users.id) | Utilizador que respondeu. |
| `quiz_id` | BIGINT Unsigned | NOT NULL | FK (quizzes.id) | Questionário respondido. |

**Regras de Negócio de Recompensa:**
- Se o `quiztype_id` corresponder a um quiz 'Final' e a pontuação em `grade` for >= 85.00%, o sistema atribui o badge e o certificado de conclusão do recurso.

---

## Tabela: quiztypes
**Descrição:** Tabela catalógica que identifica a tipologia do questionário (Diagnóstico ou Final).

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned \| NOT NULL \| PK \| Auto-Increment | ID do tipo de questionário. |
| `type` | VARCHAR(50) \| NOT NULL | Designação do tipo (ex: 'Diagnóstico', 'Final'). |

---

## Tabela: qastates
**Descrição:** Tabela catalógica que define o estado de disponibilidade dos questionários, perguntas e respostas.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned \| NOT NULL \| PK \| Auto-Increment | ID do estado. |
| `state` | VARCHAR(50) \| NOT NULL | Designação do estado (ex: 'Ativo', 'Inativo'). |

---

## Tabela: news
| Atributo | Tipo / Modificadores |
| :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment |
| `title` | VARCHAR(255) | NOT NULL |
| `description` | TEXT | NOT NULL |
| `author` | VARCHAR(150) | NOT NULL |
| `news_date` | DATETIME | NOT NULL | Default: CURRENT_TIMESTAMP |
| `img_url` | VARCHAR(500) | NULL |
| `healtharea_id` | INT Unsigned | NOT NULL | FK (healthareas.id) |
| `resourcestate_id` | INT Unsigned | NOT NULL | FK (resourcestates.id) |

---

## Tabela: activities
| Atributo | Tipo / Modificadores |
| :--- | :--- |
| `id` | BIGINT Unsigned | NOT NULL | PK | Auto-Increment |
| `title` | VARCHAR(255) | NOT NULL |
| `description` | TEXT | NULL |
| `activity_datetime` | DATETIME | NOT NULL |
| `url` | VARCHAR(500) | NULL |
| `healtharea_id` | INT Unsigned | NOT NULL | FK (healthareas.id) |
| `resourcestate_id` | INT Unsigned | NOT NULL | FK (resourcestates.id) |

---

## Tabela: contents
**Descrição:** Armazena as publicações, artigos e materiais gerais da biblioteca virtual.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | BIGINT Unsigned \| NOT NULL \| PK \| Auto-Increment | ID do conteúdo. |
| `title` | VARCHAR(255) \| NOT NULL | Título da publicação. |
| `description` | TEXT \| NULL | Resumo ou descrição do conteúdo. |
| `author` | VARCHAR(150) \| NOT NULL | Autor da publicação. |
| `url` | VARCHAR(500) \| NULL | URL de acesso ao recurso/documento. |
| `healtharea_id` | INT Unsigned \| NOT NULL \| FK (healthareas.id) | Área de saúde relacionada. |
| `resourcestate_id` | INT Unsigned \| NOT NULL \| FK (resourcestates.id) | Estado de publicação. |
| `contenttype_id` | INT Unsigned \| NOT NULL \| FK (contenttypes.id) | Tipo de conteúdo associado. |

---

## Tabela: contenttypes
**Descrição:** Tabela catalógica que categoriza os tipos de conteúdos disponíveis na biblioteca virtual.

| Atributo | Tipo / Modificadores | Descrição |
| :--- | :--- | :--- |
| `id` | INT Unsigned \| NOT NULL \| PK \| Auto-Increment | ID do tipo de conteúdo. |
| `type` | VARCHAR(50) \| NOT NULL | Designação do tipo (ex: Artigo, Publicação, Infográfico). |
---

## Mapeamento de Integridade Referencial (Foreign Keys)

| Tabela Origem | Coluna FK | Tabela Destino | Coluna PK | On Delete / On Update |
| :--- | :--- | :--- | :--- | :--- |
| `users` | `gender_id` | `genders` | `id` | RESTRICT / CASCADE |
| `users` | `schoolyear_id` | `schoolyears` | `id` | RESTRICT / CASCADE |
| `users` | `userstate_id` | `userstates` | `id` | RESTRICT / CASCADE |
| `role_user` | `user_id` | `users` | `id` | CASCADE / CASCADE |
| `role_user` | `role_id` | `roles` | `id` | CASCADE / CASCADE |
| `resources` | `healtharea_id` | `healthareas` | `id` | RESTRICT / CASCADE |
| `resources` | `resourcetype_id` | `resourcetypes` | `id` | RESTRICT / CASCADE |
| `resourcelevels` | `resource_id` | `resources` | `id` | CASCADE / CASCADE |
| `resource_user` | `user_id` | `users` | `id` | CASCADE / CASCADE |
| `resource_user` | `resource_id` | `resources` | `id` | CASCADE / CASCADE |
| `quizzes` | `resource_id` | `resources` | `id` | CASCADE / CASCADE |
| `quizzes` | `quiztype_id` | `quiztypes` | `id` | RESTRICT / CASCADE |
| `questions` | `quiz_id` | `quizzes` | `id` | CASCADE / CASCADE |
| `answers` | `question_id` | `questions` | `id` | CASCADE / CASCADE |
| `quiz_user` | `user_id` | `users` | `id` | CASCADE / CASCADE |
| `quiz_user` | `quiz_id` | `quizzes` | `id` | CASCADE / CASCADE |