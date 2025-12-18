from flask import Flask, render_template, request, send_file
from models import db, Teacher
from scheduler import generate_multiple_timetables
import pandas as pd
import io
from xhtml2pdf import pisa
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

@app.route('/')
def index():
    teachers = Teacher.query.all()
    return render_template('index.html', teachers=teachers)

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    name = request.form['name'].strip()
    subject = request.form['subject'].strip()
    periods = int(request.form['periods'])
    span = int(request.form.get('span', 1))
    db.session.add(Teacher(name=name, subject=subject, periods=periods, span=span))
    db.session.commit()
    return render_template('index.html', teachers=Teacher.query.all(), msg="Teacher added successfully!")

@app.route('/generate', methods=['POST'])
def generate():
    num_timetables = int(request.form['num_timetables'])
    periods_per_day = int(request.form['periods_per_day'])
    teachers = Teacher.query.all()

    if not teachers:
        return render_template('index.html', msg="Please add at least one teacher before generating.")

    data = [{"name": t.name, "subject": t.subject, "periods": t.periods, "span": t.span or 1} for t in teachers]
    timetables = generate_multiple_timetables(data, DAYS, periods_per_day, num_timetables)

    return render_template('timetable.html',
                           timetables=timetables,
                           days=DAYS,
                           periods=periods_per_day,
                           num_timetables=num_timetables)

if __name__ == '__main__':
    print("DB Path:", os.path.abspath("timetable.db"))
    app.run(debug=True)
