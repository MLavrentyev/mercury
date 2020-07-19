from flask import Flask, render_template
from flask_socketio import SocketIO, send
from data.data import DataPoint


app = Flask("Mercury", template_folder="src/web/templates", static_folder="src/web/static")
websocket = SocketIO(app)


@app.route("/")
def main():
    return render_template("main.html.jinja2")


@app.errorhandler(404)
def pageNotFound():
    return render_template('404.html.jinja2'), 404


def sendData(socket: SocketIO, data: DataPoint):
    ...


if __name__ == "__main__":
    websocket.run(app)
