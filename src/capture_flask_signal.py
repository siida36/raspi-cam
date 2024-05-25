"""
MIT License

Copyright (c) 2024 MasashiMurata

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author: siida36
Organization: デジラクダ
"""

# 標準ライブラリをインポート
from datetime import datetime

# サードパーティに関連するもの
import cv2
from flask import Flask, Response

# opencvのvideo capture
app = Flask(__name__)

CUR_VOTE = {
    "red": 0,
    "yellow": 0,
    "blue": 0,
    "other": 0,
}

CUR_RESULT = "other"


def camera_cheack():
    if not cap.isOpened():
        print("カメラを開けられませんでした。")
        exit()


def classify_color(b, g, r):
    if r > 100 and g < 100 and b < 100:
        return "red"
    elif r > 100 and g > 100 and b < 100:
        return "yellow"
    elif r < 100 and g < 100 and b > 100:
        return "blue"
    else:
        return "other"


def reduce_white(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_Lab2BGR)


def print_result(image, color_name, start_point):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)
    line_type = 2
    
    text_position = (start_point[0], start_point[1] - 10)
    cv2.putText(
        image, color_name, text_position,
        font, font_scale, font_color, line_type
    )
    return image


def init_vote():
    global CUR_VOTE
    CUR_VOTE = {
        "red": 0,
        "yellow": 0,
        "blue": 0,
        "other": 0,
    }


def detect_signal(image):
    global CUR_VOTE
    global CUR_RESULT

    image = reduce_white(image)

    height, width, depth = image.shape

    rect_size = 100
    start_point = (width // 2 - rect_size // 2, height // 2 - rect_size // 2)
    end_point = (width // 2 + rect_size // 2, height // 2 + rect_size // 2)

    color = (255, 100, 0)
    thickness = 2
    cv2.rectangle(image, start_point, end_point, color, thickness)

    cropped_image = image[
        start_point[1]:end_point[1], start_point[0]:end_point[0]
    ]
    center_pixel = cropped_image[rect_size // 2, rect_size // 2]
    color_name = classify_color(*center_pixel)

    CUR_VOTE[color_name] += 1
    if CUR_VOTE["red"] + CUR_VOTE["yellow"] + CUR_VOTE["blue"] + CUR_VOTE["other"] == 100:
        if CUR_VOTE["red"] > CUR_VOTE["yellow"] and CUR_VOTE["red"] > CUR_VOTE["blue"]:
            CUR_RESULT = "red"
        elif CUR_VOTE["yellow"] > CUR_VOTE["red"] and CUR_VOTE["yellow"] > CUR_VOTE["blue"]:
            CUR_RESULT = "yellow"
        elif CUR_VOTE["blue"] > CUR_VOTE["red"] and CUR_VOTE["blue"] > CUR_VOTE["yellow"]:
            CUR_RESULT = "blue"
        else:
            CUR_RESULT = "other"
        init_vote()

    image = print_result(image, CUR_RESULT, start_point)
    return image


def capture():
    cap = cv2.VideoCapture(0)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    while True:
        # フレームごとにキャプチャ
        # ret, frame = cap.read(0)
        ret, frame = cap.read()

        # フレームの取得に失敗した場合
        if not ret:
            print("フレームの取得に失敗しました。終了します。")
            break

        frame = detect_signal(frame)

        # フレームを画面に表示
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield(b"--frame\r\n"
        b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed_signal")
def video_feed_signal():
    return Response(capture(), 
        mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0", port=5000)
