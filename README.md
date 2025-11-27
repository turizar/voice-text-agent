# 🎤 Complete Voice - Text Agent

A powerful multilingual voice agent application that provides seamless **Text-to-Speech** and **Speech-to-Text** functionality with automatic language detection for Spanish and English.

## ✨ Features

### 📝 Text-to-Speech (TTS)
- **Multilingual Support**: Automatically detects and converts text in Spanish and English
- **High-Quality Audio**: Uses Tacotron2-DDC models for natural-sounding speech
- **Speed Control**: Adjustable speech rate (0.5x to 2.0x)
- **Automatic Language Detection**: Smart detection based on text content

### 🎤 Speech-to-Text (STT)
- **Browser-Based Recording**: Record audio directly from your browser (works in cloud deployments!)
- **Simple Click-to-Record**: Click microphone button to start, click again to stop
- **Audio File Upload**: Upload pre-recorded audio files (WAV, MP3, M4A, OGG)
- **Google Speech Recognition**: High-accuracy transcription
- **Multilingual Recognition**: Supports Spanish and English audio
- **Real-time Processing**: Immediate transcription results

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (required for TTS library)
- Modern web browser with microphone access
- Internet connection (for Google Speech Recognition and TTS model downloads)

### Installation

1. **Clone or download the project**
```bash
git clone https://github.com/tu-usuario/voice-text-agent.git
cd voice-text-agent
```

2. **Create and activate virtual environment**
```bash
python3.11 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate      # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

**Note:** No additional system dependencies needed! The app uses browser-based recording that works on any platform.

### Running the Application

```bash
streamlit run voice_text_agent.py
```

The application will be available at: **http://localhost:8501** (or the port shown in the terminal)

## ☁️ Cloud Deployment

This application is fully compatible with **Streamlit Cloud** and other cloud platforms:

- ✅ **Browser-based recording** works perfectly in cloud deployments
- ✅ **Text-to-Speech** functions without any server-side audio dependencies
- ✅ **File upload** works on any platform
- ✅ No special server configuration needed

See `DEPLOYMENT.md` for detailed deployment instructions to Streamlit Cloud.

## 📖 How to Use

### Text-to-Speech
1. Navigate to the **"📝 Text to Speech"** tab
2. Enter your text in the text area (supports both Spanish and English)
3. Adjust the speed slider (0.5x to 2.0x) if desired
4. Click **"🎵 Generate Audio"**
5. The system will:
   - Automatically detect the language (Spanish/English) using word-frequency analysis
   - Show the detected language
   - Generate high-quality audio using the appropriate TTS model
   - Display the audio player with file size information

### Speech-to-Text
1. Navigate to the **"🎤 Speech to Text"** tab
2. Choose your recording method:
   - **Browser Recording**: 
     - Click the microphone button (🎤) to start recording
     - Speak clearly into your microphone
     - Click the microphone button again to stop recording
     - The recorded audio will appear automatically
   - **File Upload**: Upload a pre-recorded audio file (WAV, MP3, M4A, OGG)
3. Once you have audio (recorded or uploaded):
   - Click **"🔄 Transcribe Audio"** to convert speech to text
   - The system will automatically try Spanish first, then English if needed
4. Review the transcribed text in the results area
5. Use **"🗑️ Clear Recording"** to start over if needed

**Note:** Your browser will ask for microphone permission the first time you record.

## 🛠️ Technical Details

### Models Used
- **TTS Models**:
  - English: `tts_models/en/ljspeech/tacotron2-DDC`
  - Spanish: `tts_models/es/mai/tacotron2-DDC` (with fallback to `tts_models/es/css10/vits`)
- **STT Engine**: Google Speech Recognition API

### Audio Specifications
- **Recording Sample Rate**: 44,100 Hz
- **Recording Format**: 16-bit PCM, Mono channel
- **Output Format**: WAV format
- **Recording Component**: Browser-based using `audio-recorder-streamlit`
- **Transcription**: Supports WAV, MP3, M4A, and OGG file formats

### Language Detection
The application uses a word-frequency algorithm to automatically detect whether input text is in Spanish or English. It compares the frequency of common Spanish and English words in the text to determine the language, ensuring optimal TTS model selection.

### Speech Recognition Process
The transcription process uses Google Speech Recognition API with intelligent language detection:
1. First attempts transcription in Spanish (es-ES)
2. If that fails, tries English (en-US)
3. As a final fallback, attempts without specifying a language
This ensures the best possible transcription accuracy for multilingual content.

## 📋 Requirements

```
torch>=2.0.0
streamlit>=1.28.0
soundfile>=0.12.0
numpy>=1.21.0
TTS>=0.22.0
SpeechRecognition>=3.10.0
audio-recorder-streamlit>=0.0.8
```

**Note:** Python 3.10+ is required. See `requirements.txt` for complete list.

## 🔧 Troubleshooting

### Common Issues

**"Browser-based audio recorder not available"**
- Make sure `audio-recorder-streamlit` is installed: `pip install audio-recorder-streamlit`
- Refresh the page and try again
- Check that your browser supports microphone access

**"Could not load TTS models"**
- Ensure stable internet connection for model download (first time only)
- Check available disk space (models are ~500MB each)
- Models are downloaded automatically on first use

**"Recognition service error"**
- Verify internet connection (required for Google Speech Recognition)
- Check Google Speech Recognition service status
- Try again after a few moments
- The system automatically tries Spanish first, then English - wait for all attempts to complete

**"Could not understand the audio"**
- Speak more clearly and slowly
- Reduce background noise
- Ensure microphone is working properly
- Try recording again with better audio quality

**"Microphone permission denied"**
- Allow microphone access when your browser prompts you
- Check browser settings to ensure microphone permissions are enabled
- Some browsers require HTTPS for microphone access (works fine on Streamlit Cloud)

## 🌟 Tips for Best Results

### Text-to-Speech
- Use clear, well-structured text
- Avoid special characters or symbols
- Use punctuation for natural pauses
- Keep text length reasonable for faster processing

### Speech-to-Text
- Speak clearly and at moderate pace
- Minimize background noise
- Keep microphone close to your mouth
- Use short phrases for better accuracy
- Record in a quiet environment
- The system automatically tries multiple language options for best results
- You can edit the transcribed text in the text area if needed

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Made with ❤️ for seamless voice interaction**
