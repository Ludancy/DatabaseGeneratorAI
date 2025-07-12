# main.py
from app import answer
from flask import Flask, render_template, request

app = Flask(__name__)

conversations = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    if request.form['question']:
        user_question_text = request.form['question'] # Store the raw user question
        question_for_display = 'Me: ' + user_question_text # For display in chat history

        # Pass only the clean user question to the answer function
        result = answer(user_question_text)
        respuesta = 'Assistent AI: ' + result

        conversations.append(question_for_display) # Add the "Me: " prefixed version for display
        conversations.append(respuesta)

        return render_template('index.html', chat = conversations)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=4000)