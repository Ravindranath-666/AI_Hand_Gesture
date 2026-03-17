import cv2
import mediapipe as mp
import pyautogui
import math
import os
#Volume control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
#Screen size
screen_w, screen_h = pyautogui.size()
#Smooth cursor variables
prev_x, prev_y = 0, 0
smoothening = 5
#Controls
clicked = False
snap_cooldown = False
#Volume setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_min, vol_max = volume.GetVolumeRange()[:2]
#Webcam
cap = cv2.VideoCapture(0)
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            lm_list = []

            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if len(lm_list) != 0:

                # Points
                thumb = lm_list[4]
                index = lm_list[8]
                middle = lm_list[12]
                pinky = lm_list[20]

                x_thumb, y_thumb = thumb[1], thumb[2]
                x_index, y_index = index[1], index[2]
                x_middle, y_middle = middle[1], middle[2]
                x_pinky, y_pinky = pinky[1], pinky[2]

                # ---------------- CURSOR ---------------- #
                screen_x = int((x_index / w) * screen_w)
                screen_y = int((y_index / h) * screen_h)

                curr_x = prev_x + (screen_x - prev_x) / smoothening
                curr_y = prev_y + (screen_y - prev_y) / smoothening

                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y
                dist_click = math.hypot(x_index - x_thumb, y_index - y_thumb)
                dist_whatsapp = math.hypot(x_middle - x_thumb, y_middle - y_thumb)
                dist_volume = math.hypot(x_pinky - x_thumb, y_pinky - y_thumb)


                # WhatsApp (Thumb + Middle)
                if dist_whatsapp < 30:
                    cv2.putText(frame, "WHATSAPP", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

                    if not snap_cooldown:
                        os.system("start whatsapp:")
                        snap_cooldown = True

                # Click (Thumb + Index)
                elif dist_click < 30:
                    cv2.putText(frame, "CLICK", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    if not clicked:
                        pyautogui.click()
                        clicked = True

                # Volume Control (Thumb + Pinky)
                else:
                    clicked = False
                    snap_cooldown = False

                    # Touch → Volume Down
                    if dist_volume < 30:
                        volume.SetMasterVolumeLevel(vol_min, None)
                        cv2.putText(frame, "VOLUME DOWN", (50, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    # Separate → Volume Up
                    else:
                        volume.SetMasterVolumeLevel(vol_max, None)
                        cv2.putText(frame, "VOLUME UP", (50, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("AI Hand Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()