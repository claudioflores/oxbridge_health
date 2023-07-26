# Problem 3

import pandas as pd
import numpy as np
import warnings


file_name = 'all_test_data_2023_07_13.xlsx'
events = pd.read_excel(file_name, 'medical_events')
enrollment = pd.read_excel(file_name, 'enrollment')
deaths = pd.read_excel(file_name, 'death_dates')

# Merger of enrollment dates. Solves the problem of overlapping periods.
enrollment['enrollment_start_date'] = pd.to_datetime(enrollment['enrollment_start_year_month'],format='%Y-%m')
enrollment['enrollment_end_date'] = [np.datetime64(x)+np.timedelta64(1, 'M')+np.timedelta64(-1, 'D') for x in enrollment['enrollment_end_year_month']]
enrollment = enrollment.sort_values(by=['patient_id', 'enrollment_start_date'], ascending=[True, True])
cols = ['patient_id', 'enrollment_start_date', 'enrollment_end_date']
enrollment_merged = pd.DataFrame(columns=cols)
i = 0
while i < len(enrollment):
    row = enrollment.loc[i]
    if i < len(enrollment)-1:
        start_date = row.enrollment_start_date
        end_date = row.enrollment_end_date
        for j in range(i+1, len(enrollment)):
            row_next = enrollment.loc[j]
            if row.patient_id == row_next.patient_id:
                if end_date >= row_next.enrollment_start_date:
                    end_date = row_next.enrollment_end_date
                    i += 1
                else:
                    i = j
                    break
            else:
                i = j
                break
        enrollment_merged = pd.concat([enrollment_merged, pd.DataFrame([[row.patient_id, start_date, end_date]], columns=cols)]) 
        
    else:
         enrollment_merged = pd.concat([enrollment_merged, pd.DataFrame([row], columns=cols)])
         i += 1

# Events day overlap count function               
def event_date_overlap3(df, event1_start_date, event1_end_date, event2_start_date, event2_end_date):
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

# Counts the number of days covered for every event in multiple enrollment periods.      
df = events.merge(enrollment_merged, on='patient_id', how='left')
df = df.merge(deaths, on='patient_id', how='left')
df['event_end_date2'] = [event_end_date if event_end_date<death_date or pd.isnull(death_date) else death_date for event_end_date, death_date in zip(df['event_end_date'], df['death_date'])]
df['days_event'] = (df['event_end_date2']-df['event_start_date']).astype('timedelta64[D]')+1     
df['days_covered'] = event_date_overlap3(df, 'event_start_date', 'event_end_date2', 'enrollment_start_date', 'enrollment_end_date')
df2 = df.groupby(['patient_id', 'event_id', 'days_event']).agg({'days_covered': 'sum'}).reset_index()

# Shows events where the number of days covered is the same as the length of the event.
print(df2[df2.days_event==df2.days_covered][['patient_id', 'event_id']])
