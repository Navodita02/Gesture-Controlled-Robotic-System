import cv2
import mediapipe as mp
import math
import socket

# ================= UDP SETUP ======================
robotAddressPort = ("10.78.160.64", 12345)
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendTorobot(move, speed=120):
    msg4robot = f"{move},{speed},0,0,0"
    UDPClientSocket.sendto(msg4robot.encode(), robotAddressPort)


# ================= MEDIAPIPE ======================
mp_hands = mp.solutions.hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

# Hand open/close detector (simple)
def is_fist(handLms):
    # if fingertips are below knuckles → fist
    tips = [8, 12, 16, 20]
    mcp = [5, 9, 13, 17]

    closed = True
    for t, m in zip(tips, mcp):
        if handLms.landmark[t].y < handLms.landmark[m].y:
            closed = False
    return closed


# ============= VIDEO CAPTURE ======================
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# ============= MAIN LOOP ======================
while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(imgRGB)

    move = "s"   # default STOP
    right_hand_action_done = False
    left_hand_action_done = False

    # Draw the half-circle steering zone
    cx = int(w * 0.25)
    cy = int(h * 0.60)
    radius = 200

    cv2.ellipse(frame, (cx, cy), (radius, radius), 0, 180, 360, (255, 255, 0), 4)

    # Vertical line splitting left/right steering zones
    cv2.line(frame, (cx, cy - radius), (cx, cy), (0,255,255), 2)

    # Labels
    cv2.putText(frame, "LEFT", (cx - radius + 20, cy + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)
    cv2.putText(frame, "RIGHT", (cx + 20, cy + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)

    # ============= HAND DETECTION ==================
    if results.multi_hand_landmarks:
        for idx, handLms in enumerate(results.multi_hand_landmarks):
            mp_draw.draw_landmarks(frame, handLms, mp.solutions.hands.HAND_CONNECTIONS)

            # Get wrist position
            wrist = handLms.landmark[0]
            wx, wy = int(wrist.x * w), int(wrist.y * h)

            # Identify right or left hand
            handed = results.multi_handedness[idx].classification[0].label

            # ----- RIGHT HAND CONTROLS FORWARD/BACK -----
            if handed == "Right" and not right_hand_action_done:
                if is_fist(handLms):
                    move = "b"
                    cv2.putText(frame, "BACKWARD", (900, 100), cv2.FONT_HERSHEY_SIMPLEX,
                                1.2, (0,0,255), 3)
                else:
                    move = "f"
                    cv2.putText(frame, "FORWARD", (900, 100), cv2.FONT_HERSHEY_SIMPLEX,
                                1.2, (0,255,0), 3)

                right_hand_action_done = True

            # ----- LEFT HAND CONTROLS STEERING -----
            if handed == "Left" and not left_hand_action_done:

                if is_fist(handLms):
                    # Check if fist is inside steering semicircle
                    dist = math.dist([wx, wy], [cx, cy])
                    if dist < radius:

                        if wx < cx:    # left zone of semicircle
                            move = "l"
                            cv2.putText(frame, "TURN LEFT", (50, 100),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,255), 3)

                        elif wx > cx:  # right zone of semicircle
                            move = "r"
                            cv2.putText(frame, "TURN RIGHT", (50, 100),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,255), 3)

                left_hand_action_done = True


    # Send command
    sendTorobot(move)

    cv2.imshow("Hand Control System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
