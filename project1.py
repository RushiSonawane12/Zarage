from datetime import date,datetime
from flask import Flask, render_template, request, redirect, url_for, session,flash, Response, send_file
from flask_mail import Mail, Message
from fpdf import FPDF

import numpy as np
import io

import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt 
# import seaborn as sns
from flask_mysqldb import MySQL

import MySQLdb.cursors
# plt.rcParams["figure.figsize"] = [7.50, 3.50]
# plt.rcParams["figure.autolayout"] = True
date=datetime.now()



import re


app=Flask(__name__)

app.secret_key='secret key'



app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='project'

mysql=MySQL(app)



# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'jadhavsharu11@gmail.com'
# app.config['MAIL_PASSWORD'] = '9372854229'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True



# mail = Mail(app)

# @app.route("/send")
# def index1():
#    msg = Message('Hello', sender = 'jadhavsharu11@gmail.com', recipients = ['karishmakumarimali555@gmail.com'])
#    msg.body = "This is the email body"
#    mail.send(msg)
#    return "Sent"


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/base')
def base():
    return render_template("base.html")



@app.route('/about')
def about():
    return render_template("about.html")



@app.route('/feedback',methods=['POST','GET'])
def feedback():
    msg=""
    if request.method=='POST':
        fullname=request.form['fullname']
        email_id=request.form['email_id']
        phoneno=request.form['phoneno']
        message=request.form['message']
        cursor=mysql.connection.cursor()
        cursor.execute("insert into feedback (fullname,email_id,phoneno,message) values (%s,%s,%s,%s)",(fullname,email_id,phoneno,message,))
        mysql.connection.commit()
        msg="Your feedback send successfully....."
    return render_template("feedback.html",msg=msg)



@app.route('/service')
def service():
    return render_template("service.html")



@app.route('/team')
def team():
    return render_template("team.html")



@app.route('/checkavailability',methods =['GET', 'POST']) 
def check():
    if request.method == 'POST' and 'zipcode1' in request.form:
        zipcode1 = request.form['zipcode1']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT zipcode from project.pincode')  
        data = cursor.fetchall()
        print(data)
        #for field in data:
        #    print(field)
        #    for value in field.items():
        if not re.match(r'[0-9]+', zipcode1):
            flash("zipcode must contain number")
            return redirect(url_for('index')) 
        elif len(zipcode1)==6:
            for field in data:  
                print(field)      
                for key,value in field.items():
                    if int(zipcode1) == value:
                        flash("service is available for your area")
                        return redirect(url_for('index'))
        elif len(zipcode1)!=6:
            flash("zipcode must contain six digit")
            return redirect(url_for('index'))
        else:
            flash("service is not available for your area")
            return redirect(url_for('index'))
    elif request.method == 'POST':
        flash('Please fill out the form !')
        return redirect(url_for('index')) 
    return render_template("checkavailability.html")


# @app.route('/checkavailability',methods =['GET', 'POST']) 
# def check():
#     msg=""
#     if request.method == 'POST' and 'zipcode1' in request.form:
#         zipcode1 = request.form['zipcode1']

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT zipcode from project.pincode')  
#         data = cursor.fetchall()
#         print(data)
#         #for field in data:
#         #    print(field)
#         #    for value in field.items():
#         if not re.match(r'[0-9]+', zipcode1):
#             msg="zipcode must contain number"
           
#         elif len(zipcode1)==6:
#             for field in data:  
#                 print(field)      
#                 for key,value in field.items():
#                     if int(zipcode1) == value:
#                         msg="service is available for your area"
                       
#         elif len(zipcode1)!=6:
#             msg="zipcode must contain six digit"
            
#         else:
#             msg="service is not available for your area"
            
#         print(msg)
#         return redirect(url_for('index'))
#     elif request.method == 'POST':
#         msg='Please fill out the form !'
#         return redirect(url_for('index')) 
#     return render_template("checkavailability2.html")




@app.route('/checkavailability1',methods =['GET', 'POST']) 
def check1():
    if request.method == 'POST' and 'zipcode1' in request.form:
        zipcode1 = request.form['zipcode1']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT zipcode from project.pincode')  
        data = cursor.fetchall()
        print(data)
        #for field in data:
        #    print(field)
        #    for value in field.items():
        if not re.match(r'[0-9]+', zipcode1):
            flash("zipcode must contain number")
            return redirect(url_for('index')) 
        elif len(zipcode1)==6:
            for field in data:  
                print(field)      
                for key,value in field.items():
                    if int(zipcode1) == value:
                        flash("service is available for your area")
                        return redirect(url_for('usersignin'))
        elif len(zipcode1)!=6:
            flash("zipcode must contain six digit")
            return redirect(url_for('index'))
        else:
            flash("service is not available for your area")
            return redirect(url_for('index'))
    elif request.method == 'POST':
        flash('Please fill out the form !')
        return redirect(url_for('index')) 
    return render_template("checkavailability1.html")





@app.route('/usersignin', methods =['GET', 'POST'])
def usersignin():
    msg = ''
    if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:
        email_id = request.form['email_id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE email_id = % s AND password = % s', (email_id, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['customer_id']
            session['email_id'] = account['email_id']
            return redirect(url_for('userdashboard'))
        else:
            msg = 'Incorrect email_id / password !'
    return render_template('usersignin.html', msg=msg)




@app.route('/usersignup', methods =['GET', 'POST'])
def usersignup():
    msg = ''
    if request.method == 'POST' and 'fullname' in request.form and 'phoneno' in request.form and 'email_id' in request.form and 'password' in request.form:
        fullname = request.form['fullname']
        phoneno = request.form['phoneno']
        email_id = request.form['email_id']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from customer where email_id = %s',(email_id, ))
        output = cursor.fetchone()
        if output:
            msg = 'Account already exists !'

            #singn up validations start

        elif not fullname or not phoneno or not email_id or not password:
            msg = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'password must contain only characters and numbers !'


        # singn up validations end


        else:
            cursor.execute("insert into project.customer (fullname,phoneno,email_id,password) values (%s,%s,%s,%s)",(fullname,phoneno,email_id,password, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('usersignup.html', msg = msg)



    
@app.route('/admin', methods =['GET', 'POST'])
def admin():
    msg = ''
    if request.method == 'POST' and 'adminname' in request.form and 'password' in request.form:
        adminname = request.form['adminname']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adminlogin WHERE adminname = % s AND password = % s', (adminname, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['adminname'] = account['adminname']
            return redirect(url_for('admindashboard'))

        else:
            msg = 'Incorrect adminname/ password !'
    return render_template('admin.html', msg=msg)



@app.route('/addmechanic',methods=['GET','POST'])
def addmechanic():
    print('hi')
    if request.method=='POST' and 'name' in request.form and 'password' in request.form:
        print('hello')
        name=request.form['name']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select name from project.mechanic where name = %s',(name, ))
        output = cursor.fetchone()
        print(output)
        print('hello')
        if output:
            flash('Account already exists !')
        elif not re.match(r'[A-Za-z]+', name):
            flash('password must contain only characters and numbers !')
        else:
            cursor.execute("insert into project.mechanic (name,password) values (%s,%s)",(name,password, ))
            mysql.connection.commit()
            flash("mechanic added")
        return redirect(url_for('addmechanic'))
    return render_template("addmechanic.html")



@app.route('/mechanicedit',methods=['POST','GET'])
def mechanicedit():
    cursor=mysql.connection.cursor()
    cursor.execute("select password from mechanic")
    data=cursor.fetchone()
    cursor.close()
    return render_template('mechanicupdate.html',data=data)



@app.route('/mechanicupdate/<p>',methods=['POST'])
def mechanicupdate(p):
    if request.method=='POST':
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute("update mechanic set password=%s where password=%s",(password,p))
        mysql.connection.commit()
        flash('Updated')
        return redirect(url_for('mechanicedit'))



@app.route('/mechanic', methods =['GET', 'POST'])
def mechanic():
    msg = ''
    if request.method == 'POST' and 'password' in request.form:
        mechanicname = request.form['mechanicname']
        password = request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute("select name,password from mechanic where name=%s and password=%s",(mechanicname,password,))
        data=cursor.fetchone()
        print(data)
        
        if data:
            session['loggedin'] = True
            session['mechanic']=mechanicname
            return redirect(url_for('mechanicdashboard'))
        else:
            msg = 'Incorrect service password /Mechanic Name!'
    return render_template('mechanic.html', msg=msg)





@app.route("/mechanicdashboard")
def  mechanicdashboard():
    return render_template('mechanicdashboard.html')



@app.route('/mechanicbillpending')
def mechanicbillpending():
        cursor=mysql.connection.cursor()
        cursor.execute("select billno,name,model from project.adminserviceform,project.Bill where adminrespond=%s and billstatus=%s and serviceby=%s and adminserviceform.s_id=Bill.s_id",("completed","notpaid",session['mechanic'],))
        data=cursor.fetchall()
        print(data)
        cursor.close()
        return render_template('mechanicpendingbill.html',customer=data)



@app.route('/mechanicpendingbilledit/<billno>',methods=['POST','GET'])
def mechanicpendingbilledit(billno):
        cursor=mysql.connection.cursor()
        cursor.execute("select s_id from Bill where billno=%s",(billno,))
        service_id=cursor.fetchone()
        cursor.execute("select name from adminserviceform where s_id=%s",(service_id,))
        data=cursor.fetchone()
        cursor.execute("select s_id,billno,totalbill from Bill where billno=%s",(billno,))
        data1=cursor.fetchall()
        print(data)
        print(billno)
        cursor.close()
        return render_template('mechanicpendingbillupdate.html',data1=data1,data=data) 



@app.route('/mechanicpendingbillupdate/<billno>',methods=['POST'])
def mechanicpendingbillupdate(billno):
    if request.method=='POST':
        billstatus=request.form['billstatus']
        cursor=mysql.connection.cursor()
        date1=str(date.today())
        cursor.execute("update Bill set billstatus=%s,paiddate=%s where billno=%s",(billstatus,date1,billno,))
        mysql.connection.commit()
        flash("Bill Updated")
        cursor.close()
        return redirect(url_for('mechanicbillpending'))



@app.route("/forgotpassword", methods=['POST','GET'])
def forgotpassword():
    msg = ''
    if request.method == 'POST' and 'fullname' in request.form and 'email_id' in request.form and 'password' in request.form:
        fullname = request.form['fullname']
        email_id = request.form['email_id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from customer where fullname = %s and email_id = %s', (fullname,email_id))
        acc = cursor.fetchone()
        if acc:
                cursor.execute('update customer set password = %s where fullname = %s and email_id = %s',(password,fullname,email_id))
                mysql.connection.commit()
                cursor.close()
                return render_template('usersignin.html')
        else:
            msg = 'Incorret fullname or email_id'
    return render_template("forgotpassword.html",msg=msg)


@app.route('/graph')
def graph():
    from PIL import Image
    cursor=mysql.connection.cursor()
    cursor.execute("select service_type,count(*) from adminserviceform where month(r_date)=month(current_date()) group by service_type")
    data5=cursor.fetchall()
    print(data5)
    cursor.execute("select servicename from service")
    data6=cursor.fetchall()
    x = [] 
    y = []
    label="Highest service of current month"
    explode = (0.1, 0, 0) 
    for value in data5:         
        x.append(value[0])  #x column contain data(1,2,3,4,5) 
        y.append(value[1]) 
    fig1=plt.figure(figsize =(10, 7)) 
    # plt.pie(labels=x,values=y,0.3,colors="orange",autopct='%1.1f%%', shadow=True, startangle=140)
    colors = ['lightgray', 'darkorange', 'gray']
    plt.pie(y, explode=explode, labels=x, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Highest service of current month")
    # plt.xlabel("servicetype")
    # plt.ylabel("Value")
    plt.legend()
    plt.axis('equal')
    img=fig1.savefig('static/images/highest.jpg')
    canvas=FigureCanvas(fig1)
    img=io.BytesIO()
    fig1.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/jpg')



@app.route("/admindashboard")
def  admindashboard():
    cursor=mysql.connection.cursor()
    query="select* from project.customer"
    cursor.execute(query)
    data=cursor.fetchall()
    c1=0
    for i1 in data:
        c1=c1+1
    cursor.execute("select* from enquiryresponded")
    data1=cursor.fetchall()
    c2=0
    for i in data1:
        c2=c2+1
    cursor.execute("select* from serviceform")
    data2=cursor.fetchall()
    c3=0
    for i in data2:
        c3=c3+1
    cursor.execute("select* from project.adminserviceform where adminrespond=%s",("pending",))
    data3=cursor.fetchall()
    c4=0
    for value in data3:
        c4=c4+1
    cursor.execute("select* from project.adminserviceform where adminrespond=%s",("reject",))
    data4=cursor.fetchall()
    c5=0
    for value in data4:
        c5=c5+1
    cursor.execute("select* from project.adminserviceform,Bill where adminrespond=%s and billstatus=%s and adminserviceform.s_id=Bill.s_id",("completed","paid",))
    data5=cursor.fetchall()
    c6=0
    for value in data5:
        c6=c6+1
    
    cursor.execute("select service_type,count(*) from adminserviceform where month(r_date)=month(current_date()) group by service_type")
    data6=cursor.fetchall()
    print(data6)
    cursor.execute("select servicename from service")
    data7=cursor.fetchall()
    x = [] 
    y = []
    label="Highest service of current month"
    explode = (0.1, 0, 0) 
    for value in data6:         
        x.append(value[0])  #x column contain data(1,2,3,4,5) 
        y.append(value[1]) 
    fig1=plt.figure(figsize =(5, 3)) 
    # plt.pie(labels=x,values=y,0.3,colors="dimgray",autopct='%1.1f%%', shadow=True, startangle=140)
    colors = ['lightgray', 'red', 'gray']
    plt.pie(y, labels=x, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Highest Service of Current month",color="red")
    # plt.xlabel("servicetype",color="orangered")
    # plt.ylabel("Value",color="orangered")
    plt.legend()
    plt.axis('equal')
    img=fig1.savefig('static/images/highest.jpg')
    canvas=FigureCanvas(fig1)
    img=io.BytesIO()
    fig1.savefig(img)
    img.seek(0)
    return render_template("admindashboard.html",c1=c1,c2=c2,c3=c3,c4=c4,c5=c5,c6=c6)



@app.route("/userdashboard")
def  userdashboard():
    msg=""
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE customer_id = % s', (session['id'], ))
        data=cursor.fetchone()
        return render_template("userdashboard.html",customer=data)
    else:
        msg="login first"
        return render_template("usersignin.html",msg=msg)



@app.route('/clogout')
def clogout():
        session.pop('loggedin',None)
        session.pop('id', None)
        session.pop('email_id',None)
        return redirect(url_for('index'))


@app.route('/alogout')
def alogout():
        session.pop('loggedin',None)
        session.pop('adminname',None)
        return redirect(url_for('index'))


@app.route('/mlogout')
def mlogout():
        session.pop('loggedin',None)
        session.pop('mechnanic',None)
        return redirect(url_for('index'))



@app.route('/totalregistered')
def totalregistered():
        cursor=mysql.connection.cursor()
        query="select* from project.customer"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('totalregistered.html',customer=data)



@app.route('/newservice')
def newservice():
        cursor=mysql.connection.cursor()
        cursor.execute("select service_id,s_id,name,r_date,email_id from project.serviceform,project.customer where serviceform.customer_id=customer.customer_id")
        data=cursor.fetchall()
        print(data)
        return render_template('newservice.html',customer=data)





@app.route('/editnewservice/<service_id>',methods=['POST','GET'])
def editnewservice(service_id):
        cursor=mysql.connection.cursor()
        cursor.execute("select s_id,name,model,cartype,r_no,service_type,date,time,deliverytype,pickup,dropaddress,pincode from serviceform,customer where serviceform.customer_id=customer.customer_id and service_id=%s",(service_id,))
        data=cursor.fetchall()
        cursor.execute("select servicename from service,serviceform where serviceform.s_id=service.s_id and service_id=%s",(service_id,))
        data1=cursor.fetchall()
        cursor.close()
        print(data)
        print(data1)
        return render_template('editnewservice.html',customer=data,customer1=data1) 





@app.route('/serviceformrespond/<service_id>',methods=['POST'])
def serviceformrespond(service_id):
    if request.method=='POST':
            adminrespond = request.form['adminrespond']
            dropdate = request.form['dropdate']
            droptime = request.form['droptime']
            description = request.form['description']
            cursor=mysql.connection.cursor()
            print(adminrespond)
            cursor.execute("select name,model,cartype,r_no,service_type,date,time,deliverytype,pickup,dropaddress,r_date,customer_id,pincode from serviceform where s_id=%s",(service_id,))
            data=cursor.fetchall()
            print(data)
            cursor.execute("select customer_id from serviceform where s_id=%s",(service_id,))
            data4=cursor.fetchone()
            cursor.execute("select email_id from customer where customer_id=%s",(data4,))
            data5=cursor.fetchone()
            cursor.execute("select servicename from service where s_id=%s",(service_id,))
            data1=cursor.fetchall()
            for value in data:
                print(value[7])
                session['delivery']=value[7]
            for value in data:
                print(value[7])
                if session['delivery']=="pickdrop":
                    cursor.execute("insert into adminserviceform (s_id,name,model,cartype,r_no,service_type,pickupdate,pickuptime,dropdate,droptime,deliverytype,pickup,dropaddress,r_date,customer_id,adminrespond,pincode) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(service_id,value[0],value[1],value[2],value[3],value[4],value[5],value[6],dropdate,droptime,value[7],value[8],value[9],value[10],value[11],adminrespond,value[12],))
                    mysql.connection.commit()
                    cursor.execute("delete from serviceform where s_id=%s",(service_id,))
                    mysql.connection.commit()
                    
                elif session['delivery']=="dropaddress":
                    cursor.execute("insert into adminserviceform (s_id,name,model,cartype,r_no,service_type,pickupdate,pickuptime,dropdate,droptime,deliverytype,pickup,dropaddress,r_date,customer_id,adminrespond,pincode) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(service_id,value[0],value[1],value[2],value[3],value[4],value[5],value[6],dropdate,droptime,value[7],value[8],value[9],value[10],value[11],adminrespond,value[12],))
                    mysql.connection.commit()
                    cursor.execute("delete from serviceform where s_id=%s",(service_id,))
                    mysql.connection.commit()
                    
                elif session['delivery']=="pickup":
                    cursor.execute("insert into adminserviceform (s_id,name,model,cartype,r_no,service_type,pickupdate,pickuptime,deliverytype,pickup,dropaddress,r_date,customer_id,adminrespond,pincode) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(service_id,value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10],value[11],adminrespond,value[12],))
                    mysql.connection.commit()
                    cursor.execute("delete from serviceform where s_id=%s",(service_id,))
                    mysql.connection.commit()

                else:
                    cursor.execute("insert into adminserviceform (s_id,name,model,cartype,r_no,service_type,r_date,customer_id,adminrespond,pincode) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(service_id,value[0],value[1],value[2],value[3],value[4],value[10],value[11],adminrespond,value[12],))
                    mysql.connection.commit()
                    cursor.execute("delete from serviceform where s_id=%s",(service_id,))
                    mysql.connection.commit()
            
            # for value in data1:
            #     cursor.execute("insert into service (s_id,servicename) values (%s,%s)",(service_id,value,))
            #     mysql.connection.commit()
            cursor.execute("select adminrespond from adminserviceform where s_id=%s",(service_id,))
            data3=cursor.fetchall()
            print (data3)
            print(data5)
            for value in data5:
                session['emails']=value
            if adminrespond=="accept":
                cursor.execute("update adminserviceform set adminrespond=%s where s_id=%s",("pending",service_id,))
                mysql.connection.commit()
                # msg = 'You have successfully registered !'
                # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [session['emails']])
                # msg.body = ("your car service has accepted")
                # mail.send(msg)
            elif adminrespond=="reject":
                cursor.execute('insert into serviceformreject (s_id,description) values (%s,%s)',(service_id,description,))
                mysql.connection.commit()
                cursor.execute("select description from serviceformreject where s_id=%s",(service_id,))
                data9=cursor.fetchall()
                msg = 'You have successfully registered !'
                # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [session['emails']])
                # word = ""
                # for x in  data9 :
                #     word += x[0] +" \n"
                # msg.body = ("your service has rejected \n " " Reason for rejection: \n"+str(word))
                # mail.send(msg)
            flash('Your respond has sent') 
            return redirect(url_for('newservice'))




@app.route('/serviceformpending')
def serviceformpending():
        cursor=mysql.connection.cursor()
        cursor.execute("select service_id,s_id,name,r_date from project.adminserviceform where adminrespond=%s",("pending",))
        data=cursor.fetchall()
        cursor.close()
        return render_template('serviceformpending.html',customer=data)




@app.route('/pendingedit/<service_id>',methods=['POST','GET'])
def pendingedit(service_id):
        cursor=mysql.connection.cursor()
        cursor.execute("select servicename from service where s_id=%s",(service_id,))
        data1=cursor.fetchall()
        print(data1)
        cursor.execute("select* from adminserviceform where s_id=%s",(service_id,))
        data=cursor.fetchall()
        cursor.execute("select name from mechanic")
        service=cursor.fetchall()
        print (data)
        cursor.close()
        return render_template('pendingedit.html',data=data,data1=data1,service=service) 



@app.route('/pendingupdate/<service_id>',methods=['POST'])
def pendingupdate(service_id):
    if request.method == 'POST':
        adminrespond = request.form['adminrespond']
        serviceby=request.form['serviceby']
        cursor=mysql.connection.cursor()
        cursor.execute("select customer_id from adminserviceform where s_id=%s",(service_id,))
        data4=cursor.fetchone()
        print(service_id)
        print(data4)
        print(adminrespond)
        cursor.execute("select email_id from customer where customer_id=%s",(data4,))
        data5=cursor.fetchone()
        print(data5)
        cursor.execute("update adminserviceform set adminrespond=%s, serviceby=%s where s_id=%s",(adminrespond,serviceby,service_id,))
        mysql.connection.commit()
        word = ""
        for value in data5:
            word=value
        # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [word])
        # msg.body = ("your service has completed")
        # mail.send(msg)
        flash("service updated")
        cursor.execute("select s_id,name,model,cartype,r_no,service_type,deliverytype,pickup,pickupdate,pickuptime,dropaddress,dropdate,droptime,r_date,responddate,adminrespond,pincode from adminserviceform where s_id=%s",(service_id,))
        data=cursor.fetchall()
        word=""
        car=""
        for value in data:
            word=value[2]
            car=value[3]
        print(word)
        for value in data:
            print(value[15])
        cursor.execute("select servicename from service where s_id=%s",(service_id,))
        data1=cursor.fetchall()
        print(data1)
        cursor.execute("select model_id from project.model where carname=%s",(word,))
        data2=cursor.fetchone()
        print(data2)
        rate=0
        c=0
        i=0
        for value in data1:
            if value[i]=="batterychange":
                cursor.execute("select price from project.servicebattery where s_id=%s",(service_id,))
                data6=cursor.fetchone()
                print(data6)
                for value in data6:
                    rate=rate+value
                print(rate)
            elif value[i]=="tyrechange":
                cursor.execute("select price from servicetyre where s_id=%s",(service_id,)) 
                data7=cursor.fetchone()
                cursor.execute("select tno from servicetyre where s_id=%s",(service_id,))
                data8=cursor.fetchone()
                for value in data7:
                    for n in data8:
                        ttyre=n*int(value)
                rate=rate+float(ttyre)
                print(rate)
            else:
                cursor.execute("select price from service where servicename=%s and s_id=%s",(value[0],service_id))
                data3=cursor.fetchall()
                print(data3)
                print('repair'+str(i))
                for value in data3:
                    rate=int(rate)+int(value[0])
                    print(rate)
        
        i=0
        return render_template('totalservicediscount.html',data=data,data1=data1,rate=rate)




@app.route('/billpending')
def billpending():
        cursor=mysql.connection.cursor()
        cursor.execute("select billno,name,model from project.adminserviceform,project.Bill where adminrespond=%s and billstatus=%s and adminserviceform.s_id=Bill.s_id",("completed","notpaid",))
        data=cursor.fetchall()
        print(data)
        cursor.close()
        return render_template('pendingbill.html',customer=data)




@app.route('/pendingbilledit/<billno>',methods=['POST','GET'])
def pendingbilledit(billno):
        cursor=mysql.connection.cursor()
        cursor.execute("select s_id from Bill where billno=%s",(billno,))
        service_id=cursor.fetchone()
        cursor.execute("select name from adminserviceform where s_id=%s",(service_id,))
        data=cursor.fetchone()
        cursor.execute("select s_id,billno,totalbill from Bill where billno=%s",(billno,))
        data1=cursor.fetchall()
        print(data)
        print(billno)
        cursor.close()
        return render_template('pendingbillupdate.html',data1=data1,data=data) 




@app.route('/pendingbillupdate/<billno>',methods=['POST'])
def pendingbillupdate(billno):
    if request.method=='POST':
        billstatus=request.form['billstatus']
        cursor=mysql.connection.cursor()
        cursor.execute("update Bill set billstatus=%s where billno=%s",(billstatus,billno,))
        mysql.connection.commit()
        flash("Updated")
        cursor.close()
        return redirect(url_for('billpending'))



@app.route('/servicecompleted')
def servicecompleted():
        cursor=mysql.connection.cursor()
        cursor.execute("select billno,name,model from project.adminserviceform,project.Bill where adminrespond=%s and billstatus=%s and adminserviceform.s_id=Bill.s_id order by r_date",("completed","paid",))
        data=cursor.fetchall()
        print(data)
        cursor.close()
        return render_template('servicecompleted.html',customer=data)



@app.route('/servicecompletedview/<billno>')
def servicecompletedview(billno):
    cursor=mysql.connection.cursor()
    cursor.execute('select customer_id from Bill where billno=%s',(billno,))
    data=cursor.fetchone()
    cursor.execute("select s_id from Bill where billno=%s",(billno,))
    data3=cursor.fetchall()
    cursor.execute("select name,s_id,model,cartype,r_no,adminrespond,serviceby from adminserviceform where s_id=%s order by r_date",(data3,))
    data1=cursor.fetchall()
    for value in data1:
        print(value[1])
    cursor.execute("select billno,billdate,billstatus,paiddate,totalbill from Bill where billno=%s",(billno,))
    data2=cursor.fetchall()
    cursor.close()
    return render_template("servicecompletedview.html",data1=data1,data2=data2)
        



@app.route('/totalservicecompleted')
def totalservicecompleted():
        cursor=mysql.connection.cursor()
        cursor.execute("select service_id,s_id,name,r_date from project.adminserviceform where adminrespond=%s",("completed",))
        data=cursor.fetchall()
        cursor.close()
        return render_template('totalservicecompleted.html',customer=data)



@app.route('/totalservicediscount/<d1>/<d2>',methods=['GET','POST'])
def totalservicediscount(d1,d2):
    cursor=mysql.connection.cursor()
    cursor.execute("select s_id,name,model,cartype,r_no,service_type,deliverytype,pickup,pickupdate,pickuptime,dropaddress,dropdate,droptime,r_date,responddate,adminrespond,pincode from adminserviceform where service_id=%s and s_id=%s",(d1,d2,))
    data=cursor.fetchall()
    word=""
    car=""
    for value in data:
        word=value[2]
        car=value[3]
    print(word)
    for value in data:
        print(value[15])
    cursor.execute("select servicename from service where s_id=%s",(d2,))
    data1=cursor.fetchall()
    print(data1)
    cursor.execute("select model_id from project.model where carname=%s",(word,))
    data2=cursor.fetchone()
    print(data2)
    rate=0
    c=0
    i=0
    for value in data1:
        if value[i]=="batterychange":
            cursor.execute("select price from project.servicebattery where s_id=%s",(d2,))
            data6=cursor.fetchone()
            print(data6)
            for value in data6:
                rate=rate+value
            print(rate)
        elif value[i]=="tyrechange":
            cursor.execute("select price from servicetyre where s_id=%s",(d2,))
            data7=cursor.fetchone()
            cursor.execute("select tno from servicetyre where s_id=%s",(d2,))
            data8=cursor.fetchone()
            for value in data7:
                for n in data8:
                    ttyre=n*int(value)
                rate=rate+float(ttyre)
            print(rate)
        
        else:
            cursor.execute("select price from service where servicename=%s and s_id=%s",(value[0],d2))
            data3=cursor.fetchall()
            print(data3)
            print('repair'+str(i))
            for value in data3:
                rate=rate+int(value[0])
                print(rate)
        
    i=0
    return render_template('totalservicediscount.html',data=data,data1=data1,rate=rate)




@app.route('/adddiscount/<s_id>',methods=['POST'])
def adddiscount(s_id):
    print('hi')
    if request.method=='POST':
        totalprice=request.form['totalprice']
        discount=request.form['discount']
        GST=request.form['GST']
        cursor=mysql.connection.cursor()
        cursor.execute("select customer_id from adminserviceform where s_id=%s",(s_id,))
        data=cursor.fetchone()
        session['s_id']=s_id
        n=float(totalprice)*(float(discount)/100)
        print(n)
        netbill=float(totalprice)-float(n)
        print(netbill)
        total=float(netbill)+(float(GST)%100)
        print(total)
        billno = '10'+date.today().strftime('%j')+"".join(str(datetime.now().time()).split(':'))[:4]
        cursor.execute("insert into Bill (billno,totalprice,discount,netprice,GST,totalbill,customer_id,s_id,billstatus) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(billno,totalprice,discount,netbill,GST,total,data,s_id,"notpaid",))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('viewbill'))
        



@app.route('/viewbill')
def viewbill():
        cursor=mysql.connection.cursor()
        cursor.execute("select customer_id from adminserviceform where s_id=%s",(session['s_id'],))
        data=cursor.fetchone()
        cursor.execute("select fullname,phoneno from customer where customer_id=%s",(data,))
        data1=cursor.fetchall()
        cursor.execute("select billno,billdate from Bill where s_id=%s and customer_id=%s",(session['s_id'],data,))
        data2=cursor.fetchall()
        serviceno=session['s_id']
        cursor.execute("select servicename,price from service where s_id=%s",(session['s_id'],))
        data3=cursor.fetchall()
        cursor.execute("select totalprice,discount,netprice,GST,totalbill from Bill where s_id=%s and customer_id=%s",(session['s_id'],data,))
        data4=cursor.fetchall()
        cursor.close()
        return render_template('totalbill.html',data1=data1,data2=data2,data3=data3,data4=data4,serviceno=serviceno)




@app.route('/serviceformreject')
def serviceformreject():
        cursor=mysql.connection.cursor()
        cursor.execute("select service_id,s_id,model,r_date,responddate from project.adminserviceform where adminrespond=%s order by r_date",("reject",))
        data=cursor.fetchall()
        return render_template('serviceformreject.html',customer=data)



@app.route('/serviceformrejectview/<data1>/<data2>')
def serviceformrejectview(data1,data2):
        cursor=mysql.connection.cursor()
        cursor.execute("select * from project.adminserviceform where adminrespond=%s and s_id=%s",("reject",data2,))
        data=cursor.fetchall()
        cursor.execute("select servicename from service where s_id=%s",(data2,))
        data1=cursor.fetchall()
        cursor.execute("select description from serviceformreject where s_id=%s",(data2,))
        data3=cursor.fetchall()
        print(data3)
        return render_template('serviceformrejectview.html',customer=data,customer1=data1,customer3=data3)





@app.route('/rejectedservicereportview')
def rejectedservicereportview():
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,service_type,responddate,description from adminserviceform,serviceformreject where adminrespond=%s and adminserviceform.s_id=serviceformreject.s_id and r_date between %s and %s order by r_date",("reject",session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('rejectedservicereportview.html',customer=data)





@app.route('/rejectedservicereport')
def rejectedservicereport():
    now=date.today()
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,service_type,responddate,description from adminserviceform,serviceformreject where adminrespond=%s and adminserviceform.s_id=serviceformreject.s_id and r_date between %s and %s order by r_date",("reject",session['date1'],session['date2'],))
    data1=cursor.fetchall()
    print(data1)
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.set_font('Times','I',14.0)
    pdf.ln(10)
    pdf.cell(page_width,0.0,"Report of Rejected Service",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date: "+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(18,th,"Sno",border=1,align="C")
    pdf.cell(35,th,"Name",border=1,align="C")
    pdf.cell(18,th,"Model",border=1,align="C")
    pdf.cell(33,th,"Service_Type",border=1,align="C")
    pdf.cell(25,th,"Service_Date",border=1,align="C")
    pdf.cell(57,th,"Description",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(18,th,str(i),border=1,align="C")
        pdf.cell(35,th,row[0],border=1,align="C")
        pdf.cell(18,th,row[1],border=1,align="C")
        pdf.cell(33,th,row[2],border=1,align="C")
        pdf.cell(25,th,str(row[3]),border=1,align="C")
        pdf.cell(57,th,row[4],border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Rejected_Service_Report.pdf'})






@app.route('/pendingbillreportview')
def pendingbillreportview():
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,cartype,service_type,responddate,totalbill from adminserviceform,Bill where adminrespond=%s and adminserviceform.s_id=Bill.s_id and billstatus=%s and r_date between %s and %s order by r_date",("completed","notpaid",session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('pendingbillreportview.html',customer=data)






@app.route('/pendingbillreport',methods=['GET','POST'])
def pendingbillreport():
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,cartype,service_type,responddate,totalbill from adminserviceform,Bill where adminrespond=%s and adminserviceform.s_id=Bill.s_id and billstatus=%s and r_date between %s and %s order by r_date",("completed","notpaid",session['date1'],session['date2'],))
    data1=cursor.fetchall()
    print(data1)
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report Of Pending Bill",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(18,th,"Sno",border=1,align="C")
    pdf.cell(35,th,"Name",border=1,align="C")
    pdf.cell(18,th,"Model",border=1,align="C")
    pdf.cell(22,th,"Car_Type",border=1,align="C")
    pdf.cell(33,th,"Service_Type",border=1,align="C")
    pdf.cell(25,th,"Service_Date",border=1,align="C")
    pdf.cell(33,th,"Total_Bill",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(18,th,str(i),border=1,align="C")
        pdf.cell(35,th,row[0],border=1,align="C")
        pdf.cell(18,th,row[1],border=1,align="C")
        pdf.cell(22,th,row[2],border=1,align="C")
        pdf.cell(33,th,row[3],border=1,align="C")
        pdf.cell(25,th,str(row[4]),border=1,align="C")
        pdf.cell(33,th,str(row[5]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Pending_Bill_Report.pdf'})






@app.route('/repeatedcustomerview')
def repeatedcustomerview():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT max(Total) FROM (SELECT COUNT(*) AS Total FROM adminserviceform where adminrespond=%s GROUP BY name,model,cartype) AS Results",("completed",))
    m=cursor.fetchone()
    # print(m[0])
    cursor.execute('select name,model,cartype,count(*) from adminserviceform where adminrespond=%s group by name,model,cartype',('completed',))
    data=cursor.fetchall()
    # print(data)
    i=0
    new = []
    for value in data:
        i=int(value[3])
        if i==m[0]:
            v1=value[0]
            v2=value[1]
            v3=value[2]
            print('hi')
            cursor.execute("select name,model,cartype,service_type,responddate,serviceby,totalbill from adminserviceform,Bill where name=%s and model=%s and cartype=%s and adminrespond=%s and adminserviceform.s_id=Bill.s_id order by r_date",(v1,v2,v3,"completed",))
            data1=cursor.fetchall()
            new.append(data1)
    return render_template('repeatedcustomerview.html',customer=new)






@app.route('/repeatedcustomer')
def repeatedcustomer():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT max(Total) FROM (SELECT COUNT(*) AS Total FROM adminserviceform where adminrespond=%s GROUP BY name,model,cartype) AS Results",("completed",))
    m=cursor.fetchone()
    print(m[0])
    cursor.execute('select name,model,cartype,count(*) from adminserviceform where adminrespond=%s group by name,model,cartype',('completed',))
    data=cursor.fetchall()
    print(data)
    i=0
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report Of Repeated Customer",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    for value in data:
        i=int(value[3])
        print(i)
        if i==m[0]:
            v1=value[0]
            v2=value[1]
            v3=value[2]
            print('hi')
            cursor.execute("select name,model,cartype,service_type,responddate,serviceby,totalbill from adminserviceform,Bill where name=%s and model=%s and cartype=%s and adminrespond=%s and adminserviceform.s_id=Bill.s_id order by r_date",(v1,v2,v3,"completed",))
            data1=cursor.fetchall()
            print(data1)
            pdf.set_font('Times','I',14.0)
            pdf.cell(page_width,0.0,"Customer Name:"+""+v1,align="L")
            pdf.ln(8)
            pdf.cell(page_width,0.0,"Model:"+""+v2,align="L")
            pdf.ln(10)
            pdf.cell(page_width,0.0,"Cartype:"+""+v3,align="L")
            pdf.ln(10)
            pdf.set_font('Courier','',12)
            col_width=page_width/4
            pdf.ln(1)
            th=pdf.font_size
            i=1
            pdf.set_font('Times','B',12.0)
            pdf.cell(20,th,"Sno",border=1)
            pdf.cell(35,th,"Service_Type",border=1,align="C")
            pdf.cell(35,th,"Service_Date",border=1,align="C")
            pdf.cell(35,th,"Service_By",border=1,align="C")
            pdf.cell(36,th,"Total_Bill",border=1,align="C")
            pdf.ln(th)
            th=pdf.font_size 
            pdf.set_font('Times','I',10.0)        
            for row in data1:
                pdf.cell(20,th,str(i),border=1,align="C")
              
                pdf.cell(35,th,row[3],border=1,align="C")
                pdf.cell(35,th,str(row[4]),border=1,align="C")
                pdf.cell(35,th,str(row[5]),border=1,align="C")
                pdf.cell(36,th,str(row[6]),border=1,align="C")
                i=i+1
                pdf.ln(th)
            pdf.ln(10)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Most_repeated_Customer_Report.pdf'})






@app.route('/pendingservicereportview')
def pendingservicereportview():
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,cartype,service_type,r_date,r_no from adminserviceform where adminrespond=%s and r_date between %s and %s order by r_date",("pending",session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('pendingservicereportview.html',customer=data)






@app.route('/pendingservicereport')
def pendingservicereport():
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,cartype,service_type,r_date,r_no from adminserviceform where adminrespond=%s and r_date between %s and %s order by r_date",("pending",session['date1'],session['date2'],))
    data1=cursor.fetchall()
    print(data1)
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Pending Service",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(18,th,"Sno",border=1,align="C")
    pdf.cell(38,th,"Name",border=1,align="C")
    pdf.cell(18,th,"Model",border=1,align="C")
    pdf.cell(22,th,"Car_Type",border=1,align="C")
    pdf.cell(33,th,"Service_Type",border=1,align="C")
    pdf.cell(34,th,"Registration_Date",border=1,align="C")
    pdf.cell(34,th,"Car_no",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(18,th,str(i),border=1,align="C")
        pdf.cell(38,th,row[0],border=1,align="C")
        pdf.cell(18,th,row[1],border=1,align="C")
        pdf.cell(22,th,row[2],border=1,align="C")
        pdf.cell(33,th,row[3],border=1,align="C")
        pdf.cell(34,th,str(row[4]),border=1,align="C")
        pdf.cell(34,th,str(row[5]),border=1,align="C")
       
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Pending_Service_Report.pdf'})






@app.route('/customerreport')
def customerreport():
    cursor=mysql.connection.cursor()
    cursor.execute('select fullname,phoneno,email_id from customer')
    data1=cursor.fetchall()
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Total Customer Registered",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(20,th,"Sno",border=1,align="C")
    pdf.cell(40,th,"Customer_Name",border=1,align="C")
    pdf.cell(35,th,"Phone Number",border=1,align="C")
    pdf.cell(55,th,"Email_id",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(20,th,str(i),border=1,align="C")
        pdf.cell(40,th,row[0],border=1,align="C")
        pdf.cell(35,th,str(row[1]),border=1,align="C")
        pdf.cell(55,th,str(row[2]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Total_Customer_Report.pdf'})






@app.route('/deletedreport')
def deletereport():
    return render_template("deletedreport.html")





@app.route('/printdeletedreport',methods=['POST','GET'])
def printdeletedreport():
    if request.method=='POST':
        typereport=request.form['typereport']
        date1=request.form['date1']
        session['date1']=date1
        date2=request.form['date2']
        session['date2']=date2
        if typereport=='tyreservice':
            return redirect(url_for('deletedtyrereport'))
        elif typereport=='batteryservice':
            return redirect(url_for('deletedbatteryreport'))
        elif typereport=='repairservice':
            return redirect(url_for('deletedrepairreport'))
        elif typereport=='washingservice':
            return redirect(url_for('deletedwashingreport'))





@app.route('/updatedreport')
def updatedreport():
    return render_template("updatedreport.html")





@app.route('/printupdatedreport',methods=['POST','GET'])
def printupdatedreport():
    if request.method=='POST':
        typereport=request.form['typereport']
        date1=request.form['date1']
        session['date1']=date1
        date2=request.form['date2']
        session['date2']=date2
        if typereport=='tyreservice':
            return redirect(url_for('updatedtyrereport'))
        elif typereport=='batteryservice':
            return redirect(url_for('updatedbatteryreport'))
        elif typereport=='repairservice':
            return redirect(url_for('updatedrepairreport'))
        elif typereport=='washingservice':
            return redirect(url_for('updatedwashingreport'))





@app.route('/updatedrepairreport')
def updatedrepairreport():
    cursor=mysql.connection.cursor()
    cursor.execute("select carname,servicename,price,updateprice,description,date from project.repairupdate where date between %s and %s order by date",(session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('updatedrepairreport.html',customer=data)




@app.route('/repairupdateddownload')
def repairupdateddownload():
    cursor=mysql.connection.cursor()
    cursor.execute('select carname,servicename,price,updateprice,description,date from project.repairupdate where date between %s and %s order by date',(session['date1'],session['date2'],))
    data1=cursor.fetchall()
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Repair Service Updated",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(16,th,"Sno",border=1,align="C")
    pdf.cell(28,th,"Model_Name",border=1,align="C")
    pdf.cell(29,th,"Service_Name",border=1,align="C")
    pdf.cell(20,th,"Price",border=1,align="C")
    pdf.cell(25,th,"UpdatedPrice",border=1,align="C")
    pdf.cell(52,th,"Description",border=1,align="C")
    pdf.cell(26,th,"Updated_Date",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(16,th,str(i),border=1,align="C")
        pdf.cell(28,th,row[0],border=1,align="C")
        pdf.cell(29,th,row[1],border=1,align="C")
        pdf.cell(20,th,str(row[2]),border=1,align="C")
        pdf.cell(25,th,str(row[3]),border=1,align="C")
        pdf.cell(52,th,str(row[4]),border=1,align="C")
        pdf.cell(26,th,str(row[5]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Updated_Repair_Service_Report.pdf'})






@app.route('/deletedrepairreport')
def deletedrepairreport():
    cursor=mysql.connection.cursor()
    cursor.execute("select carname,servicename,price,description,date from project.deleterepair where date between %s and %s order by date",(session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('deletedrepairreport.html',customer=data)





@app.route('/repairdeleteddownload')
def repairdeleteddownload():
    cursor=mysql.connection.cursor()
    cursor.execute('select carname,servicename,price,description,date from project.deleterepair where date between %s and %s order by date',(session['date1'],session['date2'],))
    data1=cursor.fetchall()
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Repair Service Deleted",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(20,th,"Sno",border=1,align="C")
    pdf.cell(33,th,"Model_Name",border=1,align="C")
    pdf.cell(35,th,"Service_Name",border=1,align="C")
    pdf.cell(25,th,"Price",border=1,align="C")
    pdf.cell(55,th,"Description",border=1,align="C")
    pdf.cell(26,th,"Deleted_Date",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(20,th,str(i),border=1,align="C")
        pdf.cell(33,th,row[0],border=1,align="C")
        pdf.cell(35,th,row[1],border=1,align="C")
        pdf.cell(25,th,str(row[2]),border=1,align="C")
        pdf.cell(55,th,str(row[3]),border=1,align="C")
        pdf.cell(26,th,str(row[4]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Deleted_Repair_Service_Report.pdf'})






@app.route('/updatedtyrereport')
def updatedtyrereport():
    cursor=mysql.connection.cursor()
    cursor.execute("select carname,name,size,price,updateprice,description,date from project.tyreupdate where date between %s and %s order by date",(session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('updatedtyrereport.html',customer=data)






@app.route('/tyreupdateddownload')
def tyreupdateddownload():
    cursor=mysql.connection.cursor()
    cursor.execute('select carname,name,size,price,updateprice,description,date from project.tyreupdate where date between %s and %s order by date',(session['date1'],session['date2'],))
    data1=cursor.fetchall()
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Tyre Service Updated",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(10,th,"Sno",border=1,align="C")
    pdf.cell(24,th,"Model_Name",border=1,align="C")
    pdf.cell(32,th,"Tyre_Name",border=1,align="C")
    pdf.cell(28,th,"Tyre_Size",border=1,align="C")
    pdf.cell(15,th,"Price",border=1,align="C")
    pdf.cell(22,th,"UpdatePrice",border=1,align="C")
    pdf.cell(46,th,"Description",border=1,align="C")
    pdf.cell(22,th,"Date",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(10,th,str(i),border=1,align="C")
        pdf.cell(24,th,row[0],border=1,align="C")
        pdf.cell(32,th,row[1],border=1,align="C")
        pdf.cell(28,th,str(row[2]),border=1,align="C")
        pdf.cell(15,th,str(row[3]),border=1,align="C")
        pdf.cell(22,th,str(row[4]),border=1,align="C")
        pdf.cell(46,th,str(row[5]),border=1,align="C")
        pdf.cell(22,th,str(row[6]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Updated_Tyre_Service_Report.pdf'})





@app.route('/updatedbatteryreport')
def updatedbatteryreport():
    cursor=mysql.connection.cursor()
    cursor.execute("select carname,batteryname,capacity,price,updateprice,description,date from project.batteryupdate where date between %s and %s order by date",(session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('updatedbatteryreport.html',customer=data)






@app.route('/batteryupdateddownload')
def batteryupdateddownload():
    cursor=mysql.connection.cursor()
    cursor.execute('select carname,batteryname,capacity,price,updateprice,description,date from project.batteryupdate where date between %s and %s order by date',(session['date1'],session['date2'],))
    data1=cursor.fetchall()
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Battery Service Updated",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(10,th,"Sno",border=1,align="C")
    pdf.cell(24,th,"Model_Name",border=1,align="C")
    pdf.cell(32,th,"Battery_Name",border=1,align="C")
    pdf.cell(28,th,"Capacity",border=1,align="C")
    pdf.cell(15,th,"Price",border=1,align="C")
    pdf.cell(22,th,"UpdatePrice",border=1,align="C")
    pdf.cell(46,th,"Description",border=1,align="C")
    pdf.cell(22,th,"Date",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(10,th,str(i),border=1,align="C")
        pdf.cell(24,th,row[0],border=1,align="C")
        pdf.cell(32,th,row[1],border=1,align="C")
        pdf.cell(28,th,str(row[2]),border=1,align="C")
        pdf.cell(15,th,str(row[3]),border=1,align="C")
        pdf.cell(22,th,str(row[4]),border=1,align="C")
        pdf.cell(46,th,str(row[5]),border=1,align="C")
        pdf.cell(22,th,str(row[6]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Updated_Battery_Service_Report.pdf'})






@app.route('/deletedtyrereport')
def deletedtyrereport():
    cursor=mysql.connection.cursor()
    cursor.execute("select carname,name,size,price,description,date from project.deletetyre where date between %s and %s order by date",(session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('deletedtyrereport.html',customer=data)






@app.route('/tyredeleteddownload')
def tyredeleteddownload():
    cursor=mysql.connection.cursor()
    cursor.execute('select carname,name,size,price,description,date from project.deletetyre where date between %s and %s order by date',(session['date1'],session['date2'],))
    data1=cursor.fetchall()
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Tyre Service Deleted",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(14,th,"Sno",border=1,align="C")
    pdf.cell(25,th,"Model_Name",border=1,align="C")
    pdf.cell(33,th,"Tyre_Name",border=1,align="C")
    pdf.cell(28,th,"Tyre_Size",border=1,align="C")
    pdf.cell(18,th,"Price",border=1,align="C")
    pdf.cell(54,th,"Description",border=1,align="C")
    pdf.cell(25,th,"Deleted_Date",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(14,th,str(i),border=1,align="C")
        pdf.cell(25,th,row[0],border=1,align="C")
        pdf.cell(33,th,row[1],border=1,align="C")
        pdf.cell(28,th,str(row[2]),border=1,align="C")
        pdf.cell(18,th,str(row[3]),border=1,align="C")
        pdf.cell(54,th,str(row[4]),border=1,align="C")
        pdf.cell(25,th,str(row[5]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Deleted_Tyre_Service_Report.pdf'})





@app.route('/deletedbatteryreport')
def deletedbatteryreport():
    cursor=mysql.connection.cursor()
    cursor.execute("select carname,batteryname,capacity,price,description,date from project.deletebattery where date between %s and %s order by date",(session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('deletedbatteryreport.html',customer=data)




@app.route('/batterydeleteddownload')
def batterydeleteddownload():
    cursor=mysql.connection.cursor()
    cursor.execute('select carname,batteryname,capacity,price,description,date from project.deletebattery where date between %s and %s order by date',(session['date1'],session['date2'],))
    data1=cursor.fetchall()
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','I',14.0)
    pdf.cell(page_width,0.0,"Report of Battery Service Deleted",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(14,th,"Sno",border=1,align="C")
    pdf.cell(25,th,"Model_Name",border=1,align="C")
    pdf.cell(33,th,"Battery_Name",border=1,align="C")
    pdf.cell(28,th,"Capacity",border=1,align="C")
    pdf.cell(18,th,"Price",border=1,align="C")
    pdf.cell(54,th,"Description",border=1,align="C")
    pdf.cell(25,th,"Deleted_Date",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(14,th,str(i),border=1,align="C")
        pdf.cell(25,th,row[0],border=1,align="C")
        pdf.cell(33,th,row[1],border=1,align="C")
        pdf.cell(28,th,str(row[2]),border=1,align="C")
        pdf.cell(18,th,str(row[3]),border=1,align="C")
        pdf.cell(54,th,str(row[4]),border=1,align="C")
        pdf.cell(25,th,str(row[5]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Deleted_Battery_Service_Report.pdf'})


@app.route('/areareportview')
def areareportview():
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,cartype,service_type,responddate,totalbill,pincode from adminserviceform,Bill where adminrespond=%s and adminserviceform.s_id=Bill.s_id and billstatus=%s and r_date between %s and %s",("completed","paid",session['date1'],session['date2'],))
    data1=cursor.fetchall()
    cursor.execute("select name,model,cartype,service_type,responddate,totalbill,pincode,count(*) from adminserviceform,Bill where adminrespond=%s and adminserviceform.s_id=Bill.s_id and billstatus=%s and r_date between %s and %s group by pincode",("completed","paid",session['date1'],session['date2'],))
    data=cursor.fetchall()
    x = [] 
    y = []
    # label="area"
    c=0
    for value in data:         
        x.append(value[6])  #x column contain data(1,2,3,4,5) 
        y.append(value[7]) 
    fig1=plt.figure(figsize =(9, 5)) 
    # plt.bar(x,y,0.3,0,color="darkorange",label=x)
    # colors = ['lightgray', 'darkorange', 'gray']
    plt.pie(y, labels=x,autopct='%1.1f%%', shadow=True, startangle=140)

    plt.title("Highest Service of Current month",color="orangered")
    plt.xlabel("Area Pincode",color="orangered")
    plt.ylabel("Value",color="orangered")
    plt.legend()
    # plt.axis('equal')
    # tick_label=x
    img=fig1.savefig('static/images/area.jpg')
    canvas=FigureCanvas(fig1)
    img=io.BytesIO()
    fig1.savefig(img)
    img.seek(0)
    return render_template('areawisereport.html',customer=data1)





@app.route('/areareportdownload')
def areareportdownload():
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,cartype,service_type,responddate,totalbill,pincode from adminserviceform,Bill where adminrespond=%s and adminserviceform.s_id=Bill.s_id and billstatus=%s and r_date between %s and %s order by r_date",("completed","paid",session['date1'],session['date2'],))
    data1=cursor.fetchall()
    cursor.execute("select name,model,cartype,service_type,responddate,totalbill,pincode,count(*) from adminserviceform,Bill where adminrespond=%s and adminserviceform.s_id=Bill.s_id and billstatus=%s and r_date between %s and %s group by pincode",("completed","paid",session['date1'],session['date2'],))
    data=cursor.fetchall()
    print(data1)
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',16.0)
    pdf.cell(page_width,0.0,"Report Of highly service area",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,"Report_Type:"+""+"Most Repeated"+"Area",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.image('static/images/area.jpg',x=None,y=None,w=150,h=100,type='',link='')
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(18,th,"Sno",border=1,align="C")
    pdf.cell(35,th,"Name",border=1,align="C")
    pdf.cell(18,th,"Model",border=1,align="C")
    pdf.cell(20,th,"Car_Type",border=1,align="C")
    pdf.cell(30,th,"Service_Type",border=1,align="C")
    pdf.cell(25,th,"Service_Date",border=1,align="C")
    pdf.cell(30,th,"Total_Bill",border=1,align="C")
    pdf.cell(22,th,"Pincode",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(18,th,str(i),border=1,align="C")
        pdf.cell(35,th,row[0],border=1,align="C")
        pdf.cell(18,th,row[1],border=1,align="C")
        pdf.cell(20,th,row[2],border=1,align="C")
        pdf.cell(30,th,row[3],border=1,align="C")
        pdf.cell(25,th,str(row[4]),border=1,align="C")
        pdf.cell(30,th,str(row[5]),border=1,align="C")
        pdf.cell(22,th,str(row[6]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Pincode_Service_Report.pdf'})



@app.route('/highservice')
def highservice():
        cursor=mysql.connection.cursor()
        cursor.execute("select service_type,count(*),model,cartype from adminserviceform where  r_date between %s and %s GROUP BY service_type",(session['date1'],session['date2'],))
        data5=cursor.fetchall()
        cursor.execute("select servicename from service")
        data6=cursor.fetchall()
        # cursor.execute('select model,cartype,service_type,max(Total) FROM (SELECT model,cartype,service_type,COUNT(*) AS Total FROM adminserviceform where r_date between %s and %s GROUP BY service_type,model,cartype) AS Results',(session['date1'],session['date2'],))
        # m=cursor.fetchall()
        # print(m[0])
        x = [] 
        y = []
        label="Highest service of current month"
        # explode = (0.1, 0, 0) 
        for value in data5:         
            x.append(value[0])  #x column contain data(1,2,3,4,5) 
            y.append(value[1]) 
        fig1=plt.figure(figsize =(5, 3)) 
        # plt.pie(labels=x,values=y,0.3,colors="dimgray",autopct='%1.1f%%', shadow=True, startangle=140)
        colors = ['lightgray', 'red', 'gray']
        plt.pie(y,labels=x, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title("Highest Service of Current month",color="red")
        # plt.xlabel("servicetype",color="orangered")
        # plt.ylabel("Value",color="orangered")
        plt.legend()
        plt.axis('equal')
        img=fig1.savefig('static/images/highest1.jpg')
        canvas=FigureCanvas(fig1)
        img=io.BytesIO()
        fig1.savefig(img)
        img.seek(0)
        return render_template('highservice.html',customer=data5)





@app.route('/highservicereportdownload')
def highservicereportdownload():
    cursor=mysql.connection.cursor()
    cursor.execute("select model,cartype,service_type,count(*) from adminserviceform where  r_date between %s and %s GROUP BY service_type",(session['date1'],session['date2'],))
    data5=cursor.fetchall()
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',16.0)
    pdf.cell(page_width,0.0,"Report Of Most provided Service",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,"Report_Type:"+""+"Highly provided Service",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.image('static/images/highest1.jpg',x=None,y=None,w=150,h=100,type='',link='')
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(18,th,"Sno",border=1,align="C")
    pdf.cell(35,th,"Model",border=1,align="C")
    pdf.cell(25,th,"Car_Type",border=1,align="C")
    pdf.cell(32,th,"Service_Type",border=1,align="C")
    pdf.cell(35,th,"Count of Service",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data5:
        pdf.cell(18,th,str(i),border=1,align="C")
        pdf.cell(35,th,row[0],border=1,align="C")
        pdf.cell(25,th,row[1],border=1,align="C")
        pdf.cell(32,th,row[2],border=1,align="C")
       
        pdf.cell(35,th,str(row[3]),border=1,align="C")
        
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=High_Service_Report.pdf'})






@app.route('/completedreportview')
def completedreportview():
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,cartype,service_type,responddate,totalbill,billdate from adminserviceform,Bill where adminrespond=%s and adminserviceform.s_id=Bill.s_id and billstatus=%s and r_date between %s and %s order by r_date",("completed","paid",session['date1'],session['date2'],))
    data=cursor.fetchall()
    return render_template('completedreportview.html',customer=data)


@app.route('/completedreportdownload')
def completedreportdownload():
    cursor=mysql.connection.cursor()
    cursor.execute("select name,model,cartype,service_type,responddate,totalbill,billdate from adminserviceform,Bill where adminrespond=%s and adminserviceform.s_id=Bill.s_id and billstatus=%s and r_date between %s and %s order by r_date",("completed","paid",session['date1'],session['date2'],))
    data1=cursor.fetchall()
    print(data1)
    pdf=FPDF()
    pdf.add_page()
    page_width=pdf.w-3*pdf.l_margin
    pdf.set_font('Times','B',20.0)
    pdf.cell(page_width,0.0,"Zarage Service Center",align="C")
    pdf.set_font('Times','B',16.0)
    pdf.cell(page_width,0.0,"Report Of Completed Service",align="C")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,"Report Downloaded By:"+""+"Admin",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,"Report_Type:"+""+"Completed",align="L")
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,"Date:"+""+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',12)
    col_width=page_width/4
    pdf.ln(1)
    th=pdf.font_size
    i=1
    pdf.set_font('Times','B',12.0)
    pdf.cell(18,th,"Sno",border=1,align="C")
    pdf.cell(35,th,"Name",border=1,align="C")
    pdf.cell(18,th,"Model",border=1,align="C")
    pdf.cell(20,th,"Car_Type",border=1,align="C")
    pdf.cell(30,th,"Service_Type",border=1,align="C")
    pdf.cell(25,th,"Service_Date",border=1,align="C")
    pdf.cell(30,th,"Total_Bill",border=1,align="C")
    pdf.cell(22,th,"Bill_Date",border=1,align="C")
    pdf.ln(th)
    th=pdf.font_size 
    pdf.set_font('Times','I',10.0)        
    for row in data1:
        pdf.cell(18,th,str(i),border=1,align="C")
        pdf.cell(35,th,row[0],border=1,align="C")
        pdf.cell(18,th,row[1],border=1,align="C")
        pdf.cell(20,th,row[2],border=1,align="C")
        pdf.cell(30,th,row[3],border=1,align="C")
        pdf.cell(25,th,str(row[4]),border=1,align="C")
        pdf.cell(30,th,str(row[5]),border=1,align="C")
        pdf.cell(22,th,str(row[6]),border=1,align="C")
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0, '-----End of report-----',align='C')
    return Response(pdf.output(dest='S').encode('latin-1'),mimetype="application/pdf",headers={'Content-Disposition':'attachment;filename=Completed_Service_Report.pdf'})




@app.route('/monthwise')
def monthwise():
    return render_template("monthwise.html")



@app.route('/monthwisereport',methods=['GET','POST'])
def monthwisereport():
    if request.method=="POST":
        date1=request.form['date1']
        session['date1']=date1
        date2=request.form['date2']
        session['date2']=date2
        report=request.form['report']
        print('hi')
        if report=='Rejected':
            return redirect(url_for('rejectedservicereportview'))
        elif report=='Pending':
            return redirect(url_for('pendingservicereportview'))
        elif report=='Billpending':
            return redirect(url_for('pendingbillreportview'))
        elif report=='repeated':
            return redirect(url_for('repeatedcustomerview'))
        elif report=='completed':
            return redirect(url_for('completedreportview'))
        elif report=='Area':
            return redirect(url_for('areareportview'))
        elif report=='highservice':
            return redirect(url_for('highservice'))
            

            



@app.route('/userserviceform')
def userserviceform():
        cursor=mysql.connection.cursor()
        cursor.execute("select customer_id from customer where email_id=%s",(session['email_id'],))
        data=cursor.fetchone()
        print(data)
        cursor.execute("select service_id,s_id,r_date,responddate from project.adminserviceform where customer_id=%s",(data,))
        data=cursor.fetchall()
        print(data)
        return render_template('userserviceform.html',customer=data)



@app.route('/userserviceformview/<service_id>',methods=['POST','GET'])
def userserviceformview(service_id):
        cursor=mysql.connection.cursor()
        cursor.execute("select s_id,name,model,cartype,r_no,service_type,deliverytype,pickup,pickupdate,pickuptime,dropaddress,dropdate,droptime,adminrespond,serviceby,pincode from adminserviceform,customer where adminserviceform.customer_id=customer.customer_id and service_id=%s",(service_id,))
        data=cursor.fetchall()
        cursor.execute("select servicename from service,adminserviceform where adminserviceform.s_id=service.s_id and service_id=%s",(service_id,))
        data1=cursor.fetchall()
        for value in data:
            print(value[13])
            if value[13]=="completed":
                return render_template('userserviceformbillview.html',customer=data,customer1=data1)
            else:
                return render_template('userserviceformview.html',customer=data,customer1=data1)
        cursor.close()




@app.route('/userserviceformbillview/<s_id>')
def userservceformbillview(s_id):
    cursor=mysql.connection.cursor()
    cursor.execute("select customer_id from adminserviceform where s_id=%s",(s_id,))
    data=cursor.fetchone()
    cursor.execute("select fullname,phoneno from customer where customer_id=%s",(data,))
    data1=cursor.fetchall()
    cursor.execute("select billno,billdate from Bill where s_id=%s and customer_id=%s",(s_id,data,))
    data2=cursor.fetchall()
    serviceno=s_id
    cursor.execute("select servicename,price from service where s_id=%s",(s_id,))
    data3=cursor.fetchall()
    cursor.execute("select totalprice,discount,netprice,GST,totalbill from Bill where s_id=%s and customer_id=%s",(s_id,data,))
    data4=cursor.fetchall()
    cursor.close()
    return render_template('usertotalbill.html',data1=data1,data2=data2,data3=data3,data4=data4,serviceno=serviceno)



@app.route('/repairupdate')
def repairupdate():
        cursor=mysql.connection.cursor()
        query="select* from project.repairupdate"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('repairupdate.html',customer=data)



@app.route('/tyreupdate')
def tyreupdate():
        cursor=mysql.connection.cursor()
        query="select* from project.tyreupdate"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('tyreupdate.html',customer=data)


@app.route('/washupdate')
def washupdate():
        cursor=mysql.connection.cursor()
        query="select* from project.washupdate"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('washupdate.html',customer=data)



@app.route('/batteryupdate')
def batteryupdate():
        cursor=mysql.connection.cursor()
        query="select* from project.batteryupdate"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('batteryupdate.html',customer=data)


@app.route('/deleterepair')
def deleterepair():
        cursor=mysql.connection.cursor()
        query="select* from project.deleterepair"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('deleterepair.html',customer=data)


@app.route('/deletetyre')
def deletetyre():
        cursor=mysql.connection.cursor()
        query="select* from project.deletetyre"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('deletetyre.html',customer=data)

@app.route('/deletewash')
def deletewash():
        cursor=mysql.connection.cursor()
        query="select* from project.deletewash"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('deletewash.html',customer=data)


@app.route('/deletebattery')
def deletebattery():
        cursor=mysql.connection.cursor()
        query="select* from project.deletebattery"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('deletebattery.html',customer=data)


@app.route('/profie')
def profie():
     # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE customer_id = %s', (session['id'],))
        data = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profie.html',customer=data)


@app.route('/update',methods=['POST','GET'])
def update():
    msg = ''
    if 'loggedin' in session:

        if request.method == 'POST' and 'fullname' in request.form and 'phoneno' in request.form and 'email_id' in request.form:
            fullname = request.form['fullname']
            phoneno = request.form['phoneno']
            email_id = request.form['email_id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer WHERE customer_id = % s', (session['id'], ))
            data = cursor.fetchone() 
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', fullname):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE customer SET  fullname =% s, phoneno =% s, email_id =% s  WHERE customer_id =% s', (fullname, phoneno, email_id, (session['id'], ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('update.html',msg=msg) 
    return redirect(url_for('userdashboard'))



@app.route('/inspection')
def inspection():
    return render_template("inspection.html")



@app.route('/repair')
def repair():
        cursor=mysql.connection.cursor()
        query1="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Baleno'"
        
        query2="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Ciaz'"
       
        query3="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Dzire'"
        
        query4="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Spresso'"
        
        query5="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Swift'"
        result1=cursor.execute(query1,)
        data1=cursor.fetchall()
        print(data1)
        result2=cursor.execute(query2)
        data2=cursor.fetchall()
        result3=cursor.execute(query3)
        data3=cursor.fetchall()
        result4=cursor.execute(query4)
        data4=cursor.fetchall()
        result5=cursor.execute(query5)
        data5=cursor.fetchall()
       
        query6="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Baleno'"
        cursor.execute(query6)
        data6=cursor.fetchall()
        query7="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Ciaz'"
        cursor.execute(query7)
        data7=cursor.fetchall()
        query8="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Dzire'"
        cursor.execute(query8)
        data8=cursor.fetchall()
        query9="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Spresso'"
        cursor.execute(query9)
        data9=cursor.fetchall()
        query10="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Swift'"
        cursor.execute(query10)
        data10=cursor.fetchall()
        query11="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Baleno'"
        cursor.execute(query11)
        data11=cursor.fetchall()
        query12="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Ciaz'"
        cursor.execute(query12)
        data12=cursor.fetchall()
        query13="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Dzire'"
        cursor.execute(query13)
        data13=cursor.fetchall()
        query14="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Spresso'"
        cursor.execute(query14)
        data14=cursor.fetchall()
        query15="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Swift'"
        cursor.execute(query15)
        data15=cursor.fetchall()
        print(data10)
        return render_template('repair.html',service1=data1,service2=data2,service3=data3,service4=data4,service5=data5,service6=data6,service7=data7,service8=data8,service9=data9,service10=data10,service11=data11,service12=data12,service13=data13,service14=data14,service15=data15)   


@app.route('/wash')
def wash():
        cursor=mysql.connection.cursor()
        query="select* from project.servicewashing"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('wash.html',service=data)  



@app.route('/repaircartype',methods=['POST','GET'])
def repaircartype():
    print('hi')
    cursor = mysql.connection.cursor()
    cursor.execute("select carname from model")
    data=cursor.fetchall()
    print(data)
    if request.method == 'POST':
        print('hi')
        model = request.form['model']
        
        if model=='Baleno':
            return redirect(url_for('repairbaleno'))
        elif model=='Ciaz':
            return redirect(url_for('repairciaz'))
        elif model=='Dzire':
            return redirect(url_for('repairdzire'))
        elif model=='Spresso':
            return redirect(url_for('repairspresso'))
        elif model=='Swift':
            return redirect(url_for('repairswift'))
    mysql.connection.commit()
    cursor.close()
    return render_template('repaircartype.html',data=data)




@app.route('/repairbaleno')
def repairbaleno():
    cursor=mysql.connection.cursor()
    query1="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Baleno'"
    result1=cursor.execute(query1)
    data1=cursor.fetchall()
    return render_template('repairbaleno.html',service1=data1)



@app.route('/repairciaz')
def repairciaz():
    cursor=mysql.connection.cursor()
    query2="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Ciaz'"
    result2=cursor.execute(query2)
    data2=cursor.fetchall()
    return render_template('repairciaz.html',service2=data2)




@app.route('/repairdzire')
def repairdzire():
    cursor=mysql.connection.cursor()
    query3="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Dzire'"
    result3=cursor.execute(query3)
    data3=cursor.fetchall()
    return render_template('repairdzire.html',service3=data3)




@app.route('/repairspresso')
def repairspresso():
    cursor=mysql.connection.cursor()
    query4="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Spresso'"
    result4=cursor.execute(query4)
    data4=cursor.fetchall()
    return render_template('repairspresso.html',service4=data4)




@app.route('/repairswift')
def repairswift():
    cursor=mysql.connection.cursor()
    query5="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Swift'"
    result5=cursor.execute(query5)
    data5=cursor.fetchall()
    return render_template('repairswift.html',service5=data5)



@app.route('/cartype',methods=['POST','GET'])
def cartype():
    print('hi')
    cursor = mysql.connection.cursor()
    cursor.execute("select carname from model")
    data=cursor.fetchall()
    print(data)
    if request.method == 'POST':
        print('hi')
        model = request.form['model']
        
        if model=='Baleno':
            return redirect(url_for('tyrebaleno'))
        elif model=='Ciaz':
            return redirect(url_for('tyreciaz'))
        elif model=='Dzire':
            return redirect(url_for('tyredzire'))
        elif model=='Spresso':
            return redirect(url_for('tyrespresso'))
        elif model=='Swift':
            return redirect(url_for('tyreswift'))
    mysql.connection.commit()
    cursor.close()
    return render_template('cartype.html',data=data)



@app.route('/tyrebaleno')
def tyrebaleno():
    cursor=mysql.connection.cursor()
    query1="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Baleno'"
    result1=cursor.execute(query1)
    data1=cursor.fetchall()
    return render_template('tyrebaleno.html',service1=data1)



@app.route('/tyreswift')
def tyreswift():
    cursor=mysql.connection.cursor()
    query2="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Swift'"
    result2=cursor.execute(query2)
    data2=cursor.fetchall()
    return render_template('tyreswift.html',service2=data2)



@app.route('/tyrespresso')
def tyrespresso():
    cursor=mysql.connection.cursor()
    query3="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Spresso'"
    result3=cursor.execute(query3)
    data3=cursor.fetchall()
    return render_template('tyrespresso.html',service3=data3)



@app.route('/tyredzire')
def tyredzire():
    cursor=mysql.connection.cursor()
    query4="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Dzire'"
    result4=cursor.execute(query4)
    data4=cursor.fetchall()
    return render_template('tyredzire.html',service4=data4)



@app.route('/tyreciaz')
def tyreciaz():
    cursor=mysql.connection.cursor()
    query5="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Ciaz'"
    result5=cursor.execute(query5)
    data5=cursor.fetchall()
    return render_template('tyreciaz.html',service5=data5)




@app.route('/editbalenoservice/<servicename>',methods=['POST','GET'])
def edit_balenoservice(servicename):
        cursor=mysql.connection.cursor()
        query1="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Baleno' and servicename=%s"
        cursor.execute(query1,(servicename,))
        data1=cursor.fetchall()
        cursor.close()
        print(data1[0])
        return render_template('editbalenoservice.html',service1=data1[0]) 




@app.route('/editciazservice/<servicename>',methods=['POST','GET'])
def edit_ciazservice(servicename):
        cursor=mysql.connection.cursor()
        query1="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Ciaz' and servicename=%s"
        cursor.execute(query1,(servicename,))
        data1=cursor.fetchall()
        cursor.close()
        print(data1[0])
        return render_template('editciazservice.html',service1=data1[0]) 




@app.route('/editdzireservice/<servicename>',methods=['POST','GET'])
def edit_dzireservice(servicename):
        cursor=mysql.connection.cursor()
        query1="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Dzire' and servicename=%s"
        cursor.execute(query1,(servicename,))
        data1=cursor.fetchall()
        cursor.close()
        print(data1[0])
        return render_template('editdzireservice.html',service1=data1[0]) 




@app.route('/editspressoservice/<servicename>',methods=['POST','GET'])
def edit_spressoservice(servicename):
        cursor=mysql.connection.cursor()
        query1="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Spresso' and servicename=%s"
        cursor.execute(query1,(servicename,))
        data1=cursor.fetchall()
        cursor.close()
        print(data1[0])
        return render_template('editspressoservice.html',service1=data1[0]) 




@app.route('/editswiftservice/<servicename>',methods=['POST','GET'])
def edit_swiftservice(servicename):
        cursor=mysql.connection.cursor()
        query1="select servicename,price,Service_Schedule from repairtype,model where model.model_id=repairtype.model_id and carname='Swift' and servicename=%s"
        cursor.execute(query1,(servicename,))
        data1=cursor.fetchall()
        cursor.close()
        print(data1[0])
        return render_template('editswiftservice.html',service1=data1[0]) 



@app.route('/editbalenotyre/<name>/<size>',methods=['POST','GET'])
def edit_balenotyre(name,size):
    cursor=mysql.connection.cursor()
    query1="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Baleno' and name=%s and size=%s"
    result1=cursor.execute(query1,(name,size))
    data1=cursor.fetchall()
    cursor.close()
    return render_template('editbalenotyre.html',service1=data1[0]) 




@app.route('/editswifttyre/<name>/<size>',methods=['POST','GET'])
def edit_swifttyre(name,size):
    cursor=mysql.connection.cursor()
    query2="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Swift' and name=%s and size=%s"
    result2=cursor.execute(query2,(name,size))
    data2=cursor.fetchall()
    cursor.close()
    return render_template('editswifttyre.html',service2=data2[0])




@app.route('/editspressotyre/<name>/<size>',methods=['POST','GET'])
def edit_spressotyre(name,size):
    cursor=mysql.connection.cursor()
    query3="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Spresso' and name=%s and size=%s"
    result3=cursor.execute(query3,(name,size))
    data3=cursor.fetchall()
    cursor.close()
    return render_template('editspressotyre.html',service3=data3[0])




@app.route('/editdziretyre/<name>/<size>',methods=['POST','GET'])
def edit_dziretyre(name,size):
    cursor=mysql.connection.cursor()
    query4="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Dzire' and name=%s and size=%s"
    result4=cursor.execute(query4,(name,size))
    data4=cursor.fetchall()
    cursor.close()
    return render_template('editdziretyre.html',service4=data4[0])




@app.route('/editciaztyre/<name>/<size>',methods=['POST','GET'])
def edit_ciaztyre(name,size):
    cursor=mysql.connection.cursor()
    query5="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Ciaz' and name=%s and size=%s"
    result5=cursor.execute(query5,(name,size))
    data5=cursor.fetchall()
    cursor.close()
    return render_template('editciaztyre.html',service5=data5[0])



@app.route('/batterybalenodescription/<batteryname>',methods=['POST','GET'])
def batterybalenodescription(batteryname):
    cursor=mysql.connection.cursor()
    cursor.execute("select batteryname from batterytype,model where model.model_id=batterytype.model_id and carname=%s and batteryname=%s",(session[model],batteryname,))
    data=cursor.fetchone()
    cursor.close()
    return render_template("batterybalenodescription.html",data=data)



@app.route('/batteryciazdescription/<batteryname>',methods=['POST','GET'])
def batteryciazdescription(batteryname):
    cursor=mysql.connection.cursor()
    cursor.execute("select batteryname from batterytype,model where model.model_id=batterytype.model_id and carname='ciaz' and batteryname=%s",(batteryname,))
    data=cursor.fetchone()
    print(data)
    cursor.close()
    return render_template("batteryciazdescription.html",data=data)



@app.route('/batterydziredescription/<batteryname>',methods=['POST','GET'])
def batterydziredescription(batteryname):
    cursor=mysql.connection.cursor()
    cursor.execute("select batteryname from batterytype,model where model.model_id=batterytype.model_id and carname='dzire' and batteryname=%s",(batteryname,))
    data=cursor.fetchone()
    cursor.close()
    return render_template("batterydziredescription.html",data=data)



@app.route('/batteryspressodescription/<batteryname>',methods=['POST','GET'])
def batteryspressodescription(batteryname):
    cursor=mysql.connection.cursor()
    cursor.execute("select batteryname from batterytype,model where model.model_id=batterytype.model_id and carname='spresso' and batteryname=%s",(batteryname,))
    data=cursor.fetchone()
    cursor.close()
    return render_template("batterybalenodescription.html",data=data)



@app.route('/batteryswiftdescription/<batteryname>',methods=['POST','GET'])
def batteryswiftdescription(batteryname):
    cursor=mysql.connection.cursor()
    cursor.execute("select batteryname from batterytype,model where model.model_id=batterytype.model_id and carname='swift' and batteryname=%s",(batteryname,))
    data=cursor.fetchone()
    cursor.close()
    return render_template("batteryswiftdescription.html",data=data)



@app.route('/repairbalenodescription/<servicename>',methods=['POST','GET'])
def repairbalenodescription(servicename):
    print(servicename)
    cursor=mysql.connection.cursor()
    cursor.execute("select servicename from repairtype,model where model.model_id=repairtype.model_id and carname='Baleno' and servicename=%s",(servicename,))
    data=cursor.fetchone()
    print(data)
    cursor.close()
    return render_template("repairbalenodescription.html",data=data)

    
@app.route('/repairciazdescription/<servicename>',methods=['POST','GET'])
def repairciazdescription(servicename):
    cursor=mysql.connection.cursor()
    print(servicename)
    cursor.execute("select servicename from repairtype,model where model.model_id=repairtype.model_id and carname='Ciaz' and servicename=%s",(servicename,))
    data=cursor.fetchone()
    cursor.close()
    return render_template("repairciazdescription.html",data=data)

    
@app.route('/repairdziredescription/<servicename>',methods=['POST','GET'])
def repairdziredescription(servicename):
    cursor=mysql.connection.cursor()
    cursor.execute("select servicename from repairtype,model where model.model_id=repairtype.model_id and carname='Dzire' and servicename=%s",(servicename,))
    data=cursor.fetchone()
    cursor.close()
    return render_template("repairdziredescription.html",data=data)


    
@app.route('/repairspressodescription/<servicename>',methods=['POST','GET'])
def repairspressodescription(servicename):
    cursor=mysql.connection.cursor()
    cursor.execute("select servicename from repairtype,model where model.model_id=repairtype.model_id and carname='Spresso' and servicename=%s",(servicename,))
    data=cursor.fetchone()
    cursor.close()
    return render_template("repairspressodescription.html",data=data)

    
@app.route('/repairswiftdescription/<servicename>',methods=['POST','GET'])
def repairswiftdescription(servicename):
    cursor=mysql.connection.cursor()
    cursor.execute("select servicename from repairtype,model where model.model_id=repairtype.model_id and carname='Swift' and servicename=%s",(servicename,))
    data=cursor.fetchone()
    cursor.close()
    return render_template("repairswiftdescription.html",data=data)

    

@app.route('/tyrebalenodescription/<name>/<size>',methods=['POST','GET'])
def tyrebalenodescription(name,size):
    cursor=mysql.connection.cursor()
    cursor.execute("select name,size from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Baleno' and name=%s and size=%s",(name,size))
    data=cursor.fetchone()
    cursor.close()
    return render_template("tyrebalenodescription.html",data=data)


    
@app.route('/tyreciazdescription/<name>/<size>',methods=['POST','GET'])
def tyreciazdescription(name,size):
    cursor=mysql.connection.cursor()
    cursor.execute("select name,size from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Ciaz' and name=%s and size=%s",(name,size))
    data=cursor.fetchone()
    cursor.close()
    return render_template("tyreciazdescription.html",data=data)



@app.route('/tyredziredescription/<name>/<size>',methods=['POST','GET'])
def tyredziredescription(name,size):
    cursor=mysql.connection.cursor()
    cursor.execute("select name,size from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Spresso' and name=%s and size=%s",(name,size))
    data=cursor.fetchone()
    cursor.close()
    return render_template("tyredziredescription.html",data=data)



@app.route('/tyrespressodescription/<name>/<size>',methods=['POST','GET'])
def tyrespressodescription(name,size):
    cursor=mysql.connection.cursor()
    cursor.execute("select name,size from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Spresso' and name=%s and size=%s",(name,size))
    data=cursor.fetchone()
    cursor.close()
    return render_template("tyrespressodescription.html",data=data)



@app.route('/tyreswiftdescription/<name>/<size>',methods=['POST','GET'])
def tyreswiftdescription(name,size):
    cursor=mysql.connection.cursor()
    cursor.execute("select name,size from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname='Swift' and name=%s and size=%s",(name,size))
    data=cursor.fetchone()
    cursor.close()
    return render_template("tyreswiftdescription.html",data=data)
    





@app.route('/repairbalenoupdate/<service1>',methods=['POST'])
def repairbalenoupdate(service1):
    if request.method == 'POST': 
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from repairtype where model_id=%s and servicename=%s',(1,service1))
        data=cursor.fetchone()
        cursor.execute('insert into repairupdate (carname,servicename,price,updateprice,description) values (%s,%s,%s,%s,%s)',('Baleno',service1,data,price,description))
        cursor.fetchone()
        query="update model,repairtype set price=%s where model.model_id=repairtype.model_id and carname='Baleno' and servicename=%s"
        cursor.execute(query,(price,service1))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('repairbaleno'))





@app.route('/repairciazupdate/<service1>',methods=['POST'])
def repairciazupdate(service1):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from repairtype where model_id=%s and servicename=%s',(5,service1))
        data=cursor.fetchone()
        cursor.execute('insert into repairupdate (carname,servicename,price,updateprice,description) values (%s,%s,%s,%s,%s)',('Ciaz',service1,data,price,description))
        cursor.fetchone()
        query="update model,repairtype set price=%s where model.model_id=repairtype.model_id and carname='Ciaz' and servicename=%s"
        cursor.execute(query,(price,service1))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('repairciaz'))
    



@app.route('/repairdzireupdate/<service1>',methods=['POST'])
def repairdzireupdate(service1):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from repairtype where model_id=%s and servicename=%s',(3,service1))
        data=cursor.fetchone()
        cursor.execute('insert into repairupdate (carname,servicename,price,updateprice,description) values (%s,%s,%s,%s,%s)',('Dzire',service1,data,price,description))
        cursor.fetchone()
        query="update model,repairtype set price=%s where model.model_id=repairtype.model_id and carname='Dzire' and servicename=%s"
        cursor.execute(query,(price,service1))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('repairdzire'))




@app.route('/repairspressoupdate/<service1>',methods=['POST'])
def repairspressoupdate(service1):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from repairtype where model_id=%s and servicename=%s',(4,service1))
        data=cursor.fetchone()
        cursor.execute('insert into repairupdate (carname,servicename,price,updateprice,description) values (%s,%s,%s,%s,%s)',('Spresso',service1,data,price,description))
        cursor.fetchone()
        query="update model,repairtype set price=%s where model.model_id=repairtype.model_id and carname='Spresso' and servicename=%s"
        cursor.execute(query,(price,service1))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('repairspresso'))




@app.route('/repairswiftupdate/<service1>',methods=['POST'])
def repairswiftupdate(service1):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from repairtype where model_id=%s and servicename=%s',(2,service1))
        data=cursor.fetchone()
        cursor.execute('insert into repairupdate (carname,servicename,price,updateprice,description) values (%s,%s,%s,%s,%s)',('Swift',service1,data,price,description))
        cursor.fetchone()
        query="update model,repairtype set price=%s where model.model_id=repairtype.model_id and carname='Swift' and servicename=%s"
        cursor.execute(query,(price,service1))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('repairswift'))




@app.route('/balenotyreupdate/<name>/<size>',methods=['POST'])
def tyrebalenoupdate(name,size):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        cursor.execute('insert into tyreupdate (carname,name,size,price,updateprice,description) values (%s,%s,%s,%s,%s,%s)',('Baleno',name,size,data,price,description))
        cursor.fetchone()
        query="update tyresize,tyrename,model,tyremodel set price=%s where tyresize.t_id=tyrename.t_id and tyresize.tsize_id=tyremodel.tsize_id and model.model_id=tyremodel.model_id and carname='Baleno' and name=%s and size=%s"
        cursor.execute(query,(price,name,size))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('tyrebaleno'))




@app.route('/swifttyreupdate/<name>/<size>',methods=['POST'])
def tyreswiftupdate(name,size):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        cursor.execute('insert into tyreupdate (carname,name,size,price,updateprice,description) values (%s,%s,%s,%s,%s,%s)',('Swift',name,size,data,price,description))
        cursor.fetchone()
        query="update tyresize,tyrename,model,tyremodel set price=%s where tyresize.t_id=tyrename.t_id and tyresize.tsize_id=tyremodel.tsize_id and model.model_id=tyremodel.model_id and carname='Swift' and name=%s and size=%s"
        cursor.execute(query,(price,name,size))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('tyreswift'))



@app.route('/spressotyreupdate/<name>/<size>',methods=['POST'])
def tyrespressoupdate(name,size):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        cursor.execute('insert into tyreupdate (carname,name,size,price,updateprice,description) values (%s,%s,%s,%s,%s,%s)',('Spresso',name,size,data,price,description))
        cursor.fetchone()
        query="update tyresize,tyrename,model,tyremodel set price=%s where tyresize.t_id=tyrename.t_id and tyresize.tsize_id=tyremodel.tsize_id and model.model_id=tyremodel.model_id and carname='Spresso' and name=%s and size=%s"
        cursor.execute(query,(price,name,size))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('tyrespresso'))




@app.route('/dziretyreupdate/<name>/<size>',methods=['POST'])
def tyredzireupdate(name,size):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        cursor.execute('insert into tyreupdate (carname,name,size,price,updateprice,description) values (%s,%s,%s,%s,%s,%s)',('Dzire',name,size,data,price,description))
        cursor.fetchone()
        query="update tyresize,tyrename,model,tyremodel set price=%s where tyresize.t_id=tyrename.t_id and tyresize.tsize_id=tyremodel.tsize_id and model.model_id=tyremodel.model_id and carname='Dzire' and name=%s and size=%s"
        cursor.execute(query,(price,name,size))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('tyredzire'))





@app.route('/ciaztyreupdate/<name>/<size>',methods=['POST'])
def tyreciazupdate(name,size):
    if request.method == 'POST':
        price = request.form['price'] 
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        cursor.execute('insert into tyreupdate (carname,name,size,price,updateprice,description) values (%s,%s,%s,%s,%s,%s)',('Ciaz',name,size,data,price,description))
        cursor.fetchone()
        query="update tyresize,tyrename,model,tyremodel set price=%s where tyresize.t_id=tyrename.t_id and tyresize.tsize_id=tyremodel.tsize_id and model.model_id=tyremodel.model_id and carname='Ciaz' and name=%s and szie=%s"
        cursor.execute(query,(price,name,size))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('tyreciaz'))




@app.route('/adddeletedtyre/<id>/<model>',methods=['POST','GET'])
def adddeletedtyre(id,model):
    cursor=mysql.connection.cursor()
    cursor.execute("select* from deletetyre where id=%s",(id,))
    data=cursor.fetchall()
    if request.method=='POST':
        model = request.form['model']
        tyrename1 = request.form['tyrename1']
        price = request.form['price']
        tyresize1 = request.form['tyresize1']
        cursor.execute("select model_id from model where carname=%s",(model,))
        data7=cursor.fetchone()
        cursor.execute("select name from tyrename where name=%s",(tyrename1,))
        data1=cursor.fetchone()
        print(data1)
        if data1:
            print("value : ", data1)
            cursor.execute("select t_id from tyrename where name=%s",(data1,))
            data2=cursor.fetchone()
            print(data2)
            cursor.execute("select size from tyresize where t_id=%s and size=%s",(data2,tyresize1,))
            data3=cursor.fetchone()
            print(data3)
            if data3:
                cursor.execute("select tsize_id from tyresize where t_id=%s and size=%s",(data2,data3))
                data5=cursor.fetchone()
                print('data5')
                cursor.execute("select tyremodel.model_id from tyremodel,model where tsize_id=%s and carname=%s",(data5,value))
                data4=cursor.fetchone()
                print(data4)
                if data4:
                    flash("data already exists")
                    return redirect(url_for('deletetyre'))
                else:
                    cursor.execute("insert into tyremodel (model_id,tsize_id) values (%s,%s,%s)",(data7,data5,))
                    mysql.connection.commit()
                    cursor.execute("delete from deletetyre where id=%s",(id,))
                    mysql.connection.commit()
            
                    flash("data added successfully")
                    return redirect(url_for('deletetyre'))
            else:
                cursor.execute("insert into tyresize (size,price,t_id) values (%s,%s,%s)",(tyresize1,price,data2,))
                cursor.execute("select tsize_id from tyresize where t_id=%s and size=%s",(data2,tyresize1))
                data8=cursor.fetchone()
                print(data8)
                print(data7)
                print(data2)
                cursor.execute("insert into tyremodel (model_id,tsize_id) value (%s,%s)",(data7,data8,))
                mysql.connection.commit()
                cursor.execute("delete from deletetyre where id=%s",(id,))
                mysql.connection.commit()
            
                flash("data added successfully")
                return redirect(url_for('deletetyre'))
        else:
            cursor.execute("INSERT INTO tyrename (name) VALUES (%s)",(tyrename1,))
            cursor.execute("select t_id from tyrename where name=%s",(tyrename1,))
            data6=cursor.fetchone()
            print(data6)
            cursor.execute("insert into tyresize (size,price,t_id) values (%s,%s,%s)",(tyresize1,price,data6,))
            cursor.execute("select tsize_id from tyrename where t_id=%s and size=%s",(data6,tyresize1))
            data9=cursor.fetchone()
            print('data9')
            cursor.execute("insert into tyremodel (model_id,tsize_id) value (%s,%s)",(data7,data9,))
            mysql.connection.commit()
            flash("data added successfully")
            cursor.execute("delete from deletetyre where id=%s",(id,))
            mysql.connection.commit()
            
            return redirect(url_for('deletetyre'))
    return render_template("adddeletedtyre.html",data3=data,id=id,car=model)



@app.route('/deletebalenotyre/<name>/<size>', methods = ['POST','GET'])
def deletebalenotyre(name,size):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data1=cursor.fetchone()
        cursor.execute('insert into deletetyre (carname,name,size,price,description) values (%s,%s,%s,%s,%s)',('Baleno',name,size,data1,description))
        cursor.execute('select tsize_id,tyrename.t_id from tyresize,tyrename where size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        print(data)
        query1='DELETE FROM tyremodel WHERE tsize_id =%s and model_id=1'
        cursor.execute(query1,(data[0],))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('tyrebaleno'))



@app.route('/deleteswifttyre/<name>/<size>', methods = ['POST','GET'])
def deleteswifttyre(name,size):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data1=cursor.fetchone()
        cursor.execute('insert into deletetyre (carname,name,size,price,description) values (%s,%s,%s,%s,%s)',('Swift',name,size,data1,description))
        cursor.execute('select tyresize.tsize_id,tyrename.t_id from tyresize,tyrename where size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        print(data)
        query1='DELETE FROM project.tyremodel WHERE tsize_id =%s and model_id=5'
        cursor.execute(query1,(data[0],))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('tyreswift'))



@app.route('/deletespressotyre/<name>/<size>', methods = ['POST','GET'])
def deletespressotyre(name,size):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data1=cursor.fetchone()
        cursor.execute('insert into deletetyre (carname,name,size,price,description) values (%s,%s,%s,%s,%s)',('Spresso',name,size,data1,description))
        cursor.execute('select tsize_id,tyrename.t_id from tyresize,tyrename where size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        print(data)
        query1='DELETE FROM project.tyremodel WHERE tsize_id =%s and model_id=4'
        cursor.execute(query1,(data[0],))
    
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('tyrespresso'))





@app.route('/deletedziretyre/<name>/<size>', methods = ['POST','GET'])
def deletedziretyre(name,size):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data1=cursor.fetchone()
        cursor.execute('insert into deletetyre (carname,name,size,price,description) values (%s,%s,%s,%s,%s)',('Dzire',name,size,data1,description))
        cursor.execute('select tsize_id,tyrename.t_id from tyresize,tyrename where size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        print(data)
        query1='DELETE FROM project.tyremodel WHERE tsize_id =%s and model_id=3'
        cursor.execute(query1,(data[0],))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('tyredzire'))



@app.route('/deleteciaztyre/<name>/<size>', methods = ['POST','GET'])
def deleteciaztyre(name,size):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price from tyresize,tyrename where tyrename.t_id=tyresize.t_id and size=%s and name=%s',(size,name))
        data1=cursor.fetchone()
        cursor.execute('insert into deletetyre (carname,name,size,price,description) values (%s,%s,%s,%s,%s)',('Ciaz',name,size,data1,description))
        cursor.execute('select tsize_id,tyrename.t_id from tyresize,tyrename where size=%s and name=%s',(size,name))
        data=cursor.fetchone()
        print(data)
        query1='DELETE FROM project.tyremodel WHERE tsize_id =%s and model_id=2'
        cursor.execute(query1,(data[0],))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('tyreciaz'))



@app.route('/batterycartype',methods=['POST','GET'])
def batterycartype():
    print('hi')
    cursor = mysql.connection.cursor()
    cursor.execute("select carname from model")
    data=cursor.fetchall()
    print(data)
    if request.method == 'POST':
        print('hi')
        model = request.form['model']
        session['model']=model
        if model=='Baleno':
            return redirect(url_for('batterybaleno'))
        elif model=='Ciaz':
            return redirect(url_for('batteryciaz'))
        elif model=='Dzire':
            return redirect(url_for('batterydzire'))
        elif model=='Spresso':
            return redirect(url_for('batteryspresso'))
        elif model=='Swift':
            return redirect(url_for('batteryswift'))
    mysql.connection.commit()
    cursor.close()
    return render_template('batterycartype.html',data=data)




@app.route('/batterybaleno')
def batterybaleno():
    cursor=mysql.connection.cursor()
    query1="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Baleno'"
    result1=cursor.execute(query1)
    data1=cursor.fetchall()
    return render_template('batterybaleno.html',service1=data1)


@app.route('/batteryciaz')
def batteryciaz():
    cursor=mysql.connection.cursor()
    query2="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Ciaz'"
    result2=cursor.execute(query2)
    data2=cursor.fetchall()
    return render_template('batteryciaz.html',service2=data2)


@app.route('/batterydzire')
def batterydzire():
    cursor=mysql.connection.cursor()
    query3="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Dzire'"
    result3=cursor.execute(query3)
    data3=cursor.fetchall()
    return render_template('batterydzire.html',service3=data3)


@app.route('/batteryspresso')
def batteryspresso():
    cursor=mysql.connection.cursor()
    query4="select batteryname,capacity,price from batterytype,model where model.model_id=batterytype.model_id and carname='Spresso'"
    result4=cursor.execute(query4)
    data4=cursor.fetchall()
    return render_template('batteryspresso.html',service4=data4)



@app.route('/batteryswift')
def batteryswift():
    cursor=mysql.connection.cursor()
    query5="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Swift'"
    result5=cursor.execute(query5)
    data5=cursor.fetchall()
    return render_template('batteryswift.html',service5=data5)





@app.route('/editbalenobattery/<batteryname>',methods=['POST','GET'])
def edit_balenobattery(batteryname):
    cursor=mysql.connection.cursor()
    query1="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Baleno' and batteryname=%s"
    result1=cursor.execute(query1,(batteryname,))
    data1=cursor.fetchall()
    cursor.close()
    return render_template('editbalenobattery.html',service1=data1[0]) 





@app.route('/editciazbattery/<batteryname>',methods=['POST','GET'])
def edit_ciazbattery(batteryname):
    cursor=mysql.connection.cursor()
    query1="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Ciaz' and batteryname=%s"
    result1=cursor.execute(query1,(batteryname,))
    data1=cursor.fetchall()
    cursor.close()
    return render_template('editciazbattery.html',service1=data1[0]) 





@app.route('/editdzirebattery/<batteryname>',methods=['POST','GET'])
def edit_dzirebattery(batteryname):
    cursor=mysql.connection.cursor()
    query1="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Dzire' and batteryname=%s"
    result1=cursor.execute(query1,(batteryname,))
    data1=cursor.fetchall()
    cursor.close()
    return render_template('editdzirebattery.html',service1=data1[0])




@app.route('/editspressobattery/<batteryname>',methods=['POST','GET'])
def edit_spressobattery(batteryname):
    cursor=mysql.connection.cursor()
    query1="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Spresso' and batteryname=%s"
    result1=cursor.execute(query1,(batteryname,))
    data1=cursor.fetchall()
    cursor.close()
    return render_template('editspressobattery.html',service1=data1[0])  





@app.route('/editswiftbattery/<batteryname>',methods=['POST','GET'])
def edit_swiftbattery(batteryname):
        cursor=mysql.connection.cursor()
        query1="select batteryname,capacity,warranty,price from batterytype,model where model.model_id=batterytype.model_id and carname='Swift' and batteryname=%s"
        cursor.execute(query1,(batteryname,))
        data1=cursor.fetchall()
        cursor.close()
        print(data1[0])
        return render_template('editswiftbattery.html',service1=data1[0])





@app.route('/balenobatteryupdate/<batteryname1>',methods=['POST'])
def batterybalenoupdate(batteryname1):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(1,batteryname1))
        data=cursor.fetchone()
        cursor.execute('insert into batteryupdate (carname,batteryname,capacity,warranty,price,updateprice,description) values (%s,%s,%s,%s,%s,%s,%s)',('Baleno',batteryname1,data[0],data[1],data[2],price,description))
        cursor.fetchone()
        query="update model,batterytype set price=%s where model.model_id=batterytype.model_id and carname='Baleno' and batteryname=%s"
        cursor.execute(query,(price,batteryname1,))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('batterybaleno'))




@app.route('/swiftbatteryupdate/<batteryname1>',methods=['POST'])
def batteryswiftupdate(batteryname1):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(5,batteryname1))
        data=cursor.fetchone()
        cursor.execute('insert into batteryupdate (carname,batteryname,capacity,warranty,price,updateprice,description) values (%s,%s,%s,%s,%s,%s,%s)',('Swift',batteryname1,data[0],data[1],data[2],price,description))
        cursor.fetchone()
        query="update model,batterytype set price=%s where model.model_id=batterytype.model_id and carname='Swift' and batteryname=%s"
        cursor.execute(query,(price,batteryname1,))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('batteryswift'))





@app.route('/spressobatteryupdate/<batteryname1>',methods=['POST'])
def batteryspressoupdate(batteryname1):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(4,batteryname1))
        data=cursor.fetchone()
        cursor.execute('insert into batteryupdate (carname,batteryname,capacity,warranty,price,updateprice,description) values (%s,%s,%s,%s,%s,%s,%s)',('Spresso',batteryname1,data[0],data[1],data[2],price,description))
        cursor.fetchone()
        query="update model,batterytype set price=%s where model.model_id=batterytype.model_id and carname='Spresso' and batteryname=%s"
        cursor.execute(query,(price,batteryname1,))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('batteryspresso'))





@app.route('/dzirebatteryupdate/<batteryname1>',methods=['POST'])
def batterydzireupdate(batteryname1):
    if request.method == 'POST':
        price = request.form['price']
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(3,batteryname1))
        data=cursor.fetchone()
        cursor.execute('insert into batteryupdate (carname,batteryname,capacity,warranty,price,updateprice,description) values (%s,%s,%s,%s,%s,%s,%s)',('Dzire',batteryname1,data[0],data[1],data[2],price,description))
        cursor.fetchone()
        query="update model,batterytype set price=%s where model.model_id=batterytype.model_id and carname='Dzire' and batteryname=%s"
        cursor.execute(query,(price,batteryname1,))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('batterydzire'))




@app.route('/ciazbatteryupdate/<batteryname1>',methods=['POST'])
def batteryciazupdate(batteryname1):
    if request.method == 'POST':
        price = request.form['price'] 
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(2,batteryname1))
        data=cursor.fetchone()
        cursor.execute('insert into batteryupdate (carname,batteryname,capacity,warranty,price,updateprice,description) values (%s,%s,%s,%s,%s,%s,%s)',('Ciaz',batteryname1,data[0],data[1],data[2],price,description))
        cursor.fetchone()
        query="update model,batterytype set price=%s where model.model_id=batterytype.model_id and carname='Ciaz' and batteryname=%s"
        cursor.execute(query,(price,batteryname1,))
        flash("Updated!")
        mysql.connection.commit()
        return redirect(url_for('batteryciaz'))




@app.route('/addciazbattery',methods=['POST','GET'])
def ciazbattery():
        if request.method == 'POST':
            batteryname = request.form['batteryname']
            capacity = request.form['capacity']
            warranty = request.form['warranty']
            price = request.form['price']
            cursor=mysql.connection.cursor()
            cursor.execute("select batteryname from batterytype where model_id=2 and batteryname=%s and capacity=%s and warranty=%s and price=%s",(batteryname,capacity,warranty,price))
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('batteryciaz'))
            else:
                query="INSERT INTO batterytype (batteryname,capacity,warranty,price,model_id) VALUES (%s,%s,%s,%s,%s)"
                val=(batteryname,capacity,warranty,price,2)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('batteryciaz'))
        return render_template('addciazbattery.html')




@app.route('/addbalenobattery',methods=['POST','GET'])
def balenobattery():
        if request.method == 'POST':
            batteryname = request.form['batteryname']
            capacity = request.form['capacity']
            price = request.form['price']
            warranty = request.form['warranty']
            cursor=mysql.connection.cursor()
            cursor.execute("select batteryname from batterytype where model_id=1 and batteryname=%s and capacity=%s and warranty=%s and price=%s",(batteryname,capacity,warranty,price))
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('batterybaleno'))
            else:
                query="INSERT INTO batterytype (batteryname,capacity,warranty,price,model_id) VALUES (%s,%s,%s,%s,%s)"
                val=(batteryname,capacity,warranty,price,1)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('batterybaleno'))
        return render_template('addbalenobattery.html')





@app.route('/adddzirebattery',methods=['POST','GET'])
def dzirebattery():
        if request.method == 'POST':
            batteryname = request.form['batteryname']
            capacity = request.form['capacity']
            warranty = request.form['warranty']
            price = request.form['price']
            cursor=mysql.connection.cursor()
            cursor.execute("select batteryname from batterytype where model_id=3 and batteryname=%s and capacity=%s and warranty=%s and price=%s ",(batteryname,capacity,warranty,price)) 
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('batterydzire'))
            else:
                query="INSERT INTO batterytype (batteryname,capacity,warranty,price,model_id) VALUES (%s,%s,%s,%s,%s)"
                val=(batteryname,capacity,warranty,price,3)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('batterydzire'))
        return render_template('adddzirebattery.html')





@app.route('/addspressobattery',methods=['POST','GET'])
def spresssobattery():
        if request.method == 'POST':
            batteryname = request.form['batteryname']
            capacity = request.form['capacity']
            warranty = request.form['warranty']
            price = request.form['price']
            cursor=mysql.connection.cursor()
            cursor.execute("select batteryname from batterytype where model_id=4 and batteryname=%s and capacity=%s and warranty=%s and price=%s ",(batteryname,capacity,warranty,price))
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('batteryspresso'))
            else:
                query="INSERT INTO batterytype (batteryname,capacity,warranty,price,model_id) VALUES (%s,%s,%s,%s,%s)"
                val=(batteryname,capacity,warranty,price,4)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('batteryspresso'))
        return render_template('addspressobattery.html')




@app.route('/addswiftbattery',methods=['POST','GET'])
def swiftbattery():
        if request.method == 'POST':
            batteryname = request.form['batteryname']
            capacity = request.form['capacity']
            warranty = request.form['warranty']
            price = request.form['price']
            cursor=mysql.connection.cursor()
            cursor.execute("select batteryname from batterytype where model_id=5 and batteryname=%s and capacity=%s and warranty=%s and price=%s",(batteryname,capacity,warranty,price))
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('batteryswift'))
                
            else:
                query="INSERT INTO batterytype (batteryname,capacity,warranty,price,model_id) VALUES (%s,%s,%s,%s,%s)"
                val=(batteryname,capacity,warranty,price,5)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('batteryswift'))
        return render_template('addswiftbattery.html')



@app.route('/adddeletedbattery/<id>/<model>',methods=['POST','GET'])
def adddeletedbattery(id,model):
    cursor=mysql.connection.cursor()
    cursor.execute("select* from deletebattery where id=%s",(id,))
    data3=cursor.fetchall()
    if request.method=='POST':
        model = request.form['model']
        batteryname = request.form['batteryname']
        capacity = request.form['capacity']
        warranty = request.form['warranty']
        price = request.form['price']
        cursor.execute("select model_id from model where carname=%s",(model,))
        data=cursor.fetchone()
        cursor.execute("select batteryname from batterytype where model_id=5 and batteryname=%s and capacity=%s and price=%s",(batteryname,capacity,price,))
        data2=cursor.fetchall()
        print(data2)
        if data2:
            flash('Service already exists')
            return redirect(url_for('deletebattery'))
        else:
            cursor.execute("INSERT INTO batterytype (batteryname,capacity,warranty,price,model_id) VALUES (%s,%s,%s,%s,%s)",(batteryname,capacity,warranty,price,data,))
            mysql.connection.commit()
            cursor.execute("delete from deletebattery where id=%s",(id,))
            mysql.connection.commit()
            flash('Service added')
            return redirect(url_for('deletebattery'))
    return render_template("adddeletedbattery.html",data3=data3,id=id,car=model)



@app.route('/deletebalenobattery/<batteryname1>',methods = ['POST','GET'])
def deletebalenobattery(batteryname1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor=mysql.connection.cursor()
        cursor = mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(1,batteryname1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deletebattery (carname,batteryname,capacity,warranty,price,description) values (%s,%s,%s,%s,%s,%s)',('Baleno',batteryname1,data[0],data[1],data[2],description))
        query1='DELETE FROM project.batterytype WHERE batteryname =%s and model_id=1'
        cursor.execute(query1,(batteryname1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('batterybaleno'))




@app.route('/deleteswiftbattery/<batteryname1>',methods = ['POST','GET'])
def deleteswiftbattery(batteryname1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(5,batteryname1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deletebattery (carname,batteryname,capacity,warranty,price,description) values (%s,%s,%s,%s,%s,%s)',('Swift',batteryname1,data[0],data[1],data[2],description))
        query2='DELETE FROM project.batterytype WHERE batteryname =%s and model_id=5'
        cursor.execute(query2,(batteryname1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('batteryswift'))





@app.route('/deletespressobattery/<batteryname1>',methods = ['POST','GET'])
def deletespressobattery(batteryname1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(4,batteryname1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deletebattery (carname,batteryname,capacity,warranty,price,description) values (%s,%s,%s,%s,%s,%s)',('Spresso',batteryname1,data[0],data[1],data[2],description))
        query3='DELETE FROM project.batterytype WHERE batteryname =%s and model_id=4'
        cursor.execute(query3,(batteryname1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('batteryspresso'))





@app.route('/deletedzirebattery/<batteryname1>',methods = ['POST','GET'])
def deletedzirebattery(batteryname1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(3,batteryname1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deletebattery (carname,batteryname,capacity,warranty,price,description) values (%s,%s,%s,%s,%s,%s)',('Dzire',batteryname1,data[0],data[1],data[2],description))
        query4='DELETE FROM project.batterytype WHERE batteryname =%s and model_id=3'
        cursor.execute(query4,(batteryname1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('batterydzire'))





@app.route('/deleteciazbattery/<batteryname1>',methods = ['POST','GET'])
def deleteciazbattery(batteryname1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select capacity,warranty,price from batterytype where model_id=%s and batteryname=%s',(2,batteryname1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deletebattery (carname,batteryname,capacity,warranty,price,description) values (%s,%s,%s,%s,%s,%s)',('Ciaz',batteryname1,data[0],data[1],data[2],description))
        query5='DELETE FROM project.batterytype WHERE batteryname =%s and model_id=2'
        cursor.execute(query5,(batteryname1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('batteryciaz'))




@app.route('/servicewashing')
def service_washing():
        cursor=mysql.connection.cursor()
        query="select* from project.servicewashing"
        cursor.execute(query)
        data=cursor.fetchall()
        return render_template('servicewashing.html',service=data)  



        

@app.route('/deletewashing/<cartype1>',methods = ['POST','GET'])
def deletewashing(cartype1):
    cursor = mysql.connection.cursor()
    query='DELETE FROM project.servicewashing WHERE cartype =%s'
    cursor.execute(query,(cartype1,))
    mysql.connection.commit()
    flash(' Record removed  successfully')
    return redirect(url_for('service_washing'))




@app.route('/adddeletedrepair/<id>/<model>',methods=['POST','GET'])
def adddeletedrepair(id,model):
    cursor=mysql.connection.cursor()
    cursor.execute("select* from deleterepair where id=%s",(id,))
    data3=cursor.fetchall()
    if request.method=='POST':
        model = request.form['model']
        servicename = request.form['servicename']
        price = request.form['price']
        period = request.form['period']
        cursor.execute("select model_id from model where carname=%s",(model,))
        data=cursor.fetchone()
        cursor.execute("select servicename from repairtype where model_id=%s and servicename=%s and price=%s ",(id,servicename,price))
        data2=cursor.fetchall()
        print(data2)
        if data2:
            flash('Service already exists')
            return redirect(url_for('deleterepair'))
        else:
            cursor.execute("INSERT INTO repairtype (servicename,price,Service_Schedule,model_id) VALUES (%s,%s,%s,%s)",(servicename,price,period,data,))
            mysql.connection.commit()
            cursor.execute("delete from deleterepair where id=%s",(id,))
            mysql.connection.commit()
            flash('Service added')
            return redirect(url_for('deleterepair'))
    return render_template("adddeletedrepair.html",data3=data3,id=id,car=model)




@app.route('/addbalenorepair',methods=['POST','GET'])
def balenorepair():
        if request.method == 'POST':
            servicename = request.form['servicename']
            price = request.form['price']
            period = request.form['period']
            cursor=mysql.connection.cursor()
            cursor.execute("select servicename from repairtype where model_id=1 and servicename=%s and price=%s ",(servicename,price))
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('repairbaleno'))
                
            else:
                query="INSERT INTO repairtype (servicename,price,Service_Schedule,model_id) VALUES (%s,%s,%s,%s)"
                val=(servicename,price,period,1)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('repairbaleno'))
        return render_template('addrepairbaleno.html')




@app.route('/addciazrepair',methods=['POST','GET'])
def ciazrepair():
        if request.method == 'POST':
            servicename = request.form['servicename']
            price = request.form['price']
            period = request.form['period']
            cursor=mysql.connection.cursor()
            cursor.execute("select servicename from repairtype where model_id=2 and servicename=%s and price=%s ",(servicename,price))
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('repairciaz'))
                
            else:
                query="INSERT INTO repairtype (servicename,price,Service_Schedule,model_id) VALUES (%s,%s,%s,%s)"
                val=(servicename,price,period,2)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('repairciaz'))

        return render_template('addrepairciaz.html')




@app.route('/adddzirerepair',methods=['POST','GET'])
def dzirerepair():
        if request.method == 'POST':
            servicename = request.form['servicename']
            price = request.form['price']
            period = request.form['period']
            cursor=mysql.connection.cursor()
            cursor.execute("select servicename from repairtype where model_id=3 and servicename=%s and price=%s ",(servicename,price))
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('repairdzire'))
                
            else:
                query="INSERT INTO repairtype (servicename,price,Service_Schedule,model_id) VALUES (%s,%s,%s,%s)"
                val=(servicename,price,period,3)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('repairdzire'))
        return render_template('addrepairdzire.html')





@app.route('/addspressorepair',methods=['POST','GET'])
def spressorepair():
        if request.method == 'POST':
            servicename = request.form['servicename']
            price = request.form['price']
            period = request.form['period']
            cursor=mysql.connection.cursor()
            cursor.execute("select servicename from repairtype where model_id=4 and servicename=%s and price=%s ",(servicename,price))
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('repairspresso'))
                
            else:
                query="INSERT INTO repairtype (servicename,price,Service_Schedule,model_id) VALUES (%s,%s,%s,%s)"
                val=(servicename,price,period,4)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('repairspresso'))
        return render_template('addrepairspresso.html')





@app.route('/addswiftrepair',methods=['POST','GET'])
def swiftrepair():
        if request.method == 'POST':
            servicename = request.form['servicename']
            price = request.form['price']
            period = request.form['period']
            cursor=mysql.connection.cursor()
            cursor.execute("select servicename from repairtype where model_id=5 and servicename=%s and price=%s",(servicename,price))
            data=cursor.fetchall()
            print(data)
            if data:
                flash('Service already exists')
                return redirect(url_for('repairswift'))
                
            else:
                query="INSERT INTO repairtype (servicename,price,Service_Schedule,model_id) VALUES (%s,%s,%s,%s)"
                val=(servicename,price,period,5)
                cursor.execute(query,val)
                mysql.connection.commit()
                flash('Service added successfully')
                return redirect(url_for('repairswift'))
        return render_template('addrepairswift.html')





@app.route('/addtyre',methods=['POST','GET'])
def addtyre():
    msg=''
    if request.method == 'POST':
        model = request.form.getlist('model[]')
        tyrename1 = request.form['tyrename1']
        price = request.form['price']
        tyresize1 = request.form['tyresize1']
        cursor = mysql.connection.cursor()
        for value in model:
            print(value)
            cursor.execute("select model_id from model where carname=%s",(value,))
            data7=cursor.fetchone()
            cursor.execute("select name from tyrename where name=%s",(tyrename1,))
            data1=cursor.fetchone()
            print(data1)
            if data1:
                print("value : ", data1)
                cursor.execute("select t_id from tyrename where name=%s",(data1,))
                data2=cursor.fetchone()
                print(data2)
                cursor.execute("select size from tyresize where t_id=%s and size=%s",(data2,tyresize1,))
                data3=cursor.fetchone()
                print(data3)
                
                
                if data3:
                    cursor.execute("select tsize_id from tyresize where t_id=%s and size=%s",(data2,data3))
                    data5=cursor.fetchone()
                    print('data5')
                    cursor.execute("select tyremodel.model_id from tyremodel,model where tsize_id=%s and carname=%s",(data5,value))
                    data4=cursor.fetchone()
                    print(data4)
                    if data4:
                        msg="data already exists"
                    else:
                        cursor.execute("insert into tyremodel (model_id,tsize_id) values (%s,%s,%s)",(data7,data5,))
                        mysql.connection.commit()
                        msg="data added successfully"
                else:
                    cursor.execute("insert into tyresize (size,price,t_id) values (%s,%s,%s)",(tyresize1,price,data2,))
                    cursor.execute("select tsize_id from tyresize where t_id=%s and size=%s",(data2,tyresize1))
                    data8=cursor.fetchone()
                    print(data8)
                    print(data7)
                    print(data2)
                    cursor.execute("insert into tyremodel (model_id,tsize_id) value (%s,%s)",(data7,data8,))
                    mysql.connection.commit()
                    msg="data added successfully"
            else:
                cursor.execute("INSERT INTO tyrename (name) VALUES (%s)",(tyrename1,))
                cursor.execute("select t_id from tyrename where name=%s",(tyrename1,))
                data6=cursor.fetchone()
                print(data6)
                cursor.execute("insert into tyresize (size,price,t_id) values (%s,%s,%s)",(tyresize1,price,data6,))
                cursor.execute("select tsize_id from tyrename where t_id=%s and size=%s",(data6,tyresize1))
                data9=cursor.fetchone()
                print('data9')
                cursor.execute("insert into tyremodel (model_id,tsize_id) value (%s,%s)",(data7,data9,))
                mysql.connection.commit()
                msg="data added successfully"
    return render_template('addtyre.html',msg=msg)






@app.route('/deletebalenorepair/<servicename1>', methods = ['POST','GET'])
def deletebalenoerepair(servicename1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price,Service_Schedule from repairtype where model_id=%s and servicename=%s',(1,servicename1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deleterepair (carname,servicename,price,service_schedule,description) values (%s,%s,%s,%s,%s)',('Baleno',servicename1,data[0],data[1],description))
        query1='DELETE FROM project.repairtype WHERE servicename =%s and model_id=1'
        cursor.execute(query1,(servicename1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('repairbaleno'))




@app.route('/deleteswiftrepair/<servicename1>', methods = ['POST','GET'])
def deleteswiftrepair(servicename1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price,Service_Schedule from repairtype where model_id=%s and servicename=%s',(5,servicename1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deleterepair (carname,servicename,price,service_schedule,description) values (%s,%s,%s,%s,%s)',('Baleno',servicename1,data[0],data[1],description))
        query2='DELETE FROM project.repairtype WHERE servicename =%s and model_id=5'
        cursor.execute(query2,(servicename1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('repairswift'))





@app.route('/deleteciazrepair/<servicename1>', methods = ['POST','GET'])
def deleteciazrepair(servicename1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price,Service_Schedule from repairtype where model_id=%s and servicename=%s',(2,servicename1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deleterepair (carname,servicename,price,service_schedule,description) values (%s,%s,%s,%s,%s)',('Baleno',servicename1,data[0],data[1],description))
        query2='DELETE FROM project.repairtype WHERE servicename =%s and model_id=2'
        cursor.execute(query2,(servicename1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('repairciaz'))




@app.route('/deletespressorepair/<servicename1>', methods = ['POST','GET'])
def deletespressorepair(servicename1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price,Service_Schedule from repairtype where model_id=%s and servicename=%s',(4,servicename1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deleterepair (carname,servicename,price,service_schedule,description) values (%s,%s,%s,%s,%s)',('Baleno',servicename1,data[0],data[1],description))
        query2='DELETE FROM project.repairtype WHERE servicename =%s and model_id=4'
        cursor.execute(query2,(servicename1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('repairspresso'))



@app.route('/deletedzirerepair/<servicename1>', methods = ['POST','GET'])
def deletedzirerepair(servicename1):
    print('HI')
    if request.method == 'POST':
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('select price,Service_Schedule from repairtype where model_id=%s and servicename=%s',(3,servicename1))
        data=cursor.fetchone()
        print(data)
        cursor.execute('insert into deleterepair (carname,servicename,price,service_schedule,description) values (%s,%s,%s,%s,%s)',('Baleno',servicename1,data[0],data[1],description))
        query2='DELETE FROM project.repairtype WHERE servicename =%s and model_id=3'
        cursor.execute(query2,(servicename1,))
        mysql.connection.commit()
        flash(' Record removed  successfully')
        return redirect(url_for('repairdzire'))



@app.route('/editwashing/<cartype>',methods=['POST','GET'])
def edit_washing(cartype):
        cursor=mysql.connection.cursor()
        query="select* from project.servicewashing where cartype = %s"
        cursor.execute(query,(cartype,))
        data=cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('editwashing.html',service=data[0]) 





@app.route('/washingupdate/<cartype1>',methods=['POST'])
def washingupdate(cartype1):
    if request.method == 'POST':
        exteriorwashing = request.form['exteriorwashing']
        ecowashing = request.form['ecowashing']

        interiorwashing = request.form['interiorwashing']
        cursor=mysql.connection.cursor()
        query="update project.servicewashing set exteriorwashing=%s, ecowashing=%s, interiorwashing=%s where cartype = %s"
        cursor.execute(query,(exteriorwashing,ecowashing,interiorwashing,cartype1))
        flash("Updated!")
        mysql.connection.commit()
  
        return redirect(url_for('service_washing'))  





@app.route('/addwashing',methods=['POST','GET'])
def washing1():
        if request.method == 'POST':
            cartype=request.form['cartype']
            exteriorwashing = request.form['exteriorwashing']
            ecowashing = request.form['ecowashing']
            interiorwashing = request.form['interiorwashing']
            cursor=mysql.connection.cursor()
            cusor.execute("select carname from model")
            query="INSERT INTO project.servicewashing (cartype,exteriorwashing,ecowashing,interiorwashing) VALUES (%s,%s,%s,%s)"
            val=(cartype,exteriorwashing,ecowashing,interiorwashing)
            cursor.execute(query,val)
            mysql.connection.commit()
            flash('Service added successfully')
            return redirect(url_for('service_washing'))
        return render_template('addwashing.html')
        




@app.route('/enquiry',methods=['POST','GET'])
def enquiry():
    msg = ''
    if 'loggedin' in session:
        if request.method=='POST' and 'description' in request.form:
            description = request.form['description']
            cursor=mysql.connection.cursor()
            cursor.execute("insert into project.enquiry (description,customer_id) values (%s,%s)",(description,session['id'],))
            mysql.connection.commit()
            msg = 'Your enquiry has send successfully !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('enquiry.html',msg=msg)
    return redirect(url_for('userdashboard'))




@app.route('/enquirydetail')
def enquiry_detail():
        cursor=mysql.connection.cursor()
        cursor.execute("select enquiryid,fullname,enquirydate,email_id from enquiry,customer where enquiry.customer_id=customer.customer_id")
        data=cursor.fetchall()
        cursor.close()
        return render_template('enquirydetail.html',customer=data)


@app.route('/respondenquiry/<sno>',methods=['POST','GET'])
def respondenquiry(sno):
        cursor=mysql.connection.cursor()
        cursor.execute("select enquiryid,fullname,email_id,description from enquiry,customer where enquiry.customer_id=customer.customer_id and enquiryid=%s",(sno,))
        data=cursor.fetchall()
        cursor.close()
        print(data[0])   
        return render_template('respondenquiry.html',customer=data)



@app.route('/enquiryresponded/<data1>/<data2>',methods=['POST'])
def enquiryresponded(data1,data2):
        if request.method=='POST':
            description = request.form['description']
            cursor=mysql.connection.cursor()
            print(description)
            cursor.execute("select description from enquiry,customer where enquiry.customer_id=customer.customer_id and enquiryid=%s",(data1,))
            data=cursor.fetchone()
            cursor.execute("insert into project.enquiryresponded (email_id,c_description,adminrespond) values (%s,%s,%s)",(data2,data,description,))
            cursor.execute("delete from enquiry where enquiryid=%s",(data1,))
            mysql.connection.commit()
            cursor.close()
            flash('Your respond has recorded')
            return redirect(url_for('enquiry_detail'))



@app.route('/totalenquiryrespond')
def totalenquiryrespond():
        cursor=mysql.connection.cursor()
        cursor.execute("select sno,email_id,date from enquiryresponded")
        data=cursor.fetchall()
        cursor.close()
        return render_template('totalenquiryrespond.html',customer=data)



@app.route('/totalenquiryview/<id1>')
def totalenquiryview(id1):
        cursor=mysql.connection.cursor()
        cursor.execute("select email_id,date,c_description,adminrespond from enquiryresponded where sno=%s",(id1,))
        data=cursor.fetchall()
        cursor.close()
        return render_template('totalenquiryview.html',customer=data)




@app.route('/enquiryhistory')
def enquiryhistory():
        cursor=mysql.connection.cursor()
        cursor.execute("select sno,date from enquiryresponded where email_id=%s",(session['email_id'],))
        data=cursor.fetchall()
        cursor.close()
        return render_template('enquiryhistory.html',customer=data)




@app.route('/userenquiryview/<id1>')
def userenquiryview(id1):
        cursor=mysql.connection.cursor()
        cursor.execute("select email_id,date,c_description,adminrespond from enquiryresponded where sno=%s",(id1,))
        data=cursor.fetchall()
        cursor.close()
        return render_template('userenquiryview.html',customer=data)





@app.route('/formcartype',methods=['POST','GET'])
def formcartype():
    cursor=mysql.connection.cursor()
    cursor.execute('select carname from model')
    data=cursor.fetchall()
    if request.method == 'POST':
        print("hi")
        session['model'] = request.form['model']
        print(session['model'])
        return redirect(url_for('serviceform'))
    return render_template('formcartype.html', data=data)





@app.route('/serviceform',methods=['POST','GET'])
def serviceform():
    cursor = mysql.connection.cursor()
    cursor.execute("select carname from model")
    data=cursor.fetchall()
    print(data)
    cursor.execute("select zipcode from pincode")
    data11=cursor.fetchall()
    print(data11)
    cursor.execute("select model_id from model where carname=%s",(session['model'],))
    d=cursor.fetchone()
    print(d)
    cursor.execute("select servicename,Service_Schedule,price from repairtype where model_id=%s",d)
    data3=cursor.fetchall()
    print(data3)
    cursor.execute("select cartype from servicewashing")
    data1=cursor.fetchall()
    print(data1)
    cursor.execute("select fullname from project.customer where email_id=%s",(session['email_id'],))
    name=cursor.fetchone()
    cursor.execute("select carname from project.model where model_id=%s",(d,))
    data4=cursor.fetchone()
    print(data4)
    cursor.execute("select batteryname,capacity,warranty,price from batterytype,model where batterytype.model_id=model.model_id and carname=%s",((session['model'],)))
    data5=cursor.fetchall()
    for value in data5:
        print(value[0])
    query3="select name,size,price from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname=%s"
    result=cursor.execute(query3,(session['model'],))
    data6=cursor.fetchall()
    if 'id' in session:
        msg=''  
        if request.method=='POST': 
            pincode = request.form['pincode']
            cartype = request.form['cartype']
            registration_no = request.form['registration_no']
            servicetype = request.form['servicetype']
            servicename = request.form.getlist('servicename[]')
            date1 = request.form['date1']
            time = request.form['time']
            date2 = request.form['date2']
            time2 = request.form['time2']
            deliverytype =request.form['deliverytype']
            pickup = request.form['pickup']
            dropaddress = request.form['dropaddress']
            pickup1 = request.form['pickup1']
            dropaddress1 = request.form['dropaddress1']
            cursor.execute("select fullname from project.customer where email_id=%s",(session['email_id'],))
            cus_id=cursor.fetchone()
            print(servicename)
            cursor.execute("select model_id from model where carname=%s",(session['model'],))
            data7=cursor.fetchone()
            today_year = str(date.today().year)
            if len(date.today().strftime('%j')) == 2:
                s_id = today_year+'0'+date.today().strftime('%j')+"".join(str(datetime.now().time()).split(':'))[:4]
            elif len(date.today().strftime('%j')) == 1:
                s_id = str(today_year)+'00'+date.today().strftime('%j')+"".join(str(datetime.now().time()).split(':'))[:4]
            elif len(date.today().strftime('%j')) == 3:
                s_id = str(today_year)+date.today().strftime('%j')+"".join(str(datetime.now().time()).split(':'))[:4]
            if deliverytype=="pickup":
                cursor.execute("INSERT INTO serviceform (s_id,name,model,cartype,r_no,service_type,date,time,deliverytype,pickup,customer_id,pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (s_id,cus_id,data4,cartype,registration_no,servicetype,date1,time,deliverytype,pickup,session['id'],pincode,))
                print('hi')
                for value in servicename:
                    print(value)
                    # cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                    session['s_id']=s_id
                    print(session['s_id'])
                    cursor.execute("select servicename,price from repairtype where servicename=%s and model_id=%s",(value,data7,))
                    data8=cursor.fetchall()
                    print(data8)
                    for value in data8:
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value[0],value[1],))
                        mysql.connection.commit()
                    if value=="ecowashing":
                        cursor.execute("select ecowashing from servicewashing where cartype=%s",(cartype,))
                        data10=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data10[0],))
                        mysql.connection.commit()
                    elif value=="exteriorwashing":
                        cursor.execute("select exteriorwashing from servicewashing where cartype=%s",(cartype,))
                        data11=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data11[0],))
                        mysql.connection.commit()  
                    elif value=="interiorwashing":
                        cursor.execute("select interiorwashing from servicewashing where cartype=%s",(cartype,))
                        data12=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data12[0],))
                        mysql.connection.commit()
                    if value=="tyrechange":
                        cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                        mysql.connection.commit()
                    if value=="batterychange":
                        
                        cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                        mysql.connection.commit()
                cursor.execute("select servicename from service where s_id=%s",(s_id,))
                data9=cursor.fetchall()
                print(data9)
               
                cursor.close()

                if "tyrechange" in servicename and "batterychange" in servicename:
                    
                    return redirect(url_for('tyrebattery'))
                elif "tyrechange" in servicename:
                    return redirect(url_for('tyrename'))
                elif "batterychange" in servicename:
                    return redirect(url_for('batteryname'))
                else:
                    flash("data added successfully")
                    # session['email_id']
                    # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [session['email_id']])
                    # word = ""
                    # for x in  data9 :
                    #     word += x[0] +" \n"
                    # msg.body = ("your request has been sent successfully \n " " selected service: \n"+str(word))
                    # mail.send(msg) 
                    return redirect(url_for('userdashboard'))
            elif deliverytype=="dropaddress":
                cursor.execute("INSERT INTO serviceform (s_id,name,model,cartype,r_no,service_type,deliverytype,dropaddress,customer_id,pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (s_id,cus_id,data4,cartype,registration_no,servicetype,deliverytype,dropaddress,session['id'],pincode,))
                for value in servicename:
                    # cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                    session['s_id']=s_id
                    print(session['s_id'])
                    cursor.execute("select servicename,price from repairtype where servicename=%s and model_id=%s",(value,data7,))
                    data8=cursor.fetchall()
                    print(data8)
                    for value in data8:
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value[0],value[1],))
                        mysql.connection.commit()
                    if value=="ecowashing":
                        cursor.execute("select ecowashing from servicewashing where cartype=%s",(cartype,))
                        data10=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data10[0],))
                        mysql.connection.commit()
                    elif value=="exteriorwashing":
                        cursor.execute("select exteriorwashing from servicewashing where cartype=%s",(cartype,))
                        data11=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data11[0],))
                        mysql.connection.commit()  
                    elif value=="interiorwashing":
                        cursor.execute("select interiorwashing from servicewashing where cartype=%s",(cartype,))
                        data12=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data12[0],))
                        mysql.connection.commit()
                    if value=="tyrechange":
                        cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                        mysql.connection.commit()
                    if value=="batterychange":
                        
                        cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                        mysql.connection.commit()
                
                cursor.execute("select servicename from service where s_id=%s",(s_id,))
                data9=cursor.fetchall()
                print(data9)
                cursor.close()
                if "tyrechange" in servicename and "batterychange" in servicename:
                    return redirect(url_for('tyrebattery'))
                elif "tyrechange" in servicename:
                    return redirect(url_for('tyrename'))
                elif "batterychange" in servicename:
                    return redirect(url_for('batteryname'))
                else:
                    flash("data added successfully")
                
                    # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [session['email_id']])
                    # word = ""
                    # for x in  data9 :
                    #     word += x[0] +" \n"
                    # msg.body = ("your request has been sent successfully \n " " selected service: \n"+str(word))
                    # mail.send(msg) 
                    return redirect(url_for('userdashboard'))

            elif deliverytype == "pickdrop":
                cursor.execute("INSERT INTO serviceform (s_id,name,model,cartype,r_no,service_type,date,time,deliverytype,pickup,dropaddress,customer_id,pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (s_id,cus_id,data4,cartype,registration_no,servicetype,date2,time2,deliverytype,pickup1,dropaddress1,session['id'],pincode,))
                for value in servicename:
                    # cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                    cursor.execute("select servicename,price from repairtype where servicename=%s and model_id=%s",(value,data7,))
                    data8=cursor.fetchall()
                    print(data8)
                    for value in data8:
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value[0],value[1],))
                        mysql.connection.commit()
                    if value=="ecowashing":
                        cursor.execute("select ecowashing from servicewashing where cartype=%s",(cartype,))
                        data10=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data10[0],))
                        mysql.connection.commit()
                    elif value=="exteriorwashing":
                        cursor.execute("select exteriorwashing from servicewashing where cartype=%s",(cartype,))
                        data11=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data11[0],))
                        mysql.connection.commit()  
                    elif value=="interiorwashing":
                        cursor.execute("select interiorwashing from servicewashing where cartype=%s",(cartype,))
                        data12=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data12[0],))
                        mysql.connection.commit()
                    if value=="tyrechange":
                        cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                        mysql.connection.commit()
                    if value=="batterychange":
                        
                        cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                        mysql.connection.commit()
                    session['s_id']=s_id
                    print(session['s_id'])
                mysql.connection.commit()
                cursor.execute("select servicename from service where s_id=%s",(s_id,))
                data9=cursor.fetchall()
                print(data9)
                cursor.close()
                if "tyrechange" in servicename and "batterychange" in servicename:
                    return redirect(url_for('tyrebattery'))
                elif "tyrechange" in servicename:
                    return redirect(url_for('tyrename'))
                elif "batterychange" in servicename:
                    return redirect(url_for('batteryname'))
                else:
                    flash("data added successfully")
                    # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [session['email_id']])
                    # word = ""
                    # for x in  data9 :
                    #     word += x[0] +" \n"
                    # msg.body = ("your request has been sent successfully \n " " selected service: \n"+str(word))
                    # mail.send(msg) 
                    return redirect(url_for('userdashboard'))
            else:
                cursor.execute("INSERT INTO serviceform (s_id,name,model,cartype,r_no,service_type,customer_id,pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);", (s_id,cus_id,data4,cartype,registration_no,servicetype,session['id'],pincode,))
                print('hi')
                for value in servicename:
                    print(value)
                    # cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                    session['s_id']=s_id
                    print(session['s_id'])
                    cursor.execute("select servicename,price from repairtype where servicename=%s and model_id=%s",(value,data7,))
                    data8=cursor.fetchall()
                    print(data8)
                    for value in data8:
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value[0],value[1],))
                        mysql.connection.commit()
                    if value=="ecowashing":
                        cursor.execute("select ecowashing from servicewashing where cartype=%s",(cartype,))
                        data10=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data10[0],))
                        mysql.connection.commit()
                    elif value=="exteriorwashing":
                        cursor.execute("select exteriorwashing from servicewashing where cartype=%s",(cartype,))
                        data11=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data11[0],))
                        mysql.connection.commit()  
                    elif value=="interiorwashing":
                        cursor.execute("select interiorwashing from servicewashing where cartype=%s",(cartype,))
                        data12=cursor.fetchone()
                        cursor.execute("insert into service (s_id,servicename,price) values (%s,%s,%s);",(s_id,value,data12[0],))
                        mysql.connection.commit()
                    if value=="tyrechange":
                        cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                        mysql.connection.commit()
                    if value=="batterychange":
                        
                        cursor.execute("insert into service (s_id,servicename) values (%s,%s);",(s_id,value,))
                        mysql.connection.commit()
                cursor.execute("select servicename from service where s_id=%s",(s_id,))
                data9=cursor.fetchall()
                print(data9)
               
                cursor.close()

                if "tyrechange" in servicename and "batterychange" in servicename:
                    
                    return redirect(url_for('tyrebattery'))
                elif "tyrechange" in servicename:
                    return redirect(url_for('tyrename'))
                elif "batterychange" in servicename:
                    return redirect(url_for('batteryname'))
                else:
                    flash("data added successfully")
                    # session['email_id']
                    # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [session['email_id']])
                    # word = ""
                    # for x in  data9 :
                    #     word += x[0] +" \n"
                    # msg.body = ("your request has been sent successfully \n " " selected service: \n"+str(word))
                    # mail.send(msg) 
                    return redirect(url_for('userdashboard')) 
            return render_template('serviceform.html',msg=msg,data=data,data1=data1,data3=data3,data4=data4,data5=data5,data6=data6,data11=data11)
        else:
            msg= 'please fill up the form!'
            return render_template('serviceform.html',msg=msg,data=data,data1=data1,data3=data3,name=name,data4=data4,data5=data5,data6=data6,data11=data11)




@app.route('/tyrename',methods=['POST','GET'])
def tyrename():
    cursor=mysql.connection.cursor()
    query3="select name,size from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname=%s"
    result=cursor.execute(query3,(session['model'],))
    data=cursor.fetchall()
    if request.method == 'POST':
        print('hi')
        tname = request.form['tname'] 
        print('hi')
        size = request.form['size']
        no = request.form['no'] 
        # count = request.form['count']  
        print(tname)
        cursor.execute("select price from tyresize,model,tyremodel,tyrename where tyrename.t_id=tyresize.t_id and tyresize.tsize_id=tyremodel.tsize_id and model.model_id=tyremodel.model_id and carname=%s and name=%s and size=%s",(session['model'],tname,size,))
        price=cursor.fetchone()
        cursor.execute("insert into servicetyre (s_id,tyrename,size,price,tno) values (%s,%s,%s,%s,%s)",(session['s_id'],tname,size,price,no,))
        mysql.connection.commit()
        cursor.execute("update service set price=%s where s_id=%s and servicename=%s",(price,session['s_id'],"tyrechange",))
        mysql.connection.commit()
        cursor.execute("select servicename from service where s_id=%s",(session['s_id'],))
        data9=cursor.fetchall()
        print(data9)
        # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [session['email_id']])
        # word = ""
        # for x in  data9 :
        #     word += x[0] +" \n"
        # msg.body = ("your request has been sent successfully \n " " selected service: \n"+str(word))
        # mail.send(msg) 
        flash("Service registered successfully")
        return redirect(url_for('userdashboard'))
    return render_template('tyrename.html',data=data)





@app.route('/tyrebattery',methods=['POST','GET'])
def tyrebattery():
    cursor=mysql.connection.cursor()
    query3="select name,size from tyrename inner join tyresize on tyresize.t_id=tyrename.t_id inner join tyremodel on tyremodel.tsize_id=tyresize.tsize_id inner join model on model.model_id=tyremodel.model_id where carname=%s"
    result=cursor.execute(query3,(session['model'],))
    data=cursor.fetchall()
    for value in data:
        print(value[0])
    cursor.execute("select batteryname,capacity,warranty from batterytype,model where batterytype.model_id=model.model_id and carname=%s",((session['model'],)))
    data1=cursor.fetchall()
    for value in data1:
        print(value[0])
    msg=''
    if request.method == 'POST':
        tname = request.form['tname']
        size = request.form['size'] 
        no = request.form['no']
        bname = request.form['bname']
        capacity = request.form['capacity']
        print(tname)
        print(size)
        cursor.execute("select price from tyresize,model,tyremodel,tyrename where tyrename.t_id=tyresize.t_id and tyresize.tsize_id=tyremodel.tsize_id and model.model_id=tyremodel.model_id and carname=%s and name=%s and size=%s",(session['model'],tname,size,))
        price=cursor.fetchone()
        print(price)
        print(session['model'])
        cursor.execute('select price from batterytype,model where batterytype.model_id=model.model_id and carname=%s and batteryname=%s and capacity=%s',(session['model'],bname,capacity,))
        data2=cursor.fetchone()
        print(data2)
        print(bname)
        print(capacity)
        
        cursor.execute("insert into servicetyre (s_id,tyrename,size,price,tno) values (%s,%s,%s,%s,%s)",(session['s_id'],tname,size,price,no,))
        mysql.connection.commit()
        cursor.execute("update service set price=%s where s_id=%s and servicename=%s",(price,session['s_id'],"tyrechange",))
        mysql.connection.commit()
        for value in data2:
            cursor.execute("insert into servicebattery (s_id,batteryname,price,capacity) values (%s,%s,%s,%s)",(session['s_id'],bname,value,capacity,))
            mysql.connection.commit()
            cursor.execute("update service set price=%s where s_id=%s and servicename=%s",(data2,session['s_id'],"batterychange",))
            mysql.connection.commit()
        cursor.execute("select servicename from service where s_id=%s",(session['s_id'],))
        data9=cursor.fetchall()
        print(data9)
        # cursor.close()
        # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [session['email_id']])
        # word = ""
        # for x in  data9 :
        #     word += x[0] +" \n"
        # msg.body = ("your request has been sent successfully \n " " selected service: \n"+str(word))
        # mail.send(msg) 
        flash("Service registered successfully")
        return redirect(url_for('userdashboard'))
    return render_template('tyrebattery.html', data=data,data1=data1)



@app.route('/batteryname',methods=['POST','GET'])
def batteryname():
    cursor=mysql.connection.cursor()
    cursor.execute("select batteryname,capacity,warranty from batterytype,model where batterytype.model_id=model.model_id and carname=%s",((session['model'],)))
    data=cursor.fetchall()
    print('hi')
    for value in data:
        print(value[0])
    if request.method == 'POST':
        bname = request.form['bname']
        capacity=request.form['capacity']
        print(bname)
        cursor.execute('select price from batterytype,model where batterytype.model_id=model.model_id and carname=%s and batteryname=%s and capacity=%s',(session['model'],bname,capacity,))
        data2=cursor.fetchone()
        print(data2)
        print(session['model'])
        for value in data2:
            cursor.execute("insert into servicebattery (s_id,batteryname,price,capacity) values (%s,%s,%s,%s)",(session['s_id'],bname,value,capacity,))
            mysql.connection.commit()
        cursor.execute("update service set price=%s where s_id=%s and servicename=%s",(data2,session['s_id'],"batterychange",))
        mysql.connection.commit()
        cursor.execute("select servicename from service where s_id=%s",(session['s_id'],))
        data9=cursor.fetchall()
        print(data9)
        cursor.close()
        # msg = 'You have successfully registered !'
        # msg = Message('Hello', sender = 'karishmakumarimali5@gmail.com', recipients = [session['email_id']])
        # word = ""
        # for x in  data9 :
        #     word += x[0] +" \n"
        # msg.body = ("your request has been sent successfully \n " " selected service: \n"+str(word))
        # mail.send(msg)
        cursor.close() 
        flash("Service registered successfully")
        return redirect(url_for('userdashboard'))
    return render_template('batteryname.html', data=data)


if __name__ == "__main__" :
    app.run(debug=True)
