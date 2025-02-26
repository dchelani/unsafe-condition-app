#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, request
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = r"\\192.168.4.88\Python\uploads"
EXCEL_FILE = r"\\192.168.4.88\Python\unsafe_condition.xlsx"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return '''
        <h2>Report an Unsafe Condition</h2>
        <form action="/submit" method="post" enctype="multipart/form-data">
            Location: <input type="text" name="location" required><br>
            Name: <input type="text" name="name" required><br>
            Unsafe_Condition_Act: <input type="file" name="Unsafe_Condition_Act" accept="image/*" required><br>
            Restore: <input type="file" name="Restore" accept="image/*" required><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route("/submit", methods=["POST"])
def submit():
    location = request.form.get("location")
    name = request.form.get("name")
    Unsafe_Condition_Act = request.files.get("Unsafe_Condition_Act")
    Restore = request.files.get("Restore")

    if not (location and name and Unsafe_Condition_Act and Restore):
        return "All fields are required!", 400

    image_paths = []
    for img in [Unsafe_Condition_Act, Restore]:
        if img.filename:
            img_path = os.path.join(UPLOAD_FOLDER, img.filename)
            img.save(img_path)
            image_paths.append(img_path)

    data = pd.DataFrame([[location, name, image_paths[0], image_paths[1], datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                        columns=["Location", "Name", "Unsafe_Condition_Act", "Restore", "Timestamp"])

    if os.path.exists(EXCEL_FILE):
        existing_data = pd.read_excel(EXCEL_FILE)
        data = pd.concat([existing_data, data], ignore_index=True)

    data.to_excel(EXCEL_FILE, index=False)

    return "Report submitted successfully!"

if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:




