# Gesture-Controlled-Robotic-System

## 🚀 Overview 
A real-time computer vision system that allows users to control a robotic device using hand gestures. The system uses a webcam to track hand movements and translates them into control commands for a robot.

## ⚙️ Features
- Real-time hand gesture recognition
- Touchless control using computer vision
- Gesture-to-command mapping (forward, backward, left, right, stop)
- Low-latency response for smooth control
- Wireless communication with robotic hardware

## 🛠 Tech Stack
- Python
- OpenCV
- MediaPipe
- ESP8266 (NodeMCU)
- UDP / Wi-Fi Communication

## ▶️ Demo Video

👉 [Demo 1](gesture_control_bot_video.mp4)
    [demo 2](gesture_detection.mp4)


## 🔌 System Architecture
- Camera captures real-time video
- MediaPipe detects hand landmarks
- Python processes gestures
- Commands are sent via Wi-Fi (ESP8266)
- Robot executes movement based on input

## 🔄 How It Works
- Webcam captures hand gestures
- MediaPipe tracks hand landmarks
- Gesture is interpreted into command
- Command sent wirelessly to robot
- Robot performs corresponding action

## 📊 Use Cases
- Touchless robotic control
- Assistive technology
- Smart automation systems
- Human-computer interaction research

## ⚠️ Limitations
- Performance depends on lighting conditions
- Limited gesture vocabulary
- Requires camera calibration for accuracy

## 🚀 Future Improvements
- Advanced gesture recognition using AI/ML
- Mobile-based gesture control
- Improved accuracy in low-light conditions
- Integration with automation systems

## 📂 Project Structure
                      gesture-controlled-robot/
                      │── src/                              # Python code
                      │── README.md
                      │── gesture_control_bot_video/        # video1
                      │── arduino/                          # ESP8266 code
                      │── deture_detection                  #video2

## 📫 Author

Navodita Amit Singh

🔗 LinkedIn: https://www.linkedin.com/in/navodita-singh-7350a3299
