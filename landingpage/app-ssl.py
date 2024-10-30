from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import fitz 

app = Flask(__name__)



# Set the upload folder path

UPLOAD_FOLDER = '/home/ubuntu/leech'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# Allowed file extensions

ALLOWED_EXTENSIONS = {'pdf'}



def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])

def upload_file():

    if request.method == 'POST':

        if 'file' not in request.files:

            return 'No file part'

        

        file = request.files['file']

        if file.filename == '':

            return 'No selected file'

        

        if file and allowed_file(file.filename):

            filename = file.filename

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)



            # Get selected processing options

            options = request.form.getlist('process_option')

            results = process_file(filepath, options)

            return render_template('result.html', results=results)

    

    return render_template('upload.html')



def process_file(filepath, options):

    results = []

    # Placeholder functionality for each option
    if 'convert_to_text' in options:
        text = convert_pdf_to_text(filepath)
        results.append(text)  # Append the extracted text

    if 'split' in options:

        results.append("File has been split into parts.")  # Replace with actual splitting code

    if 'anonymize' in options:

        results.append("File has been anonymized.")  # Replace with actual anonymization code

    if 'summarize_first' in options:

        results.append("Summary of the first part generated.")  # Replace with summarization code

    if 'summarize_second' in options:

        results.append("Summary of the second part generated.")  # Replace with summarization code

    if 'seek_similar' in options:

        results.append("A similar file has been found.")  # Replace with actual similarity search code

    

    return results



def convert_pdf_to_text(filepath):
    text = ""
    with fitz.open(filepath) as pdf_document:
        for page in pdf_document:
            text += page.get_text()
    return text






@app.route('/success')

def upload_success():

    return render_template('success.html')



if __name__ == '__main__':


    app.run(host='0.0.0.0', port=443, ssl_context=(

    '/etc/letsencrypt/live/www.melborp.solutions/fullchain.pem',

    '/etc/letsencrypt/live/www.melborp.solutions/privkey.pem'

    ))
