import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, Menu
import requests
import json
from datetime import datetime
import subprocess
import re
import threading

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

# ----- Color Scheme -----
COLOR_BG_FRAME = "#1f1f1f"
COLOR_BG_CHAT = "#000000"
COLOR_BG_INPUT = "#000000"

COLOR_TEXT_INPUT = "#ffffff"
COLOR_TEXT_USER = "#ffffff"
COLOR_TEXT_ASSIST = "#ffd54a"
COLOR_TEXT_SYSTEM = "#b0b0b0"

COLOR_BTN_BG = "#2a2a2a"
COLOR_BTN_FG = "#ffffff"
COLOR_BTN_ACTIVE_BG = "#3a3a3a"
COLOR_BORDER = "#3a3a3a"

FONT_MAIN = ("Sans", 11)
FONT_CHAT = ("Sans", 11)
FONT_BTN = ("Sans", 10, "bold")

# Popular Ollama models available for installation
AVAILABLE_MODELS = [
    ("gemma3:12b", "Gemma 3 12B - Fast and capable"),
    ("gemma3:27b", "Gemma 3 27B - More powerful"),
    ("qwen2.5:7b", "Qwen 2.5 7B - Efficient"),
    ("qwen2.5:14b", "Qwen 2.5 14B - Balanced"),
    ("qwen2.5:32b", "Qwen 2.5 32B - High performance"),
    ("llama3.2:3b", "Llama 3.2 3B - Very fast"),
    ("llama3.2:1b", "Llama 3.2 1B - Ultra lightweight"),
    ("llama3.1:8b", "Llama 3.1 8B - Popular choice"),
    ("llama3.1:70b", "Llama 3.1 70B - Top tier"),
    ("mistral:7b", "Mistral 7B - Excellent quality"),
    ("mixtral:8x7b", "Mixtral 8x7B - Expert model"),
    ("phi3:mini", "Phi 3 Mini - Compact"),
    ("phi3:medium", "Phi 3 Medium - Balanced"),
    ("codellama:7b", "Code Llama 7B - Code specialist"),
    ("deepseek-coder:6.7b", "DeepSeek Coder 6.7B - Coding"),
]

# Theme presets
THEMES = {
    "Dark": {
        "bg_frame": "#1f1f1f",
        "bg_chat": "#000000",
        "bg_input": "#000000",
        "text_input": "#ffffff",
        "text_user": "#ffffff",
        "text_assist": "#ffd54a",
        "text_system": "#b0b0b0",
        "btn_bg": "#2a2a2a",
        "btn_fg": "#ffffff",
        "btn_active_bg": "#3a3a3a",
        "border": "#3a3a3a",
    },
    "Light": {
        "bg_frame": "#e8e8e8",
        "bg_chat": "#ffffff",
        "bg_input": "#ffffff",
        "text_input": "#000000",
        "text_user": "#1a1a1a",
        "text_assist": "#0066cc",
        "text_system": "#666666",
        "btn_bg": "#d0d0d0",
        "btn_fg": "#000000",
        "btn_active_bg": "#b0b0b0",
        "border": "#cccccc",
    },
    "Matrix": {
        "bg_frame": "#000000",
        "bg_chat": "#000000",
        "bg_input": "#001a00",
        "text_input": "#00ff00",
        "text_user": "#00ff00",
        "text_assist": "#00ff00",
        "text_system": "#008800",
        "btn_bg": "#001a00",
        "btn_fg": "#00ff00",
        "btn_active_bg": "#003300",
        "border": "#00ff00",
    },
    "Nord": {
        "bg_frame": "#2e3440",
        "bg_chat": "#3b4252",
        "bg_input": "#3b4252",
        "text_input": "#eceff4",
        "text_user": "#eceff4",
        "text_assist": "#88c0d0",
        "text_system": "#d8dee9",
        "btn_bg": "#4c566a",
        "btn_fg": "#eceff4",
        "btn_active_bg": "#5e81ac",
        "border": "#4c566a",
    },
    "Dracula": {
        "bg_frame": "#282a36",
        "bg_chat": "#1e1f29",
        "bg_input": "#1e1f29",
        "text_input": "#f8f8f2",
        "text_user": "#f8f8f2",
        "text_assist": "#bd93f9",
        "text_system": "#6272a4",
        "btn_bg": "#44475a",
        "btn_fg": "#f8f8f2",
        "btn_active_bg": "#6272a4",
        "border": "#6272a4",
    },
}


class SpellChecker:
    """Simple spell checker using aspell"""
    
    def __init__(self):
        self.enabled = self._check_aspell()
    
    def _check_aspell(self):
        """Check if aspell is installed"""
        try:
            subprocess.run(['aspell', '--version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def check_word(self, word):
        """Check if a word is spelled correctly"""
        if not self.enabled or not word.strip():
            return True
        
        # Skip if it's a number, URL, or has special chars
        if re.match(r'^[\d\W]+$', word) or '://' in word or '@' in word:
            return True
        
        # Skip very short words
        if len(word) < 2:
            return True
        
        try:
            result = subprocess.run(
                ['aspell', '-a'],
                input=word + '\n',
                capture_output=True,
                text=True,
                timeout=1
            )
            # aspell returns lines: first line is version, then results
            lines = result.stdout.strip().split('\n')[1:]  # Skip version line
            if lines:
                first_line = lines[0]
                # '*' means correct, '&' or '#' means incorrect
                return first_line.startswith('*')
            return True
        except:
            return True
    
    def get_suggestions(self, word):
        """Get spelling suggestions for a word"""
        if not self.enabled or not word.strip():
            return []
        
        try:
            result = subprocess.run(
                ['aspell', '-a'],
                input=word + '\n',
                capture_output=True,
                text=True,
                timeout=1
            )
            
            # Parse aspell output for suggestions
            lines = result.stdout.strip().split('\n')[1:]  # Skip version line
            for line in lines:
                if line.startswith('&'):
                    # Format: & word count offset: suggestion1, suggestion2, ...
                    parts = line.split(':')
                    if len(parts) > 1:
                        suggestions = [s.strip() for s in parts[1].split(',')]
                        return suggestions[:5]
            return []
        except:
            return []


class OllamaChatUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ollama Chat – Model Selector")
        self.geometry("950x750")
        self.configure(bg=COLOR_BG_FRAME)

        self.messages = []
        self.current_model = None
        self.connected = False
        self.web_search_enabled = False  # Default to OFF
        self.spell_checker = SpellChecker()
        self.total_tokens = 0  # Track total tokens in conversation
        self.input_tokens = 0  # Track user input tokens
        self.output_tokens = 0  # Track AI output tokens
        self.current_theme = "Dark"  # Track current theme
        
        # Model display names
        self.model_display_names = {
            "gemma3:12b": "Claire",
            "gemma3:27b": "Jane",
            "qwen2.5:14b": "Maria"
        }

        outer = tk.Frame(self, bg=COLOR_BG_FRAME,
                         highlightbackground=COLOR_BORDER,
                         highlightthickness=2)
        outer.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # ----- Model Selection Frame -----
        model_frame = tk.Frame(outer, bg=COLOR_BG_FRAME)
        model_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        model_label = tk.Label(
            model_frame, text="Model:",
            bg=COLOR_BG_FRAME, fg=COLOR_TEXT_INPUT,
            font=FONT_MAIN
        )
        model_label.pack(side=tk.LEFT, padx=(0, 10))

        self.model_var = tk.StringVar(value="Claire (gemma3:12b)")
        # Create button that shows current model
        self.model_btn = tk.Button(
            model_frame,
            textvariable=self.model_var,
            command=self._show_model_menu,
            bg=COLOR_BTN_BG,
            fg=COLOR_BTN_FG,
            font=FONT_MAIN,
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5,
            width=20,
            anchor="w"
        )
        self.model_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.connect_btn = tk.Button(
            model_frame, text="Connect",
            command=self.toggle_connection,
            bg="#223b22", fg=COLOR_BTN_FG,
            activebackground="#2f5a2f",
            relief=tk.FLAT, bd=0,
            font=FONT_BTN, padx=15, pady=5,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER
        )
        self.connect_btn.pack(side=tk.LEFT)

        self.search_toggle_btn = tk.Button(
            model_frame, text="🌐 Internet: OFF",
            command=self.toggle_web_search,
            bg="#22223b", fg=COLOR_BTN_FG,
            activebackground="#2f2f5a",
            relief=tk.FLAT, bd=0,
            font=FONT_BTN, padx=15, pady=5,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER
        )
        self.search_toggle_btn.pack(side=tk.LEFT, padx=(10, 0))

        self.settings_btn = tk.Button(
            model_frame, text="⚙️ Settings",
            command=self.show_settings,
            bg="#3b3b22", fg=COLOR_BTN_FG,
            activebackground="#5a5a2f",
            relief=tk.FLAT, bd=0,
            font=FONT_BTN, padx=15, pady=5,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER
        )
        self.settings_btn.pack(side=tk.RIGHT, padx=(0, 0))

        self.status_label = tk.Label(
            model_frame, text="⚫ Disconnected",
            bg=COLOR_BG_FRAME, fg="#888888",
            font=FONT_MAIN
        )
        self.status_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Token counter with input/output breakdown
        self.token_label = tk.Label(
            model_frame, text="Tokens: 0 (In: 0 | Out: 0)",
            bg=COLOR_BG_FRAME, fg="#888888",
            font=FONT_MAIN
        )
        self.token_label.pack(side=tk.LEFT, padx=(15, 0))

        # ----- Chat Log with Model Name -----
        chat_container = tk.Frame(outer, bg=COLOR_BG_FRAME)
        chat_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 8))
        
        # Create a frame to hold text widget
        self.chat_frame = tk.Frame(chat_container, bg=COLOR_BG_CHAT)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Model name in fancy script at top-right
        self.model_name_label = tk.Label(
            self.chat_frame,
            text="",
            font=("Brush Script MT", 48, "italic"),  # Smaller font
            fg="#5a5a5a",
            bg=COLOR_BG_CHAT
        )
        self.model_name_label.place(relx=1.0, y=10, x=-50, anchor="ne")  # Top-right corner with more padding
        
        # Chat log
        self.chat_log = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            state="disabled",
            font=FONT_CHAT,
            bg=COLOR_BG_CHAT,
            insertbackground=COLOR_TEXT_INPUT,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
            padx=10,
            pady=10
        )
        self.chat_log.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Raise model name label so it appears on top
        self.model_name_label.lift()

        self.chat_log.tag_configure("user", foreground=COLOR_TEXT_USER)
        self.chat_log.tag_configure("assistant", foreground=COLOR_TEXT_ASSIST)
        self.chat_log.tag_configure("system", foreground=COLOR_TEXT_SYSTEM)
        self.chat_log.tag_configure("search", foreground="#64B5F6")

        # ----- Input Area with Spell Check -----
        bottom = tk.Frame(outer, bg=COLOR_BG_FRAME)
        bottom.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.user_input = tk.Text(
            bottom, height=4, wrap=tk.WORD,
            font=FONT_MAIN, bg=COLOR_BG_INPUT,
            fg=COLOR_TEXT_INPUT,
            insertbackground=COLOR_TEXT_INPUT,
            relief=tk.FLAT, bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
            padx=10, pady=10
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure spell check tag
        self.user_input.tag_configure("misspelled", 
                                     foreground="#ff6666",
                                     underline=True)
        
        # Bind events for spell checking
        if self.spell_checker.enabled:
            self.user_input.bind("<KeyRelease>", self._check_spelling)
            self.user_input.bind("<Button-3>", self._show_suggestions)
        
        self.user_input.bind("<Return>", self.on_enter_key)
        self.bind("<Control-Return>", lambda e: self.on_submit())

        btn_frame = tk.Frame(bottom, bg=COLOR_BG_FRAME)
        btn_frame.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.Y)

        self.submit_btn = self._make_btn(btn_frame, "Submit", self.on_submit)
        self.submit_btn.pack(fill=tk.X, pady=(0, 8))

        self.clear_btn = self._make_btn(btn_frame, "Clear", self.on_clear)
        self.clear_btn.pack(fill=tk.X, pady=(0, 8))

        self.save_btn = self._make_btn(btn_frame, "Save Chat", self.on_save_chat)
        self.save_btn.pack(fill=tk.X, pady=(0, 8))

        self.load_btn = self._make_btn(btn_frame, "Load Chat", self.on_load_chat)
        self.load_btn.pack(fill=tk.X, pady=(0, 8))

        self.exit_btn = self._make_btn(
            btn_frame, "Exit", self.on_exit,
            bg="#3b2222", active="#5a2f2f"
        )
        self.exit_btn.pack(fill=tk.X)

        self._set_chat_controls(False)
        self.append_system("Select a model and click Connect to begin")
        self.append_system("Internet search disabled - enable with 🌐 Internet button if needed")
        if self.spell_checker.enabled:
            self.append_system("Spell checking enabled - right-click misspelled words for suggestions")

    def _show_model_menu(self):
        """Show dropdown menu for model selection"""
        menu = Menu(self, tearoff=0)
        
        # Try to get installed models from Ollama
        installed_models = self._get_installed_models()
        
        if installed_models:
            for model_id in installed_models:
                # Use display name if available, otherwise use model_id
                display_name = self.model_display_names.get(model_id, model_id)
                label = f"{display_name} ({model_id})" if model_id in self.model_display_names else model_id
                menu.add_command(
                    label=label,
                    command=lambda m=model_id: self._select_model(m)
                )
        else:
            # Fallback to hardcoded list if API fails
            models = [
                ("gemma3:12b", "Claire"),
                ("gemma3:27b", "Jane"),
                ("qwen2.5:14b", "Maria")
            ]
            
            for model_id, display_name in models:
                menu.add_command(
                    label=f"{display_name} ({model_id})",
                    command=lambda m=model_id: self._select_model(m)
                )
        
        # Show menu below the button
        x = self.model_btn.winfo_rootx()
        y = self.model_btn.winfo_rooty() + self.model_btn.winfo_height()
        
        # Bind to close menu on focus loss
        def close_menu(event=None):
            menu.unpost()
        
        menu.bind("<FocusOut>", close_menu)
        self.bind("<Button-1>", lambda e: close_menu(), add="+")
        
        try:
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()
    
    def _get_installed_models(self):
        """Get list of installed models from Ollama"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Extract model names
            models = []
            if 'models' in data:
                for model in data['models']:
                    if 'name' in model:
                        models.append(model['name'])
            
            return sorted(models)
        except Exception as e:
            print(f"Failed to get installed models: {e}")
            return []

    def _select_model(self, model_id):
        """Select a model from the dropdown"""
        display_name = self.model_display_names.get(model_id, model_id)
        self.model_var.set(f"{display_name} ({model_id})")
        
        # If currently connected, disconnect first
        if self.connected:
            self.disconnect_model()

    def _check_spelling(self, event=None):
        """Check spelling in the input box"""
        if not self.spell_checker.enabled:
            return
        
        # Remove all misspelling tags first
        self.user_input.tag_remove("misspelled", "1.0", tk.END)
        
        # Get all text
        text = self.user_input.get("1.0", tk.END)
        
        # Split into words and check each
        for match in re.finditer(r'\b[a-zA-Z]{2,}\b', text):
            word = match.group()
            if not self.spell_checker.check_word(word):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.user_input.tag_add("misspelled", start, end)

    def _show_suggestions(self, event):
        """Show spelling suggestions on right-click"""
        if not self.spell_checker.enabled:
            return
        
        # Get word at cursor
        try:
            index = self.user_input.index(f"@{event.x},{event.y}")
        except:
            return
        
        # Find word boundaries
        line_start = self.user_input.index(f"{index} linestart")
        line_end = self.user_input.index(f"{index} lineend")
        line_text = self.user_input.get(line_start, line_end)
        
        # Get character position in line
        col = int(index.split('.')[1])
        
        # Find word at position
        words = list(re.finditer(r'\b[a-zA-Z]+\b', line_text))
        current_word = None
        word_start_idx = None
        word_end_idx = None
        
        for match in words:
            if match.start() <= col <= match.end():
                current_word = match.group()
                word_start_idx = match.start()
                word_end_idx = match.end()
                break
        
        if not current_word:
            return
        
        # Check if word is misspelled
        if self.spell_checker.check_word(current_word):
            return
        
        # Get suggestions
        suggestions = self.spell_checker.get_suggestions(current_word)
        
        if suggestions:
            # Create context menu
            menu = Menu(self, tearoff=0)
            
            row = index.split('.')[0]
            word_start = f"{row}.{word_start_idx}"
            word_end = f"{row}.{word_end_idx}"
            
            for suggestion in suggestions:
                menu.add_command(
                    label=suggestion,
                    command=lambda s=suggestion, ws=word_start, we=word_end: 
                        self._replace_word(ws, we, s)
                )
            
            menu.add_separator()
            menu.add_command(label="Ignore", command=lambda: None)
            
            # Bind to close menu on focus loss
            def close_menu(event=None):
                menu.unpost()
            
            menu.bind("<FocusOut>", close_menu)
            self.bind("<Button-1>", lambda e: close_menu(), add="+")
            
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

    def _replace_word(self, start, end, new_word):
        """Replace misspelled word with suggestion"""
        self.user_input.delete(start, end)
        self.user_input.insert(start, new_word)
        self._check_spelling()

    def _make_btn(self, parent, text, cmd, bg=COLOR_BTN_BG, active=COLOR_BTN_ACTIVE_BG):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=bg, fg=COLOR_BTN_FG,
            activebackground=active,
            relief=tk.FLAT, bd=0,
            font=FONT_BTN, padx=20, pady=10,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
            width=15
        )

    # ---------- Settings Menu ----------
    def show_settings(self):
        """Show settings dropdown menu"""
        menu = Menu(self, tearoff=0)
        
        # Themes - opens dialog
        menu.add_command(label="🎨 Themes...", command=self.show_themes_dialog)
        
        menu.add_separator()
        
        # Model Management - single option that opens dialog
        menu.add_command(label="🤖 Model Management", command=self.show_model_management_dialog)
        
        menu.add_separator()
        
        # Documentation
        menu.add_command(label="📚 Documentation", command=self.open_documentation)
        
        # Calculate position - align to right edge of button
        button_x = self.settings_btn.winfo_rootx()
        button_y = self.settings_btn.winfo_rooty()
        button_width = self.settings_btn.winfo_width()
        button_height = self.settings_btn.winfo_height()
        
        # Get screen width to check if menu will go off screen
        screen_width = self.winfo_screenwidth()
        menu_width = 200  # Approximate menu width
        
        # Position menu - if too close to right edge, shift left
        if button_x + menu_width > screen_width:
            x = button_x + button_width - menu_width
        else:
            x = button_x
        
        y = button_y + button_height
        
        # Bind to close menu on focus loss
        def close_menu(event=None):
            menu.unpost()
        
        menu.bind("<FocusOut>", close_menu)
        self.bind("<Button-1>", lambda e: close_menu(), add="+")
        
        try:
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()
    
    def open_documentation(self):
        """Open the Guides folder and create documentation if it doesn't exist"""
        import os
        import subprocess
        
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        guides_dir = os.path.join(script_dir, "Guides")
        
        # Create Guides directory if it doesn't exist
        if not os.path.exists(guides_dir):
            os.makedirs(guides_dir)
            self.append_system("Created Guides directory")
        
        # Create documentation files if they don't exist
        self._create_documentation_files(guides_dir)
        
        # Open the folder in file manager
        try:
            if os.name == 'posix':  # Linux/Mac
                subprocess.Popen(['xdg-open', guides_dir])
            elif os.name == 'nt':  # Windows
                subprocess.Popen(['explorer', guides_dir])
            self.append_system("Opened documentation folder")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder:\n{str(e)}")
    
    def _create_documentation_files(self, guides_dir):
        """Create all documentation files"""
        import os
        
        # README.md - General info
        readme_path = os.path.join(guides_dir, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, 'w') as f:
                f.write("""# Ollama Chat UI - Documentation

Welcome to the Ollama Chat UI documentation!

## What is this?

This is a graphical user interface for chatting with locally-hosted Ollama language models. It provides an easy way to interact with AI models on your own computer without needing to use the command line.

## Features

- 🤖 **Model Management** - Install, delete, and switch between AI models
- 🌐 **Internet Search** - Enable web search for current information
- 💾 **Save/Load Chats** - Save conversations and reload them later
- 📊 **Token Counter** - Track conversation length (input/output tokens)
- 🎨 **Themes** - Choose from 5 color schemes
- ✅ **Spell Checking** - Right-click suggestions for misspelled words
- 💬 **Conversation Memory** - Models remember chat history

## Requirements

### System Requirements
- Linux (Ubuntu, Pop!_OS, Fedora, Arch, Mint, etc.)
- Python 3.7 or higher
- Ollama installed and running

### Installation

1. **Install Ollama** (if not already installed):
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Install Python dependencies**:
   ```bash
   pip install requests duckduckgo-search --break-system-packages
   ```

3. **Install tkinter** (if not already installed):
   ```bash
   # Ubuntu/Debian/Mint/Pop!_OS
   sudo apt install python3-tk
   
   # Fedora
   sudo dnf install python3-tkinter
   
   # Arch
   sudo pacman -S tk
   ```

4. **Optional - Spell checking**:
   ```bash
   sudo apt install aspell
   ```

5. **Run the application**:
   ```bash
   python3 ollama_UI_Final.py
   ```

## Quick Start

1. Launch the app
2. Click **📥 Install Model** (in Settings → Model Management)
3. Select a model and install
4. Click the **Model** dropdown and select your installed model
5. Click **Connect**
6. Start chatting!

## Getting Help

- Check the other guides in this folder for specific topics
- Report issues on GitHub
- Join the community discussions

## License

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

**You can:**
- Use it for free
- Modify it
- Share it
- Build upon it

**You cannot:**
- Sell it
- Use it commercially

See LICENSE.txt for full details.

---

**Enjoy chatting with your AI models!** 🚀
""")
        
        # LICENSE.txt
        license_path = os.path.join(guides_dir, "LICENSE.txt")
        if not os.path.exists(license_path):
            with open(license_path, 'w') as f:
                f.write("""Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

Copyright (c) 2026 Ollama Chat UI Contributors

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License.

You are free to:
  - Share: copy and redistribute the material in any medium or format
  - Adapt: remix, transform, and build upon the material

Under the following terms:
  - Attribution: You must give appropriate credit, provide a link to the license, and 
    indicate if changes were made.
  
  - NonCommercial: You may NOT use this material for commercial purposes. This means you 
    cannot sell this software or use it in a commercial product/service.
  
  - ShareAlike: If you remix, transform, or build upon the material, you must distribute 
    your contributions under the same license as the original.
  
  - No additional restrictions: You may not apply legal terms or technological measures 
    that legally restrict others from doing anything the license permits.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT.

Full license text: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
""")
        
        # Change_Model_Names.md
        model_names_path = os.path.join(guides_dir, "Change_Model_Names.md")
        if not os.path.exists(model_names_path):
            with open(model_names_path, 'w') as f:
                f.write("""# How to Change Model Display Names

You can give your AI models custom names like "Claire", "Bob", "Assistant", etc.

## Steps

1. **Open the Python file** in a text editor:
   ```bash
   nano ollama_UI_Final.py
   # or
   gedit ollama_UI_Final.py
   ```

2. **Find the model_display_names section** (around line 150):
   ```python
   self.model_display_names = {
       "gemma3:12b": "Claire",
       "gemma3:27b": "Jane",
       "qwen2.5:14b": "Maria"
   }
   ```

3. **Add or modify entries**:
   ```python
   self.model_display_names = {
       "gemma3:12b": "Claire",
       "llama3.1:8b": "Bob",
       "mistral:7b": "Assistant",
       "your-model:tag": "Your Custom Name"
   }
   ```

4. **Save and close** the file

5. **Restart the application**

## Notes

- The **key** (left side) must match the exact model name from `ollama list`
- The **value** (right side) is your custom display name
- Names appear in the model dropdown and in chat
- The fancy model name appears in the top-right corner during chat

## Finding Model Names

To see your installed model names:
```bash
ollama list
```

Use the exact name from the "NAME" column.
""")
        
        # Customize_Themes.md
        themes_path = os.path.join(guides_dir, "Customize_Themes.md")
        if not os.path.exists(themes_path):
            with open(themes_path, 'w') as f:
                f.write("""# How to Add Custom Themes

You can create your own color themes for the UI!

## Steps

1. **Open the Python file** in a text editor

2. **Find the THEMES dictionary** (around line 18):
   ```python
   THEMES = {
       "Dark": { ... },
       "Light": { ... },
       # Add your theme here
   }
   ```

3. **Add your custom theme**:
   ```python
   THEMES = {
       "Dark": { ... },
       "Light": { ... },
       "MyTheme": {
           "bg_frame": "#1a1a2e",
           "bg_chat": "#16213e",
           "bg_input": "#0f3460",
           "text_input": "#eee",
           "text_user": "#ffffff",
           "text_assist": "#53a8b6",
           "text_system": "#95a5a6",
           "btn_bg": "#1a1a2e",
           "btn_fg": "#ffffff",
           "btn_active_bg": "#16213e",
           "border": "#53a8b6"
       }
   }
   ```

4. **Save and restart** the application

5. **Select your theme** in Settings → Themes

## Color Codes

- Use hex color codes: `#RRGGBB`
- Find colors at: https://htmlcolorcodes.com
- Test different combinations for readability

## Theme Elements

- `bg_frame` - Top toolbar and side panel background
- `bg_chat` - Main chat area background
- `bg_input` - Text input box background
- `text_input` - Text you type
- `text_user` - Your messages in chat
- `text_assist` - AI responses
- `text_system` - System messages
- `btn_bg` - Button background
- `btn_fg` - Button text
- `btn_active_bg` - Button hover/active color
- `border` - Border colors

## Tips

- Keep good contrast between background and text
- Test in both daylight and dark environments
- Dark themes are easier on the eyes for long sessions
""")
        
        # Troubleshooting.md
        troubleshooting_path = os.path.join(guides_dir, "Troubleshooting.md")
        if not os.path.exists(troubleshooting_path):
            with open(troubleshooting_path, 'w') as f:
                f.write("""# Troubleshooting Guide

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
pip install requests duckduckgo-search --break-system-packages
```

### "error: externally-managed-environment"

This is normal on newer Linux systems. Use the `--break-system-packages` flag:
```bash
pip install package-name --break-system-packages
```

## Connection Issues

### "Connection refused" or can't connect to models

**Check if Ollama is running:**
```bash
ollama list
```

If you get an error, start Ollama:
```bash
# Usually starts automatically, but you can restart with:
systemctl restart ollama
```

### No models in dropdown

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

## Internet Search Issues

### Search not working

1. Check internet connection
2. Try disabling/re-enabling with 🌐 Internet button
3. DuckDuckGo might be blocked - try a VPN

### Getting wrong/outdated results

- Search engines aren't perfect
- Try rephrasing your question
- Be specific with dates: "bitcoin price today"

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
""")

    def show_themes_dialog(self):
        """Show theme selection dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Select Theme")
        dialog.geometry("400x450")
        dialog.configure(bg=COLOR_BG_FRAME)
        dialog.transient(self)
        dialog.grab_set()
        
        title_label = tk.Label(
            dialog,
            text="Choose a Theme",
            font=("Sans", 16, "bold"),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_INPUT
        )
        title_label.pack(pady=20)
        
        info_label = tk.Label(
            dialog,
            text="Select a color theme for the interface:",
            font=("Sans", 10),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_SYSTEM
        )
        info_label.pack(pady=(0, 20))
        
        # Create buttons for each theme
        for theme_name in THEMES.keys():
            theme_frame = tk.Frame(dialog, bg=COLOR_BG_FRAME)
            theme_frame.pack(fill=tk.X, padx=40, pady=5)
            
            # Show current theme indicator
            is_current = theme_name == self.current_theme
            indicator = "●" if is_current else "○"
            
            theme_btn = tk.Button(
                theme_frame,
                text=f"{indicator}  {theme_name}",
                command=lambda t=theme_name: [self.apply_theme(t), dialog.destroy()],
                bg=COLOR_BTN_BG if not is_current else COLOR_BTN_ACTIVE_BG,
                fg=COLOR_BTN_FG,
                font=("Sans", 11, "bold" if is_current else "normal"),
                anchor="w",
                padx=20,
                pady=12,
                width=20
            )
            theme_btn.pack(fill=tk.X)
        
        close_btn = tk.Button(
            dialog,
            text="Cancel",
            command=dialog.destroy,
            bg=COLOR_BTN_BG,
            fg=COLOR_BTN_FG,
            font=FONT_BTN,
            padx=30,
            pady=10
        )
        close_btn.pack(pady=30)
    
    def show_model_management_dialog(self):
        """Show unified model management dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Model Management")
        dialog.geometry("650x550")
        dialog.configure(bg=COLOR_BG_FRAME)
        dialog.transient(self)
        dialog.grab_set()
        
        title_label = tk.Label(
            dialog,
            text="Model Management",
            font=("Sans", 16, "bold"),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_INPUT
        )
        title_label.pack(pady=20)
        
        # === INSTALL SECTION ===
        install_frame = tk.LabelFrame(
            dialog,
            text=" Install New Model ",
            font=("Sans", 11, "bold"),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_INPUT,
            bd=2,
            relief=tk.GROOVE
        )
        install_frame.pack(fill=tk.X, padx=30, pady=(10, 15))
        
        install_info = tk.Label(
            install_frame,
            text="Download and install models from Ollama's library",
            font=("Sans", 9),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_SYSTEM
        )
        install_info.pack(pady=(10, 10))
        
        install_btn = tk.Button(
            install_frame,
            text="📥 Install Model",
            command=lambda: [dialog.destroy(), self.show_install_dialog()],
            bg="#223b22",
            fg=COLOR_BTN_FG,
            font=FONT_BTN,
            padx=20,
            pady=8
        )
        install_btn.pack(pady=(0, 15))
        
        # === DELETE SECTION ===
        delete_frame = tk.LabelFrame(
            dialog,
            text=" Delete Installed Model ",
            font=("Sans", 11, "bold"),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_INPUT,
            bd=2,
            relief=tk.GROOVE
        )
        delete_frame.pack(fill=tk.X, padx=30, pady=(0, 15))
        
        delete_info = tk.Label(
            delete_frame,
            text="Remove models you no longer need",
            font=("Sans", 9),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_SYSTEM
        )
        delete_info.pack(pady=(10, 10))
        
        delete_btn = tk.Button(
            delete_frame,
            text="🗑️ Delete Model",
            command=lambda: [dialog.destroy(), self.show_delete_dialog()],
            bg="#3b2222",
            fg=COLOR_BTN_FG,
            font=FONT_BTN,
            padx=20,
            pady=8
        )
        delete_btn.pack(pady=(0, 15))
        
        # === CUSTOM NAMES SECTION ===
        names_frame = tk.LabelFrame(
            dialog,
            text=" Custom Model Names ",
            font=("Sans", 11, "bold"),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_INPUT,
            bd=2,
            relief=tk.GROOVE
        )
        names_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 15))
        
        if self.model_display_names:
            names_info = tk.Label(
                names_frame,
                text="Your custom model names:",
                font=("Sans", 9),
                bg=COLOR_BG_FRAME,
                fg=COLOR_TEXT_SYSTEM
            )
            names_info.pack(pady=(10, 10))
            
            for model_id, display_name in self.model_display_names.items():
                name_row = tk.Frame(names_frame, bg=COLOR_BG_FRAME)
                name_row.pack(fill=tk.X, padx=20, pady=3)
                
                model_label = tk.Label(
                    name_row,
                    text=model_id,
                    font=("Monospace", 9),
                    bg=COLOR_BG_FRAME,
                    fg=COLOR_TEXT_SYSTEM,
                    width=22,
                    anchor="w"
                )
                model_label.pack(side=tk.LEFT)
                
                arrow = tk.Label(
                    name_row,
                    text="→",
                    font=("Sans", 9),
                    bg=COLOR_BG_FRAME,
                    fg=COLOR_TEXT_SYSTEM
                )
                arrow.pack(side=tk.LEFT, padx=5)
                
                display_label = tk.Label(
                    name_row,
                    text=display_name,
                    font=("Sans", 10, "bold"),
                    bg=COLOR_BG_FRAME,
                    fg=COLOR_TEXT_ASSIST
                )
                display_label.pack(side=tk.LEFT)
        else:
            no_names_label = tk.Label(
                names_frame,
                text="No custom names configured",
                font=("Sans", 9),
                bg=COLOR_BG_FRAME,
                fg=COLOR_TEXT_SYSTEM
            )
            no_names_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            names_frame,
            text="\nTo add or edit custom names, modify the model_display_names\ndictionary in the Python code (around line 150).\n\nExample:\nself.model_display_names = {\n    \"gemma3:12b\": \"Claire\",\n    \"llama3.1:8b\": \"Bob\"\n}",
            font=("Monospace", 8),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_SYSTEM,
            justify=tk.LEFT
        )
        instructions.pack(pady=(10, 15))
        
        # Close button
        close_btn = tk.Button(
            dialog,
            text="Close",
            command=dialog.destroy,
            bg=COLOR_BTN_BG,
            fg=COLOR_BTN_FG,
            font=FONT_BTN,
            padx=30,
            pady=10
        )
        close_btn.pack(pady=(0, 20))
    
    
    def apply_theme(self, theme_name):
        """Apply a theme to the UI"""
        if theme_name not in THEMES:
            return
        
        self.current_theme = theme_name
        theme = THEMES[theme_name]
        
        # Apply theme colors to all widgets
        try:
            # Update main window and frames
            self.configure(bg=theme["bg_frame"])
            
            # Update chat area
            self.chat_log.configure(
                bg=theme["bg_chat"],
                fg=theme["text_user"]
            )
            
            # Update chat text tags
            self.chat_log.tag_configure("user", foreground=theme["text_user"])
            self.chat_log.tag_configure("assistant", foreground=theme["text_assist"])
            self.chat_log.tag_configure("system", foreground=theme["text_system"])
            
            # Update input area
            self.user_input.configure(
                bg=theme["bg_input"],
                fg=theme["text_input"]
            )
            
            # Update model name label
            self.model_name_label.configure(
                bg=theme["bg_chat"],
                fg=theme["text_assist"]
            )
            
            self.append_system(f"✓ {theme_name} theme applied")
            
        except Exception as e:
            messagebox.showerror("Theme Error", f"Failed to apply theme:\n{str(e)}")
    
    def show_delete_dialog(self):
        """Show dialog to select and delete a model"""
        dialog = tk.Toplevel(self)
        dialog.title("Delete Ollama Model")
        dialog.geometry("600x500")
        dialog.configure(bg=COLOR_BG_FRAME)
        dialog.transient(self)
        dialog.grab_set()
        
        # Title
        title_label = tk.Label(
            dialog,
            text="Select a model to delete:",
            font=("Sans", 12, "bold"),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_INPUT
        )
        title_label.pack(pady=(20, 10))
        
        warning_label = tk.Label(
            dialog,
            text="⚠️ Warning: This action cannot be undone!",
            font=("Sans", 10),
            bg=COLOR_BG_FRAME,
            fg="#ff6b6b"
        )
        warning_label.pack(pady=(0, 10))
        
        # Model list frame
        list_frame = tk.Frame(dialog, bg=COLOR_BG_FRAME)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollable listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        model_listbox = tk.Listbox(
            list_frame,
            font=FONT_MAIN,
            bg=COLOR_BG_CHAT,
            fg=COLOR_TEXT_INPUT,
            selectbackground=COLOR_BTN_ACTIVE_BG,
            selectforeground=COLOR_TEXT_INPUT,
            yscrollcommand=scrollbar.set,
            height=15
        )
        model_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=model_listbox.yview)
        
        # Get installed models
        installed_models = self._get_installed_models()
        
        if not installed_models:
            model_listbox.insert(tk.END, "No models installed")
        else:
            for model_id in installed_models:
                model_listbox.insert(tk.END, model_id)
        
        # Button frame
        btn_frame = tk.Frame(dialog, bg=COLOR_BG_FRAME)
        btn_frame.pack(pady=20)
        
        def on_delete():
            selection = model_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a model to delete.")
                return
            
            selected_text = model_listbox.get(selection[0])
            
            if selected_text == "No models installed":
                return
            
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete {selected_text}?\n\nThis action cannot be undone!"
            )
            
            if confirm:
                dialog.destroy()
                self.delete_model(selected_text)
        
        delete_btn = tk.Button(
            btn_frame,
            text="Delete Selected",
            command=on_delete,
            bg="#3b2222",
            fg=COLOR_BTN_FG,
            activebackground="#5a2f2f",
            font=FONT_BTN,
            padx=20,
            pady=10
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=COLOR_BTN_BG,
            fg=COLOR_BTN_FG,
            activebackground=COLOR_BTN_ACTIVE_BG,
            font=FONT_BTN,
            padx=20,
            pady=10
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def delete_model(self, model_id):
        """Delete a model using ollama rm command"""
        self.append_system(f"Deleting model {model_id}...")
        
        try:
            import subprocess
            result = subprocess.run(
                ['ollama', 'rm', model_id],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.append_system(f"✓ Successfully deleted {model_id}")
                messagebox.showinfo("Success", f"Model {model_id} deleted successfully!")
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                self.append_system(f"✗ Failed to delete {model_id}: {error_msg}")
                messagebox.showerror("Deletion Failed", f"Failed to delete {model_id}:\n{error_msg}")
                
        except subprocess.TimeoutExpired:
            self.append_system(f"✗ Deletion timed out for {model_id}")
            messagebox.showerror("Timeout", "Deletion operation timed out.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Ollama command not found. Is Ollama installed?")
        except Exception as e:
            self.append_system(f"✗ Error deleting {model_id}: {str(e)}")
            messagebox.showerror("Error", f"Failed to delete model:\n{str(e)}")

    # ---------- Model Installation ----------
    def show_install_dialog(self):
        """Show dialog to select and install a model"""
        dialog = tk.Toplevel(self)
        dialog.title("Install Ollama Model")
        dialog.geometry("600x500")
        dialog.configure(bg=COLOR_BG_FRAME)
        dialog.transient(self)
        dialog.grab_set()
        
        # Title
        title_label = tk.Label(
            dialog,
            text="Select a model to install:",
            font=("Sans", 12, "bold"),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_INPUT
        )
        title_label.pack(pady=(20, 10))
        
        # Model list frame
        list_frame = tk.Frame(dialog, bg=COLOR_BG_FRAME)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollable listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        model_listbox = tk.Listbox(
            list_frame,
            font=FONT_MAIN,
            bg=COLOR_BG_CHAT,
            fg=COLOR_TEXT_INPUT,
            selectbackground=COLOR_BTN_ACTIVE_BG,
            selectforeground=COLOR_TEXT_INPUT,
            yscrollcommand=scrollbar.set,
            height=15
        )
        model_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=model_listbox.yview)
        
        # Populate with models
        for model_id, description in AVAILABLE_MODELS:
            model_listbox.insert(tk.END, f"{model_id} - {description}")
        
        # Button frame
        btn_frame = tk.Frame(dialog, bg=COLOR_BG_FRAME)
        btn_frame.pack(pady=20)
        
        def on_install():
            selection = model_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a model to install.")
                return
            
            selected_text = model_listbox.get(selection[0])
            model_id = selected_text.split(" - ")[0]
            
            # Confirm installation
            confirm = messagebox.askyesno(
                "Confirm Installation",
                f"Install {model_id}?\n\nThis may take several minutes depending on model size and your internet connection."
            )
            
            if confirm:
                dialog.destroy()
                self.install_model(model_id)
        
        install_btn = tk.Button(
            btn_frame,
            text="Install Selected",
            command=on_install,
            bg="#223b22",
            fg=COLOR_BTN_FG,
            activebackground="#2f5a2f",
            font=FONT_BTN,
            padx=20,
            pady=10
        )
        install_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#3b2222",
            fg=COLOR_BTN_FG,
            activebackground="#5a2f2f",
            font=FONT_BTN,
            padx=20,
            pady=10
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def install_model(self, model_id):
        """Install a model using Ollama API with progress tracking"""
        self.append_system(f"Starting installation of {model_id}...")
        
        # Create progress dialog
        progress_dialog = tk.Toplevel(self)
        progress_dialog.title("Installing Model")
        progress_dialog.geometry("500x200")
        progress_dialog.configure(bg=COLOR_BG_FRAME)
        progress_dialog.transient(self)
        progress_dialog.grab_set()
        
        status_label = tk.Label(
            progress_dialog,
            text=f"Installing {model_id}...",
            font=("Sans", 12),
            bg=COLOR_BG_FRAME,
            fg=COLOR_TEXT_INPUT
        )
        status_label.pack(pady=20)
        
        progress_text = tk.Text(
            progress_dialog,
            height=6,
            width=60,
            bg=COLOR_BG_CHAT,
            fg=COLOR_TEXT_INPUT,
            font=("Monospace", 9)
        )
        progress_text.pack(padx=20, pady=10)
        
        def update_progress(message):
            progress_text.insert(tk.END, message + "\n")
            progress_text.see(tk.END)
            progress_dialog.update()
        
        def do_install():
            try:
                url = "http://localhost:11434/api/pull"
                payload = {"name": model_id, "stream": True}
                
                with requests.post(url, json=payload, stream=True, timeout=3600) as response:
                    response.raise_for_status()
                    
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line.decode('utf-8'))
                            
                            if 'status' in data:
                                status = data['status']
                                
                                if 'total' in data and 'completed' in data:
                                    total = data['total']
                                    completed = data['completed']
                                    percent = (completed / total * 100) if total > 0 else 0
                                    update_progress(f"{status}: {percent:.1f}%")
                                else:
                                    update_progress(status)
                            
                            if data.get('status') == 'success':
                                update_progress("✓ Installation complete!")
                                self.append_system(f"Successfully installed {model_id} - now available in model selector")
                                progress_dialog.after(2000, progress_dialog.destroy)
                                return
                
            except Exception as e:
                update_progress(f"✗ Error: {str(e)}")
                self.append_system(f"Failed to install {model_id}: {str(e)}")
                messagebox.showerror("Installation Failed", f"Error installing {model_id}:\n{str(e)}")
        
        # Run installation in a thread to avoid blocking UI
        import threading
        thread = threading.Thread(target=do_install, daemon=True)
        thread.start()

    # ---------- Connection Management ----------
    def toggle_connection(self):
        if self.connected:
            self.disconnect_model()
        else:
            self.connect_model()

    def toggle_web_search(self):
        self.web_search_enabled = not self.web_search_enabled
        status = "ON" if self.web_search_enabled else "OFF"
        self.search_toggle_btn.configure(text=f"🌐 Internet: {status}")
        self.append_system(f"Internet search {'enabled' if self.web_search_enabled else 'disabled'}")

    def connect_model(self):
        selected = self.model_var.get()
        # Extract model ID from "DisplayName (model:id)" format
        if '(' in selected and ')' in selected:
            self.current_model = selected.split('(')[1].split(')')[0]
        else:
            self.current_model = selected
            
        self.connected = True
        
        display_name = self.model_display_names.get(self.current_model, self.current_model)
        self.title(f"Ollama Chat – {display_name}")
        self.connect_btn.configure(text="Disconnect", bg="#3b2222", activebackground="#5a2f2f")
        self.status_label.configure(text=f"🟢 Connected to {display_name}", fg="#4CAF50")
        self.model_btn.configure(state="disabled")
        
        # Update fancy model name label
        self.model_name_label.configure(text=display_name)
        
        self._set_chat_controls(True)
        self.append_system(f"Connected to {display_name}")
        self.user_input.focus_set()

    def disconnect_model(self):
        self.connected = False
        self.current_model = None
        self.messages = []
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.update_token_count()
        
        self.title("Ollama Chat – Model Selector")
        self.connect_btn.configure(text="Connect", bg="#223b22", activebackground="#2f5a2f")
        self.status_label.configure(text="⚫ Disconnected", fg="#888888")
        self.model_btn.configure(state="normal")
        
        # Clear fancy model name label
        self.model_name_label.configure(text="")
        
        self._set_chat_controls(False)
        self.append_system("Disconnected. Select a model to reconnect.")

    # ---------- Web Search ----------
    def needs_web_search(self, query):
        query_lower = query.lower()
        
        current_keywords = [
            'today', 'now', 'current', 'latest', 'recent', 
            'price', 'trading', 'news', 'forecast', 'tomorrow',
            'this week', 'this month', 'what is', 'what are'
        ]
        
        current_topics = [
            'crypto', 'bitcoin', 'ethereum', 'stock', 'market',
            'weather', 'sports', 'election', 'covid'
        ]
        
        has_current_keyword = any(kw in query_lower for kw in current_keywords)
        has_current_topic = any(topic in query_lower for topic in current_topics)
        
        return has_current_keyword or has_current_topic

    def is_crypto_price_query(self, query):
        query_lower = query.lower()
        
        crypto_names = [
            'bitcoin', 'btc', 'ethereum', 'eth', 'dogecoin', 'doge',
            'cardano', 'ada', 'solana', 'sol', 'ripple', 'xrp',
            'polkadot', 'dot', 'litecoin', 'ltc', 'chainlink', 'link'
        ]
        
        price_keywords = ['price', 'trading', 'worth', 'value', 'cost', 'at']
        
        has_crypto = any(crypto in query_lower for crypto in crypto_names)
        has_price_keyword = any(kw in query_lower for kw in price_keywords)
        
        return has_crypto and has_price_keyword

    def is_crypto_news_query(self, query):
        query_lower = query.lower()
        
        crypto_keywords = ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'altcoin', 'defi', 'nft', 
                          'btc', 'eth', 'solana', 'dogecoin', 'cardano', 'ripple', 'xrp']
        news_keywords = ['news', 'headlines', 'latest', 'updates', 'happening', 'developments']
        
        has_crypto = any(kw in query_lower for kw in crypto_keywords)
        has_news = any(kw in query_lower for kw in news_keywords)
        
        return has_crypto and has_news

    def get_crypto_prices(self, query):
        try:
            query_lower = query.lower()
            
            crypto_map = {
                'bitcoin': 'bitcoin', 'btc': 'bitcoin',
                'ethereum': 'ethereum', 'eth': 'ethereum',
                'dogecoin': 'dogecoin', 'doge': 'dogecoin',
                'cardano': 'cardano', 'ada': 'cardano',
                'solana': 'solana', 'sol': 'solana',
                'ripple': 'ripple', 'xrp': 'ripple',
                'polkadot': 'polkadot', 'dot': 'polkadot',
                'litecoin': 'litecoin', 'ltc': 'litecoin',
                'chainlink': 'chainlink', 'link': 'chainlink'
            }
            
            mentioned_cryptos = []
            for name, coin_id in crypto_map.items():
                if name in query_lower and coin_id not in mentioned_cryptos:
                    mentioned_cryptos.append(coin_id)
            
            if not mentioned_cryptos:
                mentioned_cryptos = ['bitcoin']
            
            ids = ','.join(mentioned_cryptos[:5])
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
            
            self.append_search(f"💰 Fetching crypto prices from CoinGecko...")
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None
            
            result = "Real-time cryptocurrency prices (CoinGecko API):\n\n"
            for coin_id in mentioned_cryptos:
                if coin_id in data:
                    price = data[coin_id]['usd']
                    change = data[coin_id].get('usd_24h_change', 0)
                    change_symbol = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                    result += f"{coin_id.capitalize()}: ${price:,.2f} USD {change_symbol} ({change:+.2f}% 24h)\n"
            
            result += f"\nTimestamp: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n"
            
            self.append_search(f"✓ Retrieved prices for {len(data)} cryptocurrencies")
            return result
            
        except Exception as e:
            self.append_search(f"✗ CoinGecko API error: {str(e)}")
            return None

    def is_realtime_query(self, query):
        """Detect if query is asking for current/real-time information"""
        query_lower = query.lower()
        
        # Skip if it's a crypto query (those have their own handlers)
        crypto_keywords = ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'btc', 'eth', 
                          'coin', 'price', 'solana', 'dogecoin', 'cardano', 'ripple', 'xrp']
        if any(kw in query_lower for kw in crypto_keywords):
            return False
        
        # Time-sensitive keywords that indicate "right now" news
        realtime_keywords = [
            'today', 'right now', 'currently', 'current', 
            'happening now', 'just happened', 'breaking',
            'this morning', 'this afternoon', 'this evening', 'tonight'
        ]
        
        # Only trigger if has strong time indicator
        return any(kw in query_lower for kw in realtime_keywords)

    def get_crypto_news(self, max_articles=8):
        try:
            url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
            
            self.append_search(f"📰 Fetching crypto news from CryptoCompare...")
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'Data' not in data:
                self.append_search(f"⚠️ Unexpected API response structure")
                return None
            
            articles = data['Data'][:max_articles]
            
            if not articles:
                self.append_search(f"⚠️ No articles returned from API")
                return None
            
            current_date = datetime.now().strftime('%B %d, %Y')
            result = f"=== LATEST CRYPTOCURRENCY NEWS ({current_date}) ===\n\n"
            result += f"Retrieved {len(articles)} recent articles from trusted crypto news sources:\n\n"
            
            for i, article in enumerate(articles, 1):
                title = article.get('title', 'No title')
                body = article.get('body', '')
                # Get more content for better context
                body_preview = body[:500] + "..." if len(body) > 500 else body
                source = article.get('source', 'Unknown')
                article_url = article.get('url', '')
                published_timestamp = article.get('published_on', 0)
                
                if published_timestamp:
                    published = datetime.fromtimestamp(published_timestamp)
                    time_ago = self._time_ago(published)
                else:
                    time_ago = "unknown time"
                
                result += f"ARTICLE {i}:\n"
                result += f"Title: {title}\n"
                result += f"Source: {source}\n"
                result += f"Published: {time_ago}\n"
                result += f"Summary: {body_preview}\n"
                if article_url:
                    result += f"URL: {article_url}\n"
                result += f"{'-' * 60}\n\n"
            
            self.append_search(f"✓ Retrieved {len(articles)} news articles")
            return result
            
        except Exception as e:
            self.append_search(f"✗ Error fetching news: {str(e)}")
            return None

    def _time_ago(self, timestamp):
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"

    def search_web(self, query, max_results=8):
        try:
            self.append_search(f"🔍 Searching the web for: {query}")
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            
            if not results:
                self.append_search("⚠ No results found - trying simpler query...")
                simple_query = ' '.join(query.split()[:3])
                with DDGS() as ddgs:
                    results = list(ddgs.text(simple_query, max_results=max_results))
            
            if not results:
                self.append_search("✗ Search failed - model will answer without current data")
                return "SEARCH_FAILED"
            
            formatted_results = "=== WEB SEARCH RESULTS ===\n\n"
            formatted_results += f"Found {len(results)} relevant sources for: \"{query}\"\n\n"
            
            for i, result in enumerate(results, 1):
                formatted_results += f"RESULT {i}:\n"
                formatted_results += f"Title: {result['title']}\n"
                formatted_results += f"Content: {result['body']}\n"
                formatted_results += f"Source: {result['href']}\n"
                formatted_results += f"{'-' * 60}\n\n"
            
            self.append_search(f"✓ Found {len(results)} results")
            return formatted_results
            
        except Exception as e:
            self.append_search(f"✗ Search error: {str(e)}")
            return "SEARCH_FAILED"

    # ---------- Key handling ----------
    def on_enter_key(self, event):
        if not self.connected:
            return "break"
        if event.state & 0x0001:
            return
        self.on_submit()
        return "break"

    # ---------- Chat helpers ----------
    def _append(self, text, tag):
        self.chat_log.configure(state="normal")
        self.chat_log.insert(tk.END, text, tag)
        self.chat_log.see(tk.END)
        self.chat_log.configure(state="disabled")
        self.update_idletasks()

    def append_system(self, text):
        ts = datetime.now().strftime("%H:%M:%S")
        self._append(f"[{ts}] {text}\n", "system")

    def append_search(self, text):
        self._append(f"    {text}\n", "search")

    def append_user(self, text):
        self._append(f"\nYou: {text}\n", "user")

    def append_assistant_start(self):
        display_name = self.model_display_names.get(self.current_model, self.current_model)
        self._append(f"{display_name}: ", "assistant")

    def append_assistant_chunk(self, text):
        self._append(text, "assistant")
    
    def estimate_tokens(self, text):
        """Estimate token count (roughly 4 characters per token for English)"""
        # Simple estimation: ~4 chars per token, or word count * 1.3
        char_estimate = len(text) / 4
        word_estimate = len(text.split()) * 1.3
        return int((char_estimate + word_estimate) / 2)
    
    def update_token_count(self):
        """Update the token counter display with input/output breakdown"""
        self.token_label.configure(
            text=f"Tokens: {self.total_tokens:,} (In: {self.input_tokens:,} | Out: {self.output_tokens:,})",
            fg="#64B5F6" if self.total_tokens > 0 else "#888888"
        )

    # ---------- Actions ----------
    def on_submit(self):
        if not self.connected:
            messagebox.showwarning("Not Connected", "Please connect to a model first.")
            return

        prompt = self.user_input.get("1.0", tk.END).strip()
        if not prompt:
            return

        self.user_input.delete("1.0", tk.END)
        self.append_user(prompt)

        search_context = None
        if self.web_search_enabled and self.needs_web_search(prompt):
            if self.is_crypto_news_query(prompt):
                search_context = self.get_crypto_news()
            elif self.is_crypto_price_query(prompt):
                search_context = self.get_crypto_prices(prompt)
            else:
                # Use DuckDuckGo for all other searches
                # For real-time queries, enhance with time keywords
                if self.is_realtime_query(prompt):
                    enhanced_query = f"{prompt} today latest news"
                    search_context = self.search_web(enhanced_query)
                else:
                    search_context = self.search_web(prompt)

        current_date = datetime.now().strftime("%B %d, %Y")
        
        if search_context and search_context != "SEARCH_FAILED":
            enhanced_prompt = f"""Today's date is {current_date}.

{search_context}

User's Question: {prompt}

INSTRUCTIONS: Using the search results above, provide a comprehensive and detailed answer to the user's question. Include:
- Key information from multiple sources
- Specific details, numbers, and facts when available
- Different perspectives if sources disagree
- Context and explanations to help the user understand

Be thorough and informative. Synthesize the information rather than just listing it. If the search results don't fully answer the question, clearly state what information is missing."""
            self.messages.append({"role": "user", "content": enhanced_prompt})
        elif search_context == "SEARCH_FAILED":
            enhanced_prompt = f"Today's date is {current_date}.\n\nUser question: {prompt}\n\nIMPORTANT: Web search failed. You do not have access to current information. Please inform the user that you cannot provide current data for this query and that they should try again or search manually."
            self.messages.append({"role": "user", "content": enhanced_prompt})
        else:
            self.messages.append({"role": "user", "content": prompt})

        self._set_chat_controls(False)

        try:
            self.append_assistant_start()
            reply = self.stream_ollama_chat(self.messages)
            self.messages.append({"role": "assistant", "content": reply})
            self._append("\n", "assistant")
            
            # Update token count
            user_tokens = self.estimate_tokens(prompt)
            assistant_tokens = self.estimate_tokens(reply)
            self.input_tokens += user_tokens
            self.output_tokens += assistant_tokens
            self.total_tokens += user_tokens + assistant_tokens
            self.update_token_count()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self._set_chat_controls(True)
            self.user_input.focus_set()

    def _set_chat_controls(self, enabled):
        state = "normal" if enabled else "disabled"
        self.submit_btn.configure(state=state)
        self.clear_btn.configure(state=state)
        if enabled:
            self.user_input.configure(bg=COLOR_BG_INPUT, fg=COLOR_TEXT_INPUT)
        else:
            self.user_input.configure(bg="#0a0a0a", fg="#444444")

    def stream_ollama_chat(self, messages):
        payload = {
            "model": self.current_model,
            "messages": messages,
            "stream": True
        }

        response_text = ""

        with requests.post(
            OLLAMA_CHAT_URL,
            json=payload,
            stream=True,
            timeout=600
        ) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue

                data = json.loads(line.decode("utf-8"))
                if "message" in data and "content" in data["message"]:
                    chunk = data["message"]["content"]
                    response_text += chunk
                    self.append_assistant_chunk(chunk)

                if data.get("done"):
                    break

        return response_text.strip()

    def on_clear(self):
        if not self.connected:
            return
        self.messages = []
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.update_token_count()
        self.chat_log.configure(state="normal")
        self.chat_log.delete("1.0", tk.END)
        self.chat_log.configure(state="disabled")
        self.append_system("Chat cleared. Memory reset.")
    
    def on_save_chat(self):
        """Save current conversation to a file"""
        if not self.messages:
            messagebox.showinfo("Nothing to Save", "No conversation to save yet.")
            return
        
        from tkinter import filedialog
        
        # Default filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"chat_{timestamp}.json"
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=default_name,
            filetypes=[
                ("JSON files", "*.json"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            title="Save Conversation"
        )
        
        if not filepath:
            return
        
        try:
            # Prepare data to save
            save_data = {
                "timestamp": datetime.now().isoformat(),
                "model": self.current_model,
                "total_tokens": self.total_tokens,
                "messages": self.messages
            }
            
            # Save as JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            self.append_system(f"Conversation saved to {filepath}")
            messagebox.showinfo("Saved", f"Conversation saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Save Failed", f"Failed to save conversation:\n{str(e)}")
    
    def on_load_chat(self):
        """Load a conversation from a file"""
        from tkinter import filedialog
        
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("JSON files", "*.json"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            title="Load Conversation"
        )
        
        if not filepath:
            return
        
        try:
            # Load the file
            with open(filepath, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Validate data
            if "messages" not in save_data:
                messagebox.showerror("Invalid File", "This file doesn't contain a valid conversation.")
                return
            
            # Check if we need to connect to a model first
            if not self.connected:
                model_name = save_data.get("model", "unknown")
                messagebox.showinfo(
                    "Connect First",
                    f"This conversation was with {model_name}.\nPlease connect to a model first."
                )
                return
            
            # Clear current chat
            self.messages = []
            self.chat_log.configure(state="normal")
            self.chat_log.delete("1.0", tk.END)
            self.chat_log.configure(state="disabled")
            
            # Load messages
            self.messages = save_data["messages"]
            
            # Restore token count if available
            if "total_tokens" in save_data:
                self.total_tokens = save_data["total_tokens"]
                self.update_token_count()
            
            # Display the conversation
            self.append_system(f"Loaded conversation from {filepath}")
            
            for msg in self.messages:
                role = msg.get("role", "")
                content = msg.get("content", "")
                
                if role == "user":
                    self.append_user(content)
                elif role == "assistant":
                    display_name = self.model_display_names.get(self.current_model, self.current_model)
                    self._append(f"{display_name}: {content}\n", "assistant")
            
            messagebox.showinfo("Loaded", "Conversation loaded successfully!")
            
        except json.JSONDecodeError:
            messagebox.showerror("Invalid File", "This file doesn't contain valid JSON.")
        except Exception as e:
            messagebox.showerror("Load Failed", f"Failed to load conversation:\n{str(e)}")

    def on_exit(self):
        self.destroy()


if __name__ == "__main__":
    OllamaChatUI().mainloop()