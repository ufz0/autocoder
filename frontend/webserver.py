from flask import Flask
from flask import send_file
from flask import request
import ai.invoke as invoke
import ai.agent as agent


app = Flask(__name__)

@app.route("/")
def mainWebsite():
    try:
        return send_file('index.html')
    except Exception as e:
       return str(e)

@app.route("/test")
def sendPrompt():
    prompt = request.args.get('prompt')
    result = agent.solve_code(prompt)
    summary = agent.summarize_code(result)    
    output = [result, summary]
    return output

def run():
    app.run(debug=True)