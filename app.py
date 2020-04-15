from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Rdiafuego9$@localhost/Feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tableName__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), unique=True)
    Q1 = db.Column(db.Text)
    Q2 = db.Column(db.Text)
    Q3 = db.Column(db.Text)
    Q4 = db.Column(db.Text)
    Q5 = db.Column(db.Text)
    Q6 = db.Column(db.Text)
    Q7 = db.Column(db.Text)

    def __init__(self, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7):
        self.Name = Name
        self.Q1 = Q1
        self.Q2 = Q2
        self.Q3 = Q3
        self.Q4 = Q4
        self.Q5 = Q5
        self.Q6 = Q6
        self.Q7 = Q7


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        Name = request.form.get('Name')
        Q1 = request.form.get('Q1')
        Q2 = request.form.get('Q2')
        Q3 = request.form.get('Q3')
        Q4 = request.form.get('Q4')
        Q5 = request.form.get('Q5')
        Q6 = request.form.get('Q6')
        Q7 = request.form.get('Q7')

        # print(Q1, Q2, Q3, Q4, Q5, Q6, Q7)

    if Name == "":
        return render_template('index.html', message='Please enter required fields')
    if db.session.query(Feedback).filter(Feedback.Name == Name).count() == 0:
        data = Feedback(Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7)
        db.session.add(data)
        db.session.commit()
        send_mail(Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7)
    return render_template('success.html')

    return render_template(
        'index.html',
        message='You have already submitted feedback'
        )


if __name__ == '__main__':
    app.run()