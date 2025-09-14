# 🧘‍♀️ Enhanced Yoga Poses Recommender

An intelligent, local Flask web application that provides personalized yoga pose recommendations with AI-powered descriptions and text-to-speech guidance.

## ✨ Features

### 🎯 **Smart Pose Search**
- Intelligent text-based search across 160+ yoga poses
- Always returns exactly 3 relevant recommendations
- Multi-keyword matching with intelligent scoring
- Search by pose name, difficulty level, benefits, or pose type

### 🔊 **Audio Guidance**
- Text-to-speech functionality for each pose description
- Play/Stop audio controls with visual feedback
- Local TTS using pyttsx3 (no internet required)
- Enhanced audio quality with optimized settings

### 🖼️ **Enhanced Visual Experience**
- High-quality pose images with full visibility
- Improved image display using object-contain for complete pose viewing
- Responsive design for mobile and desktop
- Modern glassmorphism UI with smooth animations

### 📊 **Comprehensive Pose Database**
- 160 yoga poses with AI-generated descriptions
- Detailed information including:
  - Sanskrit names
  - Difficulty levels (Beginner, Intermediate, Advanced)
  - Pose types (Standing, Seated, Backbend, etc.)
  - Benefits and instructions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BatchuMamatha/yoga-poses-recommender.git
   cd yoga-poses-recommender
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main_local.py
   ```

5. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:8081`

## 🎮 How to Use

1. **Search for Poses**: Enter keywords like "beginner poses", "back pain relief", "stress relief", or specific pose names
2. **View Results**: Browse through 3 recommended poses with images and descriptions
3. **Listen to Guidance**: Click the "Listen to Guide" button for audio instructions
4. **Control Audio**: Use the play/stop functionality to control audio playback

## 🏗️ Project Structure

```
yoga-poses-recommender/
├── main_local.py              # Main Flask application
├── settings.py                # Configuration settings
├── config_local.yaml          # Local configuration file
├── templates/
│   └── index.html            # Enhanced web interface
├── data/
│   └── yoga_poses_with_descriptions_full.json  # Complete poses database
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── LICENSE                  # License information
```

## ⚙️ Configuration

The application uses local configuration through `config_local.yaml`. You can customize:
- Port settings
- Gemini API key (for future enhancements)
- Search parameters

## 🔧 Technologies Used

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3 (TailwindCSS), JavaScript
- **Audio**: pyttsx3 (Local Text-to-Speech)
- **AI Integration**: Google Gemini API (optional)
- **Data**: JSON-based local database

## 🎨 Design Features

- **Modern UI**: Glassmorphism design with gradient backgrounds
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Accessibility**: Keyboard shortcuts and screen reader friendly
- **Performance**: Optimized image loading and smooth animations

## 🔍 Search Capabilities

The search engine supports various query types:
- **Difficulty**: "beginner poses", "advanced yoga"
- **Body Parts**: "back pain", "hip flexibility", "shoulder stretch"
- **Pose Types**: "standing poses", "seated positions", "backbends"
- **Benefits**: "stress relief", "strength building", "flexibility"
- **Specific Poses**: "downward dog", "warrior pose", "child's pose"

## 🎵 Audio Features

- **Local TTS**: No internet connection required
- **Quality Settings**: Optimized speech rate and volume
- **Voice Selection**: Automatic best voice selection
- **Error Handling**: Graceful fallback for audio issues

## 🛠️ Development

### Running in Development Mode
```bash
python main_local.py
```
The application runs with debug mode enabled and auto-reload on file changes.

### Adding New Poses
Add new poses to `data/yoga_poses_with_descriptions_full.json` following the existing JSON structure.

## 📝 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Contributing

This is a private repository. For questions or suggestions, please contact the repository owner.

## 🌟 Acknowledgments

- Built with modern web technologies and AI integration
- Designed for local, offline usage
- Enhanced user experience with audio and visual improvements
