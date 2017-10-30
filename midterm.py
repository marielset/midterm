from flask import Flask, render_template, request, make_response, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required
import json
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "myFunsecretKey"

class NameForm(FlaskForm):
    name = StringField('What movies have you bought?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('main_page.html')

@app.route('/movie')
def move_form():
    return render_template('movie_form.html')
## look for maybe actors in tv shows

@app.route('/movieinfo', methods=['POST', 'GET'])
def movie_songs():
    if request.method == 'GET':
        result = request.args
        movie = result.get('movie')
        base_url = 'https://itunes.apple.com/search?entity=movie&limit=5&term='
        url = base_url + movie
        resp = requests.get(url)
        data = json.loads(resp.text)
        return render_template('movie_page.html', objects=data['results'], amount=data['resultCount'])
        

@app.route('/bought_movies')
def bought_movies():
    simple_Form = NameForm()
    # resp = make_response(render_template('first.html', form=simple_Form))
    # resp.set_cookie('name', 'name')
    # return resp
    return render_template('first.html', form=simple_Form)

@app.route('/result', methods=['POST', 'GET'])
def result():
    form = NameForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # movie = request.cookies.get('name')
        name = form.name.data
        string = "Your movie name is {0}".format(name)
        base_url = 'https://itunes.apple.com/search?entity=movie&limit=5&term='
        url = base_url + name
        resp = requests.get(url)
        data = json.loads(resp.text)
        string += " and it's price is ${0}".format(data['results'][0]['trackPrice'])
        return string
    flash('All fields are required!')
    return redirect(url_for('bought_movies'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def another_issue(e):
    return render_template('500.html')


if __name__ == '__main__':
    app.run(debug = True)



## make a request to the location and play with the response object. or use shell and print out the cookie?