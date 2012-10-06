from datetime import datetime

from flask import (
    Flask,
    redirect, url_for,
    flash, render_template)

from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.wtf import (
    Form, SelectField,
    TextField,
    Email, Required)

import sendgrid

app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)
mailer = sendgrid.Sendgrid(app.config['SENDGRID_USERNAME'],
                           app.config['SENDGRID_PASSWORD'],
                           secure=True)


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    email = db.Column(db.String)
    name = db.Column(db.String)
    plan = db.Column(db.Integer)


def register_guest(name, email, plus):
    reg = Registration()
    reg.email = email
    reg.name = name
    reg.plus = int(plus)
    db.session.add(reg)
    try:
        db.session.commit()
        return reg
    except:
        return None


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
        reg = register_guest(
            form.name.data,
            form.email.data,
            form.plan.data
        )

        if not reg:
            flash("Sorry! We were unable to register you!")

        # Flash a success message and redirect to the homepage.
        flash("You have been registed! We've sent the details to the email \
you provided. Thanks!")

        m_subject = "Your invite to an exclusive event"
        m_body = "YES"
        m_html = "YES"

        message = sendgrid.Message(('invites@kiip.com', 'Kiip Invites'),
                                   m_subject, m_body, m_html)

        message.add_to(form.email.data, form.name.data)
        mailer.web.send(message)

        return redirect(url_for('index'))

    else:
        return render_template('register.html', form=form)


@app.route('/no-thanks')
def no_thanks():
    """
    The user comes here if they choose the no option out of the email.
    """
    return render_template('no-thanks.html')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(app.config['PORT'])
    app.run(host='0.0.0.0', port=port)
