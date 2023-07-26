# Problem 2:
    
from datetime import timedelta as td
import pandas as pd
import warnings


df = pd.read_csv('problem2_data.csv', parse_dates=['event1_start_date', 'event1_end_date', 'event2_start_date', 'event2_end_date'])

# SQL approach
def event_date_overlap1(df, event1_start_date, event1_end_date, event2_start_date, event2_end_date):
    def days_count(dt1a, dt1b, dt2a, dt2b):
        try:
            if dt1a>dt1b or dt2a>dt2b:
                warnings.warn('Dates out of order')
                return None
            df1 = pd.DataFrame([dt1a+td(days=x) for x in range((dt1b-dt1a).days+1)], columns = ['date'])
            df2 = pd.DataFrame([dt2a+td(days=x) for x in range((dt2b-dt2a).days+1)], columns = ['date'])
            return len(df1.merge(df2, on=['date']))
        except:
            warnings.warn('Wrong input')
    return [days_count(dt1a, dt1b, dt2a, dt2b) for dt1a, dt1b, dt2a, dt2b in zip(df[event1_start_date], df[event1_end_date], df[event2_start_date], df[event2_end_date])]

# Python approach
def event_date_overlap2(df, event1_start_date, event1_end_date, event2_start_date, event2_end_date):
    def days_count(dt1a, dt1b, dt2a, dt2b):
        try:
            if dt1a>dt1b or dt2a>dt2b:
                warnings.warn('Dates out of order')
                return None
            if dt1b<dt2a or dt2b<dt1a:
                return 0
            start_date = dt1a if dt1a>dt2a else dt2a
            end_date = dt1b if dt1b<dt2b else dt2b
            return (end_date-start_date).days+1
        except:
            warnings.warn('Wrong input')
    return [days_count(dt1a, dt1b, dt2a, dt2b) for dt1a, dt1b, dt2a, dt2b in zip(df[event1_start_date], df[event1_end_date], df[event2_start_date], df[event2_end_date])]
    
df['days_overlap1'] = event_date_overlap1(df, 'event1_start_date', 'event1_end_date', 'event2_start_date', 'event2_end_date')
df['days_overlap2'] = event_date_overlap2(df, 'event1_start_date', 'event1_end_date', 'event2_start_date', 'event2_end_date')
df.to_csv('problem2_output.csv', index=False)
