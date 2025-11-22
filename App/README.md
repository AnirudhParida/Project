# OS Agent - Voice/Text Controlled System Assistant

A fully functional AI agent that can control your Windows laptop through voice or text commands.

## Features

✅ **Voice Control** - Speak naturally to control your system  
✅ **Text Mode** - Type commands if you prefer text input  
✅ **Smart Intent Parsing** - Uses Google Gemini to understand natural language  
✅ **OS Operations** - Open apps, create files, search web, take screenshots, and more  
✅ **Safety First** - Confirmation required for destructive actions  

## Capabilities

- **Application Control**: Open/close applications (Notepad, Calculator, Chrome, etc.)
- **File Operations**: Create files and folders
- **Web Actions**: Search Google, open URLs
- **System Info**: Get system information, take screenshots
- **Shell Commands**: Run PowerShell commands (with confirmation)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Installing `pyaudio` on Windows may require additional steps:
- Download the appropriate `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Install with: `pip install path/to/PyAudio‑file.whl`

### 2. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a free API key
3. Copy `.env.example` to `.env`
4. Add your key to `.env`:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

### 3. Test Your Setup (Optional)

Test individual components:

```bash
# Test speech engine
python speech_engine.py

# Test brain (LLM parsing)
python brain.py
```

## Usage

### Voice Mode (Default)

```bash
python main.py
```

Speak your commands naturally:
- "Open notepad"
- "Search for Python tutorials"
- "Create a file called test.txt"
- "Take a screenshot"
- "What's my system information?"

Say **"exit"** or **"quit"** to stop.

### Text Mode

```bash
python main.py --mode text
```

Type your commands and press Enter.

## Example Commands

| Command | Action |
|---------|--------|
| "Open calculator" | Opens Windows Calculator |
| "Search for weather today" | Opens Google search |
| "Create a folder called MyDocs" | Creates a new folder |
| "Open Chrome" | Launches Google Chrome |
| "Take a screenshot named demo.png" | Saves screenshot |
| "Get system info" | Displays OS details |

## Safety Features

⚠️ **Destructive actions require confirmation:**
- Deleting files/folders
- Running shell commands

The agent will respond with a confirmation message instead of executing immediately.

## Architecture

```
┌─────────────────────────────────────────┐
│           User Input                     │
│     (Voice / Text)                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Speech Engine (speech_engine.py)   │
│  - Listener: STT with SpeechRecognition │
│  - Speaker: TTS with pyttsx3            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Brain (brain.py)                │
│  - Uses Google Gemini                   │
│  - Converts natural language → JSON     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Action Executor (executor.py)      │
│  - Executes OS-level operations         │
│  - File I/O, App launching, Web, etc.   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│           Response Output                │
│     (Voice / Text)                       │
└─────────────────────────────────────────┘
```

## Troubleshooting

### Microphone Issues
- Make sure your microphone is connected and set as default
- Run `speech_engine.py` to test microphone calibration

### PyAudio Installation Fails
- Windows users: Download the `.whl` file from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Choose the correct Python version and architecture (e.g., `cp311` for Python 3.11, `amd64` for 64-bit)

### API Key Errors
- Ensure `.env` file exists in the project root
- Verify your API key is valid at [Google AI Studio](https://makersuite.google.com/)

## Future Enhancements

- [ ] Add Whisper for offline speech recognition
- [ ] Implement conversation history
- [ ] Add clipboard operations
- [ ] Support for macOS and Linux
- [ ] GUI interface with system tray icon
- [ ] Custom wake word detection

## License

MIT License - Feel free to modify and extend!

## Contributing

Contributions are welcome! Some ideas:
- Add more OS operations
- Improve error handling
- Add unit tests
- Create GUI interface

---

**Made with ❤️ for seamless OS control**
