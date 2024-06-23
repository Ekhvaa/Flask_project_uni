from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from api import Film


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdashdkashdasp2131231231sadhagsdgad123oi1hoaisipd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main1.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    film_title = db.Column(db.String(100), nullable=False)
    film_genre = db.Column(db.String(100), nullable=False)
    film_rating = db.Column(db.Float, nullable=False)
    film_plot = db.Column(db.Text, nullable=False)
    film_poster_link = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f'ფილმია -- {self.film_title}'


with app.app_context():
    db.create_all()


@app.route('/')
def main():
    if 'searching' in request.args:
        search = request.args['searching']
        if search =='':
            flash('Enter Film name you want to find!')
        else:
            movie = Film(search)
            t = movie.title
            g = movie.genres
            r = movie.rating
            p = movie.plot()
            poster = movie.poster
            filmi = Movies(film_title=t, film_genre=g, film_rating=r, film_plot=p, film_poster_link=poster)
            db.session.add(filmi)
            db.session.commit()
            return redirect(url_for('search'))

    return render_template("index.html")


@app.route('/search')
def search():
    latest_movie = Movies.query.order_by(Movies.id.desc()).first()
    return render_template('search.html',
            movie_title=latest_movie.film_title,
            movie_genre=latest_movie.film_genre,
            movie_rating=latest_movie.film_rating,
            movie_plot=latest_movie.film_plot,
            movie_poster=latest_movie.film_poster_link)


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/history')
def history():

    all_movies = Movies.query.all()
    
    return render_template("history.html",all_films = all_movies)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/profile")
def profile():
    user = session.get("username", None)
    return render_template("profile.html", user=user)


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        if user=='' or passw=='':
            flash('Username or password is not filled.')
        else:
            user1 = User(username = user , password = generate_password_hash(passw))
            db.session.add(user1)
            db.session.commit()
            session['username']= user
            return redirect('/home')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/home')


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html"), 404


if __name__=="__main__":
    app.run(debug=True)

# ABOUT ERRORHANDLER FUNCTION
# ჩვენს პროექტში ჩავამატეთ errorhandler დეკორატორი, რომელიც კონკრეტულ შემთხვევაში უზრუნველყოფს, რომ თუ მომხმარებელი სერჩბარში
# შეეცდება გადავიდეს საიტის არარსებულ ფეიჯზე, გამოუგდოს custom ფეიჯი, რომლის კოდი 404.html-შია. ამ ფუნქციონალის მეორენაირად,
# დეკორატორის გარეშე შეიძლება ჯერ error_404 ფუნქციის გაწერით, შემდგომ კი app.register_error_handler(request code ამ შემთხვევაში 404, ფუნქცია error handling-ისთვის ამ შემთხვევაში error_404)
# pyhtonanywhere link: https://ekhva.pythonanywhere.com/

