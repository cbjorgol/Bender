from Tkinter import *
import time
from datetime import datetime, timedelta
import subprocess

npv_diff = 80000000
freq = "Today's"
internet_connection = True
ref_date = datetime(2017, 9, 30, 0, 0)


if freq == 'weekly': 
    prefix = "This week's"
elif freq == 'refdate':
    prefix = "Opportunity Cost (NPV so far)"
else: 
    prefix = "Today's Opportunity Cost\nin NPV (so far)"
 

lower_text = ' '

color1 = "#%02x%02x%02x" % (124, 252, 0)
color2 = "red" #"#228B22"

root = Tk()

title = Label(root, font=('Times',80, 'bold'), fg='white', bg=color2)
title.pack(fill='x')
title.config(text=prefix)

title = Label(root, font=('Times',55, 'bold'), fg='white', bg=color2)
title.pack(fill='x')
title.config(text=lower_text)




clock = Label(root, font=('times', 150, 'bold'), fg='white', bg=color2)
clock.pack(fill=BOTH, expand=1)

title2 = Label(root, font=('Times', 40, 'bold'), fg='white', bg=color2)
title2.pack(fill='x')
title2.config(text='Without MSRM2 in market')

if internet_connection:
    def command():
        return subprocess.Popen(['python', 'chuck_norris_jokes.py'])
        
    frame1 = Frame(root, bg=color2, height=5)
    frame1.pack(side=LEFT, fill='both', expand=5)

    frame2 = Frame(root, bg=color2, height=5)
    frame2.pack(side=RIGHT)

    button = Button(frame2, text='Joke', command=command, font=('Helvetica', 7), borderwidth=0)
    button.pack(side=RIGHT,anchor='e')
    button.config(text='Chuck Norris Joke')


def tick():
    if freq == 'weekly': 
        npv_per_period = npv_diff / 52.
        today = datetime.today()
        idx = (today.weekday()) % 7
        ref_date = today - timedelta(idx)
        ref_date = ref_date.replace(hour=0, minute=0, second=0, microsecond=0)
        prefix = "This week's"
        multiplier = 7
        
    elif freq == 'refdate':
        npv_per_period = npv_diff
        prefix = "Today's"
        ref_date = datetime(2018, 3, 30, 0, 0)
        multiplier = 365

    else:
        npv_per_period = npv_diff / 365.
        ref_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        prefix = "Today's"
        multiplier = 1
        
    time2 = time.strftime('%H:%M:%S')
    time_this_week = datetime.now() - ref_date
    pct_of_day = time_this_week.total_seconds() / float(multiplier*24*60*60)
    time2 = '${:,.0f}'.format(pct_of_day * npv_per_period)
    
# if time string has changed, update it
    clock.config(text=time2)
# calls itself every 200 milliseconds
# to update the time display as needed
# could use >200 ms, but display gets jerky
    clock.after(40, tick)


tick()
root.mainloop( )
