# GCP Cloud Run Deployment Setup Guide

This guide will help you set up CI/CD deployment to Google Cloud Run using GitHub Actions.

## Prerequisites

- A Google Cloud Platform (GCP) account
- A GitHub repository for this project
- `gcloud` CLI installed locally (for initial setup)

## Step 1: GCP Project Setup

### 1.1 Create or Select a GCP Project

```bash
# Create a new project (or use existing)
gcloud projects create YOUR_PROJECT_ID --name="Blackhawk Backend"

# Set the project
gcloud config set project YOUR_PROJECT_ID
```

### 1.2 Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Artifact Registry API
gcloud services enable artifactregistry.googleapis.com

# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com
```

### 1.3 Create Artifact Registry Repository

```bash
# Create a Docker repository in Artifact Registry
gcloud artifacts repositories create blackhawk-repo \
    --repository-format=docker \
    --location=YOUR_REGION \
    --description="Docker repository for Blackhawk Backend"

# Example regions: us-central1, asia-south1, europe-west1
```

## Step 2: Create Service Account for GitHub Actions

### 2.1 Create Service Account

```bash
# Create service account
gcloud iam service-accounts create github-actions-deployer \
    --display-name="GitHub Actions Deployer"
```

### 2.2 Grant Required Permissions

```bash
# Get your project ID
PROJECT_ID=$(gcloud config get-value project)

# Grant Cloud Run Admin role
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

# Grant Artifact Registry Writer role
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

# Grant Service Account User role (required for Cloud Run)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

### 2.3 Create and Download Service Account Key

```bash
# Create key file
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions-deployer@$PROJECT_ID.iam.gserviceaccount.com

# This will create a key.json file in your current directory
# IMPORTANT: Keep this file secure and never commit it to Git!
```

## Step 3: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

### Required Secrets:

1. **GCP_PROJECT_ID**
   - Value: Your GCP project ID (e.g., `blackhawk-backend-123456`)

2. **GCP_REGION**
   - Value: Your chosen region (e.g., `us-central1`, `asia-south1`)

3. **GCP_SA_KEY**
   - Value: Contents of the `key.json` file you created
   - Copy the entire JSON content and paste it

4. **DATABASE_URL**
   - Value: Your production database URL
   - Format: `mysql+pymysql://user:password@host:port/database`
   - Example: `mysql+pymysql://root:password@/cloudsql/project:region:instance/dbname`

5. **PROJECT_NAME**
   - Value: `Blackhawk Backend` (or your preferred name)

6. **PROJECT_VERSION**
   - Value: `1.0.0` (or your version)

7. **BACKEND_CORS_ORIGINS**
   - Value: Comma-separated list of allowed origins
   - Example: `https://yourdomain.com,https://www.yourdomain.com`

## Step 4: Database Setup (Cloud SQL)

### 4.1 Create Cloud SQL Instance (Optional)

If you want to use Cloud SQL for MySQL:

```bash
# Create Cloud SQL instance
gcloud sql instances create blackhawk-db \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=YOUR_REGION

# Create database
gcloud sql databases create black_hawk \
    --instance=blackhawk-db

# Set root password
gcloud sql users set-password root \
    --host=% \
    --instance=blackhawk-db \
    --password=YOUR_SECURE_PASSWORD
```

### 4.2 Connect Cloud Run to Cloud SQL

Update the deployment command in `.github/workflows/deploy-cloud-run.yml`:

Add this flag to the `gcloud run deploy` command:
```yaml
--add-cloudsql-instances=YOUR_PROJECT_ID:YOUR_REGION:blackhawk-db \
```

Update DATABASE_URL secret to:
```
mysql+pymysql://root:password@/cloudsql/YOUR_PROJECT_ID:YOUR_REGION:blackhawk-db/black_hawk
```

## Step 5: Test Deployment

### 5.1 Push to Main Branch

```bash
git add .
git commit -m "Add Cloud Run deployment workflow"
git push origin main
```

### 5.2 Monitor Deployment

- Go to your GitHub repository → Actions tab
- Watch the deployment workflow run
- Check for any errors

### 5.3 Access Your Deployed Service

After successful deployment, get the URL:

```bash
gcloud run services describe blackhawk-backend \
    --region=YOUR_REGION \
    --format='value(status.url)'
```

Or check the GitHub Actions output for the deployment URL.

## Step 6: Run Database Migrations

After first deployment, you may need to run migrations:

```bash
# Connect to Cloud Run service
gcloud run services proxy blackhawk-backend --region=YOUR_REGION

# Or use Cloud Run Jobs to run migrations
gcloud run jobs create blackhawk-migrations \
    --image=YOUR_IMAGE \
    --region=YOUR_REGION \
    --execute-now \
    --command="alembic,upgrade,head"
```

## Troubleshooting

### Common Issues:

1. **Permission Denied Errors**
   - Ensure service account has all required roles
   - Check that `GCP_SA_KEY` secret is correctly formatted

2. **Image Push Fails**
   - Verify Artifact Registry repository exists
   - Check repository name matches workflow

3. **Database Connection Fails**
   - Verify DATABASE_URL is correct
   - Check Cloud SQL instance is running
   - Ensure Cloud Run has Cloud SQL connection configured

4. **CORS Errors**
   - Update `BACKEND_CORS_ORIGINS` secret with your frontend URL

## Security Best Practices

1. **Never commit `key.json` to Git**
   - Add it to `.gitignore`
   - Delete local copy after adding to GitHub secrets

2. **Use Secret Manager** (Advanced)
   - Consider using GCP Secret Manager instead of environment variables
   - More secure for production deployments

3. **Restrict Service Account Permissions**
   - Use principle of least privilege
   - Create separate service accounts for different environments

4. **Enable Cloud Armor** (Optional)
   - Add DDoS protection and WAF rules
   - Protect against common web attacks

## Cost Optimization

1. **Set appropriate min/max instances**
   - Current: min=0, max=10
   - Adjust based on traffic patterns

2. **Right-size resources**
   - Current: 512Mi memory, 1 CPU
   - Monitor and adjust as needed

3. **Use Cloud SQL proxy**
   - Reduces connection overhead
   - Better for serverless workloads

## Next Steps

1. Set up staging environment
2. Add health checks and monitoring
3. Configure custom domain
4. Set up Cloud Logging and Monitoring
5. Implement automated testing in CI/CD

## Support

For issues or questions:
- Check GCP Cloud Run documentation
- Review GitHub Actions logs
- Check Cloud Logging for runtime errors
