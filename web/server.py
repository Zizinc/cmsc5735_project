import cherrypy

from app import create_app
from engine import SparkEngine
from paste.translogger import TransLogger


def run_server(app):

    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5432,
        'server.socket_host': '0.0.0.0'
    })

    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 80,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == "__main__":
    # Init spark context and load libraries
    # sc = init_spark_context()
    spark_engine = SparkEngine()

    app = create_app(spark_engine)

    run_server(app)
