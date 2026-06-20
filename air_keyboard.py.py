import cv2
import mediapipe as mp
import pyautogui
import time
import webbrowser
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

CAM_WIDTH = 650
TEXT_WIDTH = 450
TOTAL_WIDTH = CAM_WIDTH + TEXT_WIDTH

# Keyboard layout
keys = [['1','2','3','4','5','6','7','8','9','0'],
        ['Q','W','E','R','T','Y','U','I','O','P'],
        ['A','S','D','F','G','H','J','K','L'],
        ['Z','X','C','V','B','N','M','<','ENTER']]
key_w = 50
key_h = 50
gap = 8

# App buttons - BLUE Google, RED YouTube, GREEN WhatsApp - BACK ON TOP!
app_buttons = [
    {'name': 'GOOGLE', 'color': (255, 100, 0), 'gesture': (1,0,0,0,0), 'url': 'https://google.com'},
    {'name': 'YOUTUBE', 'color': (0, 0, 255), 'gesture': (0,1,0,0,0), 'url': 'https://youtube.com'},
    {'name': 'WHATSAPP', 'color': (0, 255, 0), 'gesture': (0,1,1,0,0), 'url': 'https://web.whatsapp.com'}
]

# MODE GESTURES - Switch between modes
MODE_GESTURES = {
    (0,0,0,0,0): "LETTER", # ✊ Fist = Letter mode
    (1,0,0,0,1): "NUMBER", # ✋👌 4 fingers bent = Number mode
    (0,0,0,0,1): "APP" # 🤙 Pinky up = App mode
}

# Letter gestures
LETTERS = {
    (0,1,0,0,0): 'A', (0,1,1,0,0): 'B', (0,1,1,1,0): 'C', (0,1,0,0,1): 'D',
    (1,0,0,0,1): 'E', (1,1,0,0,0): 'F', (1,1,1,0,0): 'G', (1,1,1,1,0): 'H',
    (0,0,0,0,1): 'I', (0,0,1,0,0): 'J', (1,0,1,0,0): 'K', (1,0,0,1,0): 'L',
    (0,1,0,1,1): 'M', (0,1,0,1,0): 'N', (0,1,0,0,1): 'O', (0,0,1,1,0): 'P',
    (0,0,1,1,1): 'Q', (0,1,1,0,1): 'R', (1,1,0,1,0): 'S', (1,1,1,0,1): 'T',
    (1,0,1,1,0): 'U', (1,0,1,1,1): 'V', (1,0,1,0,1): 'W', (1,1,1,1,0): 'X',
    (1,1,0,1,1): 'Y', (0,0,1,0,1): 'Z', (1,0,0,0,1): '<', (1,1,0,0,1): 'ENTER'
}

# Number gestures - simple thumb+fingers
NUMBERS = {
    (0,0,0,0,0): '0', (0,1,0,0,0): '1', (0,1,1,0,0): '2', (0,1,1,1,0): '3',
    (0,1,1,1,1): '4', (1,1,1,1,1): '5', (1,0,0,0,0): '6', (1,0,1,0,0): '7',
    (1,0,1,1,0): '8', (1,0,1,1,1): '9'
}

cap = cv2.VideoCapture(0)
window_name = "Air Keyboard + Apps + Modes"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, TOTAL_WIDTH, 700)

typed_text = ""
last_time = 0
cooldown = 0.5
mode_cooldown = 1.5
current_mode = "LETTER"
highlight_key = ""
highlight_time = 0

print("Started in LETTER MODE. ESC to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    canvas = np.zeros((700, TOTAL_WIDTH, 3), dtype=np.uint8)
    cam_resized = cv2.resize(frame, (CAM_WIDTH, 700))
    canvas[0:700, 0:CAM_WIDTH] = cam_resized

    img_rgb = cv2.cvtColor(cam_resized, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    fingers_tuple = None
    detected_key = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(cam_resized, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            canvas[0:700, 0:CAM_WIDTH] = cam_resized

            tips = [4, 8, 12, 16, 20]
            fingers = []
            for i, tip in enumerate(tips):
                if i == 0:
                    fingers.append(1 if hand_landmarks.landmark[tip].x < hand_landmarks.landmark[tip-1].x else 0)
                else:
                    fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y else 0)
            fingers_tuple = tuple(fingers)

            cv2.putText(canvas, f"Gesture: {fingers}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            current_time = time.time()
            app_opened = False

            # CLEAR ALL - works in any mode
            if fingers_tuple == (0,1,1,1,1) and current_time - last_time > 1.0:
                last_time = current_time
                typed_text = ""
                detected_key = "CLEAR"
                app_opened = True

            # MODE SWITCH - check first!
            elif fingers_tuple in MODE_GESTURES and current_time - last_time > mode_cooldown:
                last_time = current_time
                current_mode = MODE_GESTURES[fingers_tuple]
                detected_key = f"MODE:{current_mode}"
                print(f"Switched to {current_mode} MODE")
                app_opened = True

            # App buttons - ONLY work in APP mode now
            if current_mode == "APP" and not app_opened:
                for app in app_buttons:
                    if fingers_tuple == app['gesture'] and current_time - last_time > cooldown:
                        last_time = current_time
                        detected_key = app['name']
                        app_opened = True
                        webbrowser.open(app['url'])
                        print(f"Opened {app['name']}")
                        break

            # Typing based on mode
            if not app_opened and current_mode == "LETTER" and fingers_tuple in LETTERS and current_time - last_time > cooldown:
                key = LETTERS[fingers_tuple]
                detected_key = key
                last_time = current_time
                highlight_key = key
                highlight_time = current_time + 0.3

                if key == '<':
                    pyautogui.press('backspace')
                    typed_text = typed_text[:-1]
                elif key == 'ENTER':
                    pyautogui.press('enter')
                    typed_text += '\n'
                else:
                    pyautogui.write(key)
                    typed_text += key

            elif not app_opened and current_mode == "NUMBER" and fingers_tuple in NUMBERS and current_time - last_time > cooldown:
                key = NUMBERS[fingers_tuple]
                detected_key = key
                last_time = current_time
                highlight_key = key
                highlight_time = current_time + 0.3
                pyautogui.write(key)
                typed_text += key

    # Draw keyboard - LEFT side
    start_y = 180
    for r, row in enumerate(keys):
        total_w = len(row) * (key_w + gap)
        start_x = (CAM_WIDTH - total_w) // 2
        for c, key in enumerate(row):
            w = key_w * 2 if key in ['ENTER', '<'] else key_w
            x1 = start_x + c * (key_w + gap)
            y1 = start_y + r * (key_h + gap)
            x2 = x1 + w
            y2 = y1 + key_h

            color = (255, 100, 255)
            thickness = 2
            if detected_key == key:
                color = (0, 255, 0)
                thickness = 4
            elif highlight_key == key and time.time() < highlight_time:
                color = (0, 255, 255)

            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
            cv2.rectangle(canvas, (x1, y1), (x2, y2), (255, 255, 255), thickness)
            cv2.putText(canvas, key, (x1 + w//2 - 12, y1 + 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Draw APP BUTTONS - TOP LEFT - BACK!
    btn_w, btn_h = 140, 60
    start_x_btn = 50
    y_btn = 60
    for i, app in enumerate(app_buttons):
        x1 = start_x_btn + i * (btn_w + 20)
        x2 = x1 + btn_w
        y2 = y_btn + btn_h
        color = app['color']
        if detected_key == app['name']:
            color = (0, 255, 255) # yellow glow when clicked

        cv2.rectangle(canvas, (x1, y_btn), (x2, y2), color, -1)
        cv2.rectangle(canvas, (x1, y_btn), (x2, y2), (255, 255, 255), 3)
        cv2.putText(canvas, app['name'], (x1 + 15, y_btn + 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # RIGHT PANEL - Black background
    cv2.rectangle(canvas, (CAM_WIDTH, 0), (TOTAL_WIDTH, 700), (0, 0, 0), -1)
    cv2.line(canvas, (CAM_WIDTH, 0), (CAM_WIDTH, 700), (255, 255, 255), 2)

    # Show current mode
    mode_color = (0, 255, 0) if current_mode == "LETTER" else (255, 165, 0) if current_mode == "NUMBER" else (255, 0, 255)
    cv2.putText(canvas, f"MODE: {current_mode}", (CAM_WIDTH + 20, 40),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, mode_color, 2)

    cv2.putText(canvas, "LIVE TYPED TEXT:", (CAM_WIDTH + 20, 80),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Text wrap
    y_offset = 120
    lines = []
    line = ""
    for char in typed_text:
        line += char
        if len(line) > 28:
            lines.append(line)
            line = ""
    if line:
        lines.append(line)

    for i, line in enumerate(lines[-18:]):
        cv2.putText(canvas, line, (CAM_WIDTH + 20, y_offset + i*28),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)

    # Instructions
    cv2.putText(canvas, "SWITCH: Fist=Letter, 4bend=Number, Pinky=App", (10, 660),
               cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
    cv2.putText(canvas, "CLEAR: Open palm + Thumb down", (10, 685),
               cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

    cv2.imshow(window_name, canvas)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()