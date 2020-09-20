from flask import *  # import flask
from stars import *
import music

app = Flask(__name__)  # create an app instance


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/query')
def get_star_data():
    zip_code = request.args.get("zipcode")
    date = request.args.get("date")
    star_data = get_stars(zip_code, date)
    music.generate_music(star_data)
    return render_template("index.html", data=star_data)


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
