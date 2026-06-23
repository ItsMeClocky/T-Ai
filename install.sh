#!/bin/bash
# T-Ai Installer for Linux
echo "Installing T-Ai..."
echo "This will create a desktop shortcut for T-Ai"

# Create desktop entry
DESKTOP_FILE="$HOME/.local/share/applications/t-ai.desktop"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=T-Ai
Comment=T-Ai AI Assistant
Exec=xdg-open http://localhost:8080
Icon=t-ai
Terminal=false
Categories=Utility;
EOF

chmod +x "$DESKTOP_FILE"
echo "T-Ai installed! You can find it in your applications menu."
echo "Note: Make sure the backend server is running: python3 api_keys.py"
