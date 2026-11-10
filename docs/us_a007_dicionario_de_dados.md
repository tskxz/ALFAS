
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

## Tabelas Catalógicas do Utilizador
- **genders**: `id` (PK), `gender` VARCHAR(50) NOT NULL
- **schoolyears**: `id` (PK), `schoolyear` VARCHAR(50) NOT NULL
- **userstates**: `id` (PK), `state` VARCHAR(50) NOT NULL

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

## Tabelas Catalógicas de Recursos
- **healthareas**: `id` (PK), `title`, `subtitle`, `description`, `icon`, `img_url`, `video_url`, `resourcestate_id` (FK).
- **resourcetypes**: `id` (PK), `type` (VARCHAR(50)).
- **resourcestates**: `id` (PK), `state` (VARCHAR(50)).

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

## Tabelas Catalógicas de Quizzes
- **quiztypes**: `id` (PK), `type` VARCHAR(50) (ex: 'Diagnóstico', 'Final').
- **qastates**: `id` (PK), `state` VARCHAR(50) (ex: 'Ativo', 'Inativo').

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

## Tabela: contents e contenttypes
- **contents**: `id` (PK), `title`, `description`, `author`, `url`, `healtharea_id` (FK), `resourcestate_id` (FK), `contenttype_id` (FK).
- **contenttypes**: `id` (PK), `type` VARCHAR(50).

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