# Deployment Guide

The live demo uses two parts:

| Part | Host | URL |
|------|------|-----|
| Frontend | GitHub Pages | https://danieldemoz.github.io/ai-governance-assessment/ |
| Backend API | Render (Docker) | https://ai-governance-assessment.onrender.com |

The frontend is deployed automatically on every push to `main`. The backend requires a one-time Render setup (see below).

## One-time: Deploy the backend on Render

1. Open the deploy link:

   **https://render.com/deploy?repo=https://github.com/DanielDemoz/ai-governance-assessment**

2. Sign in with **GitHub** and authorize Render if prompted.

3. Review the blueprint (uses `render.yaml`):
   - Service name: `ai-governance-assessment`
   - Runtime: Docker
   - Plan: Free

4. Click **Apply** / **Deploy** and wait for the build to finish (about 5–10 minutes on first deploy).

5. Confirm the API is up:

   ```bash
   curl https://ai-governance-assessment.onrender.com/health
   ```

   Expected response: `{"status":"ok","version":"..."}`

6. Test the public demo:

   - Open https://danieldemoz.github.io/ai-governance-assessment/
   - Click **Start Assessment**
   - You should reach the organization profile step (not "Failed to fetch")

## Optional: Auto-redeploy on push

After Render creates the service:

1. In the [Render Dashboard](https://dashboard.render.com), open the service → **Settings** → copy the **Deploy Hook** URL.
2. In GitHub: **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: paste the deploy hook URL
3. Future pushes to `main` will trigger `.github/workflows/deploy-render.yml` automatically.

## Alternative: Full app on Render only

The Docker image serves both the API and frontend on one URL. After Render deploy, this also works as a standalone demo:

**https://ai-governance-assessment.onrender.com**

## Alternative: Vercel serverless API

If you prefer Vercel over Render for the API:

1. Install and log in: `npx vercel login`
2. Deploy: `npx vercel deploy --prod`
3. Add GitHub secrets: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`
4. Update `NEXT_PUBLIC_API_URL` in `.github/workflows/deploy-pages.yml` to your Vercel URL
5. Re-run the **Deploy GitHub Pages** workflow

## Local development

```bash
# Terminal 1 — backend
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:3000
- API: http://localhost:8000/health

## Notes

- Render free tier sleeps after ~15 minutes of inactivity. The first request after sleep may take 30–60 seconds (cold start).
- Demo data is stored in SQLite on Render's ephemeral disk and resets on redeploy. Reference questions are re-seeded on startup.
- Do not enter confidential or personal information in the public demo.
