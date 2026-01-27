# Troubleshooting Guide

Common issues and solutions for Ollama Chat UI.

## Installation Issues

### "ModuleNotFoundError: No module named 'tkinter'"

**Solution:**
```bash
# Ubuntu/Debian/Mint/Pop!_OS
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### "ModuleNotFoundError: No module named 'requests'"

**Solution:**
```bash
pip install requests --break-system-packages
```

### "error: externally-managed-environment"

This is normal on newer Linux systems. Use the `--break-system-packages` flag:
```bash
pip install package-name --break-system-packages
```

## Connection Issues

### Ollama service not running (MOST COMMON)

**Symptoms:** Model dropdown is empty, can't connect, "Connection refused" errors

**Check if Ollama is running:**
```bash
systemctl status ollama
```

**If it shows "inactive (dead)" or "Active: inactive":**
```bash
# Start Ollama
sudo systemctl start ollama

# Enable it to start automatically on boot (recommended)
sudo systemctl enable ollama

# Verify it's running
systemctl status ollama
# Should show "Active: active (running)" in green
```

**Quick test to confirm Ollama is working:**
```bash
# Should list your installed models
ollama list

# OR test the API directly
curl http://localhost:11434/api/tags
```

After starting Ollama, restart your Chat UI app and the model dropdown should populate!

### "Connection refused" or can't connect to models

If Ollama is running but you still get connection errors:
```bash
# Restart Ollama service
sudo systemctl restart ollama

# Check for errors
sudo journalctl -u ollama -n 50
```

### No models in dropdown (after starting Ollama)

**Install a model first:**
```bash
ollama pull gemma3:12b
```

Or use the **📥 Install Model** button in Settings → Model Management.

## Performance Issues

### Slow responses

- **Large conversations** - Click "Clear" to reset context
- **Model too big** - Try a smaller model (3b or 7b instead of 70b)
- **System resources** - Close other applications

### High memory usage

- Use smaller models
- Clear chat history more frequently
- Restart Ollama: `systemctl restart ollama`

## UI Issues

### Menus won't close

Click outside the menu or press Escape.

### Theme not applying

Restart the application after changing themes in code.

### Spell check not working

Install aspell:
```bash
sudo apt install aspell
```

## Model Issues

### Model installation stuck

- Check internet connection
- Model might be very large (wait longer)
- Cancel and try again
- Use command line: `ollama pull model-name`

### Can't delete model

Use command line:
```bash
ollama rm model-name
```

## Getting More Help

1. Check `ollama list` for installed models
2. Check `systemctl status ollama` for Ollama status
3. Look at terminal output for error messages
4. Report issues on GitHub with error details

## Useful Commands

```bash
# List installed models
ollama list

# Check Ollama status
systemctl status ollama

# Restart Ollama
systemctl restart ollama

# Pull a model manually
ollama pull gemma3:12b

# Remove a model
ollama rm model-name

# Check Python version
python3 --version

# Check if tkinter is installed
python3 -c "import tkinter"
```
