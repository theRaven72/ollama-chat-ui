# How to Edit Your Modelfile (Customize AI Personality)

Make your AI models remember your preferences, coding style, or act with a specific personality!

## What is a Modelfile?

A Modelfile is like a configuration file that tells your AI model:
- How to behave
- What to remember about you
- How to respond (formal, casual, technical, etc.)
- Default settings (temperature, context length, etc.)

## Why Edit It?

**Examples of what you can do:**
- "Always write code comments"
- "Use British English spelling"
- "Be concise and direct"
- "Remember I'm a Python developer learning Rust"
- "Act as a creative writing assistant"
- "Use emojis in responses"

## Step-by-Step Guide

### Step 1: Create a Modelfile

Create a new text file called `Modelfile` (no extension):

```bash
nano ~/Modelfile
```

Or use any text editor.

### Step 2: Write Your Modelfile

Here's a template:

```
FROM gemma3:12b

# Set the temperature (creativity level: 0.0 = focused, 1.0 = creative)
PARAMETER temperature 0.7

# Set context window (how much conversation it remembers)
PARAMETER num_ctx 4096

# System prompt - this is where you customize personality!
SYSTEM """
You are Claire, a helpful AI assistant.

IMPORTANT INSTRUCTIONS:
- Always be friendly and encouraging
- Use clear, concise language
- When writing code, always include comments
- Prefer Python examples when possible
- If unsure, ask clarifying questions

ABOUT THE USER:
- User is a Linux enthusiast (Pop!_OS user)
- Interested in AI and machine learning
- Learning Python and web development
- Prefers practical examples over theory
"""
```

### Step 3: Create Your Custom Model

```bash
ollama create claire-custom -f ~/Modelfile
```

This creates a new model called `claire-custom` based on your Modelfile.

### Step 4: Use Your Custom Model

The new model will appear in the Ollama Chat UI model dropdown as `claire-custom:latest`.

1. Open Ollama Chat UI
2. Select `claire-custom:latest` from Model dropdown
3. Click Connect
4. Chat!

## Modelfile Options Explained

### FROM
Which base model to use:
```
FROM gemma3:12b
FROM llama3.1:8b
FROM qwen2.5:14b
```

### PARAMETER temperature
Creativity level (0.0 to 2.0):
- `0.0` - Very focused, deterministic, factual
- `0.7` - Balanced (default)
- `1.0` - More creative and varied
- `1.5+` - Very creative, sometimes unpredictable

### PARAMETER num_ctx
Context window size (how much conversation it remembers):
- `2048` - Short memory (faster)
- `4096` - Standard
- `8192` - Long memory
- `32768` - Very long memory (if model supports it)

### PARAMETER top_p
Nucleus sampling (0.0 to 1.0):
- `0.9` - More focused responses
- `0.95` - Balanced (default)

### PARAMETER top_k
Limits vocabulary choices:
- `40` - Default
- Lower = more focused, Higher = more diverse

### SYSTEM
The personality and instructions (most important part!):
```
SYSTEM """
Your instructions here...
"""
```

## Real-World Examples

### Example 1: Python Coding Assistant

```
FROM gemma3:12b
PARAMETER temperature 0.3
PARAMETER num_ctx 8192

SYSTEM """
You are a Python programming expert.

RULES:
- Always write clean, PEP 8 compliant code
- Include docstrings for functions
- Add inline comments for complex logic
- Suggest best practices
- Test code before suggesting it

When helping debug:
1. Ask for the error message
2. Explain what is wrong
3. Provide the fix
4. Explain why it works
"""
```

### Example 2: Creative Writing Partner

```
FROM llama3.1:8b
PARAMETER temperature 1.2
PARAMETER num_ctx 4096

SYSTEM """
You are a creative writing assistant specializing in science fiction.

STYLE:
- Vivid descriptions
- Character-driven narratives
- Focus on world-building details
- Suggest plot twists
- Ask thought-provoking questions

Always encourage creativity and offer multiple options.
"""
```

### Example 3: Linux System Admin Helper

```
FROM qwen2.5:14b
PARAMETER temperature 0.5

SYSTEM """
You are a Linux system administration expert.

PREFERENCES:
- Provide command-line solutions first
- Explain what each command does
- Warn about dangerous commands
- Suggest safer alternatives
- Include examples

USER SYSTEM: Pop!_OS 22.04 (Ubuntu-based)
- Use apt for package management
- GNOME desktop environment
"""
```

### Example 4: Casual Friendly Chat

```
FROM gemma3:27b
PARAMETER temperature 0.9

SYSTEM """
You are a friendly, casual AI companion.

PERSONALITY:
- Use casual language (hey, cool, awesome)
- Occasionally use emojis
- Be encouraging and positive
- Share interesting facts
- Ask follow-up questions to keep conversation going

Keep responses conversational and fun!
"""
```

## Managing Custom Models

### List all models
```bash
ollama list
```

### Delete a custom model
```bash
ollama rm claire-custom
```

### Update a custom model
1. Edit your Modelfile
2. Run create command again (overwrites):
```bash
ollama create claire-custom -f ~/Modelfile
```

### Copy/backup your Modelfile
```bash
cp ~/Modelfile ~/Modelfile.backup
```

## Tips & Best Practices

1. **Start simple** - Begin with a basic SYSTEM prompt and add more later

2. **Be specific** - "Use Python 3.10+ features" is better than "use Python"

3. **Test and iterate** - Create the model, test it, refine the Modelfile

4. **Save your Modelfiles** - Keep them organized:
   ```
   ~/Modelfiles/
   ├── claire-coding.modelfile
   ├── claire-creative.modelfile
   └── claire-research.modelfile
   ```

5. **Temperature guide**:
   - Coding/Math: 0.1-0.3
   - General chat: 0.7-0.9
   - Creative writing: 1.0-1.3

6. **Context length trade-off**: Larger = more memory but slower

7. **Version your models**: `claire-coding-v1`, `claire-coding-v2`

## Troubleshooting

### Model not appearing in UI
Restart the Ollama Chat UI after creating a new model.

### "Model not found" error
Make sure you spelled the model name correctly:
```bash
ollama list  # Check exact name
```

### Model behaving oddly
- Check your SYSTEM prompt for contradictions
- Lower temperature for more predictable behavior
- Make instructions clearer and more specific

### Model forgot instructions mid-conversation
- Increase `num_ctx` (context window)
- Restate important rules in your prompts

## Advanced: Multiple Personalities

Create different versions of the same base model:

```bash
# Coding assistant
ollama create claire-code -f ~/Modelfiles/coding.modelfile

# Writing assistant  
ollama create claire-writer -f ~/Modelfiles/writing.modelfile

# General chat
ollama create claire-chat -f ~/Modelfiles/chat.modelfile
```

Then give them custom names in the UI (see Change_Model_Names.md)!

## Resources

- Official Ollama Modelfile docs: https://github.com/ollama/ollama/blob/main/docs/modelfile.md
- Example Modelfiles: https://github.com/ollama/ollama/tree/main/examples

---

**Customize your AI to fit YOUR needs!** 🎨
