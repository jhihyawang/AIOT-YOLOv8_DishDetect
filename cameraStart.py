import cv2
import base64
import requests
from datetime import datetime
import time
from ultralytics import YOLO
import sqlite3
import json

# 使用 ultralytics YOLOv8 模型
model = YOLO('best.pt')  # 替换为你自己的模型路径
class_names = model.names

# 開啟鏡頭
#cap = cv2.VideoCapture('food.mov')
cap = cv2.VideoCapture(0)

def detect_and_draw(frame, model):
    results = model(frame)
    detections = results[0].boxes.xyxy  # 得到检测框的坐标
    classes = results[0].boxes.cls  # 得到每个检测框对应的类别
    return detections, classes

def get_nutrition_data(items):
    # 連接到SQLite資料庫
    conn = sqlite3.connect('nutrition.db')
    cursor = conn.cursor()

    # 初始化總價和總營養成分
    total_price = 0
    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbohydrates = 0
    total_fiber = 0

    # 初始化結果字典
    result = {
        "selected_items": [],
        "total_price": 0,
        "total_nutrition": {
            "calories": 0,
            "protein": 0,
            "fat": 0,
            "carbohydrates": 0,
            "fiber": 0
        }
    }

    # 處理選擇的菜單
    for item in items:
        cursor.execute("SELECT * FROM items WHERE name=?", (item,))
        res = cursor.fetchone()
        if res:
            name, price, calories, protein, fat, carbohydrates, fiber = res
            total_price += price
            total_calories += calories
            total_protein += protein
            total_fat += fat
            total_carbohydrates += carbohydrates
            total_fiber += fiber
            
            # 添加到結果字典
            result["selected_items"].append({
                "name": name,
                "price": price,
                "calories": calories,
                "protein": protein,
                "fat": fat,
                "carbohydrates": carbohydrates,
                "fiber": fiber
            })

    # 填充總價和總營養成分
    result["total_price"] = total_price
    result["total_nutrition"]["calories"] = total_calories
    result["total_nutrition"]["protein"] = total_protein
    result["total_nutrition"]["fat"] = total_fat
    result["total_nutrition"]["carbohydrates"] = total_carbohydrates
    result["total_nutrition"]["fiber"] = total_fiber

    # 關閉連接
    conn.close()
    return result

while True:
    ret, frame = cap.read()
    # if not ret:
    #     print("Error: Failed to capture image")
    #     print("Error: Failed to capture image")
    #         # 要POST的資料
    #     data = {'image': "NC", 'timestamp': "0"}
    #         # 發送POST請求
    #     try:
    #         response = requests.post(
    #             'http://127.0.0.1:5000//post_camera_frame', json=data)
    #         if response.status_code == 200:
    #             print("err sent successfully")
    #         else:
    #             print(

    #                 f"Failed to send err. Status code: {response.status_code}")

    #     except requests.exceptions.RequestException as e:
    #         print("Failed to send err:", e)

    #     time.sleep(0.5)
    #     continue

    detections, classes = detect_and_draw(frame, model)
    predict=[]
    for det, cls in zip(detections, classes):
        x1, y1, x2, y2 = map(int, det)  # 获取检测框的坐标
        label = class_names[int(cls)]  # 获取检测的标签

        # 绘制检测框
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 绘制标签
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        predict.append(label)

    # 目前時間
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 添加目前時間
    cv2.putText(frame, current_time, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # 轉為Base64
    _, buffer = cv2.imencode('.jpg', frame)
    img_base64 = base64.b64encode(buffer)
    
    # 要POST的資料
    data = {'image': img_base64.decode('utf-8'), 'timestamp': current_time,'predict':get_nutrition_data(predict)}

    # print(data['predict'])

    #get_nutrition_data(data['predict'])

    # 發送POST請求
    try:
        response = requests.post(
            'http://127.0.0.1:5000//post_camera_frame', json=data)
        if response.status_code == 200:
            print("Image sent successfully")
        else:
            print(
                f"Failed to send image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("Failed to send image:", e)
    # 等待
    time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()