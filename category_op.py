from flask import render_template,redirect,request,url_for
import mysql.connector

con = mysql.connector.connect(host='localhost',user='root',password='user',database='OnlineBookStore')

def addCategory():
    if request.method == "GET":
        return render_template('addCategory.html')
    else:
        cname = request.form.get("cname")
        sql = "insert into Category (cname) values (%s)"
        val = (cname,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()
        #return render_template('addCategory.html')
        return redirect(url_for('showAllCategory'))

def showAllCategory():
    sql = "select * from Category" 
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    return render_template('showAllCategories.html',cats=cats)

def deleteCategory(cid):
    if request.method == "GET":
        return render_template('deleteCategory.html')
    else:
        action = request.form.get("action")
        if action == "Yes":
            sql = "DELETE from Category where cid = %s"
            val = (cid,)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
        # else:
        #     return "Hello"
            return redirect(url_for('showAllCategory'))
        
def editCategory(cid):
    if request.method == "GET":
        sql = "select * from Category where cid = %s"
        val = (cid,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        cat = cursor.fetchone()
        return render_template('editCategory.html',cat=cat)
    else:
        cname = request.form.get("cname")
        sql = "update Category set cname = %s where cid = %s"
        val = (cname,cid)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect(url_for('showAllCategory'))