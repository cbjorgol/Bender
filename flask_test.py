#!python3 Flask
# streaming clock per http://flask.pocoo.org/docs/1.0/patterns/streaming

from flask import Flask, Response, render_template, url_for
from datetime import datetime
import time

app = Flask(__name__)


NPV_DIFF = 80000000
FREQ = "Today's"
REF_DATE = datetime(2017, 9, 30, 0, 0)

@app.route('/')
def index():
    return render_template('index.html')

def get_value(npv_diff):
    npv_per_period = npv_diff / 365.
    ref_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    multiplier = 1
    time_this_week = datetime.now() - ref_date
    pct_of_day = time_this_week.total_seconds() / float(multiplier * 24 * 60 * 60)
    return '${:,.0f}'.format(pct_of_day * npv_per_period)

@app.route('/time_feed')
def time_feed():
    def generate():
        yield get_value(NPV_DIFF)  # return also will work
    return Response(generate(), mimetype='text')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)