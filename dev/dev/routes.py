import os
#import secrets
#from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session
from dev import app, db, bcrypt
# from dev.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from dev.models import  *
from flask_login import login_user, current_user, logout_user, login_required


# @app.route("/")
# @app.route("/home")
# def home():
#     me = user(first_name='admin', email='admin@example.com')
#     db.session.add(me)
#     db.session.commit()
    
#     peter = user.query.filter_by(first_name='lokesh').first()
#     return "Hello World "+ peter.email 


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET','POST'])
def login():

    if request.method == "POST":
        #print(request.form['username'])
        print(request.form['email'])
        print(request.form['password'])
        print(request.form.get('slct1'))

        session['role'] = request.form.get('slct1')
        if session['role'] = 

    #     if current_user.is_authenticated:
    #         print("line 29")
    #         uname = current_user.username
    #         return redirect(url_for('emp_profile',uname=uname ))

    #     user = authentication.query.filter_by(username=request.form['username']).first()
    #     print(user)
    #     if user and bcrypt.check_password_hash(user.password, request.form['password']):
    #         print("line 34")
    #         login_user(user)
    #         uname = current_user.username
    #         return redirect(url_for('emp_profile', uname = uname))

    #         next_page = request.args.get('next')
    #         return redirect(next_page) if next_page else redirect(url_for('home'))
    #     else:
    #         return "Login Unuccessfull!!"
    #         flash('Login Unsuccessful. Please check email and password', 'danger')
          

    # #curruser = employee_personal.query.filter_by(emp_id=current_user.emp_id).first()
    
    return render_template('login.html')


@app.route("/emp_profile/<uname>", methods=['GET'])
@login_required
def emp_profile(uname):
    print(uname)

    curruser = employee_personal.query.filter_by(emp_id=current_user.emp_id).first()
    return render_template('emphome.html', curruser=curruser )


@app.route("/<uname>/emotion_form", methods=['GET'])
@login_required
def emotion_form(uname):
        return render_template('Depression_Analysis.html')


@app.route("/<uname>/attrition_form", methods=['GET'])
@login_required
def attrition_form(uname):

    dep_filled = depression.query.filter_by(emp_id=current_user.emp_id).first()
    
    if dep_filled:
        return render_template('Employee_Attrition_Form.html')
    else:
        curruser = employee_personal.query.filter_by(emp_id=current_user.emp_id).first()
        #return redirect(url_for('emp_profile', uname = uname))
        return render_template('emphome.html', curruser=curruser )

        #return redirect(url_for('emp_profile', uname = uname))
 


@app.route("/logout")
@login_required
def logout():
    logout_user()
    print("logged out")
    print(current_user)
    return redirect(url_for('home'))


@app.route("/trial")
def home2():

    # hashed_password = bcrypt.generate_password_hash('56789').decode('utf-8')
    # me = authentication(emp_id=1001,username='kuk', password=hashed_password)
    # db.session.add(me)
    # db.session.commit()

    # peter = authentication.query.filter_by(username='sank').first()

    # x = bcrypt.check_password_hash(peter.password, '54321')   
   
    return "Hello"
    


@app.route("/<uname>/emotion_form/submit",  methods=['POST'])
@login_required
def depression_data(uname):

    answers_list = []

    if request.method == 'POST':
        answers_list.append(request.form['q19_1I'])
        answers_list.append(request.form['q2_2My'])
        answers_list.append(request.form['q3_3It'])
        answers_list.append(request.form['q4_4The'])
        answers_list.append(request.form['q5_5I'])
        answers_list.append(request.form['q6_6I'])
        answers_list.append(request.form['q7_7I'])
        answers_list.append(request.form['q8_8I'])
        answers_list.append(request.form['q9_9I'])
        answers_list.append(request.form['q10_10It'])
        answers_list.append(request.form['q11_11I'])
        answers_list.append(request.form['q12_12I'])
        answers_list.append(request.form['q13_13I'])
        answers_list.append(request.form['q14_14My'])
        answers_list.append(request.form['q15_15I'])
        answers_list.append(request.form['q16_16I'])
        answers_list.append(request.form['q17_17I'])
        answers_list.append(request.form['q18_18Without'])
        

        answers_key = {'Not at all':1, 'Just a little':2, 'Somewhat':3, 'Moderately':4, 'Quite a lot':5, 
            'Very much':6}
        dep_score=0
        for i in answers_list:
            dep_score += answers_key[i]


        print( dep_score)


        depress = depression(emp_id= current_user.emp_id, Q_1 = answers_list[0], Q_2 = answers_list[1],
        Q_3 = answers_list[2], Q_4 = answers_list[3], Q_5 = answers_list[4], Q_6 = answers_list[5],
        Q_7 = answers_list[6], Q_8 = answers_list[7], Q_9 = answers_list[8], Q_10 = answers_list[9],
        Q_11 = answers_list[10], Q_12 = answers_list[11], Q_13 = answers_list[12], Q_14 = answers_list[13],
        Q_15 = answers_list[14], Q_16 = answers_list[15], Q_17 = answers_list[16], Q_18 = answers_list[17],
        dep_score = dep_score)

        db.session.add(depress)
        db.session.commit()

        return redirect(url_for('emp_profile', uname = uname))




@app.route("/<uname>/attrition_form/submit",  methods=['POST'])
@login_required
def attrition_data(uname):
    
    answers_list = []

    if request.method == 'POST':
        answers_list.append(request.form['q9_howOld'])
        answers_list.append(request.form['q13_gender'])
        answers_list.append(request.form['q36_1Enter'])
        answers_list.append(request.form['q29_2How'])
        answers_list.append(request.form['q37_3How'])
        answers_list.append(request.form['q39_4How'])
        answers_list.append(request.form['q40_5How'])
        answers_list.append(request.form['q41_6Do'])
        answers_list.append(request.form['q42_7Do'])
        answers_list.append(request.form['q43_8Do'])
        answers_list.append(request.form['q44_9How'])
        answers_list.append(request.form['q45_10How'])
        answers_list.append(request.form['q46_11How'])
        answers_list.append(request.form['q47_12How'])
        answers_list.append(request.form['q48_13How'])
        answers_list.append(request.form['q49_14Does'])
        answers_list.append(request.form['q50_15Do'])
        answers_list.append(request.form['q51_16How'])
        answers_list.append(request.form['q52_17Your'])
        answers_list.append(request.form['q53_18How'])
        answers_list.append(request.form['q54_19Years'])
        answers_list.append(request.form['q58_20Rate58'])
        answers_list.append(request.form['q59_21Does'])
        answers_list.append(request.form['q60_22How'])
        answers_list.append(request.form['q61_23Do'])
        answers_list.append(request.form['q62_24Number'])
        answers_list.append(request.form['q63_25Total'])
        answers_list.append(request.form['q64_26Do'])
        answers_list.append(request.form['q65_27How'])
        answers_list.append(request.form['q66_28Do'])
        answers_list.append(request.form['q67_29When'])
        answers_list.append(request.form['q68_30Are'])
        answers_list.append(request.form['q69_31Daily'])
        answers_list.append(request.form['q70_32How'])
        answers_list.append(request.form['q71_33Do'])
        answers_list.append(request.form['q72_34To'])
        answers_list.append(request.form['q73_35What'])
        answers_list.append(request.form['q74_36Years'])
        answers_list.append(request.form['q75_37Do'])
        answers_list.append(request.form['q76_38Do'])
        answers_list.append(request.form['q78_39How'])
        answers_list.append(request.form['q79_40How'])
        answers_list.append(request.form['q80_41If'])
        answers_list.append(request.form['q81_42Overall'])
        answers_list.append(request.form['q82_43Do'])
        answers_list.append(request.form['q83_44How'])
        answers_list.append(request.form['q84_45Are'])
        answers_list.append(request.form['q85_46How'])
        answers_list.append(request.form['q86_47Do'])
        answers_list.append(request.form['q87_48Overall'])
        answers_list.append(request.form['q88_49How'])
        answers_list.append(request.form['q90_50Any'])
        

        depval = depression.query.filter_by(emp_id= current_user.emp_id).first()
        depscore = depval.dep_score

        print(depscore)

        if depscore in range(0,25):
            depression_r = 'No Depression'
        elif depscore in range(25,43):
            depression_r = 'Mild - Moderate Depression'
        else:
            depression_r = 'Severe'
        answers_list.append(depression_r)


        batw, nratw, nswtsal, mental = 0,0,0,0
        fset = []

        if request.form['q41_6Do'] == 'No':
            batw += 1
        if request.form['q61_23Do'] == 'No':
            batw += 1
        if  request.form['q76_38Do'] == 'Yes': 
            batw += 1 
        if batw >= 2:
            fset.append('Biasedness at work')
        

        if request.form['q42_7Do'] == "No":
            fset.append('Suppressed Opinions')
        

        if request.form['q43_8Do'] == 1 or request.form['q43_8Do'] == 2:
            nratw += 1
        if request.form['q44_9How'] == 1 or request.form['q44_9How'] == 2:
            nratw += 1
        if nratw >= 1:
            fset.append('Not respected at workplace')


        if request.form['q60_22How']==1:
            nswtsal += 1
        if request.form['q61_23Do']=='No':
            nswtsal += 1
        if request.form['q73_35What']==1:
            nswtsal += 1
        if request.form['q74_36Years']=='2 years':
            nswtsal += 1
        if nswtsal >=2 :
            fset.append('Not satisfied with salary')
        

        if request.form['q71_33Do'] == 'Yes':
            fset.append('Medical Issues')


        if request.form['q52_17Your'] == 'More than 10 hrs' or request.form['q75_37Do'] == 'Yes':
            fset.append('More working hours')
        

        if request.form['q64_26Do']==1 or request.form['q64_26Do']==2:
            mental += 1
        if request.form['q70_32How'] == 1:
            mental += 1
        if request.form['q76_38Do'] == 'Yes':
            mental += 1
        if depscore == 'Severe':
            mental += 1
        if mental>=2:
            fset.append('Mental Health Issues')



        print(request.form['q60_22How'])
        print(fset)

        
        
        # ML MODEL ---------------------------------------------------------------------------------

        data = answers_list[3:51]
        data.append(depression_r)
        print(data)

        # ----------------ONE HOT ENCODING -------------------------------------------------

        
        data = onehoten(data) 
        data = data.tolist()
        print(type(data))

        #------------------------------------------------------------------------------

        j_data = json.dumps([data])
        print("J_DATA")
        print(j_data)
        print()
        print()
        url = 'http://127.0.0.1:5000/apiformodel'
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

        print("Before req")
        r = requests.post(url, data=j_data, headers=headers)
        print("After req, now response")
        print(r)
        rep = r.text.replace('\n','')
        y = rep.replace(" ",'')
        print(y)

        # -----------------------------------------------------------------------------------------
    

        if y[1] == '0':
            answers_list.append('No')
        else:
            answers_list.append('Yes')
        answers_list.append(fset)

        print(len(answers_list))

        attr = attrition( emp_id = current_user.emp_id, age_group = answers_list[0], gender =answers_list[1], 
        job_role = answers_list[2], work_years= answers_list[3], mission_understanding=answers_list[4],
        mission_connection = answers_list[5], info_company = answers_list[6], bias = answers_list[7], 
        opinion = answers_list[8], feedback = answers_list[9], work_value = answers_list[10], 
        communicate = answers_list[11], compititiveness = answers_list[12], meaningful = answers_list[13], 
        challenging = answers_list[14], passion = answers_list[15], responsibility_defined = answers_list[16], 
        involvement = answers_list[17], working_hours = answers_list[18], business_travel = answers_list[19], 
        year_manager = answers_list[20], relation_manager = answers_list[21], manager_development = answers_list[22], 
        salary_satis = answers_list[23], fair_paid = answers_list[24], no_of_companies = answers_list[25],  
        total_working_years = answers_list[26], stressed = answers_list[27], personal_satis = answers_list[28], 
        balance_prof = answers_list[29], encourage_learn = answers_list[30], married = answers_list[31], 
        travel_hours = answers_list[32], tired = answers_list[33], medical_issues = answers_list[34], 
        individual_goals = answers_list[35], salary_hike = answers_list[36], promotion = answers_list[37], 
        overtime = answers_list[38], extra_work = answers_list[39], missing_deadline = answers_list[40], 
        overall_performance = answers_list[41], better_job = answers_list[42], job_satis = answers_list[43], 
        training = answers_list[44], benefits = answers_list[45], campus_envi = answers_list[46], 
        canteen = answers_list[47], leaves_emergency = answers_list[48], confidence_company = answers_list[49], 
        overall_rating = answers_list[50], suggestions = answers_list[51], depression = answers_list[52], 
        result = answers_list[53], feature_set = answers_list[54])

        db.session.add(attr)
        db.session.commit()

        return redirect(url_for('emp_profile', uname = uname))



@app.route('/apiformodel', methods = ['POST'])
def api():
    if request.method == "POST":
        data = request.get_json()
        print("Length: ", len(data[0]))
        modelfile = 'dev/mlmodel/attrition_prediction.pickle'
        attr_model = pickle.load(open(modelfile, 'rb'))
        print("Pickle loaded")
        prediction = attr_model.predict(data)
        
        prediction = prediction.tolist()
        return jsonify(prediction)


def onehoten(data):
    #print(data)
    dataset = pd.read_csv('dev/dataset/employee_dataset_A1.csv')
    x=dataset.iloc[:,0:49].values

    #print(x[0])
    x = np.append(x,[data],axis=0)

    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), 
        [0,4,5,12,13,14,15,16,18,21,22,28,29,31,33,34,35,36,37,39,45,48])], remainder='passthrough')

    x1 = np.array(ct.fit_transform(x))
    
    print("Lenght onehot: ",len(x1[0]))

    return x1[-1]




