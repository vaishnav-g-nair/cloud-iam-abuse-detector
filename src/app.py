from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd

from input_handler import load_log_file
from detect_anomalies import run_all_detections

app = Flask(__name__)

UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "logfile" not in request.files:
            return "No file uploaded", 400

        file = request.files["logfile"]

        if file.filename == "":
            return "No selected file", 400

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Load and analyze
        df = load_log_file(file_path)
        alerts = run_all_detections(df)

        return render_template(
            "results.html",
            alerts=alerts,
            logs=df.to_dict(orient="records")
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
