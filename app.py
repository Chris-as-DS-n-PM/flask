import pandas as pd
import datetime

from flask import Flask, request, render_template
from datetime import timedelta
from collections import defaultdict, OrderedDict

# Util Functions
def preprocess_coursebook_data(coursebook_df: pd.DataFrame) -> None:
    """Update df data to have datetime objects"""
    coursebook_df['Start_Time'] = [pd.to_datetime(i).time() for i in coursebook_df['Start_Time']]
    coursebook_df['End_Time'] = [pd.to_datetime(i).time() for i in coursebook_df['End_Time']]

def substract_datetime_time(time1: datetime.time, time2: datetime.time) -> int:
    sum_of_time1_minutes = time1.hour * 60 + time1.minute
    sum_of_time2_minutes = time2.hour * 60 + time2.minute

    diff = sum_of_time2_minutes - sum_of_time1_minutes
    if (diff < 0):
        raise Exception('difference in time was negative, make sure time2 is greater than time1')

    if (time1 == datetime.time(0,0)):
        return float('inf')
    elif (time2 == datetime.time(23,59)):
        return float('inf')
    return diff


def difference_of_datetime_time_formatted(time1: datetime.time, time2: datetime.time) -> str:
    sum_of_time1_minutes = time1.hour * 60 + time1.minute
    sum_of_time2_minutes = time2.hour * 60 + time2.minute

    diff = sum_of_time2_minutes - sum_of_time1_minutes
    if (diff < 0):
        raise Exception('difference in time was negative, make sure time2 is greater than time1')

    if (time2 == datetime.time(23, 59)):
        return f'After {time1.strftime("%I:%M %p")}'
    elif (time1 == datetime.time(0,0)):
        return f'Before {time2.strftime("%I:%M %p")}'
    elif (diff // 60 == 0):
        return f'Between {time1.strftime("%I:%M %p")} and {time2.strftime("%I:%M %p")} ({diff} mins)'
    else:
        return f'Between {time1.strftime("%I:%M %p")} and {time2.strftime("%I:%M %p")} ({diff // 60} hr and {diff % 60} mins)'


def get_open_rooms(
    coursebook_df: pd.DataFrame,
    day_of_week: str,
    start_time: datetime.time) -> pd.DataFrame:

    mask_for_all_classes_held_today = coursebook_df['Day'] == day_of_week
    mask_classes_start_time_less_than_current_time = coursebook_df['Start_Time'] <= start_time
    mask_classes_current_time_less_than_end_time = start_time <= coursebook_df['End_Time']
    combined = mask_for_all_classes_held_today & mask_classes_start_time_less_than_current_time & mask_classes_current_time_less_than_end_time

    return sorted(set(coursebook_df['Location']) - set(coursebook_df[combined]['Location']))


def get_time_ranges_for_rooms(
    coursebook_df: pd.DataFrame,
    rooms: list[str],
    day_of_week: str,
    start_time: datetime.time,
    minimum_time_wanted: int) -> pd.DataFrame:

    open_room_groups = defaultdict(dict)
    for room in rooms:
        open_room_groups[room.split(' ')[0]][room] = None

    for room_group_key, room_group in open_room_groups.items():
        for room in room_group.keys():

            schedule = coursebook_df[
                (coursebook_df['Location'] == room) & (coursebook_df['Day'] == day_of_week)
            ].sort_values('Start_Time')

            if (len(schedule) == 0):
                open_room_groups[room_group_key][room] = []
                continue


            top_of_the_day = schedule['Start_Time'].iloc[0]
            end_of_the_day = schedule['End_Time'].iloc[-1]
            range_when_class_is_free = list(zip(schedule['End_Time'], schedule['Start_Time'].shift(-1).dropna()))
            range_when_class_is_free.insert(0, (datetime.time(0,0), top_of_the_day))
            range_when_class_is_free.append((end_of_the_day, datetime.time(23, 59)))

            range_when_class_is_free = list(filter(
                lambda time_range: time_range[1] >= start_time, range_when_class_is_free
            ))

            range_when_class_is_free = list(filter(
                lambda time_range: substract_datetime_time(time_range[0], time_range[1]) >= minimum_time_wanted,
                range_when_class_is_free
            ))

            ranges_as_strings = list(map(
                lambda time_range: difference_of_datetime_time_formatted(time_range[0], time_range[1]),
                range_when_class_is_free
            ))

            open_room_groups[room_group_key][room] = ranges_as_strings

    return dict(open_room_groups)

#---------------------
# load in coursebook data
df = pd.read_csv('./static/cleaned_25s.csv')
preprocess_coursebook_data(df) 

buildings = {
    'AD' : 'Administration Building',
    'AH2': 'Arts and Humanities 2',
    'ATC' : 'Arts and Technology Building',
    'CB' : 'Classroom Building',
    'CBH' : 'Classroom Building',
    'CCTC': 'CCTC',
    'CD1' : 'Callier Dallas Building',
    'CD2' : 'Callier Dallas Building',
    'CHEC' : 'Collin Higher Education Center',
    'CR' : 'Callier Center Richardson',
    'CRA' : 'Callier Center Richardson Addition',
    'ECSN' : 'Engineering and Computer Science North',
    'ECSS' : 'Engineering and Computer Science South',
    'ECSW' : 'Engineering and Computer Science West',
    'FN' : 'Founders North',
    'FO' : 'Founders Building',
    'GR' : 'Cecil H. Green Hall',
    'HH' : 'Karl Hoblitzelle Hall',
    'JO' : 'Erik Jonsson Academic Center',
    'JSOM' : 'Naveen Jindal School of Management',
    'MC' : 'Eugene McDermott Library',
    'ML1' : 'Modular Lab 1',
    'ML2' : 'Modular Lab 2',
    'PHY' : 'Physics Building',
    'RHNW' : 'Residence Hall Northwest',
    'RHW' : 'Residence Hall West',
    'RL': 'Natural Science and Engineering Research Lab',
    'ROC' : 'Research and Operations Center',
    'ROW' : 'Research and Operations Center West',
    'SCI' : 'Sciences Building',
    'SLC' : 'Science Learning Center',
    'SP2' : 'Synergy Park North 2',
    'SPN' : 'Synergy Park North',
    'TH' : 'University Theatre'
}

all_rooms = sorted({room: buildings[room.split(' ')[0]] for room in df['Location'].unique()}.items(), key=lambda i: i[0])

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


app = Flask(__name__)

#---- Open Rooms -----

@app.route('/')
def time_slot_form():
    current_time_cst_str = ':'.join((str((datetime.datetime.utcnow() - timedelta(hours=5)).time()).split(':')[:2]))
    weekday_idx = (datetime.datetime.utcnow() - timedelta(hours=5)).weekday()
    days_rotated = days[weekday_idx:] + days[:weekday_idx]

    return render_template('open_rooms_form.html', 
                           buildings=buildings.items(), 
                           days_list=days_rotated, 
                           current_time=current_time_cst_str)

@app.route('/', methods=['POST'])
def time_slot_post():
    day = request.form.get('days')
    start_time = request.form['start-time']
    min_time = int(request.form['min-time'])
    locations = set(request.form.getlist('locations'))

    if len(locations) == 0:
        current_time_cst_str = ':'.join((str((datetime.datetime.utcnow() - timedelta(hours=5)).time()).split(':')[:2]))
        weekday_idx = (datetime.datetime.utcnow() - timedelta(hours=5)).weekday()
        days_rotated = days[weekday_idx:] + days[:weekday_idx]
        return render_template('open_rooms_form.html', 
                           buildings=buildings.items(), 
                           days_list=days_rotated, 
                           current_time=current_time_cst_str, 
                           invalid_sub=True)


    current_time_cst = datetime.datetime.strptime(start_time, '%H:%M').time()
    open_rooms = get_open_rooms(df, day, current_time_cst)
    filtered_open_rooms = [room for room in open_rooms 
                           if room.split(' ')[0] in locations]

    open_room_groups = get_time_ranges_for_rooms(df, filtered_open_rooms, day, current_time_cst, min_time)

    return render_template('open_rooms_data.html', data=open_room_groups, buildings=buildings)

#---- Rooms Schedule -----

@app.route('/room_schedule')
def class_give_loc_form():
    weekday_idx = (datetime.datetime.utcnow() - timedelta(hours=5)).weekday()
    days_rotated = days[weekday_idx:] + days[:weekday_idx]
	
    return render_template('room_schedule_form.html', all_rooms=all_rooms, days_list=days_rotated)


@app.route('/room_schedule', methods=['POST'])
def get_room_schedule_post():
    day = request.form.get('days')
    rooms = request.form.getlist('locations')

    if len(rooms) == 0:
        weekday_idx = (datetime.datetime.utcnow() - timedelta(hours=5)).weekday()
        days_rotated = days[weekday_idx:] + days[:weekday_idx]
        return render_template('room_schedule_form.html', 
                               all_rooms=all_rooms, 
                               days_list=days_rotated,
                               invalid_sub=True)

    schedule_data = {}
    no_classes_rooms = []

    for room in rooms:
        sch = df[(df['Location'] == room) & (df['Day'] == day)]

        if len(sch) == 0:
            no_classes_rooms.append(room)
            continue

        classes = []
        for _, class_data in sch.iterrows():
            time_str = f"{class_data['Start_Time'].strftime('%I:%M %p')} - {class_data['End_Time'].strftime('%I:%M %p')}"
            classes.append([class_data['Class Title'], class_data['Instructor'], time_str])
        
        schedule_data[room] = classes
    
    no_classes_rooms = ', '.join(no_classes_rooms)
    schedule_data = OrderedDict(sorted(schedule_data.items()))

    return render_template('room_schedule_data.html',
                           schedule_data=schedule_data,
                           no_classes_rooms=no_classes_rooms)
