from JobtransparencyNLP import app
from flask import render_template
import nltk
nltk.download('all')

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)