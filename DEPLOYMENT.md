# Deployment configuration for DigitalOcean

## Prerequisites
- DigitalOcean account
- GitHub repository with your code
- GitHub connected to your DigitalOcean account

## Step-by-step Deployment:

1. **Push your code to GitHub**
   - Create a repository on GitHub
   - Push your FastAPI project there

2. **Create a DigitalOcean App Platform deployment:**
   - Go to https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Connect your GitHub repository
   - DigitalOcean will auto-detect the requirements.txt
   - Review the configuration in `app.yaml`
   - Add any environment variables needed
   - Deploy!

## Alternative: Manual Deployment via CLI

```bash
# Install doctl CLI
# https://docs.digitalocean.com/reference/doctl/

doctl auth init  # Login to DigitalOcean

doctl apps create --spec app.yaml
```

## Environment Variables to Set

In DigitalOcean dashboard or `app.yaml`:
- `PORT`: Automatically set by DigitalOcean (default 8000)
- `ENVIRONMENT`: Set to "production"
- Add database credentials if needed

## Database Considerations

If your app uses a database:
1. Create a managed database in DigitalOcean
2. Add connection string as environment variable
3. Run migrations on deployment

## Monitoring

- Access logs in DigitalOcean dashboard
- Monitor resource usage
- Set up alerts for high CPU/memory

