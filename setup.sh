#!/bin/bash

# Office Availability App Setup Script
set -e

echo "Setting up Office Availability App..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is required but not installed. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed. Please install pip3 first."
    exit 1
fi

# Install requirements
echo "Installing Python requirements..."
pip3 install -r requirements.txt

# Create logs directory
mkdir -p logs

# Create a safer alias approach - write to a separate file
echo "Setting up office-app command..."

# Create the alias in a separate file to avoid bashrc conflicts
cat > ~/.office-app-alias << 'EOF'
# Office Availability App alias
alias office-app='cd REPLACE_PATH && nohup python3 app.py > logs/app.log 2>&1 & echo "Office app started in background. PID: $!" && echo "View logs: tail -f logs/app.log"'
EOF

# Replace the placeholder with actual path
sed -i "s|REPLACE_PATH|$(pwd)|g" ~/.office-app-alias

# Check if the source line exists in bashrc
if ! grep -q "source ~/.office-app-alias" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Office Availability App" >> ~/.bashrc  
    echo "source ~/.office-app-alias" >> ~/.bashrc
    echo "Alias added to bashrc"
else
    echo "Alias already configured"
fi

# Create stop script
cat > stop-office-app.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping Office Availability App..."
pkill -f "python3 app.py" && echo "✅ App stopped" || echo "ℹ️  App was not running"
EOF

chmod +x stop-office-app.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Usage:"
echo "  Start app:  office-app"
echo "  Stop app:   ./stop-office-app.sh"
echo "  View logs:  tail -f logs/app.log"
echo ""
echo "🌐 App will be available at: http://localhost:8000"
echo ""
echo "💡 Remember to run 'source ~/.bashrc' to activate the alias!"
