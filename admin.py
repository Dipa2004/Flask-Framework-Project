from flask import render_template,request,redirect,url_for,session
import mysql.connector 

con = mysql.connector.connect(host='localhost',user='root',password='user',database='OnlineBookStore')

def adminlogin():
    if request.method == "GET":
        return render_template("adminlogin.html")
    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        sql =  "select count(*) from adminlogin where username=%s and password=%s"
        val = (uname,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        count = count[0]
        #Invalid input
        if count == 0:
            return redirect(url_for("adminlogin"))
        else:
            #Login successful
            session["uname"]=uname
            return redirect(url_for('adminDashboard'))
def adminDashboard():
    if "uname" in session:
        return render_template("adminDashboard.html")
    else:
        return redirect(url_for("adminlogin"))
