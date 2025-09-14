from flask import render_template,redirect,request,url_for
import mysql.connector
from werkzeug.utils import secure_filename

con = mysql.connector.connect(host='localhost',user='root',password='user',database='OnlineBookStore')


def addBook():
    if request.method == "GET":
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("addBook.html",cats = cats)    
    else:        
        cname = request.form.get("cname")
        price = request.form.get("price")
        description = request.form.get("description") 
        quantity = request.form.get("quantity")
        if quantity == "":
            quantity = 0
        else:
            quantity = int(quantity)    
        cid = request.form.get("cid")   
        f = request.files['image_url'] 
        filename = secure_filename(f.filename)
        filename = "static/Images/"+f.filename
        f.save(filename) #This will upload the file on the server
        image_url ="Images/"+ f.filename
        sql = "insert into Book (book_title,price,description,image_url,quantity,cid) values (%s,%s,%s,%s,%s,%s)"
        val = (cname,price,description,image_url,quantity,cid)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return "Record Added.."

def showAllBooks():
    sql = "select * from book_book"
    cursor = con.cursor()
    cursor.execute(sql)
    books = cursor.fetchall()
    return render_template("showAllBooks.html",books = books)

    