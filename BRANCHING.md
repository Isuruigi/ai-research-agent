# Git Branching Strategy

## Branch Structure

### `main` - Production Branch
- **Purpose**: Stable, production-ready code
- **Deploys to**: Railway (automatic)
- **Protection**: Only merge from `development` via pull requests
- **Status**: Currently deployed

### `development` - Active Development Branch
- **Purpose**: Ongoing development and testing
- **Use for**: New features, experiments, improvements
- **Testing**: Test locally before merging to main
- **Current**: ✅ Created and pushed

---

## Workflow

### Making Changes

**1. Switch to development branch:**
```bash
git checkout development
```

**2. Make your changes:**
```bash
# Edit files, add features, fix bugs
```

**3. Commit changes:**
```bash
git add .
git commit -m "Add new feature: XYZ"
```

**4. Push to GitHub:**
```bash
git push origin development
```

**5. Test locally:**
```bash
python test_demo.py
```

**6. When ready for production, create Pull Request:**
- Go to GitHub: https://github.com/Isuruigi/ai-research-agent
- Click "Pull requests" → "New pull request"
- Base: `main` ← Compare: `development`
- Create pull request → Merge

**7. Railway auto-deploys from main** ✅

---

## Quick Commands

**Check current branch:**
```bash
git branch
```

**Switch branches:**
```bash
git checkout main          # Switch to production
git checkout development   # Switch to development
```

**Create new feature branch:**
```bash
git checkout -b feature/new-feature
```

**Delete branch:**
```bash
git branch -d branch-name
```

**See all branches:**
```bash
git branch -a
```

---

## Best Practices

✅ **DO:**
- Work on `development` for new features
- Test thoroughly before merging to `main`
- Use descriptive commit messages
- Create pull requests for code review

❌ **DON'T:**
- Push directly to `main` (except critical hotfixes)
- Commit `.env` files or secrets
- Merge without testing

---

## Current Status

- ✅ **main**: Deployed to Railway (production)
- ✅ **development**: Active development branch
- 🔄 **Workflow**: dev → test → PR → main → auto-deploy

**You're currently on:** `development` branch

Happy coding! 🚀
