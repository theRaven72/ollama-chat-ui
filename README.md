# Ollama Chat UI - Setup Instructions

A Python-based UI for interacting with Ollama models with automatic service management.

## Features
- 🚀 **Auto-start Ollama** when launching the UI
- 🛑 **Auto-stop Ollama** when exiting (frees GPU resources)
- 💬 Multiple model support with custom display names
- 🌐 Web search integration (DuckDuckGo)
- 📊 Token counting and conversation management
- 🎨 Multiple themes (Dark, Light, Matrix, Nord, Dracula)

## ⚠️ IMPORTANT: Required Setup (One-Time)

Before running this UI, you **MUST** configure sudo permissions to allow automatic Ollama start/stop without password prompts.

### Setup Steps:

**1. Open the sudoers file safely:**
```bash
sudo visudo
```

**2. Add this line at the very bottom of the file:**
```
YOUR_USERNAME ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop ollama, /usr/bin/systemctl start ollama
```

**Replace `YOUR_USERNAME` with your actual username.** For example:
```
john ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop ollama, /usr/bin/systemctl start ollama
```

**3. Save and exit:**
- In nano: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`
- In vim: Press `Esc`, type `:wq`, press `Enter`

**4. Test it works (should NOT ask for password):**
```bash
sudo systemctl stop ollama
sudo systemctl start ollama
```

If it asks for a password, the sudoers entry wasn't added correctly. Try again.

### Why is this needed?

The UI automatically manages the Ollama service to:
- **Start Ollama** when you launch the UI (so it's ready immediately)
- **Stop Ollama** when you exit (to free GPU VRAM and prevent memory leaks)

Without this sudo configuration, you'll get password prompts or the service management will fail silently.

### Security Note

This configuration allows your user account to **ONLY** start and stop the Ollama service, nothing else. An attacker with access to your account:
- ✅ Can stop/start Ollama (minor inconvenience)
- ❌ **CANNOT** delete files, modify system settings, or escalate privileges

For a personal desktop/workstation, this is a safe and reasonable trade-off for convenience.

## Installation

**1. Install dependencies:**
```bash
# Install Python packages
pip install requests duckduckgo-search

# Optional: Install spell checker (for typo detection)
sudo apt install aspell
```

**2. Ensure Ollama is installed and configured:**
```bash
# Check Ollama is installed
ollama --version

# Check Ollama service exists
systemctl status ollama
```

**3. Complete the sudoers setup above**

**4. Run the UI:**
```bash
python3 ollama_UI_Final_with_auto_start_stop.py
```

## Usage

1. **Launch the UI** - Ollama starts automatically
2. **Select a model** from the dropdown
3. **Click "Connect"**
4. **Start chatting!**
5. **Toggle web search** if you need current information
6. **Click "Exit"** when done - Ollama stops automatically

## Troubleshooting

### "Connection refused" error on launch
- **Cause:** Ollama service didn't start
- **Check:** Did you complete the sudoers setup?
- **Test:** Run `sudo systemctl start ollama` manually - does it ask for a password?
- **Fix:** Re-do the sudoers configuration above

### Ollama doesn't stop when I exit the UI
- **Check:** Your sudoers entry is correct
- **Test:** Run `sudo systemctl stop ollama` - does it work without a password?
- **Temporary fix:** Manually run `sudo systemctl stop ollama` after closing the UI

### UI launches but can't find models
- **Check:** Ollama has models installed
- **Fix:** Pull some models:
  ```bash
  ollama pull llama3.1:8b
  ollama pull gemma3:12b
  ```

### Permission denied when editing sudoers
- **Fix:** You need to use `sudo visudo`, not edit the file directly

## Alternative: Skip Auto-Management

If you don't want to configure sudoers, you can:

1. **Manually start Ollama before launching the UI:**
   ```bash
   sudo systemctl start ollama
   python3 ollama_UI_Final_with_auto_start_stop.py
   ```

2. **Manually stop Ollama after exiting:**
   ```bash
   sudo systemctl stop ollama
   ```

The UI will still work, but you'll need to manage Ollama yourself.

## Model Display Names

The UI uses friendly names for models. Edit these in the code:
```python
self.model_display_names = {
    "gemma3:12b": "Dana",
    "gemma3:27b": "Jane",
    "qwen2.5:14b": "Maria",
    "qwen2.5:7b-instruct": "Claire"
}
```

## License

MIT License - feel free to modify and use as needed.

## Contributing

Pull requests welcome! Please ensure:
- Code follows existing style
- New features are documented
- Security implications are considered

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify Ollama is working: `ollama run llama3.1:8b`
3. Check Ollama service: `systemctl status ollama`
4. Open an issue on GitHub with error details
