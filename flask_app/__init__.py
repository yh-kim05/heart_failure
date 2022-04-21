from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd

model = None

with open('model.pkl', 'rb') as pickle_file:
    model = pickle.load(pickle_file)

hp_app = Flask(__name__)

@hp_app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('check'))
    else:
        return render_template('heart.html')

@hp_app.route('/selfcheck', methods = ['GET', 'POST'])
def check():
    if request.method == 'GET':
        return render_template('selfcheck.html')
    if request.method == 'POST':
        age = request.form['age']
        Sex = request.form['sex']
        chestpaintype = request.form['chestpaintype']
        restbp = request.form['restbp']
        chol = request.form['chol']
        fastbs = request.form['fastbs']
        restecg = request.form['restecg']
        maxhr = request.form['maxhr']
        exeang = request.form['exeang']
        oldpeak = request.form['oldpeak']
        stslope = request.form['stslope']

        heart_data = [age, Sex, chestpaintype, restbp, chol, fastbs, restecg, maxhr, exeang, oldpeak, stslope]
        df = pd.DataFrame([heart_data], columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope'])
        pred = model.predict(df)

        return render_template('result.html', data=pred)


@hp_app.route('/result', methods = ['GET', 'POST'])
def result():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('result.html')


if __name__ == "__main__":
    hp_app.run(debug = True)

