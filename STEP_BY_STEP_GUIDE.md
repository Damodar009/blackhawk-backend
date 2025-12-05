# Complete Setup Guide: GitHub to GCP Cloud Run (Web Console Only)

Follow these steps using only your web browser - no CLI installation needed!

---

## Part 1: GCP Console Setup (30-45 minutes)

### Step 1: Create Google Cloud Account

1. Go to: https://console.cloud.google.com/
2. Sign in with your Google account
3. Accept terms of service
4. **New users get $300 free credits for 90 days!**

---

### Step 2: Create a New Project

1. Click the project dropdown (top left, next to "Google Cloud")
2. Click **"New Project"**
3. **Project name:** `Blackhawk Backend Production`
4. **Project ID:** `blackhawk-backend-prod` (or auto-generated)
5. Click **"Create"**
6. Wait for project creation (~30 seconds)
7. **Select your new project** from the dropdown

**Save your Project ID - you'll need it later!**

---

### Step 3: Enable Billing

1. Go to: https://console.cloud.google.com/billing
2. Click **"Link a billing account"**
3. Follow prompts to add payment method
4. **Don't worry:** You have $300 free credits and won't be charged initially

---

### Step 4: Enable Required APIs

1. Go to: https://console.cloud.google.com/apis/library
2. Search and enable each of these (click "Enable" button):
   - Search: `cloud run` → Enable **"Cloud Run Admin API"**
   - Search: `artifact registry` → Enable **"Artifact Registry API"**
   - Search: `cloud build` → Enable **"Cloud Build API"**
   - Search: `cloud sql admin` → Enable **"Cloud SQL Admin API"**

**Tip:** After enabling each, click the back button to search for the next one.

---

### Step 5: Create Artifact Registry Repository

1. Go to: https://console.cloud.google.com/artifacts
2. Click **"Create Repository"**
3. Fill in:
   - **Name:** `blackhawk-repo`
   - **Format:** Docker
   - **Mode:** Standard
   - **Location type:** Region
   - **Region:** Choose closest to you (e.g., `us-central1`, `asia-south1`)
4. Click **"Create"**

**Save your chosen region - you'll need it later!**

---

### Step 6: Create Cloud SQL Instance

1. Go to: https://console.cloud.google.com/sql/instances
2. Click **"Create Instance"**
3. Choose **"MySQL"**
4. Fill in:
   - **Instance ID:** `blackhawk-db`
   - **Password:** Create a strong password (save it securely!)
   - **Database version:** MySQL 8.0
   - **Region:** Same as Step 5
   - **Zonal availability:** Single zone
   - **Machine type:** Shared core → **1 vCPU, 0.614 GB** (cheapest)
5. Click **"Create Instance"**

**This takes 5-10 minutes. Wait for it to complete.**

---

### Step 7: Create Database

1. Still in Cloud SQL, click on **"blackhawk-db"** instance
2. Go to **"Databases"** tab
3. Click **"Create Database"**
4. **Database name:** `black_hawk`
5. Click **"Create"**

---

### Step 8: Get Cloud SQL Connection Name

1. In Cloud SQL instance page (blackhawk-db)
2. Look for **"Connection name"** in the overview
3. **Copy this value** (format: `project:region:instance`)
4. Example: `blackhawk-backend-prod:us-central1:blackhawk-db`

**Save this - you'll need it for GitHub secrets!**

---

### Step 9: Create Service Account

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click **"Create Service Account"**
3. Fill in:
   - **Service account name:** `github-actions-deployer`
   - **Service account ID:** (auto-filled)
   - **Description:** `Service account for GitHub Actions deployments`
4. Click **"Create and Continue"**
5. **Grant roles** - Add these 4 roles one by one:
   - `Cloud Run Admin`
   - `Artifact Registry Writer`
   - `Service Account User`
   - `Cloud SQL Client`
6. Click **"Continue"** → **"Done"**

---

### Step 10: Create Service Account Key

1. In Service Accounts page, find `github-actions-deployer`
2. Click the **3 dots** (⋮) → **"Manage keys"**
3. Click **"Add Key"** → **"Create new key"**
4. Choose **"JSON"**
5. Click **"Create"**
6. A JSON file will download automatically

**IMPORTANT:** 
- Open this file in a text editor
- You'll copy its entire contents to GitHub
- Keep it secure - don't share it!

---

## Part 2: GitHub Setup (10-15 minutes)

### Step 11: Push Code to GitHub

1. Go to: https://github.com/new
2. Create a new repository:
   - **Repository name:** `blackhawk-backend`
   - **Visibility:** Private (recommended) or Public
3. Click **"Create repository"**

4. In your terminal (on your Mac):
```bash
cd /Users/damodarthegreat/Documents/Project/Black-hawk/blackhawk-backend

git init
git add .
git commit -m "Initial commit with Cloud Run deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/blackhawk-backend.git
git push -u origin main
```

---

### Step 12: Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** for each:

#### Secret 1: GCP_PROJECT_ID
- **Name:** `GCP_PROJECT_ID`
- **Value:** Your project ID from Step 2 (e.g., `blackhawk-backend-prod`)

#### Secret 2: GCP_REGION
- **Name:** `GCP_REGION`
- **Value:** Your region from Step 5 (e.g., `us-central1`)

#### Secret 3: GCP_SA_KEY
- **Name:** `GCP_SA_KEY`
- **Value:** 
  1. Open the JSON file from Step 10
  2. Copy **ENTIRE contents** (all the JSON)
  3. Paste here

#### Secret 4: CLOUD_SQL_CONNECTION_NAME
- **Name:** `CLOUD_SQL_CONNECTION_NAME`
- **Value:** Connection name from Step 8 (e.g., `blackhawk-backend-prod:us-central1:blackhawk-db`)

#### Secret 5: DATABASE_URL
- **Name:** `DATABASE_URL`
- **Value:** Build this carefully:
```
mysql+pymysql://root:YOUR_PASSWORD@/cloudsql/YOUR_CONNECTION_NAME/black_hawk
```

**Example:**
```
mysql+pymysql://root:MyPass123@/cloudsql/blackhawk-backend-prod:us-central1:blackhawk-db/black_hawk
```
Replace:
- `YOUR_PASSWORD` with password from Step 6
- `YOUR_CONNECTION_NAME` with value from Step 8

#### Secret 6: PROJECT_NAME
- **Name:** `PROJECT_NAME`
- **Value:** `Blackhawk Backend`

#### Secret 7: PROJECT_VERSION
- **Name:** `PROJECT_VERSION`
- **Value:** `1.0.0`

#### Secret 8: BACKEND_CORS_ORIGINS
- **Name:** `BACKEND_CORS_ORIGINS`
- **Value:** 
  - For testing: `*`
  - For production: `https://yourdomain.com,https://www.yourdomain.com`

---

## Part 3: Deploy! (5-10 minutes)

### Step 13: Trigger First Deployment

**Option A: Push a change**
```bash
# In your terminal
cd /Users/damodarthegreat/Documents/Project/Black-hawk/blackhawk-backend
echo "# Blackhawk Backend API" > README.md
git add README.md
git commit -m "Trigger deployment"
git push origin main
```

**Option B: Manual trigger**
1. Go to GitHub → **Actions** tab
2. Click **"Deploy to Cloud Run"** workflow
3. Click **"Run workflow"** button → **"Run workflow"**

---

### Step 14: Monitor Deployment

1. In GitHub → **Actions** tab
2. Click on the running workflow
3. Watch each step execute:
   - ✅ Checkout code
   - ✅ Authenticate to Google Cloud
   - ✅ Build Docker image
   - ✅ Push to Artifact Registry
   - ✅ Deploy to Cloud Run
4. Wait for completion (~5-10 minutes)

---

### Step 15: Get Your Deployment URL

**Option A: From GitHub Actions**
- Scroll to the last step "Show deployment URL"
- Copy the URL shown

**Option B: From GCP Console**
1. Go to: https://console.cloud.google.com/run
2. Click on **"blackhawk-backend"** service
3. Copy the URL at the top

---

### Step 16: Test Your API

Open your browser and visit:
```
https://YOUR_CLOUD_RUN_URL/health-check
```

**Expected response:**
```json
{"message":"API up and running"}
```

---

### Step 17: Run Database Migrations

**Option A: Using Cloud Shell (Easiest)**

1. Go to: https://console.cloud.google.com/
2. Click **Cloud Shell icon** (>_) at top right
3. Wait for shell to start
4. Run these commands:

```bash
# Connect to Cloud SQL
gcloud sql connect blackhawk-db --user=root

# Enter your password when prompted

# Switch to database
USE black_hawk;

# Exit
exit;
```

5. Now run migrations using Cloud Run Jobs:

```bash
# Get your connection name
export CONNECTION_NAME=$(gcloud sql instances describe blackhawk-db --format="value(connectionName)")

# Get your region
export REGION=us-central1  # Change to your region

# Get your project ID
export PROJECT_ID=$(gcloud config get-value project)

# Create migration job
gcloud run jobs create blackhawk-migrations \
    --image=$REGION-docker.pkg.dev/$PROJECT_ID/blackhawk-repo/blackhawk-backend:latest \
    --region=$REGION \
    --set-cloudsql-instances=$CONNECTION_NAME \
    --set-env-vars="DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@/cloudsql/$CONNECTION_NAME/black_hawk" \
    --command="alembic" \
    --args="upgrade,head"

# Run the migration
gcloud run jobs execute blackhawk-migrations --region=$REGION
```

Replace `YOUR_PASSWORD` with your database password.

**Option B: Manual SQL (If Option A fails)**

1. Go to: https://console.cloud.google.com/sql/instances
2. Click **"blackhawk-db"**
3. Click **"Cloud SQL Studio"** tab
4. Click **"Authorize"** and **"Connect"**
5. Run your migration SQL manually

---

## Part 4: Verification

### Checklist:
- [ ] GitHub Actions workflow shows green checkmark
- [ ] Cloud Run service is visible in console
- [ ] Health check endpoint returns success
- [ ] Database migrations completed
- [ ] Can access API endpoints

---

## Troubleshooting

### Deployment Failed?

1. **Check GitHub Actions logs**
   - Look for red X marks
   - Read error messages

2. **Verify all 8 secrets are correct**
   - Go to Settings → Secrets → Actions
   - Check for typos

3. **Check GCP Console**
   - Cloud Run: https://console.cloud.google.com/run
   - Logs: https://console.cloud.google.com/logs

### Common Issues:

**"Permission denied"**
- Verify service account has all 4 roles (Step 9)

**"Image not found"**
- Check Artifact Registry repository exists
- Verify region matches

**"Database connection failed"**
- Double-check DATABASE_URL format
- Verify password is correct
- Check CLOUD_SQL_CONNECTION_NAME

---

## Viewing Logs

1. Go to: https://console.cloud.google.com/run
2. Click **"blackhawk-backend"**
3. Click **"Logs"** tab
4. See real-time application logs

---

## Cost Estimate

- **Cloud Run:** $0-5/month (2M free requests)
- **Cloud SQL:** $10-15/month (smallest instance)
- **Artifact Registry:** $0-1/month (0.5GB free)

**Total:** ~$10-20/month for low traffic

---

## Next Steps

✅ Set up custom domain
✅ Configure monitoring alerts
✅ Add staging environment
✅ Set up automated backups

---

## Need Help?

- **GitHub Actions logs:** Check for specific errors
- **GCP Logs:** https://console.cloud.google.com/logs
- **Cloud Run docs:** https://cloud.google.com/run/docs

Good luck! 🚀
