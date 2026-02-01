# ⚠️ REQUIRED SETUP - READ THIS FIRST ⚠️

**This UI requires a one-time sudo configuration to work properly.**

## Quick Setup (2 minutes)

### Step 1: Edit sudoers file
```bash
sudo visudo
```

### Step 2: Add this line at the bottom

**Replace `YOUR_USERNAME` with your actual Linux username:**

```
YOUR_USERNAME ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop ollama, /usr/bin/systemctl start ollama
```

**Example (if your username is "john"):**
```
john ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop ollama, /usr/bin/systemctl start ollama
```

### Step 3: Save and exit
- **nano:** `Ctrl+O` → `Enter` → `Ctrl+X`
- **vim:** `Esc` → `:wq` → `Enter`

### Step 4: Test it works
```bash
sudo systemctl stop ollama
sudo systemctl start ollama
```

**If it asks for a password, you did something wrong. Try again.**

### Step 5: Run the UI
```bash
python3 ollama_UI_Final_with_auto_start_stop.py
```

---

## What does this do?

✅ Allows the UI to automatically start Ollama when you launch it  
✅ Allows the UI to automatically stop Ollama when you exit (frees GPU memory)  
✅ **Only affects Ollama service** - cannot be used to damage your system  

## Don't want to do this?

You can skip this setup, but you'll need to **manually** start/stop Ollama:

```bash
# Before running UI:
sudo systemctl start ollama

# After exiting UI:
sudo systemctl stop ollama
```

---

**For detailed instructions and troubleshooting, see [README.md](README.md)**
