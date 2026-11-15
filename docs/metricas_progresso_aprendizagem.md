# Métricas de Avaliação do Progresso de Aprendizagem

## Métricas e fórmulas

### Evolução absoluta da aprendizagem

Mede a diferença entre a classificação obtida no questionário final e a classificação obtida no diagnóstico inicial.

**Fórmula:**

`Evolução = Nota Final - Nota Inicial`

**Variáveis:**
- Nota inicial: classificação do questionário de diagnóstico.
- Nota final: classificação do questionário final.

**Origem dos dados:**
- `quiz_user.grade`
- `quiz_user.user_id`
- `quiz_user.quiz_id`
- `quizzes.quiztype_id`
- `quizzes.resource_id`
- `quiztypes.type`

O diagnóstico e a avaliação final devem pertencer ao mesmo utilizador e ao mesmo recurso formativo.

### Evolução percentual relativa

Representa a evolução da classificação final relativamente à classificação inicial.

**Fórmula:**

`Evolução (%) = ((Nota Final - Nota Inicial) / Nota Inicial) * 100`

**Variáveis:**
- Nota inicial.
- Nota final.

**Origem dos dados:** os mesmos campos identificados na métrica anterior.

**Regra:** quando a nota inicial é igual a zero, a evolução percentual relativa não deve ser calculada, para evitar uma divisão por zero. Nesse caso, deve ser apresentada apenas a evolução absoluta.

### Taxa de conclusão dos níveis formativos

Permite avaliar a percentagem de níveis concluídos por um utilizador numa determinada formação.

**Fórmula:**

`Taxa de conclusão (%) = (Número de níveis concluídos / Número total de níveis da formação) * 100`

Considera-se um nível concluído quando o campo `progress` apresenta o valor de 100%.

**Variáveis:**
- Progresso individual de cada nível.
- Número total de níveis associados ao recurso.
- Identificador do utilizador e do recurso.

**Origem dos dados:**
- `resourcelevel_user.user_id`
- `resourcelevel_user.resourcelevel_id`
- `resourcelevel_user.progress`
- `resourcelevels.id`
- `resourcelevels.resource_id`

### Taxa de aprovação na avaliação final

Mede a percentagem de utilizadores que alcançam a classificação mínima de 85% na avaliação final.

**Fórmula:**

`Taxa de aprovação (%) = (Número de utilizadores aprovados / Número de utilizadores com avaliação final) * 100`

Considera-se aprovado o utilizador que obtenha uma classificação igual ou superior a 85%.

**Variáveis:**
- Classificação final.
- Tipo de questionário.
- Identificador do utilizador.
- Identificador do recurso formativo.

**Origem dos dados:**
- `quiz_user.grade`
- `quiz_user.user_id`
- `quiz_user.quiz_id`
- `quizzes.quiztype_id`
- `quizzes.resource_id`
- `quiztypes.type`

### Data de início da formação

Permite identificar quando um utilizador iniciou uma determinada formação e analisar o intervalo entre o início e a submissão da avaliação final.

**Variáveis:**
- Data e hora de início da formação.
- Data e hora de submissão da avaliação final.

**Origem dos dados:**
- `resource_user.started_at` — novo campo proposto.
- `quiz_user.grade_date` — data e hora da submissão.

O intervalo entre estas datas representa o tempo decorrido entre o início da formação e a submissão da avaliação final. Não representa o tempo efetivo de estudo.

## Mapeamento das variáveis no modelo relacional

| Tabela | Campo | Utilização |
|---|---|---|
| `quiz_user` | `grade` | Classificação obtida |
| `quiz_user` | `grade_date` | Data/hora da submissão |
| `quiz_user` | `user_id` | Identificação do utilizador |
| `quiz_user` | `quiz_id` | Identificação do questionário |
| `quizzes` | `quiztype_id` | Identificação do tipo de questionário |
| `quizzes` | `resource_id` | Identificação da formação |
| `quiztypes` | `type` | Distinguir diagnóstico e avaliação final |
| `resourcelevel_user` | `progress` | Percentagem de conclusão do nível |
| `resourcelevel_user` | `user_id` | Identificação do utilizador |
| `resourcelevel_user` | `resourcelevel_id` | Identificação do nível |
| `resourcelevels` | `resource_id` | Associação do nível à formação |
| `resources` | `healtharea_id` | Associação da formação à área temática |
| `resource_user` | `started_at` | Data/hora de início da formação — proposta |

## Alteração proposta ao Dicionário de Dados

Propõe-se acrescentar o seguinte campo à tabela `resource_user`:

| Campo | Tipo | Nulidade | Descrição |
|---|---|---|---|
| `started_at` | DATETIME | NULL | Data e hora em que o utilizador iniciou a formação. |

O campo deve ser preenchido no primeiro início da formação e manter o seu valor original em acessos posteriores.

Esta alteração permite identificar a data de início, mas não permite medir a duração efetiva do estudo.

A alteração deverá ser validada pela equipa e refletida no Modelo Relacional (US_A003) e no Dicionário de Dados (US_A007), caso seja aprovada.

## Limitações e necessidades futuras

O modelo atual permite calcular a evolução entre avaliações, o progresso dos níveis e a taxa de aprovação. Contudo, existem indicadores que exigem informação adicional:

- **Tempo efetivo de estudo:** seria necessário registar sessões de estudo e respetiva duração.
- **Retenção da aprendizagem:** seria necessário implementar uma avaliação de acompanhamento posterior à avaliação final.
- **Análise ao nível de cada pergunta:** seria necessário registar a resposta selecionada por cada utilizador, associando-a à respetiva pergunta e submissão.

A conclusão de níveis formativos não deve ser confundida com retenção da aprendizagem. São indicadores diferentes.

## Regras de validação

1. A comparação de classificações deve considerar o mesmo utilizador e o mesmo recurso formativo.
2. A classificação inicial deve corresponder a um questionário do tipo Diagnóstico.
3. A classificação final deve corresponder a um questionário do tipo Final.
4. As classificações devem estar compreendidas entre 0 e 100.
5. A evolução percentual relativa não deve ser calculada quando a classificação inicial é zero.
6. Um nível só é considerado concluído quando `progress = 100`.
7. A taxa de aprovação deve considerar apenas avaliações finais válidas.
8. O campo `started_at` deve conservar a primeira data de início da formação.