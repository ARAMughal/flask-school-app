from flask import Flask, render_template, request, session, redirect
import os
import random
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json','r')as c:
    params = json.load(c)['params']


project_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.secret_key = 'super-sectret-key'

database_file = "sqlite:///{}".format(os.path.join(project_dir, "SchoolDb.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Teachers(db.Model):
    __tablename__ = "teachers"
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    joining_date = db.Column(db.String(50), nullable=False)
    retirement_date = db.Column(db.String(50), nullable=False)

class Students(db.Model):
    __tablename__ = "students"
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    degree = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    joining_date = db.Column(db.String(50), nullable=False)
    retirement_date = db.Column(db.String(50), nullable=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/TeacherPortal',  methods=['GET', 'POST'])
def TeacherPortal():
    person = "Teachers"
    return render_template('StudentReq.html', person=person)

@app.route('/StudentPortal',  methods=['GET', 'POST'])
def StudentPortal():
    person = "Students"
    '''
    email = request.form.get('email')
    person_found = Students.query.filter_by(name=email).first()
    if('user' in session and session['user'] == person_found):
        return render_template('StudentPortal.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        if (email == person_found):
            session['user'] = email 
            return render_template('StudentPortal.html')
      '''                         
    return render_template('StudentReq.html', person=person)
    # return render_template('login.html')

@app.route('/Test')
def Test():
    return render_template('Test.html')


@app.route('/login')
def login():
    person = "Admin"
    action = "dashboard"
    return render_template('login.html',person=person,action=action)

@app.route('/loginTeacher')
def loginTeacher():
    person = "Teacher"
    action = "TeacherPortal"
    '''
    person_mail = request.form.get('email')
    person_pass = request.form.get('pass')
    person_found = Students.query.filter_by(name=(person_mail and person_pass)).first()

    if('user' in session and session['user'] == person_found):
        user = Students.query.all()
        db.session.commit()
        return render_template('TeacherPortal.html',person=person,action=action,user=user)

    elif (person_mail == person_found):
        session['user'] = person_mail
        user = Students.query.all()
        return render_template('TeacherPortal.html',person=person,action=action,user=user)

    # user = Students.query.all()
    # person_mail = request.form['email']
    # person_pass = request.form['password']
    # person_found = User.query.filter_by(name=person_mail).first()
'''
    return render_template('login.html',person=person,action=action )

@app.route('/loginStudent')
def loginStudent():
    person = "Student"
    action = "StudentPortal"
    '''
    person_mail = request.form.get('email')
    person_found = Students.query.filter_by(name=person_mail).first()

    if('user' in session and session['user'] == person_found):
        user = Students.query.all()
        db.session.commit()
        return render_template('StudentPortal.html',person=person,action=action,user=user)

    elif (person_mail == person_found):
        session['user'] = person_mail
        user = Students.query.all()
        return render_template('StudentPortal.html',person=person,action=action,user=user)
'''

    return render_template('login.html',person=person,action=action)

@app.route('/teachers')
def teachers():
    teachers = Teachers.query.all()
    return render_template('teachers.html',params=params, teachers=teachers)

@app.route('/addTeachers', methods=['GET', 'POST'])
def addTeachers():
    router = "addTeachers"
    person = "Teacher"
    extra = "Phone"
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('Phone')
        password = random.randint(111111,999999)
        joining_date = request.form.get('joining_date')
        retirement_date = request.form.get('retirement_date')
        entry = Teachers(name=name,email=email,phone=phone,password=password,joining_date=joining_date,retirement_date=retirement_date)
        db.session.add(entry)
        db.session.commit()
    return render_template('register.html',params=params,person=person,router=router,extra=extra)

@app.route('/students')
def students():
    students = Students.query.all()
    return render_template('students.html',params=params, students=students)

@app.route('/addStudents', methods=['GET', 'POST'])
def addStudents():
    router = "addStudents"
    person = "Student"
    extra = "Degree"
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        degree = request.form.get('Degree')
        password = random.randint(111111,999999)
        joining_date = request.form.get('joining_date')
        retirement_date = request.form.get('retirement_date')
        entry = Students(name=name,email=email,degree=degree,password=password,joining_date=joining_date,retirement_date=retirement_date)
        db.session.add(entry)
        db.session.commit()
    return render_template('register.html',params=params,person=person,router=router,extra=extra)

@app.route("/dashboard",  methods=['GET', 'POST'])
def dashboard():
    if('user' in session and session['user'] == params['admin_mail']):
        # teachers = Teachers.query.all()
        return render_template('dashboard.html',params=params)

    elif request.method == 'POST':
        userMail = request.form.get('email')
        userpass = request.form.get('pass')
        
        if ((userMail == params['admin_mail']) and (userpass == params['admin_password'])):
            session['user'] = userMail
            # teachers = Teachers.query.all()
            return render_template('dashboard.html',params=params)

    
    return render_template('login.html',params=params)

@app.route('/deleteTeacher', methods=["POST"])
def delete_teacher():
    teacher_name = request.form['target_teacher']

    teacher_found = Teachers.query.filter_by(name=teacher_name).first()

    db.session.delete(teacher_found)
    db.session.commit()

    myTeachers = Teachers.query.all()

    return render_template('teachers.html', teachers=myTeachers)

@app.route('/deleteStudent', methods=["POST"])
def delete_student():
    student_name = request.form['target_student']
    student_found = Students.query.filter_by(name=student_name).first()

    db.session.delete(student_found)
    db.session.commit()

    myStudents = Students.query.all()

    return render_template('students.html', students=myStudents)

@app.route("/edit/<string:srno>", methods=['GET', 'POST'])
def edit(srno):
    router = "addStudents"
    person = "Student"
    extra = "Degree"
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        degree = request.form.get('Degree')
        password = random.randint(111111,999999)
        joining_date = request.form.get('joining_date')
        retirement_date = request.form.get('retirement_date')

        student = Students.query.filter_by(srno=srno).first()
        student.name = name
        student.email = email
        student.degree = degree
        student.password = password
        student.joining_date = joining_date
        student.retirement_date = retirement_date
        db.session.commit()
        return redirect('/edit/'+srno)

    student = Students.query.filter_by(srno=srno).first()
    return render_template('edit.html',params=params,student=student,router=router,person=person,extra=extra,srno=srno)


@app.route("/editT/<string:srno>", methods=['GET', 'POST'])
def editT(srno):
    router = "addStudents"
    person = "Student"
    extra = "Phone"
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('Phone')
        password = random.randint(111111,999999)
        joining_date = request.form.get('joining_date')
        retirement_date = request.form.get('retirement_date')

        teacher = Teachers.query.filter_by(srno=srno).first()
        teacher.name = name
        teacher.email = email
        teacher.phone = phone
        teacher.password = password
        teacher.joining_date = joining_date
        teacher.retirement_date = retirement_date
        db.session.commit()
        return redirect('/editT/'+srno)

    student = Teachers.query.filter_by(srno=srno).first()
    return render_template('editT.html',params=params,teacher=teacher,router=router,person=person,extra=extra,srno=srno)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")


app.run(debug=True)