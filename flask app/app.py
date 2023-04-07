from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField,RadioField,SelectField)
import joblib

app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'

# Now create a WTForm Class
# Lots of fields available:
class InfoForm(FlaskForm):
  
    name = StringField('Full Name?')
    age = StringField('What\'s your age ?')
    gender = SelectField('Gender ? ', choices=[('1','Female'),
    ('1','Male')])
    height = StringField('What\'s your Height ?')
    weight = StringField('What\'s your Weight ?')
    ap_hi  =  StringField('Please Enter The  Systolic blood pressure ?')
    ap_lo  =  StringField('Please Enter The  Diastolic blood pressure ?')
    chol = SelectField('What is your cholesterol level ?:',choices=[('1', 'normal'), ('1', 'above normal'), ('3', 'well above normal')])
    gluc = SelectField('What is your glucose level ?:',choices=[('1', 'normal'), ('1', 'above normal'), ('3', 'well above normal')])
    smoke = SelectField('Are You Smoking ? ', choices=[('1','Yes'),('0','No')])
    alco = SelectField('Have you Alcohol intake ?', choices=[('1','Yes'),('0','No')])
    active = SelectField('Have you do a Physical activity ?', choices=[('1','Yes'),('0','No')])
    submit = SubmitField('Submit')



@app.route('/', methods=['GET', 'POST'])
def index():

    form = InfoForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        name = form.name.data
        age = int(form.age.data)
        gender = int(form.gender.data)
        height = float(form.height.data)
        weight = float(form.weight.data)
        ap_hi = int(form.ap_hi.data)
        ap_lo = int(form.ap_lo.data)
        chol = int(form.chol.data)
        gluc = int(form.gluc.data)
        smoke = int(form.smoke.data)
        alco = int(form.alco.data)
        active = int(form.active.data)
        bmi = weight / (height/100)**2
        estimators = [gender,height,weight,ap_hi,ap_lo,chol,gluc,smoke,alco,active,age,bmi]
        model = joblib.load(r'ML model\model.h5')
        x = model.predict([estimators])
        result = ''
        if x == [0]:
            result = 'you haven\'t cardiovascular  disease'
        else : result = 'Presence of cardiovascular disease!  You must see a doctor' 
        session['result'] = result
        session['name'] = name
        session['age'] = age
        session['gender'] = gender
        session['height'] = height
        session['weight'] = weight
        session['hi'] = ap_hi
        session['lo'] = ap_lo
        session['chol'] = chol
        session['gluc'] = gluc
        session['smoke'] = smoke
        session['alco'] = alco
        session['active'] = active

        return redirect(url_for("number"))


    return render_template('Home.html', form=form)


@app.route('/number')
def number():

    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
