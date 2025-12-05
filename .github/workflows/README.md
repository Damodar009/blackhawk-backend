# GitHub Actions Workflows

## deploy-cloud-run.yml

Automatically deploys the Blackhawk Backend to Google Cloud Run when code is pushed to the `main` branch.

### Workflow Triggers

- **Push to main branch**: Automatic deployment
- **Manual trigger**: Can be triggered manually from GitHub Actions tab

### What it does

1. Checks out the code
2. Authenticates with Google Cloud
3. Builds Docker image using `docker/Dockerfile`
4. Pushes image to Google Artifact Registry
5. Deploys to Cloud Run
6. Displays deployment URL

### Required Setup

See [DEPLOYMENT_SETUP.md](../../DEPLOYMENT_SETUP.md) for complete setup instructions.

### Quick Reference - Required Secrets

| Secret Name | Description | Example |
|------------|-------------|---------|
| `GCP_PROJECT_ID` | Your GCP project ID | `blackhawk-backend-123456` |
| `GCP_REGION` | Deployment region | `us-central1` |
| `GCP_SA_KEY` | Service account JSON key | `{...}` |
| `DATABASE_URL` | Database connection string | `mysql+pymysql://...` |
| `PROJECT_NAME` | Application name | `Blackhawk Backend` |
| `PROJECT_VERSION` | Version number | `1.0.0` |
| `BACKEND_CORS_ORIGINS` | Allowed CORS origins | `https://example.com` |

### Customization

You can modify the following in the workflow file:

- **Service name**: Change `SERVICE_NAME` env variable
- **Resources**: Adjust `--memory`, `--cpu`, `--min-instances`, `--max-instances`
- **Timeout**: Modify `--timeout` value
- **Port**: Change `--port` if your app uses different port
- **Authentication**: Remove `--allow-unauthenticated` to require auth

### Monitoring Deployments

1. Go to GitHub repository → Actions tab
2. Click on the latest workflow run
3. View logs for each step
4. Check deployment URL in the final step

### Rollback

To rollback to a previous version:

```bash
# List revisions
gcloud run revisions list --service=blackhawk-backend --region=YOUR_REGION

# Rollback to specific revision
gcloud run services update-traffic blackhawk-backend \
    --to-revisions=REVISION_NAME=100 \
    --region=YOUR_REGION
```
