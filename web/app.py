from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action_package/add')
def add_action_package():
    triggerHTML = open("templates/snippets/add_action_package/action/trigger/pattern.html", "r").read().replace('\n', '').replace('\r', '').replace('"', '\\"')
    print(repr(triggerHTML))
    return render_template('add_action_package.html', triggerHTML=triggerHTML)

@app.route('/is-assistant-running')
def is_assistant_running():
    try:
        return "Running" if 'active (running)' in str(subprocess.check_output("systemctl status assistant.service", shell=True)) else "Halted"
    except:
        return "Halted"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
