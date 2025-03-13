from flask import Flask, render_template, request, redirect, url_for
import formatter
import ai.invoke as invoke
import ai.agent as agent
import formatter.blockheadercomment as bh
from pdf.textscraper import getPdfContent
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
cwd = os.getcwd()
UPLOAD_FOLDER = cwd+'/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
filename = ""
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route("/manual")
def mainWebsite():
    return render_template('index.html')

@app.route("/prompt", methods=["GET", "POST"])
def sendPrompt():
    prompt = request.form.get('prompt') if request.method == "POST" else request.args.get('prompt')
    name = request.form.get('name') if request.method == "POST" else None

    if prompt:
        thought, result = agent.solve_code(prompt)
        summary = agent.summarize_code(result)
        bhc = bh.get_bhc(name, summary)

        full_code = bhc+result


        return render_template('result.html', result=full_code, summary=summary, thought=thought, name=name)
    else:
        return redirect(url_for('mainWebsite'))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Extract the name from the form data
        name = request.form.get('name', ' ')  

        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            upload_path = app.config['UPLOAD_FOLDER']

            # Create folder if it doesn't exist yet
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            file.save(os.path.join(upload_path, filename))
            fileDir = os.path.join(os.getcwd(), "uploads", filename)

            content = getPdfContent(fileDir) + ". Do include all code needed for a functioning program"
            prompt = content

            if prompt:
                thought, result = agent.solve_code(prompt)
                summary = agent.summarize_code(result)
                bhc = bh.get_bhc(name, summary)

                full_code = bhc + result
                os.remove(fileDir)
                return render_template('result.html', result=full_code, summary=summary, thought=thought, name=name)
            else:
                return redirect(url_for('mainWebsite'))
            

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type="text" name="name" placeholder="Enter your name">
      <input type=submit value=Upload>
    </form>
    '''


def run():
    app.run(debug=True)
