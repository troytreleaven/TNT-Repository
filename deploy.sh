#!/bin/bash

# Quick deploy script for dashboard
# Usage: ./deploy.sh "Your commit message"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Deploying dashboard to GitHub...${NC}"

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found. Are you in the dashboard directory?"
    exit 1
fi

# Get commit message
if [ -z "$1" ]; then
    COMMIT_MSG="Update dashboard - $(date '+%Y-%m-%d %H:%M')"
else
    COMMIT_MSG="$1"
fi

# Add all changes
echo -e "${YELLOW}📦 Adding changes...${NC}"
git add .

# Commit
if git commit -m "$COMMIT_MSG"; then
    echo -e "${GREEN}✅ Committed: $COMMIT_MSG${NC}"
else
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
    exit 0
fi

# Push to GitHub
echo -e "${YELLOW}📤 Pushing to GitHub...${NC}"
if git push origin main; then
    echo -e "${GREEN}✅ Pushed successfully!${NC}"
    echo -e "${GREEN}🌐 Netlify will auto-deploy in 30-60 seconds${NC}"
    echo ""
    echo -e "${YELLOW}📊 Check your Netlify dashboard for deployment status${NC}"
else
    echo -e "${YELLOW}⚠️  Push failed. Trying to pull latest changes first...${NC}"
    git pull origin main --rebase
    if git push origin main; then
        echo -e "${GREEN}✅ Pushed successfully after rebase!${NC}"
    else
        echo -e "${RED}❌ Push failed. Please resolve conflicts manually.${NC}"
        exit 1
    fi
fi
