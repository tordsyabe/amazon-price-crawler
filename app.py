from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from dataclasses import dataclass
from functools import wraps

from flask_sqlalchemy import SQLAlchemy

from amazon import amazon_crawler
from noon import noon_crawler
from rustoleum_batch_code import convert_batch_to_mfg
import os

def basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == os.environ.get("BASIC_AUTH_USERNAME") and auth.password == os.environ.get("BASIC_AUTH_PASSWORD"):
            return f(*args, **kwargs)

        return make_response("Could not verify login, go back <a href='/'>Home</a>", 401, {"WWW-Authenticate": "Basic realm='Login Required'"})

    return decorated


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@dataclass
class Email(db.Model):
    __tablename__ = "email"

    id: int = db.Column(db.Integer, primary_key=True)
    email_address: str = db.Column(db.String(255), nullable=False)
    employee_name: str = db.Column(db.String(64), nullable=False)
    designation: str = db.Column(db.String(64), nullable=False)
    status: str = db.Column(db.String(64), nullable=False)

    def __init__(self, email_address, employee_name, designation, status):
        self.email_address = email_address
        self.employee_name = employee_name
        self.designation = designation
        self.status = status


STATUS_CHOICE = [('active', 'Active'), ('restricted', 'Restricted'), ('inactive', "Inactive")]


class EmailForm(FlaskForm):
    email_address = StringField("Email Address", validators=[DataRequired()])
    employee_name = StringField("Employee", validators=[DataRequired()])
    designation = StringField("Designation", validators=[DataRequired()])
    status = SelectField(u'Status', choices=STATUS_CHOICE)


@app.route("/", methods=['GET'])
def index():
    return render_template('amazon-price.html')


@app.route("/rustoleum-batch-code", methods=['GET'])
def rustoleum_batch_code():
    return render_template('rustoleum-batch-code.html')


@app.route("/compute-batch-code", methods=['POST'])
def compute_batch_code():
    if request.method == 'POST':

        batch_code = request.form['batchCode']
        if batch_code == '':
            return render_template('rustoleum-batch-code.html', message='Please enter required fields')

        split_batch_code = batch_code.split(" ")
        print(split_batch_code)
        batch_codes = convert_batch_to_mfg(split_batch_code)

        print(batch_codes)

    return render_template('rustoleum-batch-code.html', batch_codes=batch_codes)


@app.route('/crawler', methods=['GET', 'POST'])
def crawler():
    if request.method == 'POST':

        url = request.form['url']
        if url == '':
            return render_template('amazon-price.html', message='Please enter required fields')

        split_url = url.split("/")
        table_data = {}

        print(split_url)

        for item in split_url:
            if "B" in item and len(item) == 10:
                table_data = amazon_crawler(url)
                break
            elif "N" in item and len(item) == 10:

                table_data = noon_crawler(url)
                break

        return render_template('amazon-price.html', table_data=table_data)


@app.route("/active-emails", methods=["GET", "POST"])
@basic_auth
def active_emails():
    form = EmailForm()

    emails = Email.query.all()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email_address.data
        empl = form.employee_name.data
        designation = form.designation.data
        status = form.status.data

        new_email = Email(email, empl, designation, status)

        db.session.add(new_email)
        db.session.commit()

        return redirect(url_for("active_emails"))

    return render_template("active-emails.html", form=form, emails=emails)


@app.route("/api/emails", methods=["GET"])
@basic_auth
def email_api():
    emails = Email.query.all()

    print(emails)

    return jsonify(emails)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

    app.debug(True)
