from flask import Flask, render_template, request, send_file
from docx import Document
from datetime import datetime
import os

app = Flask(__name__)

TEMPLATE_PATH = "SpectoV_Cert.docx"
OUTPUT_DOCX = "static/Final_Certificate.docx"

pronouns = {"male": ("he", "him"), "female": ("she", "her"), "other": ("they", "them")}

@app.route('/', methods=['GET', 'POST'])
def generate_certificate():
    if request.method == 'POST':
        name = request.form['name']
        domain = request.form['domain']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        gender = request.form['gender'].lower()
        he_she, him_her = pronouns.get(gender, ("they", "them"))
        issued_date = datetime.today().strftime('%B %d, %Y')

        # Ensure 'static' folder exists
        if not os.path.exists('static'):
            os.makedirs('static')

        doc = Document(TEMPLATE_PATH)
        for para in doc.paragraphs:
            para.text = para.text.replace("{{Name}}", name)
            para.text = para.text.replace("{{Domain}}", domain)
            para.text = para.text.replace("{{Start Date}}", start_date)
            para.text = para.text.replace("{{End Date}}", end_date)
            para.text = para.text.replace("{{he/she/they}}", he_she)
            para.text = para.text.replace("{{him/her/them}}", him_her)
            if "ISSUED DATE :" in para.text:
                para.text = para.text.replace("ISSUED DATE :", f"ISSUED DATE : {issued_date}")

        doc.save(OUTPUT_DOCX)
        return send_file(OUTPUT_DOCX, as_attachment=True)

    return render_template('form.html')
