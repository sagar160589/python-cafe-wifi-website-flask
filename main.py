from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SelectField, SubmitField, URLField
from wtforms.validators import DataRequired
import csv


class CoffeeForm(FlaskForm):
    name = StringField(label='Name', validators = [DataRequired()])
    location = StringField(label='Location', validators = [DataRequired()])
    openTime = StringField(label='Open Time', validators = [DataRequired()])
    closeTime = StringField(label='Close Time', validators=[DataRequired()])
    coffee = SelectField(label='Coffee', choices=['☕','☕☕','☕☕☕','☕☕☕☕'])
    wifi = SelectField(label='Wifi', choices=['💪','💪💪','💪💪💪','💪💪💪💪','✘'])
    power = SelectField(label='Power',choices=['🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌'])
    submit = SubmitField(label='Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/cafes')
def all_cafes():
    with open('cafe-data.csv', mode='r', encoding="utf8") as cafes:
        column_list = []
        row_list = []
        spamreader = csv.reader(cafes, delimiter=',')
        line_count = 0
        for row in spamreader:
            if line_count == 0:
                column_list.extend(row)
                line_count += 1
            else:
                row_list.append(row)
                line_count += 1
    return render_template('cafes.html', cafe_columns = column_list, cafe_rows= row_list)

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    print(request.method)
    coffeeForm = CoffeeForm()
    if coffeeForm.validate_on_submit():
        coffee_add = [coffeeForm.name.data, coffeeForm.location.data, coffeeForm.openTime.data,
                      coffeeForm.closeTime.data, coffeeForm.coffee.data, coffeeForm.wifi.data, coffeeForm.power.data]

        with open('cafe-data.csv', mode='a', encoding="utf8", newline='') as cafes:
            csvwriter = csv.writer(cafes)
            csvwriter.writerow(coffee_add)
        return redirect(url_for('all_cafes'))

    return render_template('add.html', cafe_form = coffeeForm )


if __name__ == ('__main__'):
    app.run(debug=True)