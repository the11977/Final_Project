from flask import Flask, render_template
import os
app = Flask(__name__)

questions_data = {
   'question1' : 'When you are looking for a show to watch you tend to lean towards a comedy show versus a drama based one:',
   'fields'   : ['Agree', 'Disagree',  'Neither']
}

@app.route('/')
def root():
    return render_template('index.html', data=questions_data)
 
if __name__ == "__main__":
    app.run(debug=True)
 
 