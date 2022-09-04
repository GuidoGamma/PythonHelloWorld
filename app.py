from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def home():  # put application's code here
    return render_template('index.html', title="Login pagina")


if __name__ == '__main__':
    app.run()
