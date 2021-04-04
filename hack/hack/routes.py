import os
#import secrets
#from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session, Flask
from hack import app, db, bcrypt
# from dev.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from hack.models import  *
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        #print(request.form['username'])
        print(request.form['email'])
        print(request.form['password'])
        #print(request.form.get('slct'))
        
        session.pop('role',None)
        session['role'] = request.form.get('slct')
        
        if session['role'] == 'Student':
            user = student.query.filter_by(email=request.form['email']).first()
            login_user(user)
            print(current_user)
            print(current_user.i_id)
            return redirect(url_for('student_page'))
        
        elif session['role'] == 'Faculty':
            user = faculty.query.filter_by(email=request.form['email']).first()

            login_user(user)
          
            return redirect(url_for('faculty_page'))
        
        elif session['role'] == 'Principal':

            user = faculty.query.filter_by(email=request.form['email']).first()

            if principal.query.filter_by(emp_id=user.emp_id).first():

                login_user(user)
                
                return redirect(url_for('principal_page'))
            else:
                print('Invalid')
                return redirect(url_for('login'))


        elif session['role'] == 'Admin':
            user = admin1.query.filter_by(ad_mail=request.form['email']).first()
            login_user(user)

            return redirect(url_for('admin_page'))
            
        
        else:
            user = faculty.query.filter_by(email=request.form['email']).first()

            if hod.query.filter_by(emp_id=user.emp_id).first():
                login_user(user)

                return redirect(url_for('hod_page'))
            else:
                print('Invalid')
                return redirect(url_for('login'))
    
    return render_template('login.html')



@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('role',None)
    print("logged out")
    return redirect(url_for('home'))


@app.route("/admin", methods=['GET'])
@login_required
def admin_page():

    add_fac = department.query.all()
    add_ins_fac = committees.query.filter_by(level=1)
    add_dep_fac = committees.query.filter_by(level=2)
    add_stu_fac = committees.query.filter_by(level=3)

    cominsid = committees.query.filter_by(level=1)
    fac_ins_query, fac_ins_id=[],[]
    for i in cominsid:
        fac_ins_query.append(fac_comm_members.query.filter_by(comit_id = i.comit_id))
    for i in fac_ins_query:
        for j in i:
            fac_ins_id.append(j)
  
    comdepid = committees.query.filter_by(level=2)
    fac_dep_query, fac_dep_id=[],[]
    for i in comdepid:
        fac_dep_query.append(fac_comm_members.query.filter_by(comit_id = i.comit_id))
    for i in fac_dep_query:
        for j in i:
            fac_dep_id.append(j)

    comstuid = committees.query.filter_by(level=3)
    fac_stu_query, fac_stu_id=[],[]
    for i in comstuid:
        fac_stu_query.append(fac_comm_members.query.filter_by(comit_id = i.comit_id))
    for i in fac_stu_query:
        for j in i:
            fac_stu_id.append(j)
            print(j.emp_id)

    return render_template('admin.html', add_fac=add_fac, add_ins_fac = add_ins_fac, add_dep_fac = add_dep_fac, 
      add_stu_fac = add_stu_fac, fac_ins_id=fac_ins_id, fac_dep_id=fac_dep_id, fac_stu_id=fac_stu_id )


@app.route("/addfaculty", methods=['POST'])
def addfaculty():

    dept_id = request.form.get('slct')
    fac_name = request.form['fac_name']
    fac_email = request.form['fac_email']
    fac_contact = request.form['fac_contact']
    password = '12345'

    fac = faculty(dep_id = dept_id, emp_name = fac_name, email = fac_email, password=password, phone = fac_contact)
    db.session.add(fac)
    db.session.commit()

    return redirect(url_for('admin_page'))


@app.route("/adddepartment", methods=['POST'])
def adddepartment():

    dep_name = request.form['dep_name']
    fac_id = request.form['hodid']

    dep = department(dep_name = dep_name)
    db.session.add(dep)
    db.session.commit()

    dep_obj = department.query.filter_by(dep_name=dep_name).first()

    h = hod(emp_id= fac_id, dep_id = dep_obj.dep_id)
    db.session.add(h)
    db.session.commit()


    return redirect(url_for('admin_page'))

@app.route("/checkhod", methods=['POST'])
def checkhod():
   
    fac_id = request.form.get('id')

    user = faculty.query.filter_by(emp_id=fac_id).first()

    if user:
        return user.emp_name
    else:
        return "Not Exists"

@app.route("/addinstcommittee", methods=['POST'])
def addinstcommittee():
    print("YES")

    comm_name = request.form['commname']

    curr_yr = date.today().year
    if date.today().month < 8:
        curr_yr-=1

    com  = committees(comit_name= comm_name, year = curr_yr, level=1)
    db.session.add(com)
    db.session.commit()

    return redirect(url_for('admin_page'))

@app.route("/adddeptcommittee", methods=['POST'])
def adddeptcommittee():
    print("YES")

    comm_name = request.form['commname']

    curr_yr = date.today().year
    if date.today().month < 8:
        curr_yr-=1

    com  = committees(comit_name= comm_name, year = curr_yr, level=2)
    db.session.add(com)
    db.session.commit()


    return redirect(url_for('admin_page'))

@app.route("/addstubodycommittee", methods=['POST'])
def addstubodycommittee():
    print("YES")

    comm_name = request.form['commname']

    curr_yr = date.today().year
    if date.today().month < 8:
        curr_yr-=1

    com  = committees(comit_name= comm_name, year = curr_yr, level=3)
    db.session.add(com)
    db.session.commit()

    return redirect(url_for('admin_page'))

@app.route("/addinstfaculty", methods=['POST'])
def addinstfaculty():
    print("YES")

    com_id = request.form.get('slctinsfac')
    fac_id = request.form['ins_fac_id']
    fac_role = request.form['ins_fac_role']

    facmem = fac_comm_members(emp_id=fac_id, comit_id=com_id, role = fac_role)

    db.session.add(facmem)
    db.session.commit()

    return redirect(url_for('admin_page'))

@app.route("/adddeptfaculty", methods=['POST'])
def adddeptfaculty():
    print("YES")

    com_id = request.form.get('slctdepfac')
    fac_id = request.form['dep_fac_id']
    fac_role = request.form['dep_fac_role']

    facmem = fac_comm_members(emp_id=fac_id, comit_id=com_id, role = fac_role)

    db.session.add(facmem)
    db.session.commit()

    return redirect(url_for('admin_page'))


@app.route("/addstubodyfaculty", methods=['POST'])
def addstubodyfaculty():
    print("YES")

    com_id = request.form.get('slctstufac')
    fac_id = request.form['stu_fac_id']
    fac_role = request.form['stu_fac_role']

    facmem = fac_comm_members(emp_id=fac_id, comit_id=com_id, role = fac_role)

    db.session.add(facmem)
    db.session.commit()

    return redirect(url_for('admin_page'))


@app.route("/modifyinsrole", methods=['POST'])
def modifyinsrole():

    emp_id = request.form.get('emp_ins_id')
    ins_role = request.form['modinsrole']

    user = fac_comm_members.query.filter_by(emp_id=emp_id).first()
    user.role = stu_role
    db.session.commit()

    return redirect(url_for('admin_page'))

@app.route("/modifydeprole", methods=['POST'])
def modifydeprole():

    emp_id = request.form.get('emp_dep_id')
    dep_role = request.form['moddeprole']

    user = fac_comm_members.query.filter_by(emp_id=emp_id).first()
    user.role = stu_role
    db.session.commit()


    return redirect(url_for('admin_page'))


@app.route("/modifysturole", methods=['POST'])
def modifysturole():

    emp_id = request.form.get('emp_stu_id')
    stu_role = request.form['modsturole']

    user = fac_comm_members.query.filter_by(emp_id=emp_id).first()
    user.role = stu_role
    db.session.commit()

    return redirect(url_for('admin_page'))



@app.route('/faculty', methods=['GET'])
@login_required
def faculty_page():

    cm = fac_comm_members.query.filter_by(emp_id=current_user.emp_id).first()
    
    role = cm.role
    cnamequery = committees.query.filter_by(comit_id = cm.comit_id).first()
    userdata = {'role':role, 'cmname':cnamequery}

    eve = events.query.all()


    return render_template('faculty.html', userdata=userdata, eve=eve )



@app.route("/checkstudent", methods=['POST'])
def checkstudent():
   
    stu_id = request.form.get('id')

    user = student.query.filter_by(i_id=stu_id).first()

    if user:
        return user.stu_name
    else:
        return "Not Exists"


@app.route("/addstudent", methods=['POST'])
def addstudent():

    cmt_id = request.form.get('addstucomit')
    s_id = request.form['stid']
    role = request.form['role']
    
    if request.form.get('chkbox'):
        flag=1
    else:
        flag=0

    stu_mem = stu_comm_members(i_id= s_id, comit_id= cmt_id, role= role, flag = flag )
    db.session.add(stu_mem)
    db.session.commit()

    return redirect(url_for('faculty_page'))


@app.route('/modifystudentmember',methods=['POST'])
def modifystudentmember():

    s_id = request.form['modstuid']
    role = request.form['modrole']
    if request.form.get('modaccess'):
        flag=1
    else:
        flag=0

    user = stu_comm_members.query.filter_by(i_id = s_id).first()

    user.role = role
    user.flag = flag
    db.session.commit()
    
    return redirect(url_for('faculty_page'))


@app.route('/createevent',methods=['POST'])
def createevent():

    eve_name = request.form['event_name']
    comm_date = request.form['comm_date']
    end_date = request.form['end_date']
    comm_time = request.form['comm_time']
    end_time = request.form['end_time']
    event_type_select = request.form.get('event_type_select')
    team_size = request.form['team_size']
    event_venue = request.form['event_venue']
    event_desc = request.form['event_desc']
    if not team_size:
        team_size=1
    getorgidquery = fac_comm_members.query.filter_by(emp_id=current_user.emp_id).first()
    organizer_id = getorgidquery.member_id
    commit_id = getorgidquery.comit_id

    eve = events (event_name = eve_name, comit_id = commit_id, organizer_id=organizer_id, is_student=0, date_start=comm_date,
        date_end=end_date, time_start=comm_time, time_end=end_time, event_venue=event_venue, event_desc=event_desc,
        event_type= event_type_select, team_size=team_size )
    db.session.add(eve)
    db.session.commit()

    return redirect(url_for('faculty_page'))



@app.route('/event/<eid>', methods=['GET'])
@login_required
def evedetails(eid):


    eve = events.query.filter_by(event_id=eid).first()
    
    everes = eve_result.query.filter_by(event_id=eid).first()
    evemedia=[]
    if everes:
        evem = eve_media.query.filter_by(res_id = everes.res_id).distinct(eve_media.photos).all()
        print(evem)
        for i in evem:
            evemedia.append(i)
            print(i.photos)

    return render_template('details.html', eve=eve, everes= everes, evemedia = evemedia)



@app.route('/student', methods=['GET'])
@login_required
def student_page():

    cm = stu_comm_members.query.filter_by(i_id=current_user.i_id).first()
    
    cnamequery = committees.query.filter_by(comit_id = cm.comit_id).first()
    userdata = {'cm':cm, 'cmname':cnamequery}

    eve = events.query.all()

    eve_reg = events.query.filter_by(approval_status='Approved', completion_status="Upcoming")    

    eve_rep = events.query.filter_by(approval_status='Approved', completion_status="Upcoming")

    return render_template('student.html', userdata=userdata, eve=eve, eve_reg=eve_reg, eve_rep=eve_rep )



@app.route('/createeventstu',methods=['POST'])
def createeventstu():

    eve_name = request.form['event_name']
    comm_date = request.form['comm_date']
    end_date = request.form['end_date']
    comm_time = request.form['comm_time']
    end_time = request.form['end_time']
    event_type_select = request.form.get('event_type_select')
    team_size = request.form['team_size']
    event_venue = request.form['event_venue']
    event_desc = request.form['event_desc']

    if not team_size:
        team_size=1

    getorgidquery = stu_comm_members.query.filter_by(i_id=current_user.i_id).first()
    organizer_id = getorgidquery.member_id
    commit_id = getorgidquery.comit_id

    eve = events (event_name = eve_name, comit_id = commit_id, organizer_id=organizer_id, is_student=1, date_start=comm_date,
        date_end=end_date, time_start=comm_time, time_end=end_time, event_venue=event_venue, event_desc=event_desc,
        event_type= event_type_select, team_size=team_size )
    db.session.add(eve)
    db.session.commit()

    return redirect(url_for('student_page'))


@app.route('/getteamsize', methods=["POST"])
def getteamsize():
    
    x = request.form['id']
    j= x[-1]

    e = events.query.filter_by(event_id=int(j)).first()
    ts = e.team_size
    print(ts)
    return str(ts)



@app.route('/addparticipants', methods=["POST"])
def addparticipants():
    
    e_id = request.form.get('dropdownevereg')[-1]
    print("Add Parti: ", e_id)
    e = events.query.filter_by(event_id=int(e_id)).first()
    ts = e.team_size

    tname = request.form['teamname']

    if ts == 1:
        member1id = request.form['name1']
        evereg = eve_reg(event_id= int(e_id), team_name = tname,  i_id1 =  member1id)
        db.session.add(evereg)
        db.session.commit()

    elif ts==2:
        member1id = request.form['name1']
        member2id = request.form['name2']

        evereg = eve_reg(event_id= int(e_id), team_name = tname,  i_id1 =  member1id, i_id2= member2id)
        db.session.add(evereg)
        db.session.commit()
    elif ts==3:
        member1id = request.form['name1']
        member2id = request.form['name2']
        member3id = request.form['name3']
        
        evereg = eve_reg(event_id= int(e_id), team_name = tname,  i_id1 =  member1id, i_id2= member2id,
            i_id3 = member3id)
        db.session.add(evereg)
        db.session.commit()
    else:
        member1id = request.form['name1']
        member2id = request.form['name2']
        member3id = request.form['name3']
        member4id = request.form['name4']

        evereg = eve_reg(event_id= int(e_id), team_name = tname,  i_id1 =  member1id, i_id2= member2id,
            i_id3 = member3id, i_id4= member4id)
        db.session.add(evereg)
        db.session.commit()

    return redirect(url_for('student_page'))


@app.route('/eventreport', methods=["POST"])
def eventreport():

    eve_id = request.form.get('eventreportname')
    win_id = request.form['winnerid']
    runup_id = request.form['runnerupid']


    eventobject = events.query.filter_by(event_id = eve_id).first()
    eventobject.completion_status = "Completed"
    db.session.commit()

    getwinnamequery = eve_reg.query.filter_by(event_id= eve_id, team_id = win_id).first()
    win_name = getwinnamequery.team_name
    
    getrunupnamequery = eve_reg.query.filter_by(event_id= eve_id, team_id = runup_id).first()
    runup_name = getrunupnamequery.team_name

    print(eve_id, win_id, runup_id)

    everes = eve_result(event_id = eve_id, winner_name= win_name, runner_up= runup_name)
    db.session.add(everes)
    db.session.commit()

    results = eve_result.query.filter_by(event_id = eve_id, winner_name= win_name, runner_up= runup_name).first()
    
    uploaded_files = request.files.getlist("imgfile[]")
    print(uploaded_files)
    for i in uploaded_files:
        print(i.filename)
        if i :
            i.save(os.path.join(app.config['UPLOAD_FOLDER'], i.filename))
            evemedia = eve_media(res_id = results.res_id, photos = i.filename)
            db.session.add(evemedia)
            db.session.commit()

    return redirect(url_for('student_page'))


@app.route('/principal', methods=['GET','POST'])
@login_required
def principal_page():

    comitobj = committees.query.filter_by(level=1).all()
    print(comitobj)
    instevents = []
    for i in comitobj:
        if events.query.filter_by(approval_status='Pending', comit_id = i.comit_id).all():
            instevents.append(events.query.filter_by(approval_status='Pending', comit_id = i.comit_id).all())
    print(instevents)

    ins_eve = []
    for i in instevents:
        for j in i:
            ins_eve.append(j)

    return render_template('princi.html', ins_eve = ins_eve)


@app.route('/hod', methods=['GET','POST'])
@login_required
def hod_page():

    comitobj = committees.query.filter_by(level=2).all()
    print(comitobj)
    deptevents = []
    for i in comitobj:
        if events.query.filter_by(approval_status='Pending', comit_id = i.comit_id).all():
            deptevents.append(events.query.filter_by(approval_status='Pending', comit_id = i.comit_id).all())
    print(deptevents)

    dep_eve = []
    for i in deptevents:
        for j in i:
            dep_eve.append(j)

    return render_template('hod.html', dep_eve = dep_eve)



@app.route('/appdisappevent/<level>/<eid>', methods=["POST"])
def appdisappevent(level,eid):

    if level == '1':

        if request.form['action'] == "Approve":
            
            eve = events.query.filter_by(event_id = eid).first()

            eve.approval_status = 'Approved'
            eve.completion_status = "Upcoming"
            db.session.commit()

        elif request.form['action'] == "Disapprove":
            eve = events.query.filter_by(event_id = eid).first()

            eve.approval_status = 'Disapproved'
            eve.completion_status = "Cancelled"
            db.session.commit()

        return redirect(url_for('principal_page'))
    
    elif level == '2':

        if request.form['action'] == "Approve":
            
            eve = events.query.filter_by(event_id = eid).first()

            eve.approval_status = 'Approved'
            eve.completion_status = "Upcoming"
            db.session.commit()

        elif request.form['action'] == "Disapprove":
            eve = events.query.filter_by(event_id = eid).first()

            eve.approval_status = 'Disapproved'
            eve.completion_status = "Cancelled"
            db.session.commit()

        return redirect(url_for('hod_page'))

    elif level == '3':

        if request.form['action'] == "Approve":
            
            eve = events.query.filter_by(event_id = eid).first()

            eve.approval_status = 'Approved'
            eve.completion_status = "Upcoming"
            db.session.commit()

        elif request.form['action'] == "Disapprove":
            eve = events.query.filter_by(event_id = eid).first()

            eve.approval_status = 'Disapproved'
            eve.completion_status = "Cancelled"
            db.session.commit()

        return redirect(url_for('hod_page'))




