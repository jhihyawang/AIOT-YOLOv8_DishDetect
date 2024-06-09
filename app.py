from flask import Flask, jsonify, render_template, request, Response, stream_with_context, redirect, session
import json
import time
import sqlite3

# 在这里设置正确的用户名和密码
CORRECT_USERNAME = "aiot"
CORRECT_PASSWORD = "8888"

# 标识用户是否已登录
logged_in = False

app = Flask(__name__, template_folder="templates")
app.secret_key = "8888"  # 设置会话密钥

@app.route("/")
def index():
    conn = sqlite3.connect('nutrition.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return render_template("index.html", items=items)


@app.get("/detect_and_calculate")
def detect():
    return render_template("camera_view.html")


class camera_view:
    def __init__(self):
        self.a_camera_frame = {"image": "NC", "timestamp": "", "predict": ""}

    def update_camera_frame(self, frame):
        self.a_camera_frame = frame

    def get_camera_frame(self):
        return self.a_camera_frame

a_camera_view = camera_view()


@app.post("/post_camera_frame")
def receive_camera_frame():
    try:
        content = request.get_json()
        a_camera_view.update_camera_frame(content)
    except Exception as e:
        print(f"Error receiving data: {str(e)}")
        return jsonify({"success": False, "error": str(e)})
    return "camera_frame updated successfully"


@app.route('/get_camera_stream')
def make_stream():
    @stream_with_context
    def generate():
        try:
            while True:
                yield "data:" + json.dumps(a_camera_view.get_camera_frame()) + "\n\n"
                time.sleep(0.1)
        except GeneratorExit:
            print('closed')

    return Response(generate(), mimetype='text/event-stream')


@app.route("/edit_menu")
def edit_menu():
    if "logged_in" in session and session["logged_in"]:
        conn = sqlite3.connect('nutrition.db')
        cursor = conn.cursor()
        cursor.execute("SELECT rowid, name, price FROM items")
        items = cursor.fetchall()
        conn.close()
        return render_template("edit_menu.html", items=items)
    else:
        return redirect("/login")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            session["logged_in"] = True
            return redirect("/edit_menu")
        else:
            return render_template("login.html", message="Incorrect username or password")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/")

@app.route("/update_prices", methods=["POST"])
def update_prices():
    if request.method == "POST":
        try:
            data = request.get_json()
            conn = sqlite3.connect('nutrition.db')
            cursor = conn.cursor()
            for item in data:
                cursor.execute("UPDATE items SET price = ? WHERE rowid = ?", (item["price"], item["id"]))
            conn.commit()
            conn.close()
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
