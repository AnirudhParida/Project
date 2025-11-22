# Quick Start Guide

## Installation Fixed! ✅

All dependencies are now installed successfully. Here's what to do next:

## Step 1: Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key

## Step 2: Add Your API Key

Open the `.env` file in the Project folder and replace `your_api_key_here` with your actual API key:

```
GEMINI_API_KEY=AIzaSyD...your_actual_key_here
```

## Step 3: Run the Agent

### Option A: Text Mode (Recommended for first test)

```bash
.\run_text.bat
```

Or:
```bash
.\venv\Scripts\python.exe main.py --mode text
```

**Test commands:**
- Type: `hello`
- Type: `open notepad`
- Type: `search for Python tutorials`
- Type: `exit`

### Option B: Voice Mode

```bash
.\run_voice.bat
```

Or:
```bash
.\venv\Scripts\python.exe main.py
```

**Speak naturally:**
- "Open calculator"
- "Create a file called test.txt"
- "Exit"

## Troubleshooting

### If you see "API key not found" error:
- Make sure `.env` file exists in the Project folder
- Verify your API key is correct (no extra spaces)
- The key should start with `AIza`

### If microphone doesn't work (voice mode):
- Check Windows microphone permissions
- Ensure microphone is set as default recording device
- Try text mode instead

## What Changed

I fixed the installation issue by updating `requirements.txt`:
- **Before:** Strict Pillow 10.1.0 (required building from source - failed)
- **After:** Flexible Pillow >=10.0.0 (uses pre-built wheels - success)

All packages installed:
✅ SpeechRecognition 3.10.0
✅ pyttsx3 2.90
✅ PyAudio 0.2.14
✅ google-generativeai 0.3.2
✅ pyautogui 0.9.54
✅ Pillow 12.0.0
✅ comtypes 1.4.13

**You're ready to go! Just add your API key and run the agent.** 🚀
