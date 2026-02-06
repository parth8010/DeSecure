# Git Guide - Simple Steps

## First Time Setup (One-time only)

### Step 1: Install Git
Download and install: https://git-scm.com/download/win

### Step 2: Configure Git
Open PowerShell and run:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Push Your Code to GitHub

### Step 1: Create GitHub Repository
1. Go to https://github.com
2. Click the **"+"** icon → **"New repository"**
3. Name it: `cybersecurity-platform`
4. Keep it **Private** (for now)
5. **DON'T** check "Initialize with README"
6. Click **"Create repository"**

### Step 2: Initialize Git in Your Project
Open PowerShell in your backend folder:
```bash
cd D:\Hackethon\MainFile\backend

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - API Key Management backend"

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/cybersecurity-platform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Enter GitHub Credentials
- When prompted, enter your GitHub username
- For password, use a **Personal Access Token** (not your password):
  1. Go to https://github.com/settings/tokens
  2. Click **"Generate new token (classic)"**
  3. Select scopes: `repo` (full control)
  4. Copy the token and paste as password

## Making Changes & Updating

### After You Change Files:
```bash
# See what changed
git status

# Add changed files
git add .

# Commit with message
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

## Connect Railway to GitHub (Auto-Deploy)

### Step 1: In Railway Dashboard
1. Click your project (or create new)
2. Click **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub
4. Select your `cybersecurity-platform` repository

### Step 2: Configure
- Railway auto-detects Python
- No extra config needed!
- Click **"Deploy"**

### Step 3: Auto-Deploy is Now Active! 🎉
- Every time you `git push`, Railway auto-deploys
- No manual uploads needed!

## Quick Reference

```bash
# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "Your message here"

# Push to GitHub (and auto-deploy to Railway!)
git push

# See commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

## Working with Your Buddy

### Step 1: Add Them as Collaborator
1. Go to your GitHub repo
2. Settings → Collaborators
3. Add their GitHub username

### Step 2: They Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/cybersecurity-platform.git
cd cybersecurity-platform
```

### Step 3: Collaborate
Before working:
```bash
git pull  # Get latest changes
```

After making changes:
```bash
git add .
git commit -m "What you did"
git push
```

## Tips

✅ **Commit often** - Small commits are better than big ones
✅ **Good commit messages** - "Added user authentication" not "updates"
✅ **Pull before push** - Always `git pull` before starting work
✅ **Use .gitignore** - Already created, keeps secrets safe

## Troubleshooting

**Problem: "Permission denied"**
```bash
# Use personal access token instead of password
```

**Problem: "Merge conflict"**
```bash
git pull
# Fix conflicts in files
git add .
git commit -m "Resolved conflicts"
git push
```

**Problem: "Repository not found"**
```bash
# Check remote URL
git remote -v

# Fix if wrong
git remote set-url origin https://github.com/YOUR_USERNAME/repo-name.git
```

---

**After setup, your workflow is simple:**
1. Make changes to code
2. `git add .`
3. `git commit -m "What you did"`
4. `git push`
5. Railway auto-deploys! 🚀
