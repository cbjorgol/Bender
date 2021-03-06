#!python3 Flask
# streaming clock per http://flask.pocoo.org/docs/1.0/patterns/streaming

from flask import Flask, Response, render_template, url_for
from datetime import datetime
import time

app = Flask(__name__)


NPV_DIFF1 = 80000000
NPV_DIFF2 = 65000000
NPV_DIFF3 = 27000000
FREQ = "Today's"
REF_DATE1 = datetime(2019, 1, 1, 0, 0)
REF_DATE2 = datetime(2019, 4, 1, 0, 0)
REF_DATE3 = None

@app.route('/')
def index():
    return render_template('index.html')

def get_value(npv_diff, ref_date=None):
    npv_per_period = npv_diff / 365.

    # This is the index date/time
    if ref_date is None:
        ref_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    multiplier = 1
    time_this_week = datetime.now() - ref_date
    pct_of_day = time_this_week.total_seconds() / float(multiplier * 24 * 60 * 60)
    return '${:,.0f}'.format(pct_of_day * npv_per_period)

@app.route('/time_feed')
def time_feed():
    def generate():
        yield get_value(NPV_DIFF1, ref_date=REF_DATE1)  # return also will work
    return Response(generate(), mimetype='text')

@app.route('/time_feed2')
def time_feed2():
    def generate():
        yield get_value(NPV_DIFF2, ref_date=REF_DATE2)  # return also will work
    return Response(generate(), mimetype='text')

@app.route('/time_feed3')
def time_feed3():
    def generate():
        yield get_value(NPV_DIFF3, ref_date=REF_DATE3) # return also will work
    return Response(generate(), mimetype='text')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)