from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'clave-secreta'

# Configuración para almacenar sesiones en el sistema de archivos
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Lista global para almacenar mensajes
messages = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name
        return redirect('/chat')
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'name' not in session:
        return redirect('/')
    if request.method == 'POST':
        message = request.form['message']
        messages.append({'name': session['name'], 'message': message})
    return render_template('chat.html', messages=messages, name=session['name'])

@app.route('/get_messages')
def get_messages():
    return jsonify(messages)

@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect('/')
