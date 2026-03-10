#!/bin/bash
# OpenClaw Daily Backup Script
# Backs up workspace to GitHub

set -e

WORKSPACE_DIR="/data/.openclaw/workspace"
BACKUP_LOG="/data/.openclaw/logs/backup.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Create log directory if needed
mkdir -p "$(dirname "$BACKUP_LOG")"

log() {
    echo "[$DATE] $1" | tee -a "$BACKUP_LOG"
}

cd "$WORKSPACE_DIR"

log "Starting backup..."

# Check if there are changes to commit
if git diff --quiet && git diff --cached --quiet; then
    log "No changes to backup."
    exit 0
fi

# Add all changes
git add -A

# Commit with timestamp
COMMIT_MSG="Daily backup: $DATE"
git commit -m "$COMMIT_MSG" 2>&1 | tee -a "$BACKUP_LOG"

# Push to GitHub (if remote is configured)
if git remote | grep -q origin; then
    git push origin master 2>&1 | tee -a "$BACKUP_LOG"
    log "Backup pushed to GitHub successfully!"
else
    log "No remote configured. Run setup first."
    exit 1
fi

log "Backup complete!"
