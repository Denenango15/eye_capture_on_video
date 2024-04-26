''' The program finds the eyes in the video,
highlights them in a frame, repaints them in gray and blurs them.
All these options can be changed '''
import cv2

cap = cv2.VideoCapture('video.mov')
eye_cascade = cv2.CascadeClassifier('eye.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10)

    if len(eyes) >= 2:
        # Создаем список координат / Creating a list of coordinates
        eyes_x = [x for x, y, w, h in eyes]
        eyes_y = [y for x, y, w, h in eyes]
        eyes_w = [w for x, y, w, h in eyes]
        eyes_h = [h for x, y, w, h in eyes]

        # Находим минимальные и максимальные координаты для создания прямоугольника
        # Finding the minimum and maximum coordinates to create a rectangle
        x = min(eyes_x)
        y = min(eyes_y)
        w = max(eyes_x) + max(eyes_w) - x
        h = max(eyes_y) + max(eyes_h) - y

        # Рисуем прямоугольник / Draw a rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), thickness=2)

        # Создаем копию области внутри прямоугольника
        # Creating a copy of the area inside the rectangle
        roi = frame[y:y + h, x:x + w].copy()

        # Преобразуем в оттенки серого / Convert to shades of gray
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Применяем размытие к копии / Applying a blur to the copy
        blurred_roi = cv2.blur(roi_gray, (35, 20))

        # Накладываем размытую копию области / Applying a blurred copy of the area
        frame[y:y + h, x:x + w] = cv2.cvtColor(blurred_roi, cv2.COLOR_GRAY2BGR)

    cv2.imshow('Res', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
