import cv2

# Картинку отрисовывает


def image_proc():
    img = cv2.imread('sample.jpg')

    # Поворачивает
    # w, h = img.shape[:2]
    # (cX, cY) = (w // 2, h // 2)
    # M = cv2.getRotationMatrix2D((cX, cY), 45, 1.0)
    # rotated = cv2.warpAffine(img, M, (w, h))
    # cv2.imshow('image', rotated)

    # Обрезает
    # cat = img[250:580, 20:280]
    # cv2.imshow('image', cat)

    # Рисует что-то
    # cv2.line(img, (0, 0), (580, 600), (255, 0, 0), 5)
    # cv2.rectangle(img, (384, 10), (510, 128), (0, 2500, 0), 2)
    # cv2.putText(img, 'DVB-2', (10, 500), cv2.FONT_HERSHEY_SIMPLEX,
    #             3, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('image', img)

# image_proc()

# Выводит видео


def video_proc():
    cap = cv2.VideoCapture('sample.mp4')

    left_counter = 0
    right_counter = 0
    is_on_left = True

    WIDTH = 640
    HEIGHT = 480
    down_points = (WIDTH, HEIGHT)

    # Пока сами не выйдем
    while True:
        # Считываем данные с видео
        ret, frame = cap.read()
        if not ret:
            break

        # Обрезаем и переводим в черно-белое
        frame = cv2.resize(frame, down_points)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Подсвечиваем только то, что больше порога
        ret, thresh = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow('vid', thresh)

        # Получаем контуры
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Рисуем прямоугольник вокруг контура
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            # Проверяем, на какой стороне кадра
            if x < WIDTH / 2:
                if not is_on_left:
                    left_counter += 1
                    is_on_left = True
            else:
                if is_on_left:
                    right_counter += 1
                    is_on_left = False

        cv2.putText(frame, str(left_counter), (10, 400), cv2.FONT_HERSHEY_SIMPLEX,
                    3, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str(right_counter), (560, 400), cv2.FONT_HERSHEY_SIMPLEX,
                    3, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('vid', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


video_proc()

cv2.waitKey(0)
cv2.destroyAllWindows()
