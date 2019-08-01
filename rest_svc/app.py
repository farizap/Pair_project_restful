from flask import Flask, request
from flask_restful import Api
import logging, sys
from logging.handlers import RotatingFileHandler


from blueprints import app, manager

from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

######################################

## initiate flask-restful instance
api = Api(app, catch_all_404s=True)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'db':
            manager.run()
    except Exception as e:
        # define log format and create a rotating log with max size of 10mb and max backup to 10 files
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)s} %(levelname)s - %(message)s")
        log_handler = RotatingFileHandler("%s/%s" %(app.root_path, '../storage/log/app.log'), maxBytes=10000000, backupCount=10)
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)


    app.run(debug=True, host='0.0.0.0', port=5000)

