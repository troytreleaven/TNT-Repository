# Dashboard Deployment Setup Guide

## Overview
This setup will enable automatic deployment to Netlify whenever you push changes to GitHub.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Name it: `troy-dashboard` (or whatever you prefer)
3. Make it **Private** (recommended)
4. Click "Create repository"
5. Copy the repository URL (e.g., `https://github.com/YOURUSERNAME/troy-dashboard`)

## Step 2: Push Dashboard to GitHub

Run these commands in your terminal (from the dashboard directory):

```bash
# Navigate to dashboard folder
cd /data/.openclaw/workspace/dashboard

# Initialize git repo
git init

# Add all files
git add .

# Commit
git commit -m "Initial dashboard commit"

# Add remote (replace with your actual repo URL)
git remote add origin https://github.com/YOURUSERNAME/troy-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Connect Netlify to GitHub

1. Go to https://app.netlify.com/
2. Click "Add new site" → "Import an existing project"
3. Choose "GitHub" as your Git provider
4. Authorize Netlify to access your GitHub account
5. Select your `troy-dashboard` repository
6. Configure build settings:
   - **Build command:** (leave empty - static site)
   - **Publish directory:** `/` (root)
7. Click "Deploy site"

## Step 4: Test Auto-Deploy

1. Make any small change to a file (e.g., edit index.html)
2. Commit and push:
   ```bash
   git add .
   git commit -m "Test auto-deploy"
   git push
   ```
3. Watch Netlify automatically deploy! (usually takes 30-60 seconds)

## Step 5: Update Your Site URL (Optional)

Netlify will give you a random URL like `abc123.netlify.app`

To use your custom domain (`precious-genie-03fbce.netlify.app`):
1. Go to Site settings → Domain management
2. Click "Add custom domain"
3. Enter your domain
4. Update DNS if needed

## Quick Deploy Script

I've created `deploy.sh` for you. Just run:
```bash
./deploy.sh "Your commit message"
```

This will:
- Add all changes
- Commit with your message
- Push to GitHub
- Netlify auto-deploys!

## Troubleshooting

**If push fails:**
```bash
git pull origin main --rebase
git push
```

**If you see merge conflicts:**
```bash
# See what's conflicting
git status

# Fix conflicts in files, then:
git add .
git rebase --continue
git push
```

## Next Steps

Once this is working, we'll add:
1. ✅ Google Sheets sync button
2. ✅ Persistent Kanban with Sheets backend

You're all set! Let me know once you've completed these steps. 🚀
