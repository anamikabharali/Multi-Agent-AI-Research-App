# Deploying MarketMind to Streamlit Cloud

## Quick Deployment Steps:

### 1. Prepare Your Repository
```bash
# Make sure your code is in a GitHub repository
git add .
git commit -m "MarketMind ready for deployment"
git push origin main
```

### 2. Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set the main file path to: `app.py`
6. Click "Deploy"

### 3. Configure Environment Variables
In Streamlit Cloud dashboard:
1. Go to your app settings
2. Add these secrets:
```toml
OPENAI_API_KEY = "your_openai_key"
SERPER_API_KEY = "your_serper_key" 
FIRECRAWL_API_KEY = "your_firecrawl_key"
```

### 4. Share with Stakeholders
- Send them the public URL (e.g., `https://your-app-name.streamlit.app`)
- They can access it from any browser
- No installation required!

## Benefits:
- ✅ **Free hosting**
- ✅ **No setup required for users**
- ✅ **Automatic updates** when you push to GitHub
- ✅ **Professional interface**
- ✅ **Works on mobile and desktop**

## Alternative: Deploy to Heroku

If you prefer Heroku:

### 1. Create Heroku App
```bash
# Install Heroku CLI
heroku create your-marketmind-app
```

### 2. Add Buildpacks
```bash
heroku buildpacks:add heroku/python
```

### 3. Create Procfile
```bash
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
```

### 4. Set Environment Variables
```bash
heroku config:set OPENAI_API_KEY="your_key"
heroku config:set SERPER_API_KEY="your_key"
heroku config:set FIRECRAWL_API_KEY="your_key"
```

### 5. Deploy
```bash
git push heroku main
```

## Option 3: Docker Container (For IT Teams)

Create a Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t marketmind .
docker run -p 8501:8501 marketmind
```

## Option 4: Local Network Deployment

For internal company use:

```bash
# Run on your machine
streamlit run app.py --server.port=8501 --server.address=0.0.0.0

# Share your IP address with stakeholders
# They access: http://YOUR_IP:8501
```

## Recommended Approach:

**For business stakeholders: Use Streamlit Cloud**
- Easiest to set up
- Professional appearance
- No technical knowledge required
- Free hosting
- Automatic updates

**For IT teams: Use Docker**
- More control
- Can be deployed internally
- Better for enterprise environments 