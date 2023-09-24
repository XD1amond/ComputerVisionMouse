# Import Libraries
import cv2
import mediapipe as mp
import pyautogui
import time

# Setup variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
pyautogui.FAILSAFE = False

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Initially set finger count to 0 for each cap
    finger_Count = 0
    right_finger_Count = 0
    left_finger_Count = 0
    

    # Set individual fingers raised to false:
    left_thumb_raised = False
    left_index_raised = False
    left_middle_raised = False
    left_ring_raised = False
    left_pinky_raised = False

    right_thumb_raised = False
    right_index_raised = False
    right_middle_raised = False
    right_ring_raised = False
    right_pinky_raised = False

    if results.multi_hand_landmarks:

      for hand_landmarks in results.multi_hand_landmarks:
        # Get hand index to check label (left or right)
        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
        handLabel = results.multi_handedness[handIndex].classification[0].label

        # Set variable to keep landmarks positions (x and y)
        handLandmarks = []

        # Fill list with x and y positions of each landmark
        for landmarks in hand_landmarks.landmark:
          handLandmarks.append([landmarks.x, landmarks.y])

        # Test conditions for each finger: Count is increased if finger is considered raised.
        # Thumb: TIP x position must be greater or lower than IP x position depending on hand label.
        if handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
          left_finger_Count = left_finger_Count+1
          left_thumb_raised = True
        elif handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
          right_finger_Count = right_finger_Count+1
          right_thumb_raised = True

        # Other fingers: TIP y position must be lower than PIP y position as image origin is in the upper left corner.
        if handLabel == "Right" and handLandmarks[8][1] < handLandmarks[6][1]:       #Index finger
          left_finger_Count = left_finger_Count+1
          left_index_raised = True
        if handLabel == "Right" and handLandmarks[12][1] < handLandmarks[10][1]:     #Middle finger
          left_finger_Count = left_finger_Count+1
          left_middle_raised = True
        if handLabel == "Right" and handLandmarks[16][1] < handLandmarks[14][1]:     #Ring finger
          left_finger_Count = left_finger_Count+1
          left_ring_raised = True
        if handLabel == "Right" and handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
          left_finger_Count = left_finger_Count+1
          left_pinky_raised = True

        if handLabel == "Left" and handLandmarks[8][1] < handLandmarks[6][1]:       #Index finger
          right_finger_Count = right_finger_Count+1
          right_index_raised = True
        if handLabel == "Left" and handLandmarks[12][1] < handLandmarks[10][1]:     #Middle finger
          right_finger_Count = right_finger_Count+1
          right_middle_raised = True
        if handLabel == "Left" and handLandmarks[16][1] < handLandmarks[14][1]:     #Ring finger
          right_finger_Count = right_finger_Count+1
          right_ring_raised = True
        if handLabel == "Left" and handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
          right_finger_Count = right_finger_Count+1
          right_pinky_raised = True

        # Draw hand landmarks 
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        
        # List values of fingers raised
        list_left = [left_thumb_raised, left_index_raised, left_middle_raised, left_ring_raised, left_pinky_raised]
        list_right = [right_thumb_raised, right_index_raised, right_middle_raised, right_ring_raised, right_pinky_raised]
        printed_list_left = str(list_left)
        printed_list_right = str(list_right)

        # Display finger count
        finger_Count = left_finger_Count + right_finger_Count
        half1 = "Total: " + str(finger_Count) + "Left: "
        half2 = str(left_finger_Count) + "Right: " + str(right_finger_Count)
        cv2.putText(image, str(half1 + half2), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

        # Display fingers raised
        cv2.putText(image, str(list_left), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

        # Make the mouse
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frameHeight, frameWidth, _ = frame.shape
        screenWidth, screenHeight = pyautogui.size()
        if list_right == [True, True, True, True, True]:
          x = int(landmarks.x*frameWidth)
          y = int(landmarks.y*frameHeight)
          mousePositionX = screenWidth/frameWidth*x
          mousePositionY = screenHeight/frameHeight*y
          pyautogui.moveTo(1920-mousePositionX, mousePositionY)
        
        
        # Make controls
        start_time = time.time()
        # Left click
        while handLabel == "Left" and handLandmarks[8][1] > handLandmarks[10][1] and handLandmarks[8][1] < handLandmarks[9][1]:
            end_time = time.time()
            if (end_time - start_time > .3):
              pyautogui.leftClick()
              break
        # Right click
        while handLabel == "Left" and handLandmarks[12][1] > handLandmarks[6][1] and handLandmarks[12][1] < handLandmarks[5][1] and handLandmarks[12][1] > handLandmarks[14][1] and handLandmarks[12][1] > handLandmarks[13][1]:
            end_time = time.time()
            if (end_time - start_time > .3):
              pyautogui.rightClick()
              break
        # Middle click
        while list_right == [False, False, True, False, False]:
            end_time = time.time()
            if (end_time - start_time > .75):
              pyautogui.middleClick
              break
        # Scrolling
        while list_right == [True, False, False, False, False]:
            end_time = time.time()
            if (end_time - start_time > .3):
              pyautogui.scroll(30)
              break
        while list_right == [False, True, False, False, False]:
            end_time = time.time()
            if (end_time - start_time > .3):
              pyautogui.scroll(-30)
              break
        # Play/Pause media
        while handLabel == "Left" and handLandmarks[8][0] > handLandmarks[4][0] and handLandmarks[8][1] > handLandmarks[4][1] and list_right[2] == False and  list_right[3] == False and list_right[4] == False:
            end_time = time.time()
            if (end_time - start_time > 1):
              pyautogui.press("playpause")           
              break
        # Volume
        while list_right == [False, True, True, False, False]:
            end_time = time.time()
            if (end_time - start_time > .3):
              pyautogui.press('volumeup')
              break
        while list_right == [True, True, False, False, False]:
            end_time = time.time()
            if (end_time - start_time > .3):
              pyautogui.press('volumedown')
              break
        # Skip/Previous Track
        while list_right == [False, False, False, False, True]:
            end_time = time.time()
            if (end_time - start_time > 1):
              pyautogui.press('prevtrack')
              break
        while list_right == [True, False, False, False, True]:
            end_time = time.time()
            if (end_time - start_time > 1):
              pyautogui.press('nexttrack')
              break

        # Controls cheatsheet:
        # Mouse Controls:
          # Mouse: Open palm.
          # Clicking: Pointer finger halfway down: Left Click. Middle finger down: Right Click.
          # Scrolling: Scroll up: Only thumb up. Scroll down: Only Pointer up: Scroll up.
        # Media Controls:
          # Play/Pause: Cross pointer finger below the first knuckle of thumb.
          # Volume: Volume up: Only pointer and middle finger up. Volume down: Only thumb and pointer up.
          # Skip/Previous track: Previous track: Only pinky up. Next track: Only thumb and pinky up.


    # Display image
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()