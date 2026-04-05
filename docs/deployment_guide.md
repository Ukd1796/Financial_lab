# Deployment Guide — tactiq.in

## Architecture Overview

```
tactiq.in           → Vercel (frontend — free tier)
api.tactiq.in       → Railway (FastAPI backend — ~$5/mo)
cron (2 jobs)       → Railway (paper signals + orders — same service)
Database            → Supabase B (already running — free tier)
```

Railway hosts the backend + cron jobs.
Vercel hosts the React frontend as a static site.
Your domain `tactiq.in` is split: root → Vercel, `api.` subdomain → Railway.

---

## Part 1 — Backend on Railway

### 1.1 What already exists

`railway.toml` is already in the repo root:
```toml
[build]
builder = "nixpacks"
```

Nixpacks auto-detects Python, installs from `requirements.txt` and `api/requirements.txt`, and builds the app.

### 1.2 Add a start command

Railway needs to know how to start the API. Create a `Procfile` at the repo root:

```
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

Railway injects `$PORT` automatically — never hardcode 8000 in production.

### 1.3 Environment variables to set in Railway

Go to your Railway service → **Variables** tab and add:

| Variable | Value |
|---|---|
| `DATABASE_URL` | `postgresql://postgres:PASSWORD@db.dbptdhnamqtfwvupscia.supabase.co:5432/postgres` |
| `OPENAI_API_KEY` | `sk-...` |
| `EMAIL_FROM` | `ujjwalkumar1796@gmail.com` |
| `EMAIL_TO` | `ukdwiwedi1357@gmail.com` |
| `EMAIL_APP_PASSWORD` | your Gmail app password |
| `ALLOWED_ORIGINS` | `https://tactiq.in,https://www.tactiq.in` |
| `SUPPRESS_NEW_BUYS` | `0` |

> **Never commit `.env` to git.** Railway variables replace the `.env` file in production.

### 1.4 Deploy steps

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Link to your project (create one first at railway.app)
railway link

# 4. Deploy
railway up
```

Or connect your GitHub repo in the Railway dashboard and enable auto-deploy on push to `main`.

### 1.5 Verify

```bash
# Check logs
railway logs

# Hit the health endpoint
curl https://your-service.railway.app/api/health
# → {"status": "ok"}
```

---

## Part 2 — Cron Jobs on Railway

Railway supports cron jobs natively — same project, separate service, minimal extra cost.

### 2.1 Create two cron services

In your Railway project dashboard → **+ New** → **Cron Job** (repeat twice):

**Job 1 — Paper Signals (3:35 PM IST = 10:05 UTC)**

| Field | Value |
|---|---|
| Schedule | `5 10 * * 1-5` |
| Command | `python -m api.run_paper_signals` |
| Root directory | `/` (same repo) |
| Environment | Same variables as the web service |

**Job 2 — Paper Orders (9:15 AM IST = 3:45 UTC)**

| Field | Value |
|---|---|
| Schedule | `45 3 * * 1-5` |
| Command | `python -m api.run_paper_orders` |
| Root directory | `/` (same repo) |
| Environment | Same variables as the web service |

> Both cron jobs use the same repo and the same env vars. Railway builds them from the same `nixpacks` config. No separate Dockerfile needed.

### 2.2 Cost estimate

| Service | Railway plan | Est. monthly |
|---|---|---|
| Web API | Hobby ($5 credit/mo) | ~$3–5 |
| Cron signals | Shared with hobby credit | ~$0–1 |
| Cron orders | Shared with hobby credit | ~$0–1 |
| **Total Railway** | | **~$5/mo** |
| Supabase | Free tier (500 MB) | $0 |
| Vercel | Free tier | $0 |
| **Total** | | **~$5/mo** |

---

## Part 3 — Frontend on Vercel

Vercel is the lowest-friction host for a Vite/React app and has a generous free tier.

### 3.1 Deploy steps

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. In the frontend directory
cd /Users/ujjwalkumar/strategy-compass
vercel

# Follow the prompts:
#   Set up and deploy? Y
#   Which scope? your account
#   Link to existing project? N (first time)
#   Project name: tactiq
#   In which directory is your code? ./
#   Override build settings? N
```

Or go to vercel.com → Import Git Repository → select `strategy-compass`.

### 3.2 Vercel build settings

| Setting | Value |
|---|---|
| Framework preset | Vite |
| Build command | `npm run build` |
| Output directory | `dist` |
| Install command | `npm install` |

### 3.3 Environment variables in Vercel

Go to Vercel project → **Settings** → **Environment Variables**:

| Variable | Value |
|---|---|
| `VITE_API_URL` | `https://api.tactiq.in/api` |
| `VITE_SUPABASE_URL` | `https://dbptdhnamqtfwvupscia.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | your anon key |

> `VITE_` prefix is required — Vite only exposes variables with this prefix to the browser bundle.

---

## Part 4 — Custom Domain `tactiq.in`

### 4.1 DNS records to add

Log in to your domain registrar (wherever `tactiq.in` is registered) and add:

```
# Frontend (root domain → Vercel)
Type   Name    Value
A      @       76.76.21.21
CNAME  www     cname.vercel-dns.com

# Backend API (subdomain → Railway)
CNAME  api     your-service.up.railway.app
```

> Get the Railway hostname from: Railway dashboard → your web service → **Settings** → **Domains** → copy the `.railway.app` URL.

### 4.2 Add domains in Railway

Railway service → **Settings** → **Domains** → **+ Custom Domain** → enter `api.tactiq.in`

Railway will provision a TLS certificate automatically via Let's Encrypt.

### 4.3 Add domain in Vercel

Vercel project → **Settings** → **Domains** → add `tactiq.in` and `www.tactiq.in`

Vercel will verify via the DNS records and issue a TLS certificate.

### 4.4 DNS propagation

Changes typically propagate within 5–30 minutes. Verify with:

```bash
dig api.tactiq.in CNAME
curl https://api.tactiq.in/api/health
# → {"status": "ok"}
```

---

## Part 5 — Update CORS for Production

Once `api.tactiq.in` is live, the `ALLOWED_ORIGINS` Railway variable already covers it:
```
ALLOWED_ORIGINS=https://tactiq.in,https://www.tactiq.in
```

The frontend's `VITE_API_URL=https://api.tactiq.in/api` means all API calls go to the Railway backend. No proxy needed.

---

## Part 6 — Supabase Auth Redirect URLs

Supabase Auth needs to know your production URL for OAuth and email magic links.

Supabase B dashboard → **Authentication** → **URL Configuration**:

| Setting | Value |
|---|---|
| Site URL | `https://tactiq.in` |
| Redirect URLs | `https://tactiq.in/**` |

---

## Deployment Checklist

| Step | Action | Done |
|---|---|---|
| 1 | Create `Procfile` at repo root | ⬜ |
| 2 | Push repo to GitHub | ⬜ |
| 3 | Create Railway project, link repo | ⬜ |
| 4 | Set all Railway env vars | ⬜ |
| 5 | Add `api.tactiq.in` custom domain in Railway | ⬜ |
| 6 | Create 2 Railway cron jobs (signals + orders) | ⬜ |
| 7 | Deploy frontend to Vercel, link repo | ⬜ |
| 8 | Set Vercel env vars (`VITE_API_URL`, Supabase keys) | ⬜ |
| 9 | Add `tactiq.in` + `www.tactiq.in` to Vercel domains | ⬜ |
| 10 | Add DNS records at registrar (A + CNAME for both) | ⬜ |
| 11 | Update Supabase Auth redirect URLs | ⬜ |
| 12 | Verify: `curl https://api.tactiq.in/api/health` | ⬜ |
| 13 | Verify: open `https://tactiq.in` in browser | ⬜ |
