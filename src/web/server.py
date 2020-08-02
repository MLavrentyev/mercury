import logging
import click
from flask import Flask, render_template


app = Flask("Mercury", template_folder="src/web/templates", static_folder="src/web/static")


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
    return render_template("main.html.jinja2", websocketPort=80)
