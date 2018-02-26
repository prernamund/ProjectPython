from flask import Flask,render_template,request,redirect,flash,url_for
from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,validators,BooleanField,DateField,SelectField,IntegerField
from wtforms.validators import DataRequired,required,Length,Email
from flask_mysqldb import MySQL
import MySQLdb
import passlib
from passlib.hash import sha256_crypt



import os

mysql=MySQL()

app=Flask(__name__,static_url_path='/static')
conn= MySQLdb.connect(host="127.0.0.1",user="root",password="",db="project")
# conn.close()




class Sign(Form):
  username=StringField('Email',[validators.Length(min=6,max=30),validators.Email('Invalid Email')])
  password=PasswordField('Password',[validators.required("password must be alphanumeric"), validators.Length(min=6,max=20)])
  confirmpassword=PasswordField('ConfirmPassword',[validators.required("passwords don't match")])
  
class LogIn(Form):
  username=StringField('Email',[validators.Email('Invalid Email')])
  password=PasswordField('Password',[validators.required('Invalid Credential')]) 
  remember=BooleanField('Remember Me')
class Regy(Form):
  name=StringField('Name',[validators.Length(min=5,max=20),validators.required('Please Enter Your Name')])
  mobile=StringField('Mobile',[validators.Length(min=10,max=12),validators.required('Please Enter Your Number')])
  email=StringField('Email',[validators.Length(min=6,max=30),validators.Email('Invalid Email')])
  Course = SelectField(u'Course', choices=[('None','None'),('Python','Python'),('AWS','AWS'),('C#','C#')],validators=[DataRequired()])
  source = SelectField(u'Source', choices=[('None','None'),('Website','Website'),('Facebook','Facebook'),('Suleka','Suleka')],validators=[DataRequired()])
  leadstatus = SelectField(u'leadstatus',choices=[('None','None'),('Demo','Demo'),('Counselling','Counselling'),('Callback','Callback')],validators=[DataRequired()])
  dm_coulg_cb = DateField('dm_coulg_cb', format='%Y-%m-%d')
  counselor=StringField('Counsellor',[validators.required('*')])
  remark=StringField('Remarks',[validators.required('*')])
class Cally(Form): 

  democall=SelectField(u'democall',choices=[('None','None'),('Demo','Demo'),('Counselling','Counselling'),('Callback','Callback')],validators=[DataRequired()])
  demodate = DateField('demodate', format='%Y-%m-%d')
class Counsel(Form): 
  todaydate=DateField('Todays Date',format='%Y-%m-%d')
  Course = SelectField(u'Course', choices=[('None','None'),('Python','Python'),('AWS','AWS'),('C#','C#')],validators=[DataRequired()])

  
class Joinny(Form): 
  name=StringField('Name',[validators.Length(min=5,max=20),validators.required('Please Enter Your Name')])
  Course = SelectField(u'Course', choices=[('None','None'),('Python','Python'),('AWS','AWS'),('C#','C#')],validators=[DataRequired()])
  completion_date=DateField('Completion Date',format='%Y-%m-%d')
  coursefee=StringField('Course_Fee',[validators.required("*")])
  joiningdate=DateField('JoiningDate',format='%Y-%m-%d')
  instructor=StringField("Instructor",[validators.required("*")])
  adhaarnum=StringField("AdhaarNumber",[validators.required("*")])
  email=StringField('Email',[validators.Length(min=6,max=30),validators.Email('Invalid Email')])
  remark=StringField('Remarks',[validators.required('*')])
  mobile=StringField('Mobile',[validators.Length(min=10,max=12),validators.required('Please Enter Your Number')])


class Update(Form):
     Name=StringField('Name',[validators.Length(min=5,max=20),validators.required('Please Enter Your Name')])
     Completion_date=DateField('Completion Date',format='%Y-%m-%d')

class Del(Form):
     Id=IntegerField('ID',[validators.required('*')])
     
class UpdateCounsel(Form):
     Name=StringField('Name',[validators.Length(min=5,max=20),validators.required('Please Enter Your Name')])
     Willing_Date=DateField('Completion Date',format='%Y-%m-%d')


@app.route("/")
def index():
  return render_template("index.html",title="SignUp")


@app.route("/SignUp", methods=['GET','POST'])  
def SignUp():
   form = Sign()
   print(form.errors)
   if form.is_submitted():
        print("submitted")

   if form.validate():
        print("valid")

   print(form.errors)
   if form.validate_on_submit() :
      username=str(request.form["username"])
      password=sha256_crypt.encrypt((str(form.password.data)))
      confirmpassword=sha256_crypt.encrypt((str(form.confirmpassword.data)))
   
      cursor=conn.cursor()
      cursor.execute("INSERT INTO signup (user_name,paswrd,con_pass) VALUES( %s,%s,%s)", (username,password,confirmpassword))
      conn.commit()
   # conn.close()
      return redirect(url_for("home"))  
   return render_template('index.html',form=form)      



@app.route("/Authenticate", methods=['GET','POST'])
def Authenticate():
  form = LogIn()
  print(form.errors)
  if form.is_submitted():
      print("submitted")

  if form.validate():
        print("valid")

  print(form.errors)
  if form.validate_on_submit() :
    username = form.username.data
    password = form.password.data
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM signup WHERE user_name='" + username + "' and paswrd='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return redirect(url_for("home"))
  return render_template('login.html',form=form)  

@app.route("/home")  
def home():
  return render_template("home.html")



@app.route('/register',methods=['GET','POST'])
def register():
    form=Regy()
    print(form.errors)
    

    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)
    if form.validate_on_submit():


        name=form.name.data
        mobile=form.mobile.data
        email=form.email.data
        Course=form.Course.data
        source=form.source.data
        leadstatus=form.leadstatus.data
        dm_coulg_cb=form.dm_coulg_cb.data
        counselor=form.counselor.data
        remark=form.remark.data 
        
        
        cursor=conn.cursor()
        cursor.execute("INSERT INTO registers (Name,Mobile_No,Email,Course,Source,LeadStatus,Dm_coulg_cb,Counsellor,Remark) VALUES( %s,%s,%s,%s,%s,%s,%s,%s,%s)", (name,mobile,email,Course,source,leadstatus,dm_coulg_cb,counselor,remark))
        conn.commit()
        # conn.close()


      
        return redirect(url_for('walkins'))      

    return render_template('register.html',form=form)   



@app.route('/calling',methods=['GET','POST'])

def calling():
    form=Cally()
    print(form.errors)
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)
    if form.validate_on_submit():
       democall=form.democall.data
       demodate=form.demodate.data
       cursor=conn.cursor()

       cursor.execute('''SELECT * FROM registers WHERE LeadStatus =%s AND Dm_coulg_cb=%s''',(democall,demodate))
       return render_template('calling1.html',rv=cursor.fetchall(),form=form)
       # conn.close()
       # data=cursor.fetchone()
       # if data is None:
       #  return "DataNotFound"
       # else:
        
       #  return 'calling'
       
       
    return render_template('calling.html',form=form)  


  
@app.route('/counselling', methods=['GET','POST'])     

def  counselling(): 


    form=Counsel()
    print(form.errors)
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)
    if form.validate_on_submit() :


        todaydate=form.todaydate.data
        Course=form.Course.data
        cursor=conn.cursor()
        cursor.execute('''SELECT * FROM registers WHERE   Dm_coulg_cb=%s AND Course=%s  ''',(todaydate,Course))
       

        return render_template('counsel1.html', rv = cursor.fetchall(),form=form)
        
    return render_template('counselling.html',form=form)   

@app.route('/Joinings', methods=['GET','POST'])

def Joining():
    form=Joinny()
    print(form.errors)
    

    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)
    if form.validate_on_submit():


        name=form.name.data
        Course=form.Course.data
        completion_date=form.completion_date.data
        joiningdate=form.joiningdate.data
        coursefee=form.coursefee.data
        instructor=form.instructor.data
        adhaarnum=form.adhaarnum.data
        mobile=form.mobile.data
        email=form.email.data
        remark=form.remark.data
        cursor=conn.cursor()
        cursor.execute("INSERT INTO joinings (Name,Course,CompletionDate,JoiningDate,CourseFee,Instructor,AdhaarNo,Mobile_No,Email,Remark) VALUES( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name,Course,completion_date,joiningdate,coursefee,instructor,adhaarnum,mobile,email,remark))
        conn.commit()
        
        return '<h1>Joined</h1>'
    return render_template('joinin.html',form=form)  

@app.route('/walkins',methods=['GET'])
def walkins():

  form=Regy()
  cursor=conn.cursor()
  cursor.execute('''SELECT * FROM registers''')

  
  return render_template('walkins.html',rv=cursor.fetchall(),form=form)


@app.route('/status',methods=['GET'])
def status():

  form=Joinny()
  cursor=conn.cursor()
  cursor.execute('''SELECT * FROM joinings  WHERE   DATE_FORMAT(CompletionDate, '%Y-%m-%d') AND  CompletionDate <= (CURDATE() - INTERVAL 30 DAY)''')
  

  return render_template('status.html',rv=cursor.fetchall(),form=form)

  
@app.route('/currentstatus',methods=['GET'])
def currentstatus():
  form=Joinny()
  cursor=conn.cursor()
  cursor.execute('''SELECT  ID,Course,Name,CompletionDate,JoiningDate,Instructor,Mobile_No,Email FROM joinings''')

  return render_template('currstatus.html',rv=cursor.fetchall(),form=form)


@app.route('/updateprofile',methods=['GET','POST']) 
def updateprofile():
  form=Update()
  
  if form.validate_on_submit():
    Name=form.Name.data
    Completion_date=form.Completion_date.data

    cursor=conn.cursor()
    cursor.execute('''UPDATE joinings SET CompletionDate=%s WHERE Name=%s''',(Name,Completion_date)) 
    conn.commit()
    
    return '<h1>Updated</h1>'
  return render_template('update.html',form=form)
@app.route("/updateCouns",methods=['GET','POST'])
def updateCouns():
  form=UpdateCounsel()
  if form.validate_on_submit():
    Name=form.Name.data
    Willing_Date=form.Willing_Date.data
    cursor=conn.cursor()
    cursor.execute('''UPDATE registers SET Dm_coulg_cb=%s WHERE Name=%s''',(Willing_Date,Name))
    conn.commit()
    return '<h1>Updated</h1>'
    # return render_template('updatecounsel.html',form=form)
  return render_template('updatecounsel.html',form=form)
@app.route('/deletepro',methods=['GET','POST'])
def deletepro():
  form=Del()
  
  Id=form.Id.data
  cursor=conn.cursor()
  cursor.execute('''DELETE FROM registers WHERE ID=%d''',(Id))
  conn.commit()
  
  return redirect(url_for('home'))





if __name__=='__main__':
    app.secret_key = 'xyz'
    app.run(debug=True)