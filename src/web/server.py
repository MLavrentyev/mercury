import logging
import click
from flask import Flask, render_template
from utils.config import Config


def turnOffFlaskLogging():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    def secho(text, file=None, nl=None, err=None, color=None, **styles):
        pass

    def echo(text, file=None, nl=None, err=None, color=None, **styles):
        pass

    click.echo = echo
    click.secho = secho


def createApp(config: Config) -> Flask:
    appName: str = config.getSetting("dashboard.app.name")
    app = Flask(appName, template_folder="src/web/templates", static_folder="src/web/static")

    @app.route("/")
    def main():
        websocketPort: int = config.getSetting("dashboard.websocket.port")
        return render_template("main.html.jinja2", websocketPort=websocketPort)

    return app
