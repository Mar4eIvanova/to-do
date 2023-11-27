from flask import Flask, render_template, request, json, redirect, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, InputRequired
import os


app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///list.db')
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLES
class CreateList(db.Model):
    __tablename__ = "to_do"
    id = db.Column(db.Integer, primary_key=True)
    element = db.Column(db.String(250), nullable=False)


# with app.app_context():
#     db.create_all()


# CREATE FORM
class ToDo(FlaskForm):
    line = StringField('Type here e.g. buy bacon', validators=[DataRequired()])
    submit = SubmitField('Submit')


item_list = []

@app.route('/', methods=["GET", "POST"])
def home():

    form = ToDo()
    if form.validate_on_submit():
        new_element = form.line.data
        item_list.append(new_element)
        new_element = CreateList(element=form.line.data)
        db.session.add(new_element)
        db.session.commit()

        return redirect(url_for("to_do"))
    return render_template("index.html", form=form)


@app.route('/new_list', methods=["GET", "POST"])
def to_do():
    today = datetime.today().strftime('%d-%m-%Y')
    results = db.session.execute(db.select(CreateList.element))
    list_elements = results.scalars().all()
    form = ToDo()
    if form.validate_on_submit():
        new_element = form.line.data
        item_list.append(new_element)
        new_element = CreateList(element=form.line.data)
        db.session.add(new_element)
        db.session.commit()
        return redirect(url_for("to_do"))
    return render_template("new.html", element=item_list, form=form, today=today)

#element=list_elements


@app.route('/final_list')
def final():
    results = db.session.execute(db.select(CreateList.element))
    list_elements = results.scalars().all()
    form = ToDo()
    return render_template("crated.html", element=list_elements, form=form)


@app.route("/delete/<item>")
def delete_item(item):
    with app.app_context():
        item_to_delete = db.session.execute(db.select(CreateList).where(CreateList.element == item))
        db.session.delete(item_to_delete.scalar())
        db.session.commit()
        return redirect(url_for('final'))



if __name__ == "__main__":
    app.run(debug=True)
