from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/add_action')
def add_action():
    return render_template('add_action.html')    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
