import argparse
import shutil
import sys
from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer


# Settings
# =============
DEBUG = True
# FREEZER_DESTINATION = '../'
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'


# CLI
# =============
parser = argparse.ArgumentParser(
  description='Flask app for generating website.'
)

## dummy init and reset for the shell script
shellscript = 'flasksite'
parser.add_argument(
  'activate', action='store_true',
  help=f'run \'source {shellscript} activate\' to activiate the virtualenv for Flask app.'
)
parser.add_argument(
  'init', action='store_true',
  help=f'run \'{shellscript} init\' to initialize the virtualenv.'
)
parser.add_argument(
  'reset', action='store_true',
  help=f'run \'{shellscript} reset\' to remove and reinitialize the virtualenv.'
)

## option to host the flask app
parser.add_argument(
  '-l', '--live', action='store_true',
  help='host the app live on localhost.'
)

## option to build static site
parser.add_argument(
  '-b', '--build', action='store_true',
  help='build static site.'
)

if len(sys.argv) < 2:
  parser.print_help()
  sys.exit(1)
else:
  args = parser.parse_args()


# Flask app
# =============
app = Flask(__name__)
app.config.from_object(__name__)
freezer = Freezer(app)
pages = FlatPages(app)

## Homepage
@app.route('/')
def index():
  return render_template('index.html', pages=pages)

## Render FlatPages
@app.route('/<path:path>/')
def page(path):
  page = pages.get_or_404(path)
  return render_template('page.html', page=page)


# Build or host
# =============
if args.build:
  freezer.freeze()
  shutil.move('build', '../')

if args.live:
  app.run(debug=True)