from datetime import datetime, date
from hack import db, login_manager
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import SET, ENUM, YEAR
from flask import session

# @login_manager.user_loader
# def load_user(emp_id):
#     return authentication.query.get(int(emp_id))

@login_manager.user_loader
def load_user(id):

    print("USER LOADER:", session['role'])
    if session['role'] == 'Faculty' or session['role'] == 'Principal' or session['role'] == 'HOD':
        return faculty.query.get(id)
    elif session['role'] == 'Student':
        return student.query.get(id)
    elif session['role'] == 'Admin':
        return admin1.query.get(id)


class admin1(db.Model, UserMixin):
    a_id = db.Column(db.Integer, primary_key=True)
    ad_mail = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def get_id(self):
        return (self.a_id)

class department(db.Model, UserMixin):
    dep_id = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(40), nullable=False)

class faculty(db.Model, UserMixin):
    emp_id = db.Column(db.Integer, primary_key=True)
    dep_id = db.Column(db.Integer, nullable=False)
    emp_name = db.Column(db.String(250), nullable=False)
    date_join = db.Column(db.Date, nullable=False, default = (date.today()).strftime("%Y-%m-%d"))
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

    def get_id(self):
        return (self.emp_id)

class hod(db.Model, UserMixin):
    emp_id = db.Column(db.Integer, nullable=False, primary_key=True)
    dep_id = db.Column(db.Integer, nullable=False)

class principal(db.Model, UserMixin):
    emp_id = db.Column(db.Integer, nullable=False,  primary_key=True)

class student(db.Model, UserMixin):
    i_id = db.Column(db.Integer, primary_key=True)
    dep_id = db.Column(db.Integer, nullable=False)
    stu_name = db.Column(db.String(250), nullable=False)
    date_join = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

    def get_id(self):
        return (self.i_id)

class committee_level(db.Model, UserMixin):
    level = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(255), nullable=False)


class committees(db.Model, UserMixin):
    comit_id = db.Column(db.Integer, primary_key=True)
    comit_name = db.Column(db.String(100), nullable=False)
    year = db.Column(YEAR, nullable=False)
    level = db.Column(db.Integer, nullable=False)


class events(db.Model, UserMixin):
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    comit_id = db.Column(db.Integer, nullable=False)
    organizer_id = db.Column(db.Integer, nullable=False)
    is_student = db.Column(db.Integer, nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    time_start = db.Column(db.Time, nullable=False)
    time_end = db.Column(db.Time, nullable=False)
    approval_status = db.Column(db.String(200), nullable=False, default= "Pending")
    completion_status = db.Column(db.String(200), nullable=False)
    event_venue = db.Column(db.String(100), nullable=False)
    event_desc = db.Column(db.Text, nullable=False)
    event_type = db.Column(ENUM('Solo','Group'), nullable=False)
    team_size = db.Column(db.Integer, nullable=False)

class eve_reg(db.Model, UserMixin):
    team_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    team_name = db.Column(db.String(200), nullable=False)
    i_id1 = db.Column(db.Integer, nullable=False)
    i_id2 = db.Column(db.Integer, nullable=False)
    i_id3 = db.Column(db.Integer, nullable=False)
    i_id4 = db.Column(db.Integer, nullable=False)

class eve_result(db.Model, UserMixin):
    res_id = db.Column(db.Integer, primary_key=True)
    event_id =  db.Column(db.Integer, nullable=False)
    winner_name = db.Column(db.String(100), nullable=False)
    runner_up = db.Column(db.String(100), nullable=False)

class eve_media(db.Model, UserMixin):
    media_id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer, nullable=False)
    photos =  db.Column(db.String(255), nullable=False)


class fac_comm_members(db.Model, UserMixin):
    member_id = db.Column(db.Integer, primary_key=True)
    emp_id =  db.Column(db.Integer, nullable=False)
    comit_id =  db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(100), nullable=False)

class stu_comm_members(db.Model, UserMixin):
    member_id = db.Column(db.Integer, primary_key=True)
    i_id =  db.Column(db.Integer, nullable=False)
    comit_id =  db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(100), nullable=False)
    flag =  db.Column(db.Integer, nullable=False)

