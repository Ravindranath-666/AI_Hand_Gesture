# AI Virtual Hand Gesture Controller

## Project Overview

This project is a real-time computer vision system that allows users to control their computer using hand gestures through a webcam.

It enables touchless human-computer interaction by mapping hand gestures to system-level operations like cursor movement, click actions, volume control, and launching applications.


## Features

* 🖱️ Smooth cursor movement using index finger
* 👆 Click action using thumb + index finger
* 📱 Open WhatsApp using thumb + middle finger gesture
* 🔊 Volume control using thumb and pinky finger gesture (touch for decrease, release for increase)
* ⚡ Real-time hand tracking

## Tech Stack

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* Pycaw
* OS module

##  How It Works

1. Webcam captures live video
2. MediaPipe detects 21 hand landmarks
3. Finger positions are analyzed
4. Gestures are mapped to actions:

   * Index finger → Cursor movement
   * Thumb + Index → Click
   * Thumb + Middle → WhatsApp open
   * Finger bending → Volume control
5. System actions are executed in real-time


## Installation & Run

1) open Vscode 

git clone https://github.com/Ravindranath-666/AI_Hand_Gesture.git
cd AI_Hand_Gesture

Install dependencies:
pip install -r requirements.txt

Run the project:
python main.py

## 👨‍💻 Author

** Bala Venkata Naga Ravindranath Sangam **  
🎓 MSc Artificial Intelligence and Robotics  
🏛️ University of Hertfordshire
