# start with the imports
from sqlalchemy import exc
import pandas as pd
import random
import requests
import json
import pprint
import pdb
import sqlite3
from functools import wraps
from sqlalchemy.types import String
from flask import Flask, request, render_template, url_for, flash, redirect, g, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy

DATABASE ='./jobify.db'


app = Flask(__name__)
bcrypt = Bcrypt(app)
proxied = FlaskBehindProxy(app)

app.config['SECRET_KEY'] = 'f8ab5567ef84a9ee5c1e3d86bb8b9ef9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobify.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db = SQLAlchemy(app)
Session(app)

# '''# interchange use of API Keys to limit searches to not get 100
API_KEYS = ('e21193f2b2ee7a0a7042c7a414822b20b10c84609c42a408732401d8b62ddc06',
            '9e8e77e8075bf5f1bfbbef8848ba3b735d1cf01e0490877307eded9945e41777',
            'c385df59163477b88fa13574e0bb8886c32b687a8eb0b8dded75b959def7262b')

key_index = random.randint(0, 2)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            flash("Error: Need to be logged in to access.", 'error')
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.id}')"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def valid_login(username, password):
    try:
        user = query_db('select * from User where username = ?', [username], one=True)
        if user is None:
            return False
        hashed_pw = user[2]
        return bcrypt.check_password_hash(hashed_pw, password)
    except ValueError as e:
        flash("Invalid login")

@app.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('homepage'))

def log_the_user_in(username):
    if session.get('username', None):
        return True
    session['username'] = username
    return redirect(url_for('job_search'))

class SavedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    job_title=db.Column(db.String())
    company_name=db.Column(db.String())
    location=db.Column(db.String())
    description=db.Column(db.String())
    def __repr__(self):
        return f"Job:('{self.job_title}: {self.company_name}')"

@app.route("/saved_jobs", methods=('GET', 'POST'))
def save_job():
    #new comment test
    # print(request_data.get('job_title'))
    #get value from checkbox?
    if request.method == 'POST':
        job_title = request.json.get('job_title')
        company_name = request.json.get('company_name')
        job_location = request.json.get('location')
        job_description = request.json.get('description')
        savedjob = SavedJob(username=session['username'], job_title=job_title,company_name=company_name, location=job_location, description=job_description)
        db.session.add(savedjob)
        db.session.commit()
        # return jsonify(status="success")
        # return render_template(('saved_jobs.html'), job_title=job_title, company_name=company_name, job_location=job_location, job_description=job_description)

@app.route("/resume-builder", methods=('GET', 'POST'))
def resume_builder():
    return render_template('resume-builder.html')
    #get info from form, present it as a template
    
@app.route("/resume_display", methods=('GET', 'POST'))
def resume_display():
    if request.method == 'POST':
        print(request.form.get('name'))
        try:
            name = request.form.get('name')
            title = request.form.get('title')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            education = request.form.get('phone_number')
            education_address = request.form.get('education_address')
            major = request.form.get('major')
            gpa = request.form.get('gpa')
            skill_title1 = request.form.get('skill_title1')
            skill_description1 = request.form.get('skill_description1')
            skill_title2 = request.form.get('skill_title2')
            skill_description2 = request.form.get('skill_description2')
            skill_title3 = request.form.get('skill_title3')
            skill_description3 = request.form.get('skill_description3')
            #relevant skills
            relevant_skill1 =  request.form.get('relevant_skill1')
            relevant_skill2 =  request.form.get('relevant_skill2')
            relevant_skill3 =  request.form.get('relevant_skill3')
            relevant_skill4 =  request.form.get('relevant_skill4')
            relevant_skill5 =  request.form.get('relevant_skill5')
            relevant_skill6 =  request.form.get('relevant_skill6')
            relevant_skill7 =  request.form.get('relevant_skill7')
            relevant_skill8 =  request.form.get('relevant_skill8')
            relevant_skill9 =  request.form.get('relevant_skill9')
            relevant_skill10 =  request.form.get('relevant_skill10')
            #professional exeperince section
            company1 = request.form.get('company1')
            position1 = request.form.get('position1')
            position_description1 = request.form.get('position_description1')
            start_date1 = request.form.get('start_date1')
            end_date1 = request.form.get('end_date1')

            company2 = request.form.get('company2')
            position2 = request.form.get('position2')
            position_description2 = request.form.get('position_description2')
            start_date2 = request.form.get('start_date2')
            end_date2 = request.form.get('end_date2')

            company3 = request.form.get('company3')
            position3 = request.form.get('position3')
            position_description3 = request.form.get('position_description3')
            start_date3 = request.form.get('start_date3')
            end_date3 = request.form.get('end_date3')

            company4 = request.form.get('company4')
            position4 = request.form.get('position4')
            position_description4 = request.form.get('position_description4')
            start_date4 = request.form.get('start_date4')
            end_date4 = request.form.get('end_date4')

            company5 = request.form.get('company5')
            position5 = request.form.get('position5')
            position_description5 = request.form.get('position_description5')
            start_date5 = request.form.get('start_date5')
            end_date5 = request.form.get('end_date5')

            #Affiliations/Interests Tab
            affiliations = request.form.get('affiliations')
            certifications = request.form.get('certifications')
            awards = request.form.get('awards')
            interests = request.form.get('interests')
            publications = request.form.get('publications')
            volunteer = request.form.get('volunteer') 
        except KeyError:
            flash('Error: Try Again')
    return render_template('resume_display.html', name = name, title = title, email = email,
            phone_number = phone_number, education = education,
            major = major, gpa = gpa, education_address = education_address,
            skill_title1 = skill_title1, skill_description1 = skill_description1,
            skill_title2 = skill_title2, skill_description2 = skill_description2,
            skill_title3 = skill_title3, skill_description3 = skill_description3,
            relevant_skill1 =  relevant_skill1, relevant_skill2 =  relevant_skill2,
            relevant_skill3 =  relevant_skill3, relevant_skill4 =  relevant_skill4,
            relevant_skill5 =  relevant_skill5, relevant_skill6 =  relevant_skill6,
            relevant_skill7 =  relevant_skill7, relevant_skill8 =  relevant_skill8,
            relevant_skill9 =  relevant_skill9, relevant_skill10 =  relevant_skill10,
            company1 = company1, position1 = position1, 
            position_description1 = position_description1,
            start_date1 = start_date1, end_date1 = end_date1, company2 = company2, 
            position2 = position2,
            position_description2 = position_description2, start_date2 = start_date2, 
            end_date2 = end_date2, company3 = company3, position3 = position3,
            position_description3 = position_description3,
            start_date3 = start_date3, end_date3 = end_date3,company4 = company4, 
            position4 = position4, position_description4 = position_description4, 
            start_date4 = start_date4, end_date4 = end_date4,
            company5 = company5, position5 = position5,
            position_description5 = position_description5, start_date5 = start_date5,
            end_date5 = end_date5, affiliations = affiliations,
            certifications = certifications, awards = awards, interests = interests,
            publications = publications, volunteer = volunteer )
    

@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/job_search", methods=('GET', 'POST'))
@login_required
def job_search():
    if request.method == 'POST':
        try:
            job_fields = request.form['fields']
            job_location = request.form['location']
            #parse info from form into api to get request
            r = requests.get(f'https://serpapi.com/search.json?engine=google_jobs&q={job_fields}&location={job_location}&api_key={API_KEYS[key_index]}')
            data = r.json()['jobs_results']
            return render_template('jobs_list.html', data = data)
        except KeyError:
            return render_template('error.html')
    return render_template('job_search.html')

@app.route("/jobs_list")
@login_required
def jobs_list():
    return render_template('jobs_list.html')


@app.route("/about")
@login_required
def about_page():
    return render_template('about.html')

@app.route("/saved-jobs")
@login_required
def saved_jobs_page():
    engine = db.create_engine('sqlite:///jobify.db', {})
    query = engine.execute(f"SELECT * FROM saved_job WHERE username = '{session['username']}';").fetchall()
    # jobs_saved = saved_job.query.all()
    return render_template('saved-jobs.html', jobs = query)

@app.route("/contact")
def contact_page():
    return render_template('contact.html')

@app.route('/register', methods=('GET', 'POST'))
def register_form():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        try:
            hashed_pw = bcrypt.generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=hashed_pw)
            # engine = db.create_engine('sqlite:///jobify.db', {})
            # id = engine.execute("INSERT INTO user (username, password) VALUES(?, ?)", form.username.data, form.password.data)
            # print(id)
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
        except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            if 'UNIQUE' in error:
                flash('Unique Error: Username already taken. Please Try again with a Different Username', 'error')
            else:
                flash('Error: Try Again', 'error')
            return redirect(url_for('register_form'))
        else:
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('homepage'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    session.clear()
    print(session)
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'

    return render_template('login.html', error=error)

@app.route('/delete_job', methods=('GET', 'POST'))
def delete_job():
    if request.method == 'POST':
        print("Post request working")
        job_title = request.json.get('job_title')
        engine = db.create_engine('sqlite:///jobify.db', {})
        # query = engine.execute(f"DELETE FROM saved_job WHERE job_description = '{job_description}';").fetchall()
        query = engine.execute(f"DELETE FROM saved_job WHERE job_title = '{job_title}';")
        db.session.commit()
        return render_template('delete_job.html')



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    db.create_all()
# comment for testing git mob
'''# interchange use of API Keys to limit searches to not get 100
API_KEYS = ('e21193f2b2ee7a0a7042c7a414822b20b10c84609c42a408732401d8b62ddc06',
            '9e8e77e8075bf5f1bfbbef8848ba3b735d1cf01e0490877307eded9945e41777')

key_index = random.randint(0, 1)


def print_func(query):
    df = pd.DataFrame(query)
    df.columns = ['user_id', 'title', 'company_name', 'location', 'via', 'description', 'job_id', 'detected_extensions.posted_at', 'detected_extensions.schedule_type']
    pprint.pprint(df)

def print_links(id_list):
        list_data = []
        for id in id_list:
            request = requests.get(f'https://serpapi.com/search.json?\
engine=google_jobs_listing&q={id}&api_key={API_KEYS[key_index]}')
            link_data = request.json()["apply_options"]
            list_data.append(link_data)
        for i in range(len(list_data)):
            print(f'job {i + 1}:')
            for j in range(len(list_data[i])):
                for key, value in list_data[i][j].items():
                    if key == 'link' and j <= 3:
                        print(f'Application Link {j}: {list_data[i][j][key]}')

def user_check(user_name):
    if user_name == None:
        return False
    names = user_name.split('_')
    if len(names) != 2:
        print("Invalid firstname_lastname")
        return False
    for name in names:
        for letter in name:
            if not ('a' <= letter <= 'z') and not ('A' <= letter <= 'Z'):
                print("Invalid firstname_lastname")
                return False
    return True

def enter_into_database(data, user):
    data_table = pd.json_normalize(data)
    data_table.insert(0, 'user_id', user)
    # print(data_table)
    engine = db.create_engine('sqlite:///job-search-results.db')
    data_table.to_sql('jobs', con=engine, if_exists='append', index=False)#need to fix
    query = engine.execute(f"SELECT * FROM jobs WHERE user_id='{user}'").fetchall()
    print_func(query)
    return engine

def program_driver(user_name):
    engine = db.create_engine('sqlite:///job-search-results.db')
    num_user = engine.execute(f"SELECT COUNT(user_id) FROM jobs WHERE user_id='{user_name}';").fetchone()[0]
    if num_user > 0:
        print(f"Welcome back, {user_name.replace('_', ' ').title()}!")
        query = engine.execute(f"SELECT * FROM jobs WHERE user_id='{user_name}';")
        id_list = engine.execute(f"SELECT job_id FROM jobs WHERE user_id='{user_name}';").fetchall()
        id_list = [id[0] for id in id_list]
        print_func(query)
        print_links(id_list)
        answer = input("If you would like to research different jobs, press 'y' and hit enter. Otherwise, hit enter: ").lower().strip()
        if answer == 'y':
            search_api()
    else:
        search_api()

def print_links(job_id):
            list_data = []
            request = requests.get(f'https://serpapi.com/search.json?\
            engine=google_jobs_listing&q={job_id}&api_key={API_KEYS[key_index]}')
            try:
                link_data = request.json()["apply_options"]
                list_data.append(link_data)
            except KeyError as k:
                return None
            return list_data
def search_api():
    job_fields = input("Enter comma-separated fields \
in which you would like to search for jobs: ").strip()
    location = input("(OPTIONAL) Enter a location for jobs,\
else hit enter: ").strip()

    
    # make GET request and convert to json data containing job results
    r = requests.get(f'https://serpapi.com/search.json?engine=google_jobs&q={job_fields}&location={location}&api_key={API_KEYS[key_index]}')
    data = r.json()['jobs_results']
    for job in data:
        job.pop('extensions', None)
        job.pop('thumbnail', None)
    pprint.pprint(data[:5])

    job_nums = input("type the number of the job you are interested in. \
(Number meaning what place in the order shown) If you are interested \
in multiple, seperate numbers with a ',': ")
    nums = job_nums.split(',')
    id_list = []
    dict_list = []
    for num in nums:
        id_list.append(data[int(num) - 1]['job_id'])
        dict_list.append(data[int(num) - 1])   
    enter_into_database(dict_list, user_name)
    print_links(id_list) 

if __name__ == '__main__':
    user_name = None
    while not user_check(user_name):
        user_name = input("Please type your firstname_lastname: ").lower().strip()
    program_driver(user_name)'''
