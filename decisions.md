# Design Decisions

Only the decisions you can't work out by reading the code are listed here, with the reasoning and the alternatives that were rejected.

## Architecture and data

- **Nutrition is never trusted from the LLM.** Spoonacular values override LLM estimates in pipeline step 4. LLM macro estimates are unreliable, and macro accuracy is what makes the product worth using.
- **The LLM step sits behind its own interface.** It's meant to be replaced by a collaborative-filtering model in Phase 2, once interaction data exists. Don't let ranking, enrichment or prompt code depend on LLM-specific types.
- **`MealPlan.recipe_data` is JSON, not normalised tables.** Recipe shape varies by source. Verified nutrition is copied into `NutritionLog` at log time, so history doesn't depend on the plan row surviving.
- **`NutritionLog.meal_plan_id` uses `ON DELETE SET NULL`, while other FKs cascade.** Deleting or regenerating a plan must not erase what the user actually ate.
- **`RebalanceEvent` stores before and after snapshots.** These are an immutable audit trail and feed the diff UI in Week 5. They are not live data.
- **The JWT carries only `sub` and `exp`.** Profile data is fetched fresh on each request, so a stale token never holds outdated or revocable claims.
- **Ingredient search requires auth even though it doesn't use the user.** Otherwise anyone could drain the 150 req/day Spoonacular quota.
- **Pantry items store the Spoonacular `ingredient_id`, not just a name.** This gives later nutrition lookups and plan-vs-pantry diffs a stable key instead of fuzzy-matching free text.
- **Search is debounced at 400ms and cache keys are lowercased.** Both exist to protect the API quota.

## Environment

- **Postgres runs in Docker on host port 5433, not 5432.** A leftover local Windows Postgres service holds 5432 and was silently answering connections, which caused `InvalidPasswordError` against the right credentials.
- **bcrypt is pinned to 4.0.1.** passlib 1.7.4 is incompatible with bcrypt 5.x, which raises a spurious "password cannot be longer than 72 bytes" error. Keep `passlib[bcrypt]` and this pin together.
- **Node is 20.19 through nvm-windows.** Node 24's bundled npm was broken ("Class extends value undefined"), and create-vite needs at least 20.12 (`util.styleText`).
- **Alembic `env.py` is async.** It uses `create_async_engine` with `run_sync`, and the URL comes from `app.config` rather than `alembic.ini`, so there's one source of truth for the connection string.

## Rejected approaches

| Rejected | Chosen | Why |
|---|---|---|
| Local Postgres/Redis installs | docker-compose | Reproducible, disposable, no global installs on Windows |
| psycopg2 / sync driver | asyncpg | Whole stack is async. A plain `postgresql://` URL silently selects psycopg2 |
| Tailwind v4 | Tailwind v3 | v4 has breaking config changes and fewer learning resources |
| oxlint | ESLint | More mature React rules and ecosystem |
| Shared pooled `httpx` client (deferred, not rejected) | New `AsyncClient` per call | Simpler while learning. Revisit if external-call latency matters |
| Two `.gitignore` files | Single root `.gitignore` | Unanchored patterns already match at any depth |

## Open questions

1. **Register returns 500 from the UI (current blocker).** The top suspect is that `PantryItem.user` declares `back_populates="pantry_items"`, but `User` has no `pantry_items` relationship. This only surfaced once `main.py` imported the pantry router, because mapper configuration then fails on the first query. That would explain why register worked in Week 1 but fails now. The browser's CORS error is a side effect, since unhandled 500s bypass the CORS headers. Confirm with the uvicorn traceback.
2. **bcrypt rounds.** The PRD requires at least 12. `bcrypt__rounds=12` was removed while debugging the bcrypt version issue. passlib's default is 12, but it should be set explicitly again now that bcrypt is pinned.
3. **The token lives in `localStorage`, which is exposed to XSS.** An httpOnly cookie is safer but needs CSRF handling. Decide before deploying.
4. **LLM provider.** The PRD allows OpenAI or Anthropic, and the requirements file only has `langchain-openai`. Pick one before Week 3, and keep the interface provider-agnostic either way.
5. **LLM fallback "cached recommendation".** What's the cache key (user + slot + pantry hash?) and how stale can a result be?
6. **Unit mismatches between pantry and recipes** (g vs cup vs pcs) will affect pantry auto-deduction in Week 4 and the shopping-list diff in Week 6. A conversion strategy is needed.
7. **Spoonacular errors currently surface as raw 500s.** The PRD wants a user-facing retry prompt. This is planned for Week 6 polish.
