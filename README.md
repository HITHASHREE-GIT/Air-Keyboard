# Air Keyboard ✋⌨️

Type in the air! A virtual keyboard controlled by hand gestures using just your webcam.  
No physical keyboard needed - built with Python, OpenCV & MediaPipe.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)

## ✨ Features
- **Touchless Typing**: Type characters using finger gestures in air
- **Real-time Hand Tracking**: MediaPipe detects 21 hand landmarks instantly
- **Webcam Only**: Works on any laptop/desktop with camera
- **Lightweight**: Runs smoothly without heavy GPU requirements
- **Custom Gestures**: Pinch/click gesture to type selected keys

## 🛠️ Tech Stack
`Python` `OpenCV` `MediaPipe` `NumPy` `Computer Vision`

## 📦 Prerequisites
1. Python 3.8 or higher
2. Webcam/Camera access

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/HITHASHREE-GIT/Air-Keyboard.git
cd Air-Keyboard
2. Install dependencies:
pip install -r requirements.txt
## 🚀 How to Run
python air_keyboard.py
*Controls:*
1. Camera window will open - allow webcam permission
2. Show your hand to the camera 
3. Move finger over virtual keys to select
4. Use pinch gesture to click/type the key
5. Press `ESC` to exit

## 📁 Project Structure
Air-Keyboard/
│
├── air_keyboard.py      # Main code file
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
## 🎯 How It Works
1. *Hand Detection*: MediaPipe detects hand landmarks in each frame
2. *Gesture Recognition*: Finger positions mapped to keyboard keys
3. *Virtual Keyboard*: OpenCV renders keyboard overlay on screen
4. *Click Simulation*: Pinch gesture triggers key press event

## 🔮 Future Improvements
- [ ] Add backspace, space, enter gestures
- [ ] Multi-language keyboard support
- [ ] Save typed text to .txt file
- [ ] Improve accuracy in low light
- [ ] Add voice feedback for typed keys

## 👩‍💻 Author
*Hithashree P*  
GitHub: https://github.com/HITHASHREE-GIT/Air-Keyboard.git


## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

## 📄 License
This project is open source. Feel free to use and modify.

---
Made with ❤️ using Computer Vision. Star ⭐ this repo if you found it useful!



