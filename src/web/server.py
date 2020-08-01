import logging
import click
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from data.data import DataPoint


app = Flask("Mercury", template_folder="src/web/templates", static_folder="src/web/static")
websocket = SocketIO(app)


def turnOffFlaskLogging():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    def secho(text, file=None, nl=None, err=None, color=None, **styles):
        pass

    def echo(text, file=None, nl=None, err=None, color=None, **styles):
        pass

    click.echo = echo
    click.secho = secho


@app.route("/")
def main():
    return render_template("main.html.jinja2")


@app.errorhandler(404)
def pageNotFound():
    return render_template('404.html.jinja2'), 404


def sendData(socket: SocketIO, data: DataPoint):
    socket.send(data.toDictionary())
