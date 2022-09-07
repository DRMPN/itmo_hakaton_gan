import subprocess
from pathlib import Path
import flask
from flask import render_template, request, abort, redirect, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from glob import glob
from random import choice
import os
import time

app = flask.Flask(__name__)


def add_text_line(img_path="./static/result.png"):
    textline_path = choice(glob("text_lines/*"))
    # textline_path = "./text_lines/spb1.jpg"
    img = Image.open(img_path)
    textline = Image.open(textline_path)
    img_w, img_h = img.size
    textline_w, textline_h = textline.size
    textline_h_w = textline_h / textline_w
    insert_w = int(img_w // 1.5)
    inset_h = int(insert_w * textline_h_w)
    img.paste(textline.resize((insert_w, inset_h)), (img_w // 2 - insert_w // 2, img_h // 10),
              textline.resize((insert_w, inset_h)))
    img.save(img_path)


def start_gan():
    # style_name = os.path.basename(choice(glob("./data/style-images/spb*")))
    style_name = "spb1.jpg"
    content_name = "user_input.jpg"
    process = subprocess.Popen(['python', 'neural_style_transfer.py',
                                '--content_img_name', content_name,
                                '--style_img_name', style_name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout, stderr)
    time.sleep(3)
    # subprocess.run(f"python neural_style_transfer.py --content_img_name {content_name} --style_img_name {style_name}")


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Check request
        if "file" not in request.files:
            return redirect(request.url)
        f = request.files["file"]
        if not f:
            return

        f.save("./data/content-images/user_input.jpg")
        save_path = 'static/result.png'
        time.sleep(1)
        print("BEFORE")
        start_gan()
        print("AFTER")
        add_text_line(save_path)
        return send_file(save_path, as_attachment=True)

    return render_template("index.html")


app.run(host="0.0.0.0", port=5003)
