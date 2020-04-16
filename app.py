from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
import logging


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense
import numpy as np
import pandas as pd

import psycopg2
import pandas.io.sql as psql

from sqlalchemy import create_engine



#Pull data for training and testing



engine = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="password",
    host="final-project2.cqjpvyvxep2w.us-east-2.rds.amazonaws.com",
    port='5432'
)

train_df = psql.read_sql("SELECT * FROM public.train", engine)
xtrain_df = psql.read_sql("SELECT * FROM public.xtr1", engine)
ytrain_df = psql.read_sql("SELECT * FROM public.ytr1", engine)


engine2 = create_engine('postgresql://postgres:password@final-project2.cqjpvyvxep2w.us-east-2.rds.amazonaws.com:5432/postgres')

# feedback_df.to_sql('train', con = engine2, if_exists = 'append', chunksize = 1000)


#Initiate ML and train model off dummy data

#One-hot encoding and x-y split

train_q1 = xtrain_df["q1"]
train_q2 = xtrain_df["q2"]
train_q3 = xtrain_df["q3"]
train_q4 = xtrain_df["q4"]
train_q5 = xtrain_df["q5"]
train_q6 = xtrain_df["q6"]
train_q7 = ytrain_df["q7"]

train_h1 = pd.get_dummies(train_q1,prefix=['q1'])
train_h2 = pd.get_dummies(train_q2,prefix=['q2'])
train_h3 = pd.get_dummies(train_q3,prefix=['q3'])
train_h4 = pd.get_dummies(train_q4,prefix=['q4'])
train_h5 = pd.get_dummies(train_q5,prefix=['q5'])
train_h6 = pd.get_dummies(train_q6,prefix=['q6'])
train_h7 = pd.get_dummies(train_q7,prefix=['q7'])

x_train = pd.concat([train_h1, train_h2, train_h3,train_h4,train_h5,train_h6], axis=1)
y_train = train_h7

x_train = x_train.values
y_train = y_train.values




# Create an empty sequential model
model = Sequential()

# Add the first layer
model.add(Dense(100, activation='relu', input_dim=x_train.shape[1]))

# Add a second hidden layer
model.add(Dense(100, activation='relu'))

# Add output layer
model.add(Dense(y_train.shape[1], activation="softmax"))

# Compile the model using categorical_crossentropy for the loss function, the adam optimizer,
# and add accuracy to the training metrics
model.compile(loss="categorical_crossentropy",
              optimizer="adam", metrics=['accuracy'])

model.fit(
    x_train,
    y_train,
    epochs=100,
    shuffle=True,
    verbose=2
)

# Save the model
model.save("questions_trained.h5")

# Load the model
from tensorflow.keras.models import load_model
model = load_model("questions_trained.h5")


model_loss, model_accuracy = model.evaluate(x_train, y_train, verbose=2)
print(f"Loss: {model_loss}, Accuracy: {model_accuracy}")


app = Flask(__name__)

# ENV = 'dev'

# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@final-project2.cqjpvyvxep2w.us-east-2.rds.amazonaws.com:5432/postgres'
# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = ''

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


# class Feedback(db.Model):
#     __tableName__ = 'Feedback'
#     id = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.Text)
#     q1 = db.Column(db.Text)
#     q2 = db.Column(db.Text)
#     q3 = db.Column(db.Text)
#     q4 = db.Column(db.Text)
#     q5 = db.Column(db.Text)
#     q6 = db.Column(db.Text)
#     q7 = db.Column(db.Text)



#     def __init__(self, Name, Q1, Q2, Q3, Q4, Q5, Q6):
#         self.Name = Name
#         self.Q1 = Q1
#         self.Q2 = Q2
#         self.Q3 = Q3
#         self.Q4 = Q4
#         self.Q5 = Q5
#         self.Q6 = Q6








@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        Q7 = request.form.get('Q7')
        if Q7 != None:
            feedback2_df = pd.DataFrame({"q7":[Q7]})
            feedback2_df.to_sql('ytr1', con = engine2, if_exists = 'append', chunksize = 1000, index=False)
            return render_template('index.html')

        Name = request.form.get('Name')
        Q1 = request.form.get('Q1')
        Q2 = request.form.get('Q2')
        Q3 = request.form.get('Q3')
        Q4 = request.form.get('Q4')
        Q5 = request.form.get('Q5')
        Q6 = request.form.get('Q6')
        
        # print(f"6 {Q6}")
        # print(f"7: {Q7}")



        feedback_df = pd.DataFrame({
                    "q1":[Q1],
                    "q2":[Q2],
                    "q3":[Q3],
                    "q4":[Q4],
                    "q5":[Q5],
                    "q6":[Q6]})


        test_df = psql.read_sql("SELECT * FROM public.test", engine)
        test_df = test_df.append(feedback_df, ignore_index = True) 
        
        feedback_df.to_sql('xtr1', con = engine2, if_exists = 'append', chunksize = 1000, index=False)
        engine2.execute('delete from public.xtr1 where Q1 is null')



        test_q1 = test_df["q1"]
        test_q2 = test_df["q2"]
        test_q3 = test_df["q3"]
        test_q4 = test_df["q4"]
        test_q5 = test_df["q5"]
        test_q6 = test_df["q6"]

        test_h1 = pd.get_dummies(test_q1,prefix=['q1'])
        test_h2 = pd.get_dummies(test_q2,prefix=['q2'])
        test_h3 = pd.get_dummies(test_q3,prefix=['q3'])
        test_h4 = pd.get_dummies(test_q4,prefix=['q4'])
        test_h5 = pd.get_dummies(test_q5,prefix=['q5'])
        test_h6 = pd.get_dummies(test_q6,prefix=['q6'])


        x_test = pd.concat([test_h1, test_h2, test_h3 , test_h4 , test_h5 , test_h6], axis=1)
        
        features1 = len(x_test.columns)


        x_test = x_test.values

        test = np.expand_dims(x_test[len(x_test)-1], axis=0)

        print(f"Predicted class: {model.predict_classes(test)}")
        guess1 = model.predict_classes(test)

        if guess1 == 0:
            guess2 = "No"
        elif guess1 == 1:
            guess2 = "Yes"

        entries1 = len(x_train)


        # test_df = test_df.drop(columns=['name'])

        # print(Q1, Q2, Q3, Q4, Q5, Q6)

        # feedback_df.to_sql('Feedback', con = engine2, if_exists = 'append', chunksize = 1000)


    if Name == "":
        return render_template('index.html', message='Please enter required fields')
    # if db.session.query(Feedback).filter(Feedback.Name == Name).count() == 0:
    #     data = Feedback(Name, Q1, Q2, Q3, Q4, Q5, Q6)
    #     db.session.add(data)
    #     db.session.commit()
    #     send_mail(Name, Q1, Q2, Q3, Q4, Q5, Q6)
    
    if Name != None:
        
        #Use feedback frame to generate test data
        # feedback1
        

        send_mail(Name, Q1, Q2, Q3, Q4, Q5, Q6)
    return render_template('success.html', guess = guess2, accuracy = model_accuracy, entries = entries1, features = features1)


    return render_template(
        'index.html',
        message='You have already submitted feedback'
        )


if __name__ == '__main__':
    app.run()
