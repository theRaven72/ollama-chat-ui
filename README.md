# Ollama Chat UI

A sleek, feature-rich GUI for interacting with locally-hosted Ollama language models. Built with Python and tkinter for maximum compatibility across Linux distributions.

![Ollama Chat UI](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#-documentation)
- [Customization](#customization)
- [Quick Troubleshooting](#quick-troubleshooting)
- [Managing Models](#managing-models)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🎨 **Clean Dark Interface** - Easy on the eyes for extended coding/writing sessions
- 🤖 **Multiple Model Support** - Switch between installed models on the fly
- 📥 **Built-in Model Installer** - Download and install new Ollama models directly from the UI
- 🌐 **Internet Search Integration** - Enable web search for current information (powered by DuckDuckGo)
- 💬 **Streaming Responses** - Watch AI responses appear in real-time
- 📝 **Spell Checker** - Optional spell checking with suggestions (requires aspell)
- 🎭 **Custom Model Names** - Personalize your models with friendly names
- 💾 **Conversation History** - Full chat memory within each session
- 🔄 **Easy Model Management** - Install and switch between models seamlessly

## Requirements

**GPU Acceleration (AMD GPUs)**  
> Ollama automatically uses Vulkan for GPU acceleration on supported AMD GPUs.  
> No manual configuration, environment variables, or special setup is required.

### System Requirements
- **Python 3.x** (3.7 or higher recommended)
- **Ollama** installed and running locally
- **Linux** (tested on Ubuntu, Pop!_OS, Fedora, Arch, Mint - should work on most distros)

### Python Dependencies

#### Required:
```bash
pip install requests duckduckgo-search
```

#### Tkinter (GUI library):
Most systems have this pre-installed, but if not:

**Ubuntu/Debian/Pop!_OS/Mint:**
```bash
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

**Gentoo:**
```bash
# Add 'tk' to your Python USE flags and rebuild
```

#### Optional (for spell checking):
```bash
# Ubuntu/Debian/Mint
sudo apt install aspell

# Fedora
sudo dnf install aspell

# Arch
sudo pacman -S aspell
```

### Ollama Installation

If you don't have Ollama installed:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Or visit [ollama.ai](https://ollama.ai) for other installation methods.

Make sure Ollama is running before launching the UI:
```bash
# Ollama should start automatically, but you can check with:
ollama list
```

## Installation

1. **Clone or download this repository:**
```bash
git clone https://github.com/yourusername/ollama-chat-ui.git
cd ollama-chat-ui
```

2. **Install Python dependencies:**
```bash
pip install requests duckduckgo-search
```

3. **Make sure Ollama is installed and running** (see above)

4. **Run the application:**
```bash
python3 ollama_UI_Final.py
```

## Usage

### First Time Setup

1. **Launch the application:**
   ```bash
   python3 ollama_UI_Final.py
   ```

2. **Install a model** (if you don't have any):
   - Click the **📥 Install Model** button
   - Select a model from the list
   - Confirm installation
   - Wait for download to complete

3. **Connect to a model:**
   - Click the **Model** dropdown
   - Select your desired model
   - Click **Connect**

4. **Start chatting!**

### Features Guide

#### Model Selection
- Click the model dropdown to see all installed models
- Models are dynamically loaded from your local Ollama installation
- Switch models anytime by disconnecting and selecting a new one

#### Installing New Models
- Click **📥 Install Model**
- Browse the curated list of popular models
- Select and install - progress is shown in real-time
- Newly installed models appear immediately in the model selector

#### Internet Search
- Toggle with the **🌐 Internet** button
- When enabled, the AI can search the web for current information
- Useful for questions about recent events, prices, news, etc.
- Disabled by default to keep responses fast

#### Custom Model Names
You can personalize your models by editing the `model_display_names` dictionary in the code:

```python
self.model_display_names = {
    "gemma3:12b": "Claire",
    "gemma3:27b": "Jane",
    "qwen2.5:14b": "Maria"
}
```

The custom name will appear in the top-right corner when connected!

#### Keyboard Shortcuts
- **Enter** - Send message
- **Ctrl+Enter** - Also sends message (useful if you want to add Enter for newlines)
- **Right-click** on misspelled words for spelling suggestions (if aspell is installed)

## Customization

### Color Scheme
Edit the color constants at the top of the file:
```python
COLOR_BG_FRAME = "#1f1f1f"      # Main background
COLOR_BG_CHAT = "#000000"        # Chat area background
COLOR_TEXT_USER = "#ffffff"      # Your messages
COLOR_TEXT_ASSIST = "#ffd54a"    # AI responses
```

### Available Models List
To add/remove models from the installer, edit the `AVAILABLE_MODELS` list:
```python
AVAILABLE_MODELS = [
    ("model:tag", "Description"),
    # Add more models here
]
```

## 📚 Documentation

This project includes comprehensive guides for setup, customization, and troubleshooting.

### Getting Started
- **[⚠️ Compatibility & System Requirements](compatibility.md)** - Read this FIRST to see if these instructions will work for your system.

### Troubleshooting
- **[UI Troubleshooting](troubleshooting-ui.md)** - App won't start? Buttons not working? Check this guide.

### Customization Guides
- **[Change Model Display Names](change-model-names.md)** - Give your models custom names like "Claire" or "Bob"
- **[Customize Themes](customize-themes.md)** - Create your own color schemes
- **[Create Desktop Launcher](create-launcher.md)** - Add the app to your application menu
- **[Edit Modelfiles](edit-modelfiles.md)** - Customize AI personality and behavior

---

## Quick Troubleshooting

### "ModuleNotFoundError: No module named 'tkinter'"
Install tkinter for your distribution (see Requirements section above)

### "Connection refused" or can't connect to models
Make sure Ollama is running:
```bash
systemctl status ollama
# or
ollama list
```

### Models not appearing in dropdown
Verify Ollama has models installed:
```bash
ollama list
```

If no models are installed, use the **📥 Install Model** button in the UI.

### Spell checker not working
Install aspell:
```bash
sudo apt install aspell  # Ubuntu/Debian/Mint
```

### Font looks different
The fancy script font (Brush Script MT) may not be available on all systems. The app will gracefully fall back to a default font.

## Managing Models

### List installed models:
```bash
ollama list
```

### Delete a model:
```bash
ollama rm model:tag
```

### Example - keeping only your named models:
```bash
# Keep gemma3:12b, gemma3:27b, qwen2.5:14b
# Delete everything else:
ollama rm unwanted-model:tag
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

MIT License - feel free to use, modify, and distribute as you wish. Sale of the application, code, files, is prohibited.

## Acknowledgments

- Built for [Ollama](https://ollama.ai)
- Web search powered by [DuckDuckGo](https://duckduckgo.com)
- Spell checking via [GNU Aspell](http://aspell.net/)

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all requirements are installed
3. Make sure Ollama is running: `ollama list`
4. Open an issue on GitHub with error details

---

**Enjoy chatting with your AI models!** 🚀
