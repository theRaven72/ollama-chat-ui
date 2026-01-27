# How to Change Model Display Names

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
