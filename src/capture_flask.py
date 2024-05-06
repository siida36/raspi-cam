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

Author: MasashiMurata
Organization: デジラクダ
"""

# 標準ライブラリをインポート

# サードパーティに関連するもの
import cv2
from flask import Flask, Response

# opencvのvideo capture
app = Flask(__name__)

def camera_cheack():
    if not cap.isOpened():
        print("カメラを開けられませんでした。")
        exit()

def capture():
    cap = cv2.VideoCapture(0)
    while True:
        # フレームごとにキャプチャ
        ret, frame = cap.read(0)

        # フレームの取得に失敗した場合
        if not ret:
            print("フレームの取得に失敗しました。終了します。")
            break
        
        # フレームを画面に表示
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield(b"--frame\r\n"
        b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(capture(), 
        mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0", port=5000)
