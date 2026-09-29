# 🚀 Deployment Guide: Vercel (Frontend) & Render (Backend)

This guide provides step-by-step instructions to deploy the AI-Powered Code Converter & Debugging IDE:
- **Frontend**: Hosted on [Vercel](https://vercel.com) (Vite + React SPA)
- **Backend**: Hosted on [Render](https://render.com) (Python FastAPI + Uvicorn)

---

## 🏗️ Architecture Overview

```text
┌─────────────────────────┐               ┌─────────────────────────────────────┐
│     Vercel Frontend     │  HTTPS / API  │           Render Backend            │
│  (React 19 + Vite SPA)  │ ────────────> │          (Python FastAPI)           │
│  https://*.vercel.app   │               │ https://code-converter.onrender.com │
└─────────────────────────┘               └─────────────────────────────────────┘
                                                             │
                                             ┌───────────────┴──────────────┐
                                             ▼                              ▼
                                     Google Gemini API               E2B Sandbox
                                   (Translation & Fixes)          (Code Execution)
```

---

## Part 1: Deploy Backend to Render

### Option A: Using Render Blueprint (Fastest, 1-Click)

1. Push your repository to **GitHub** or **GitLab**.
2. Go to your [Render Dashboard](https://dashboard.render.com).
3. Click **New +** > **Blueprint**.
4. Connect your repository. Render will automatically detect the [`render.yaml`](./render.yaml) file.
5. In the configuration prompt, provide your environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key.
   - `E2B_API_KEY`: Your E2B Sandbox key (from [e2b.dev](https://e2b.dev)).
6. Click **Apply**. Render will automatically provision the service, install dependencies, and start Uvicorn.

---

### Option B: Manual Web Service Setup on Render

1. Go to [Render Dashboard](https://dashboard.render.com) and click **New +** > **Web Service**.
2. Connect your Git repository.
3. Fill in the following settings:

| Setting | Value |
| :--- | :--- |
| **Name** | `code-converter-api` (or your preferred name) |
| **Region** | Choose the region closest to your users |
| **Branch** | `main` |
| **Root Directory** | *(leave empty)* |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` (or higher) |

4. Scroll down to **Advanced** and set:
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: `Yes`

5. Under **Environment Variables**, click **Add Environment Variable** for each:

| Key | Recommended Value / Description |
| :--- | :--- |
| `GEMINI_API_KEY` | Your Google Gemini API Key from [Google AI Studio](https://aistudio.google.com) |
| `GEMINI_MODEL` | `gemini-2.5-flash` |
| `E2B_API_KEY` | *(Optional but recommended)* API Key from [e2b.dev](https://e2b.dev) |
| `CORS_ORIGINS` | `*` (or your Vercel domain once deployed: `https://your-app.vercel.app`) |

6. Click **Create Web Service**.
7. Wait 2–3 minutes for the build and deployment to complete.
8. Once deployed, note down your Render Web Service URL (e.g., `https://code-converter-api.onrender.com`).
9. **Verify**: Open `https://your-backend-url.onrender.com/` in your browser. You should see:
   ```json
   {
     "status": "online",
     "service": "Code Converter & Agentic Debugging API",
     "docs": "/docs",
     "health": "/health"
   }
   ```

---

## Part 2: Deploy Frontend to Vercel

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **Add New...** > **Project**.
3. Import your Git repository.
4. In the **Configure Project** screen:
   - **Project Name**: `code-converter` (or your choice)
   - **Framework Preset**: **Vite** (Vercel automatically detects this)
   - **Root Directory**: `./` (default)
   - **Build and Output Settings**:
     - Build Command: `npm run build` (or `vite build`)
     - Output Directory: `dist`
     - Install Command: `npm install`
5. Expand the **Environment Variables** section and add:

| Key | Value |
| :--- | :--- |
| `VITE_API_URL` | Your Render backend URL (e.g. `https://code-converter-api.onrender.com`) |

> [!NOTE]
> Do NOT include a trailing slash in `VITE_API_URL`.

6. Click **Deploy**.
7. Vercel will install dependencies, compile the Vite app in under 10 seconds, and deploy to a `*.vercel.app` domain.

---

## Part 3: Verify the Connection

1. Open your live Vercel URL (e.g., `https://code-converter.vercel.app`).
2. Observe the top navigation bar:
   - The **Backend API** badge should display **Healthy** (green dot).
   - If Render is on a free instance, the first request may take ~30–50 seconds while the instance wakes from cold start.
3. Select any Preset project (e.g., *Fullstack Task Manager* or *Express Auth API*).
4. Click **Convert & Run in Sandbox** to test end-to-end translation, E2B execution, and diagnostics!

---

## 🛠️ Local Development

To run the full stack locally:

```bash
# 1. Start Python FastAPI Backend (Terminal 1)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 2. Start Vite Frontend (Terminal 2)
npm install
npm run dev
```

The Vite dev server runs at `http://localhost:3000` and automatically proxies all `/api/*` calls to `http://localhost:8000`.
