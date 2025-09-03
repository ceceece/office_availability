# 1) Clone the repo
git clone https://github.com/ceceece/office_availability.git

# 2) Make setup script executable
chmod +x setup.sh

# 3) Run setup (installs deps, creates logs/, and configures the alias)
./setup.sh

# 4) Load the alias into your shell
source ~/.bashrc

# 5) Start the app (runs in background)
office-app

# 6) Tail logs (Ctrl+C to stop tailing)
tail -f logs/app.log

# 7) Stop the app
./stop-office-app.sh
