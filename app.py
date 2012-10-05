from datetime import datetime

from flask import (
    Flask,
    request, redirect,
    url_for, flash,
    render_template)

from flaskext.sqlalchemy import SQLAlchemy

from flask.ext.wtf import (
        Form, SelectField,
        TextField,
        Email, Required)


app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)


class RegistrationForm(Form):
    """
    This is the form that registers a new attendee.
    """
    email = TextField("Email Address", [Required(), Email()])
    name = TextField("Your Full Name", [Required()])
    plan = SelectField(label="Extra Guests", choices=[('0', '0'), ('1', '1')], validators=[Required()])


class Registration(db.Model):
    """
    Stores the information about the registered attendee.
    """
    id = db.Column(db.Integer, primary_key=True, index=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, \
                        onupdate=datetime.utcnow)
    email = db.Column(db.String)
    name = db.Column(db.String)
    plan = db.Column(db.Integer)

def register_guest(name, email, plus):
    reg = Registration()
    reg.email = email
    reg.name = name
    reg.plus = int(plus)


@app.route('/')
def index():
    """
    The homepage, where the user comes when they visit the root of the domain.
    """
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    The registration page, where the user comes to register.
    """
    form = RegistrationForm()
    if form.validate_on_submit():

        # Register the user.
        register_guest(
            form.name.data,
            form.email.data,
            form.plan.data
        )

        # Flash a success message and redirect to the homepage.
        flash("You have been registed! We've sent the details to the email \
you provided. Thanks!")

        return redirect(url_for('index'))

    else:
        return render_template('register.html', form=form)

@app.route('/no-thanks')
def no_thanks():
    """
    The user comes here if they choose the no option out of the email.
    """
    return render_template('register.html')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(app.config['PORT'])
    app.run(host='0.0.0.0', port=port)
