# How to Create a Desktop Launcher

Add Ollama Chat UI to your application menu and desktop for easy access!

## What You'll Need

1. The Python script (`ollama_UI_Final.py`)
2. The icon file (`ollama-icon.png`) - included in the download
3. 5 minutes of your time

## Quick Method (Recommended)

### Step 1: Organize Your Files

Create a dedicated folder for the app:

```bash
# Create folder
mkdir -p ~/Applications/ollama-chat-ui

# Move files there
mv ollama_UI_Final.py ~/Applications/ollama-chat-ui/
mv ollama-icon.png ~/Applications/ollama-chat-ui/

# Make script executable
chmod +x ~/Applications/ollama-chat-ui/ollama_UI_Final.py
```

### Step 2: Create the Desktop Entry

Create a `.desktop` file:

```bash
nano ~/.local/share/applications/ollama-chat-ui.desktop
```

Paste this content (adjust username if needed):

```desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Ollama Chat UI
Comment=Chat with local AI models
Exec=python3 /home/YOUR_USERNAME/Applications/ollama-chat-ui/ollama_UI_Final.py
Icon=/home/YOUR_USERNAME/Applications/ollama-chat-ui/ollama-icon.png
Terminal=false
Categories=Utility;Development;
Keywords=ai;ollama;chat;llm;
StartupNotify=true
```

**IMPORTANT:** Replace `YOUR_USERNAME` with your actual username!

To find your username:
```bash
whoami
```

### Step 3: Make It Executable

```bash
chmod +x ~/.local/share/applications/ollama-chat-ui.desktop
```

### Step 4: Update Desktop Database

```bash
update-desktop-database ~/.local/share/applications/
```

### Step 5: Done!

Open your application menu and search for "Ollama Chat UI" - it should appear with the icon!

## Alternative: System-Wide Installation (All Users)

If you want all users to access it:

```bash
# Copy to system applications folder (requires sudo)
sudo cp ~/.local/share/applications/ollama-chat-ui.desktop /usr/share/applications/

# Update system database
sudo update-desktop-database /usr/share/applications/
```

## Adding to Favorites/Dock

### GNOME (Pop!_OS, Ubuntu)
1. Open application menu
2. Find "Ollama Chat UI"
3. Right-click → "Add to Favorites"
4. It appears in the dock!

### KDE Plasma
1. Find app in menu
2. Right-click → "Add to Panel"

### XFCE
1. Find app in menu
2. Right-click → "Add to Panel"

## Creating a Desktop Shortcut

Want it on your desktop?

```bash
cp ~/.local/share/applications/ollama-chat-ui.desktop ~/Desktop/
chmod +x ~/Desktop/ollama-chat-ui.desktop
```

Right-click → "Allow Launching"

## Customizing the Icon

### Using a Different Icon

1. Find an icon you like (PNG format, at least 256x256px)
2. Replace the Icon line in the .desktop file:
   ```
   Icon=/path/to/your/custom-icon.png
   ```

### Icon Search Locations

Linux looks for icons in these places:
- `~/.local/share/icons/`
- `/usr/share/icons/`
- `/usr/share/pixmaps/`

You can also use icon theme names:
```
Icon=applications-science
Icon=utilities-terminal
```

## Troubleshooting

### Launcher not appearing

1. **Check desktop file syntax:**
   ```bash
   desktop-file-validate ~/.local/share/applications/ollama-chat-ui.desktop
   ```

2. **Update database again:**
   ```bash
   update-desktop-database ~/.local/share/applications/
   ```

3. **Restart desktop environment:**
   Log out and log back in

### Icon not showing

- Use absolute paths (full path starting with `/`)
- Check icon file exists: `ls ~/Applications/ollama-chat-ui/ollama-icon.png`
- Try a different icon format (PNG, SVG)

### App doesn't launch

1. **Test manually first:**
   ```bash
   python3 ~/Applications/ollama-chat-ui/ollama_UI_Final.py
   ```

2. **Check Exec path is correct** in .desktop file

3. **Enable terminal to see errors:**
   Change `Terminal=false` to `Terminal=true` temporarily

### Permission denied

Make sure the script is executable:
```bash
chmod +x ~/Applications/ollama-chat-ui/ollama_UI_Final.py
```

## Advanced: Custom Launch Script

Create a wrapper script for additional functionality:

```bash
nano ~/Applications/ollama-chat-ui/launch.sh
```

Content:
```bash
#!/bin/bash
# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    notify-send "Starting Ollama..." "Please wait..."
    ollama serve &
    sleep 2
fi

# Launch the UI
cd ~/Applications/ollama-chat-ui
python3 ollama_UI_Final.py
```

Make it executable:
```bash
chmod +x ~/Applications/ollama-chat-ui/launch.sh
```

Update .desktop file Exec line:
```
Exec=/home/YOUR_USERNAME/Applications/ollama-chat-ui/launch.sh
```

## Multiple Instances

To allow multiple windows:

Add to .desktop file:
```
X-MultipleArgs=false
```

## Uninstalling the Launcher

```bash
# Remove from menu
rm ~/.local/share/applications/ollama-chat-ui.desktop

# Remove from desktop
rm ~/Desktop/ollama-chat-ui.desktop

# Update database
update-desktop-database ~/.local/share/applications/
```

## Desktop Entry Reference

Common options:

```desktop
[Desktop Entry]
Version=1.0                    # Desktop entry version
Type=Application               # Type of entry
Name=App Name                  # Display name
GenericName=Short Description  # Generic name
Comment=Longer description     # Tooltip text
Exec=/path/to/command         # Command to run
Icon=/path/to/icon.png        # Icon path or name
Terminal=false                 # Run in terminal?
Categories=Category1;Cat2;    # Menu categories
Keywords=word1;word2;         # Search keywords
StartupNotify=true            # Show loading cursor
NoDisplay=false               # Hide from menus?
```

Common categories:
- `Utility` - Utility apps
- `Development` - Programming tools
- `Office` - Office applications
- `Network` - Network apps
- `AudioVideo` - Multimedia
- `Graphics` - Graphics apps

## Example Desktop Files

### Minimal
```desktop
[Desktop Entry]
Type=Application
Name=Ollama Chat
Exec=python3 /home/user/ollama_UI_Final.py
Icon=applications-chat
Terminal=false
```

### Full Featured
```desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Ollama Chat UI
GenericName=AI Chat Interface
Comment=Chat with local Ollama AI models
Exec=python3 /home/user/Applications/ollama-chat-ui/ollama_UI_Final.py
Icon=/home/user/Applications/ollama-chat-ui/ollama-icon.png
Path=/home/user/Applications/ollama-chat-ui
Terminal=false
Categories=Utility;Development;Science;
Keywords=ai;ollama;chat;llm;assistant;
MimeType=application/json;
StartupNotify=true
StartupWMClass=ollama-chat-ui
```

---

**Launch your AI assistant with one click!** 🚀
