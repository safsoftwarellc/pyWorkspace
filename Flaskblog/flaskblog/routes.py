
from flask import render_template, flash, redirect, url_for
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

posts = [
    {
        "title": "Blog Post 1",
        "author": "John Doe",
        "content": "This is the latest post for this Blog",
        "date": "Jan 21 2020"
    },
    {
        "title": "Blog Post 2",
        "author": "Marry Bush",
        "content": "This is the OLD post for this Blog",
        "date": "Apr 08 2018"
    }
]


@ app.route("/")
@ app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@ app.route("/about")
def about():
    return render_template('about.html', title='About')


@ app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'User Created {{form.username.data}}', 'success')
        return redirect(url_for('home'))
    # else:
    #    flash(f'User Created {{form.username.data}}', 'success')
    return render_template('register.html', title='Register', form=form)


@ app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
