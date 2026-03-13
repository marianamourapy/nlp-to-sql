# Prompt Design Documentation

This file describes the design decisions behind each system prompt in `llm/prompts.py`.

---

## 1. `context_resolver_prompt`

**Purpose:** Rewrites the user's latest question to be fully self-contained, resolving ambiguous pronouns using the conversation history.

**Design decisions:**

- Only rewrites when ambiguous pronouns are detected (`it`, `they`, `their`, `them`, `he`, `she`, `this`, `that`). If the question is already self-contained, it is returned **exactly** as written — no paraphrasing, no additions.
- Explicit examples of self-contained questions are provided (`"tell me 2 customers"`, `"give me one product"`) to prevent the model from over-resolving questions that don't need it. This was a real bug: the model was rewriting questions that were already complete, introducing unintended context.
- The prompt does **not** ask the model to answer the question — only to rewrite it. This keeps the node single-responsibility.

---

## 2. `classifier_prompt`

**Purpose:** Classifies the user's question into one of three categories: `YES`, `NO`, or `WRITE`.

**Design decisions:**

- Originally a binary `YES`/`NO` classifier. `WRITE` was added as a third category to handle `INSERT`, `UPDATE`, `DELETE`, and `DROP` operations with a specific rejection message, instead of letting them fall through to `generate_sql` and fail at validation.
- `"When in doubt, reply YES"` is intentional — it's better to attempt a query and fail gracefully at validation than to reject a legitimate database question.
- The schema context is injected so the model can make informed decisions about what is and isn't a database question for this specific schema.

---

## 3. `generator_system_prompt`

**Purpose:** Generates a syntactically correct PostgreSQL `SELECT` query that answers the user's question.

**Design decisions:**

- PostgreSQL-specific syntax rules are injected via `POSTGRESQL_SYNTAX` (a separate module) to avoid common errors like using MySQL-style `DATE_FORMAT` instead of `EXTRACT`.
- Column names are always qualified with their table name (e.g., `customers.name`) to avoid ambiguity in JOINs.
- ID columns are excluded from `SELECT` by default unless the user explicitly asks for them. This prevents the interpreter from receiving raw IDs and presenting them as an answer.
- When sales are involved, the prompt enforces JOINs with `customers` and `products` to return human-readable names instead of foreign key IDs.
- `LIMIT` is only applied when the user explicitly requests a specific number of results, preventing arbitrary truncation of query results.

---

## 4. `interpreter_system_prompt`

**Purpose:** Translates the raw SQL result into a clear, natural language answer.

**Design decisions:**

- The model is instructed to base its answer strictly on the SQL result — no inference, no added context. This prevents hallucination when results are sparse or unexpected.
- ID handling required explicit rules after a bug where the model would refuse to show IDs even when the user explicitly asked for them. The current rules are:

  | Situation | Behavior |
  |---|---|
  | User asked for IDs | Show IDs alongside names |
  | User did NOT ask for IDs | Never mention IDs |
  | Result contains only IDs, user did not ask | State that the information is incomplete |

- Empty results are handled explicitly — the model states that no records were found rather than attempting to explain or infer why.
- Aggregated values are explained in context (e.g., `"March had 6 sales"` rather than just `"6"`).