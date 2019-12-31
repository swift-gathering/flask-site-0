from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import sys

DEBUG = True
# FREEZER_DESTINATION = '../'
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
freezer = Freezer(app)
pages = FlatPages(app)

# Homepage
@app.route('/')
def index():
  return render_template('index.html', pages=pages)

# Render FlatPages
@app.route('/<path:path>/')
def page(path):
  page = pages.get_or_404(path)
  return render_template('page.html', page=page)


if __name__ == '__main__':
  if (len(sys.argv)>1) and (sys.argv[1] == 'live'):
    app.run(debug=True)
  else:
    freezer.freeze()
