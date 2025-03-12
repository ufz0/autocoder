from flask import Flask, render_template, request, redirect, url_for
import ai.invoke as invoke
import ai.agent as agent

app = Flask(__name__)

@app.route("/")
def mainWebsite():
    return render_template('index.html')

@app.route("/prompt", methods=["GET", "POST"])
def sendPrompt():

    prompt = request.form.get('prompt') if request.method == "POST" else request.args.get('prompt')
    if prompt:
        result = agent.solve_code(prompt)
        summary = agent.summarize_code(result)

        return render_template('result.html', result=result, summary=summary)
    else:
        return redirect(url_for('mainWebsite'))

def run():
    app.run(debug=True)
