from flask import Flask, render_template, request
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    # Convert PDF to text
    text = convert_pdf_to_text(file)
    return {"text": text}

@app.route('/beautify', methods=['POST'])
def beautify():
    text = request.form['text']
    #beautified_text = beautify_text(text)
    beautified_text = text
    return jsonify(beautified_text=beautified_text)


def convert_pdf_to_text(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf_document:
        for page in pdf_document:
            text += page.get_text()
    return text

if __name__ == "__main__":
    app.run(debug=True)

