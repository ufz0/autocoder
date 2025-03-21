from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask import after_this_request
import ai.invoke as invoke
import ai.agent as agent
import formatter.blockheadercomment as bh
from pdf.textscraper import getPdfContent
import os
from werkzeug.utils import secure_filename
import requests
import pap.generate
import zipfile
import io

app = Flask(__name__)
cwd = os.getcwd()
UPLOAD_FOLDER = cwd+'/uploads'
OUTPUT_FOLDER = cwd+'/output'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
outputFileName = ""
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route("/manual")
def mainWebsite():
    return render_template('index.html')

@app.route("/styles.css")
def sendCSS():
    return send_file('templates/styles.css')

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
    clientIp = request.remote_addr
    if request.method == 'POST':
        name = request.form.get('name', ' ')  

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = clientIp + "-" + secure_filename(file.filename)
            upload_path = app.config['UPLOAD_FOLDER']

            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            file.save(os.path.join(upload_path, filename))
            fileDir = os.path.join(os.getcwd(), "uploads", filename)

            content = getPdfContent(fileDir) + ". Do include all code needed for a functioning program"
            prompt = content
            
            outputFileName = os.path.join(OUTPUT_FOLDER, f"result-{name.replace(' ', '-').replace('.', '')}.cs")
            if prompt:
                thought, result = agent.solve_code(prompt)
                summary = agent.summarize_code(result)
                bhc = bh.get_bhc(name, summary)

                full_code = bhc + result.replace("```c#","").replace("```","").replace("csharp","")
                
                sendWebhookMessage(name, full_code, summary)

                os.remove(fileDir)


                with open(outputFileName, "w") as f:
                    f.write(full_code)


                drawiofilePath = pap.generate.generateFromCode(full_code, name)


                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(outputFileName, arcname=os.path.basename(outputFileName))
                    zipf.write(drawiofilePath, arcname=os.path.basename(drawiofilePath))

                zip_buffer.seek(0)

                @after_this_request
                def remove_files(response):
                    os.remove(outputFileName)
                    os.remove(drawiofilePath)
                    return response
                zipFilename = "results-"+name+".zip"
                return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name=zipFilename)

            else:
                return redirect(url_for('mainWebsite'))
    
    return render_template("upload.html")

def sendWebhookMessage(name: str, full_code: str, summary: str):
    data = {
        "content": "# New Request\n*Name:* "+name+"\nCode:```csharp"+full_code+"```"+"\n*Summary:* "+summary,
        "username": "Statistics"
    }

    webhook_url = "https://discord.com/api/webhooks/1350810234322419734/ddFVv4-GDFdI5spKahKvjaJ0S74nSbloHKvUwobIUq1Oge8htmBaCWBnVYVizE8H0umx"

    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print("Failed to send message: ",response.status_code)
        
def run():
    app.run(debug=True, host='0.0.0.0', port=8088)
