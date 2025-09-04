# 1) Clone the repo
```bash
git clone https://github.com/ceceece/office_availability.git
```

# 2) Make setup script executable
```bash
chmod +x setup.sh
```

# 3) Run setup (installs deps, creates logs/, and configures the alias)
```bash
./setup.sh
```

# 4) Load the alias into your shell
```bash
source ~/.bashrc
```

# 5) Start the app (runs in background)
```bash
office-app
```

# 6) Tail logs (Ctrl+C to stop tailing)
```bash
tail -f logs/app.log
```

# 7) Stop the app
```bash
./stop-office-app.sh
```

# 8) Allow external access (required for remote access)
```bash
# ⚠️  CRITICAL WARNING: Always allow SSH first to avoid lockout!
# If UFW is enabled without allowing SSH, you will lose access to your server
sudo ufw allow 22
sudo ufw allow 8000

# Optional: Check UFW status to verify rules
sudo ufw status
```

**Important Notes:**
- Running `sudo ufw enable` without allowing SSH (port 22) will lock you out permanently
- Test SSH access from another terminal before enabling UFW
- If locked out, you'll need physical/console access to recover
- Consider setting up UFW rules before enabling: `sudo ufw --dry-run enable`
