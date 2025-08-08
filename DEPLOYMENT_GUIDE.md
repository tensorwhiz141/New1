# Deployment Guide for Policy Query System

## 🎯 HackRx Webhook Submission

**Your webhook endpoint**: `/api/v1/hackrx/run` (POST)
**Health check endpoint**: `/api/v1/hackrx/health` (GET)

## 🚀 Quick Start - Local Testing

Your web application is ready! To test locally:

```bash
python main.py
```

Then visit: http://127.0.0.1:5000

## 🌐 Deploy to Web

### Option 1: Heroku (Recommended)

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Create Heroku account**: https://heroku.com
3. **Deploy:**

```bash
# Login to Heroku
heroku login

# Create app (replace 'your-app-name' with your desired name)
heroku create your-policy-query-app

# Set environment variable
heroku config:set DEEPINFRA_API_KEY=Zl4nc00K9QO28bOFXUtQOrk5GFgKYa1M

# Initialize git and deploy
git init
git add .
git commit -m "Deploy policy query system"
git push heroku main

# Open your app
heroku open
```

### Option 2: Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select this repository
5. Add environment variable:
   - Key: `DEEPINFRA_API_KEY`
   - Value: `Zl4nc00K9QO28bOFXUtQOrk5GFgKYa1M`
6. Deploy!

### Option 3: Render

1. Go to https://render.com
2. Sign up and connect GitHub
3. Click "New Web Service"
4. Connect this repository
5. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`
6. Add environment variable:
   - Key: `DEEPINFRA_API_KEY`
   - Value: `Zl4nc00K9QO28bOFXUtQOrk5GFgKYa1M`

## 🔒 Security Notes

- Your API key is currently hardcoded for testing
- For production, always use environment variables
- Consider rotating your API key after deployment

## 📁 Files Created for Deployment

- `Procfile` - Tells Heroku how to run your app
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Updated with Flask dependencies
- `templates/index.html` - Web interface
- `.gitignore` - Excludes sensitive files
- `.env.example` - Template for environment variables

## 🛠️ Troubleshooting

If deployment fails:
1. Check that all files are committed to git
2. Verify environment variables are set
3. Check deployment logs on your platform
4. Ensure Python version matches runtime.txt

## 🧪 Test Your Webhook

After deployment, test your webhook:

```bash
python test_webhook.py https://your-app-name.railway.app
```

## 🎯 Submit to HackRx

Your webhook URL for submission:
```
https://your-app-name.railway.app/api/v1/hackrx/run
```

## 🎉 Success!

Once deployed, your policy query system will be available at your app's URL. Users can ask questions about your policy documents through a beautiful web interface, and the HackRx platform can test your solution via the webhook endpoint!
