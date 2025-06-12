from app import answer
from flask import Flask, render_template, request

app = Flask(__name__)

conversations = []

@app.route('/', methods=['GET', 'POST'])

def home():
    if request.method == 'GET':
        return render_template('index.html')
    if request.form['question']:
        question = 'Me: ' + request.form['question']

        result = answer(question)
        respuesta = 'Assistent AI: ' + result

        conversations.append(question)
        conversations.append(respuesta)

        return render_template('index.html', chat = conversations)
    else:
        return render_template('index.html')

    

if __name__ == '__main__':
    app.run(debug=True, port=4000)