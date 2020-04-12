from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from send_mail import send_mail

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
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    Q1 = db.Column(db.String())
    Q2 = db.Column(db.String())
    Q3 = db.Column(db.String())
    Q4 = db.Column(db.String())
    Q5 = db.Column(db.String())
    Q6 = db.Column(db.String())
    Q7 = db.Column(db.String())
    

    def __init__(self, Q1, Q2, Q3, Q4, Q5, Q6, Q7):
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
        Q1 = request.form['Q1']
        Q2 = request.form['Q2']
        Q3 = request.form['Q3']
        Q4 = request.form['Q4']
        Q5 = request.form['Q5']
        Q6 = request.form['Q6']
        Q7 = request.form['Q7']

        #print(Q1, Q2, Q3, Q4, Q5, Q6, Q7)
         
    if Q1 == '' or Q2 == '' or Q3 == '' or Q4 == '' or Q5 == '' or Q6 == '' or Q7 == '':
        return render_template('index.html', message='Please enter required fields')
    
    if db.session.query(Feedback).filter(Feedback.Q1 == Q1).count() == 0:
        data = Feedback(Q1, Q2, Q3, Q4, Q5, Q6, Q7)
        db.session.add(data)
        db.session.commit()            
        #send_mail(Q1, Q2, Q3, Q4, Q5, Q6, Q7)
        return render_template('success.html')

    return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
#   app.debug = True
    app.run()
