from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
from datetime import datetime
import os

app = Flask(__name__)

TEMPLATE_PATH = "SpectoV_Cert.docx"
OUTPUT_DOCX = "static/Final_Certificate.docx"

pronouns = {
    "male": ("he", "him"),
    "female": ("she", "her"),
    "other": ("they", "them")
}

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

        if not os.path.exists('static'):
            os.makedirs('static')

        doc = DocxTemplate(TEMPLATE_PATH)
        context = {
            "name": name,
            "domain": domain,
            "start_date": start_date,
            "end_date": end_date,
            "he_she_they": he_she,
            "him_her_them": him_her,
            "issued_date": issued_date
        }
        doc.render(context)
        doc.save(OUTPUT_DOCX)

        os.system(f'libreoffice --headless --convert-to pdf --outdir static {OUTPUT_DOCX}')
        pdf_path = OUTPUT_DOCX.replace('.docx', '.pdf')
        return send_file(pdf_path, as_attachment=True)

    return render_template('form.html')
