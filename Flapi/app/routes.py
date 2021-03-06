from app import app
from flask import render_template,flash,redirect,url_for
from app.forms import LoginForm
from flask_login import logout_user,current_user, login_user
from flask import request,Response
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from flask_login import login_required
from app.models import User,Post, CrashLocationPoint
import logging
import json


from datadog import initialize, statsd

options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}

initialize(**options)

logging.basicConfig(level=logging.DEBUG)


app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)



@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    users = Post.query.all()
    for user in users:
        print (user.body)
    return render_template('index.html',title='Home', posts=users)

@app.route('/crashPoint/getAll', methods=['GET'])
def getAllPoints():
    dict = {}
    i = 0
    s1 = 'latitude '
    s2 = 'longitude '
    points = CrashLocationPoint.query.all()
    for point in points:
        lat = point.latitude
        long = point.longitude
        #print(lat)
        t1 = s1 + str(i)
        t2 = s2 + str(i)
        dict[t1] = lat
        dict[t2] = long
        i = i + 1
        statsd.set('point_loop_i', i, tags=["environment:laptop"])

    print(dict)
    jdict = json.dumps(dict)

    return Response(jdict, status=200, mimetype = 'application/json')


@app.route('/crashPoint/add', methods=['POST'])
#curl  -H "Content-Type: application/json" -d '{"username":"john","latitude":"56.66785675","longitude":"65.4344"}' 127.0.0.1:8000/crashPoint/add

#@login_required
def addCrashLocationPoint():
    point = CrashLocationPoint()
    incoming = request.get_json()
    point.latitude = incoming['latitude']
    point.longitude = incoming['longitude']
    point.user_id = incoming['username']
    db.session.add(point)
    db.session.commit()
    app.logger.info('point created by %s added',point.user_id)

    return Response("{'latitude': incoming['latitude']}", status=200, mimetype = 'application/json')


@app.route('/post/add', methods=['POST'])
# curl  -H "Content-Type: application/json" -d '{"username":"john","body":"whats up, alri"}' 127.0.0.1:8000/post/add
#@login_required
def addPost():
    post = Post()
    #print('post recieved')
    incoming = request.get_json()
    #print(incoming['username'])
    #print(incoming['body'])
    post.body = incoming['body']
    post.user_id = incoming['username']
    db.session.add(post)
    db.session.commit()
    app.logger.info('post created by %s added',post.user_id)

    return render_template('post.html',title='Home', post=post)





@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)




    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
