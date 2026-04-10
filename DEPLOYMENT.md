# Deployment Guide

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Easiest - Recommended)

**Streamlit Cloud** provides free hosting for Streamlit apps with automatic deployments from GitHub.

#### Prerequisites
- GitHub account with your repository
- Streamlit Cloud account (free)

#### Steps

1. **Push code to GitHub**
   ```bash
   git remote add origin <your-github-repo-url>
   git branch -M main
   git push -u origin main
   ```

2. **Create Streamlit Cloud account**
   - Visit https://share.streamlit.io/
   - Sign in with GitHub
   - Authorize Streamlit

3. **Deploy from GitHub**
   - Click "New app"
   - Select your repository: `AI-Architect/Task3_Agents_MCP`
   - Select branch: `main`
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Access your app**
   - Streamlit Cloud generates a public URL
   - Share the URL with anyone!
   - Example: `https://share.streamlit.io/username/Task3_Agents_MCP/main/app.py`

#### Free Tier Limits
- CPU: 1 vCPU
- Memory: 2 GB
- Bandwidth: 1 GB/month
- Customizable timeout: 48 hours
- Good for personal/demo use

#### Configuration
Create `.streamlit/secrets.toml` for environment variables (git-ignored):

```toml
# .streamlit/secrets.toml
[api_keys]
weather_api_enabled = true
news_api_enabled = true
```

---

### Option 2: Docker + Cloud Platform

Deploy using Docker containers to any cloud platform.

#### Prerequisites
- Docker installed locally
- Cloud account (Azure, AWS, GCP, Heroku, etc.)

#### Step 1: Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Step 2: Build Docker Image

```bash
docker build -t weather-news-agent:latest .
```

#### Step 3: Test Locally

```bash
docker run -p 8501:8501 weather-news-agent:latest
```

Visit `http://localhost:8501`

#### Step 4: Push to Container Registry

**Docker Hub:**
```bash
docker login
docker tag weather-news-agent:latest <username>/weather-news-agent:latest
docker push <username>/weather-news-agent:latest
```

**Azure Container Registry:**
```bash
az login
az acr login --name <registry-name>
docker tag weather-news-agent:latest <registry-name>.azurecr.io/weather-news-agent:latest
docker push <registry-name>.azurecr.io/weather-news-agent:latest
```

#### Step 5: Deploy to Cloud

**Azure Container Instances:**
```bash
az container create \
  --resource-group <group> \
  --name weather-news-agent \
  --image <registry>.azurecr.io/weather-news-agent:latest \
  --ports 8501 \
  --environment-variables PORT=8501
```

**Heroku:**
```bash
heroku login
heroku create weather-news-agent
heroku container:push web
heroku container:release web
heroku open
```

**Railway:**
```bash
# Connect GitHub repo
# Railway auto-detects Dockerfile and deploys
```

---

### Option 3: Traditional Web Server

#### Using Gunicorn + Nginx

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8501 streamlit.web.cli:main -- run app.py
```

#### Systemd Service (Linux)

Create `/etc/systemd/system/weather-news-agent.service`:

```ini
[Unit]
Description=Weather & News Agent
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/www-data/app
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable weather-news-agent
sudo systemctl start weather-news-agent
```

---

## 📊 Deployment Comparison

| Feature | Streamlit Cloud | Docker + Cloud | Traditional |
|---------|------------------|-----------------|------------|
| Setup Difficulty | ⭐ Easy | ⭐⭐ Medium | ⭐⭐⭐ Hard |
| Cost | Free | $5-50/mo | $5-100/mo |
| Scalability | Limited | Good | Excellent |
| Maintenance | Low | Medium | High |
| Custom Domain | Yes | Yes | Yes |
| SSL/TLS | Auto | Auto | Manual |
| Best For | Demo/Testing | Production | Enterprise |

---

## 🔐 Security Considerations

### Environment Variables
Never hardcode API keys. Use environment variables:

```python
# ✗ Bad - Don't do this!
API_KEY = "your-api-key-here"

# ✓ Good - Do this instead!
import os
API_KEY = os.getenv("API_KEY")
```

### Streamlit Cloud Secrets
```bash
# In .streamlit/secrets.toml (git-ignored)
[api_keys]
openweathermap_key = "your-key"
newsapi_key = "your-key"
```

### Docker Security
```dockerfile
# Run as non-root user
RUN useradd -m streamlit
USER streamlit
```

---

## 📈 Performance Optimization

### Caching
```python
@st.cache_data(ttl=3600)
def fetch_weather(location):
    return get_current_weather(location)
```

### Async Processing
```python
async def answer_question(question):
    # Async operations
    response = await orchestrator.process_query(question)
    return response
```

### CDN Configuration
For Streamlit Cloud, static assets are automatically CDN-cached.

---

## 🔄 CI/CD Pipeline

### GitHub Actions Auto-Deploy

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Streamlit Cloud Deploy
        uses: streamlit/streamlit-cloud-action@v1
        with:
          ref: main
          repository: ${{ github.repository }}
```

---

## 📋 Pre-Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] `.gitignore` properly configured
- [ ] `.streamlit/secrets.toml` created but git-ignored
- [ ] App tested locally: `streamlit run app.py`
- [ ] Evaluation runs successfully: `python evaluation/runner.py`
- [ ] README.md updated with public URL
- [ ] Error handling for API failures
- [ ] Logging configured
- [ ] `.streamlit/config.toml` optimized
- [ ] GitHub repo is public (for Streamlit Cloud)

---

## 🆘 Troubleshooting

### App times out
**Solution**: Optimize long-running queries with caching and async

### High memory usage
**Solution**: Limit number of cached results, use `@st.cache_resource`

### API rate limits
**Solution**: Add rate limiting, exponential backoff, or caching

### Cold start delay
**Solution**: Expected on free tiers; optimized on paid plans

### Can't access from outside
**Solution**: Check firewall rules, ensure public IP exposure

---

## 📚 References

- [Streamlit Cloud Documentation](https://docs.streamlit.io/deploy/streamlit-cloud)
- [Docker Official Images](https://hub.docker.com/_/python)
- [Railway Deploy Guide](https://docs.railway.app/)
- [Heroku with Docker](https://devcenter.heroku.com/articles/container-registry-and-runtime)

---

## 🎯 Recommended Deployment

For this project:
1. **Development**: Local with `streamlit run app.py`
2. **Staging**: Streamlit Cloud on dev branch
3. **Production**: Azure Container Instances or Railway
4. **Backup**: Heroku for failover

---

**Next Steps:**
1. Choose your deployment platform
2. Follow the steps above
3. Share your public URL
4. Monitor performance and usage
5. Optimize based on metrics

Good luck! 🚀
