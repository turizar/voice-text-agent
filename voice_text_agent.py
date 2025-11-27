import streamlit as st
import torch
from TTS.api import TTS
import tempfile
import os

# Try to import audio libraries
try:
    import speech_recognition as sr
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    st.warning("⚠️ For full audio functionality, install: pip install SpeechRecognition")

# Try to import audio recorder for browser-based recording
try:
    from audio_recorder_streamlit import audio_recorder
    RECORDER_AVAILABLE = True
except ImportError:
    RECORDER_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Complete Voice - Text Agent",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 Complete Voice - Text Agent")
st.markdown("---")

# Function to initialize session variables
def initialize_session_state():
    """Initialize necessary session variables"""
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = None
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = ""

# Initialize session variables
initialize_session_state()

# Function to detect language
def detect_language(text):
    """Detects if the text is in Spanish or English"""
    # Common Spanish words
    spanish_words = ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como', 'más', 'pero', 'sus', 'me', 'ya', 'todo', 'esta', 'muy', 'sin', 'sobre', 'también', 'después', 'vida', 'años', 'año', 'vez', 'hacer', 'cada', 'donde', 'quien', 'durante', 'mientras', 'entre', 'hasta', 'desde', 'hacia', 'bajo', 'sobre', 'contra', 'según', 'mediante', 'excepto', 'salvo', 'menos', 'más', 'tanto', 'cuanto', 'cuando', 'donde', 'como', 'porque', 'aunque', 'si', 'que', 'quien', 'cual', 'cuyo', 'cuya', 'cuyos', 'cuyas']
    
    # Common English words
    english_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']
    
    # Convert text to lowercase and split into words
    words = text.lower().split()
    
    # Count Spanish and English words
    spanish_count = sum(1 for word in words if word in spanish_words)
    english_count = sum(1 for word in words if word in english_words)
    
    # Determine language based on count
    if spanish_count > english_count:
        return 'es'
    elif english_count > spanish_count:
        return 'en'
    else:
        # If tied, use Spanish as default
        return 'es'

# Initialize multilingual TTS
@st.cache_resource
def load_multilingual_tts():
    """Load TTS models for Spanish and English"""
    models = {}
    
    try:
        # Model for English
        models['en'] = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        st.success("✅ English TTS model loaded")
    except Exception as e:
        models['en'] = None
    
    try:
        # Model for Spanish
        models['es'] = TTS(model_name="tts_models/es/mai/tacotron2-DDC")
        st.success("✅ Spanish TTS model loaded")
    except Exception as e:
        try:
            # Fallback to alternative Spanish model
            models['es'] = TTS(model_name="tts_models/es/css10/vits")
            st.success("✅ Alternative Spanish TTS model loaded")
        except Exception as e2:
            models['es'] = models['en']  # Use English model as fallback
    
    return models

# Audio recording functions removed - now using audio-recorder-streamlit component

# Function to transcribe audio
def transcribe_audio(audio_bytes):
    """Transcribe audio using SpeechRecognition"""
    if not AUDIO_AVAILABLE:
        return "Error: SpeechRecognition is not available. Install: pip install SpeechRecognition"
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        # Initialize recognizer
        r = sr.Recognizer()
        
        # Configure recognizer for better accuracy
        r.energy_threshold = 300
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.8
        r.operation_timeout = None
        r.phrase_threshold = 0.3
        r.non_speaking_duration = 0.8
        
        # Load and process audio
        with sr.AudioFile(tmp_file_path) as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            # Record the audio
            audio_data = r.record(source)
        
        # Transcribe with multiple attempts
        text = None
        try:
            # Try with Spanish first
            text = r.recognize_google(audio_data, language='es-ES')
        except sr.UnknownValueError:
            try:
                # If it fails, try with English
                text = r.recognize_google(audio_data, language='en-US')
            except sr.UnknownValueError:
                try:
                    # If it fails, try without specifying language
                    text = r.recognize_google(audio_data)
                except sr.UnknownValueError:
                    return "Could not understand the audio. Try speaking more clearly and with less background noise."
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        if text:
            return text
        else:
            return "Could not transcribe the audio. Check that the microphone is working correctly."
        
    except sr.RequestError as e:
        return f"Recognition service error: {e}. Check your internet connection."
    except Exception as e:
        return f"Error processing audio: {e}"

# Load multilingual TTS models
with st.spinner("Loading TTS models..."):
    tts_models = load_multilingual_tts()

if not tts_models or (tts_models.get('en') is None and tts_models.get('es') is None):
    st.error("Could not load TTS models")
    st.stop()

# Create tabs
tab1, tab2 = st.tabs(["📝 Text to Speech", "🎤 Speech to Text"])

with tab1:
    st.subheader("📝 Convert Text to Audio")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        text = st.text_area(
            "Write your text here:",
            height=200,
            placeholder="Write here the text you want to convert to audio..."
        )
        
        # Simple controls
        speed = st.slider("Speed", 0.5, 2.0, 1.0, 0.1)
        
        # Generation button
        if st.button("🎵 Generate Audio", type="primary"):
            if text.strip():
                with st.spinner("Generating audio..."):
                    try:
                        # Detect text language
                        detected_language = detect_language(text)
                        language_name = "Spanish" if detected_language == 'es' else "English"
                        
                        # Show detected language
                        st.info(f"🌍 **Detected language:** {language_name}")
                        
                        # Load TTS models
                        tts_models = load_multilingual_tts()
                        tts_model = tts_models.get(detected_language)
                        
                        if tts_model is None:
                            st.error(f"❌ Could not load TTS model for {language_name}")
                        else:
                            # Create temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                                tmp_file_path = tmp_file.name
                            
                            # Generate audio using the appropriate model
                            tts_model.tts_to_file(
                                text=text,
                                file_path=tmp_file_path,
                                speed=speed
                            )
                            
                            # Verify that the file was created correctly
                            if os.path.exists(tmp_file_path) and os.path.getsize(tmp_file_path) > 0:
                                # Show audio
                                st.success(f"✅ Audio generated successfully in {language_name}!")
                                st.audio(tmp_file_path, format="audio/wav")
                                
                                # Show file information
                                file_size = os.path.getsize(tmp_file_path)
                                st.info(f"📁 File size: {file_size:,} bytes")
                                
                                # Clean up temporary file
                                os.unlink(tmp_file_path)
                            else:
                                st.error("❌ Error: Could not generate audio file")
                            
                    except Exception as e:
                        st.error(f"Error generating audio: {e}")
                        # Clean up temporary file in case of error
                        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                            os.unlink(tmp_file_path)
            else:
                st.warning("Please write some text")
    
    with col2:
        st.subheader("ℹ️ TTS Information")
        st.info("**Models:** Tacotron2-DDC (ES/EN)")
        st.info("**Languages:** Spanish and English")
        st.info("**Detection:** Automatic")
        st.info("**Quality:** High")
        st.info("**Speed:** Fast")
        
        st.subheader("🎛️ Controls")
        st.markdown("- **Speed**: Controls how fast it speaks")
        st.markdown("- **Text**: The content to convert")
        st.markdown("- **Audio**: Generated automatically")
        
        st.subheader("💡 Tips")
        st.markdown("- Write clear and well-structured text")
        st.markdown("- **Spanish and English** detected automatically")
        st.markdown("- Avoid special characters or symbols")
        st.markdown("- Use punctuation for natural pauses")
        st.markdown("- Long texts may take longer to process")
        st.markdown("- Language mixing may cause confusion")

with tab2:
    st.subheader("🎤 Convert Speech to Text")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("ℹ️ STT Information")
        if AUDIO_AVAILABLE and RECORDER_AVAILABLE:
            st.success("**Status:** ✅ Fully Functional")
            st.info("**Engine:** Google Speech Recognition")
            st.info("**Recording:** Browser-based (works in cloud!)")
            st.info("**Language:** Spanish & English")
            st.info("**Quality:** High")
        elif AUDIO_AVAILABLE:
            st.warning("**Status:** ⚠️ Limited (upload files only)")
            st.info("**Engine:** Google Speech Recognition")
            st.info("**Recording:** Not available")
        else:
            st.warning("**Status:** ⚠️ Limited")
            st.info("**Engine:** Not available")
            st.info("**Language:** N/A")
            st.info("**Quality:** N/A")
        
        st.subheader("🎛️ Instructions")
        if RECORDER_AVAILABLE:
            st.markdown("1. **Click** the microphone button to start recording")
            st.markdown("2. **Speak** clearly into your microphone")
            st.markdown("3. **Click** the microphone button again to stop")
            st.markdown("4. **Click** 'Transcribe Audio' to convert to text")
            st.markdown("5. **Review** the transcribed text")
        else:
            st.markdown("1. **Upload** an audio file (WAV, MP3, etc.)")
            st.markdown("2. **Click** 'Transcribe Audio' to convert to text")
            st.markdown("3. **Review** the transcribed text")
        
        st.subheader("💡 Tips")
        st.markdown("- Speak clearly and slowly")
        st.markdown("- Avoid background noise")
        st.markdown("- Keep microphone close")
        st.markdown("- Use short phrases")
        st.markdown("- Record in a quiet environment")
        st.markdown("- Works in any browser with microphone access")
    
    with col2:
        st.markdown("### 🎙️ Audio Recording")
        
        # Session state
        if 'recognized_text' not in st.session_state:
            st.session_state.recognized_text = ""
        if 'audio_data' not in st.session_state:
            st.session_state.audio_data = None
        
        # Browser-based audio recording (works in Streamlit Cloud!)
        if RECORDER_AVAILABLE:
            st.success("✅ Browser-based audio recorder available")
            st.markdown("### 🎤 Record Audio")
            
            # Instructions
            st.markdown("""
            **📋 How to record:**
            1. **Click the microphone button** below to start recording
            2. **Speak** clearly into your microphone
            3. **Click the microphone button again** to stop recording
            4. The audio will appear below automatically
            """)
            st.info("💡 **Tip:** Your browser will ask for microphone permission the first time.")
            
            # Use audio-recorder-streamlit component
            audio_bytes = audio_recorder(
                text="🎤 Click to record (click again to stop)",
                pause_threshold=2.0,
                sample_rate=44100,
                recording_color="#e74c3c",
                neutral_color="#6c757d",
                icon_name="microphone",
                icon_size="2x",
            )
            
            # If audio was recorded, save it
            if audio_bytes:
                st.session_state.audio_data = audio_bytes
                st.session_state.recognized_text = ""  # Clear previous transcription
                st.success("✅ Audio recorded successfully!")
            
            # Show audio if available
            if st.session_state.audio_data:
                st.markdown("### 🎵 Recorded Audio")
                st.audio(st.session_state.audio_data, format="audio/wav")
                
                # Button to transcribe
                if st.button("🔄 Transcribe Audio", type="primary"):
                    with st.spinner("Transcribing audio..."):
                        transcribed_text = transcribe_audio(st.session_state.audio_data)
                        st.session_state.recognized_text = transcribed_text
                        if transcribed_text and not transcribed_text.startswith("Error"):
                            st.success("✅ Transcription completed!")
                        else:
                            st.error("❌ Transcription error")
                
                # Button to clear
                if st.button("🗑️ Clear Recording"):
                    st.session_state.audio_data = None
                    st.session_state.recognized_text = ""
                    st.success("✅ Recording cleared!")
                    st.rerun()
        
        # Fallback: upload audio file (always available)
        st.markdown("---")
        st.markdown("### 📁 Or Upload Audio File")
        uploaded_file = st.file_uploader(
            "Upload an audio file (WAV, MP3, M4A, OGG)",
            type=['wav', 'mp3', 'm4a', 'ogg'],
            help="You can also upload a pre-recorded audio file"
        )
        
        if uploaded_file:
            st.session_state.audio_data = uploaded_file.read()
            st.success("✅ File uploaded successfully!")
            
            # Show audio
            st.audio(uploaded_file, format="audio/wav")
            
            # Button to transcribe
            if st.button("🔄 Transcribe Uploaded Audio", type="primary"):
                with st.spinner("Transcribing audio..."):
                    transcribed_text = transcribe_audio(uploaded_file.read())
                    st.session_state.recognized_text = transcribed_text
                    if transcribed_text and not transcribed_text.startswith("Error"):
                        st.success("✅ Transcription completed!")
                    else:
                        st.error("❌ Transcription error")
        
        # Recognized text area
        st.markdown("### 📝 Recognized Text")
        recognized_text = st.text_area(
            "Transcribed text:",
            value=st.session_state.recognized_text,
            height=150,
            placeholder="The recognized text will appear here..."
        )
        
        # Show recognized text if it exists
        if st.session_state.recognized_text:
            st.markdown("---")
            st.markdown("### 📋 Result:")
            st.info(st.session_state.recognized_text)
    

# Footer
st.markdown("---")
st.markdown("*Complete Voice Agent - Text to Speech and Speech to Text*")
