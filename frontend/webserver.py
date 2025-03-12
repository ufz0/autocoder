from flask import Flask, render_template, request, redirect, url_for
import formatter
import ai.invoke as invoke
import ai.agent as agent
import formatter.blockheadercomment

app = Flask(__name__)

@app.route("/")
def mainWebsite():
    return render_template('index.html')

@app.route("/prompt", methods=["GET", "POST"])
def sendPrompt():
    prompt = request.form.get('prompt') if request.method == "POST" else request.args.get('prompt')
    name = request.form.get('name') if request.method == "POST" else None

    if prompt:
        thought, result = agent.solve_code(prompt)
        summary = agent.summarize_code(result)
        bhc = formatter.blockheadercomment.get_bhc(name, summary)

        full_code = bhc+result

        # Include the name in the rendered template
        return render_template('result.html', result=full_code, summary=summary, thought=thought, name=name)
    else:
        return redirect(url_for('mainWebsite'))

def run():
    app.run(debug=True)
