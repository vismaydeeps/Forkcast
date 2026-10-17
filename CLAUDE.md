# Forkcast

## Goal
Forkcast is an AI meal-planning web app. A user keeps a live pantry inventory, and an LLM recommends recipes from it. Nutrition is verified through Spoonacular rather than trusted from the LLM. The app tracks daily and weekly macros, rebalances the rest of the plan when a meal is skipped or a cheat meal is logged, and builds a shopping list from the gap between plan and pantry. Scope, schema, endpoints and roadmap live in `docs/prd.md`. Read it before planning a new week. The reasoning behind past choices is in `docs/decisions.md`.

## Run / test (Windows, PowerShell)
1. `docker ps`. If postgres and redis aren't up, run `docker-compose up -d` from the repo root.
2. Backend: `cd backend; ..\.venv\Scripts\activate; uvicorn app.main:app --reload --port 8000`
   - Must run from `backend/`, or you get `No module named 'app'`. Restart after any `.env` change.
3. Frontend (second terminal): `cd frontend; npm run dev`, then open http://localhost:5173
4. Migrations (from `backend/`): `alembic revision --autogenerate -m "msg"`, then `alembic upgrade head`
5. Health: http://localhost:8000/health. Interactive API: http://localhost:8000/docs
- PowerShell `curl` is `Invoke-WebRequest`. Use `-Method/-ContentType/-Body/-UseBasicParsing`.
- No automated tests yet. Verify through the UI or `/docs`.

## Layout
```
backend/app/   config.py database.py redis_client.py main.py
               models/ schemas/ services/ routers/ middleware/
backend/alembic/   async env.py, reads URL from app.config
frontend/src/  api/ (client.js + one file per domain)  context/  hooks/  pages/  components/
docs/          prd.md  decisions.md
```

## Conventions
- Routers stay thin and call `services/<domain>_service.py`. Services raise `ValueError`, and routers map it to `HTTPException`.
- Every query on user-owned rows filters by `user_id` from `get_current_user`. This prevents IDOR.
- Each domain has three schemas: `Create`, `Update` (all optional, applied with `model_dump(exclude_unset=True)`) and `Response` (`from_attributes`).
- Models use SQLAlchemy 2.0 `Mapped[]`. Timestamps default to `lambda: datetime.now(timezone.utc)`.
- External I/O is `async` with `httpx`. Spoonacular calls go through Redis cache-aside (`<kind>:<key>`, 24h TTL).
- Endpoints that spend external quota require auth.
- Declare static routes before `/{id}` routes.
- The JWT holds only `sub` and `exp`.
- Frontend: HTTP calls only in `src/api/*`. Auth state lives in `AuthContext`. Debounce search inputs. Tailwind v3.
- Commits: `feat|fix|chore: Week N - <short summary>`, one per milestone.
- The user is new to React. Briefly explain each new file and frontend pattern, and state the tradeoffs before choosing.

## Status
- Week 1 (auth, 5 models, migrations, React shell) is done. Register and login were verified via API.
- Week 2 (pantry CRUD, Spoonacular autocomplete, Redis, Navbar, Pantry page) is written but not verified.
- Blocker: UI register returns 500. The browser's CORS error is only a side effect. See Open questions in `docs/decisions.md`.

## Next 3 tasks
1. Fix the register 500. Capture the uvicorn traceback first.
2. Verify the pantry flow end to end in the UI, then commit Week 2.
3. Plan Week 3 (the LLM pipeline) in plan mode against `docs/prd.md` before writing code.
