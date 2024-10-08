from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'voice_data_collection'
app.config['UPLOAD_FOLDER'] = 'static/recordings'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_user_data():
    if request.method == 'POST':
        age_group = request.form['age']
        gender = request.form['gender']
        region = request.form['region']

        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (age_group, gender, region) VALUES (%s, %s, %s)", (age_group, gender, region))
        mysql.connection.commit()
        user_id = cur.lastrowid
        cur.close()

        return redirect(url_for('record', user_id=user_id))


@app.route('/record/<int:user_id>', methods=['GET', 'POST'])
def record(user_id):
    if request.method == 'POST':
        file = request.files['audio_data']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO recordings (user_id, file_path) VALUES (%s, %s)", (user_id, file_path))
            mysql.connection.commit()
            cur.close()

        return 'Файл записан успешно!'

    return render_template('record.html')

if __name__ == '__main__':
    app.run(debug=True)
