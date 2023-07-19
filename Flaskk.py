from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    # Get the form values
    value1 = request.form['value1']
    value2 = request.form['value2']
    value3 = request.form['value3']
    value4 = request.form['value4']
    value5 = request.form['value5']

    # Pass the values to the Python file and print them
    subprocess.call(['python', 'ShopifyApp.py', value1, value2, value3, value4, value5])

    return 'Script executed successfully!'

if __name__ == '__main__':
    app.run()