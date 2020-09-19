from flask import *                 # import flask
app = Flask(__name__)               # create an app instance


# @app.route("/")                   # at the end point /
# def index():                      # call method hello
#     return render_template('index.html')


@app.route("/data")
def cade():
    people = ["Cade", "Cole", "Katherine", "Lizzie"]
    return {
        "people": people
    }


@app.route('/')
def login():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == "__main__":          # on running python app.py
    app.run(debug=True)             # run the flask app
