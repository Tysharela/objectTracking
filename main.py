import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Создание окна Tkinter
window = tk.Tk()
window.title("Video GUI")

# Создание панели для отображения видео
panel = tk.Label(window)
panel.pack(padx=10, pady=10)

# Создание переменной состояния видео
video_state = tk.BooleanVar()
video_state.set(False)

cap = cv2.VideoCapture('los_angeles.mp4')
#cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 700)

def show_frame():
    if video_state.get():
        _, frame1 = cap.read()
        _, frame2 = cap.read()

        diff = cv2.absdiff(frame1,
                           frame2)  # нахождение разницы двух кадров, которая проявляется лишь при изменении одного из
        # них, т.е. с этого момента наша программа реагирует на любое движение.

        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # перевод кадров в черно-белую градацию

        blur = cv2.GaussianBlur(gray, (5, 5), 0)  # фильтрация лишних контуров

        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # метод для выделения кромки объекта белым цветом

        dilated = cv2.dilate(thresh, None,
                             iterations=3)  # данный метод противоположен методу erosion(), т.е. эрозии объекта,
        # и расширяет выделенную на предыдущем этапе область

        сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)  # нахождение массива контурных точек

        for contour in сontours:
            (x, y, w, h) = cv2.boundingRect(
                contour)  # преобразование массива из предыдущего этапа в кортеж из четырех координат

            # метод contourArea() по заданным contour точкам, здесь кортежу, вычисляет площадь зафиксированного объекта в
            # каждый момент времени, это можно проверить
            print(cv2.contourArea(contour))

            if cv2.contourArea(contour) < 500:  # условие при котором площадь выделенного объекта меньше 10000 px для
                # вебкамеры, для видео 500-1000
                continue
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)  # получение прямоугольника из точек кортежа
            cv2.waitKey(0)
            # cv2.drawContours(frame1, сontours, -1, (0, 255, 0), 2)#нарисовать контур объекта

        frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        panel.imgtk = frame
        panel.config(image=frame)

    window.after(10, show_frame)

def start_video():
    video_state.set(True)


# Создание кнопки "Старт"
btn_start = tk.Button(window, text="Start",font="40", command=start_video)
btn_start.pack(fill="both", expand=True, padx=10, pady=10)

# Запуск цикла Tkinter
show_frame()
window.mainloop()

cap.release()
cv2.destroyAllWindows()
