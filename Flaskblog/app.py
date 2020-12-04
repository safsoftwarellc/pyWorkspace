# First Flask Project
# Flask Blogger

from flask import Flask, render_template
from forms import RegistrationForm, LoginForm

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

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)
