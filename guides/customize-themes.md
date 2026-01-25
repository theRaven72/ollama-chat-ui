# How to Add Custom Themes

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
