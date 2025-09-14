from datetime import datetime
from flask import render_template,request,redirect,url_for,session
import mysql.connector 

con = mysql.connector.connect(host="localhost",user="root",password="user",database='OnlineBookStore')

def homepage():
    cursor = con.cursor()
    sql = "select * from category"
    cursor.execute(sql)
    cats = cursor.fetchall()

    sql = "select * from book"
    cursor.execute(sql)
    books = cursor.fetchall()

    return render_template("homepage.html",cats=cats,books = books)

def ViewBooks(bid):
    sql = "select * from book where bid=%s"
    val = (bid,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    books = cursor.fetchall()
    
    sql = "select * from category"
    cursor.execute(sql)
    cats = cursor.fetchall()

    return render_template("homepage.html",cats=cats,books=books)

def ViewDetails(book_id):
    cursor = con.cursor()
    if request.method == "GET":
        sql = "select * from book where book_id=%s"
        val = (book_id,)
        cursor.execute(sql,val)
        book = cursor.fetchone()
        sql = "select * from category"
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("ViewDetails.html",cats=cats,book=book)
    else:
        if "uname" in session:
            #check if item is already present in cart
            book_id = request.form.get("book_id")
            qty = request.form.get("qty")
            username = session["uname"]
            sql = "select count(*) from mycart where username=%s and book_id=%s"
            val = (username,book_id)
            cursor.execute(sql,val)
            count = cursor.fetchone()[0]
            if count == 1:
                return "Item already present in cart"
            else:
                #proceed to add to cart
                sql = "insert into mycart(book_id,qty,username) values (%s,%s,%s)"
                val = (book_id,qty,username)
                cursor.execute(sql,val)
                con.commit()
                #return "Item added to cart"
                return redirect(url_for("showcart"))
        else:
            return redirect(url_for("login"))


def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        sql = "select count(*) from user_info where username=%s"
        val = (uname,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        count = count[0]
        if count == 1:
            #the user is already present
            return "User already exists"
        else:
            sql = "insert into user_info values (%s,%s)"
            val = (uname, pwd)
            cursor.execute(sql,val)
            con.commit()
            return "User created.."
        
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        sql = "select count(*) from user_info where username=%s and password=%s"
        val = (uname,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        count = count[0]
        if count == 1:
            session["uname"] = uname
            #the user is already present
            return redirect(url_for("homepage"))
        else:
            return redirect(url_for("login")) 

def logout():
    if "uname" in session:
        session.clear()
        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("login"))

def showcart():
    if request.method=="GET":
        username = session["uname"]        
        sql = "select * from mycart_vw where username=%s and order_id is null"
        val = (username,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        items = cursor.fetchall()
        sql = "select * from category"
        cursor.execute(sql)
        cats = cursor.fetchall()
        sql = "select sum(subtotal) from mycart_vw where username=%s"
        val = (username,)
        cursor.execute(sql,val)
        total = cursor.fetchone()[0]
        session["total"] = total
        return render_template("showcart.html",cats= cats,items=items)
    else:        
        action = request.form.get("action")        
        mid = request.form.get("item_id")
        if action == "delete":            
            #Perform delete operation
            sql = "delete from mycart where id=%s"
            
            val = (mid,)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
        else:
            qty = request.form.get("qty")
            sql = "update  mycart set qty=%s where id=%s"
            val = (qty,mid)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
        return redirect(url_for("showcart"))   

def payment():
    if request.method == "GET":
        return render_template("make_payment.html")
    else:
        card_no = request.form.get("card_no")
        cvv = request.form.get("cvv")
        expiry = request.form.get("expiry")

        cursor = con.cursor()

        # Card validation
        sql = "select count(*) from account_details where cardno=%s and cvv=%s and expiry=%s"
        cursor.execute(sql, (card_no, cvv, expiry))
        count = cursor.fetchone()[0]

        if count == 1:
            # Deduct buyer balance
            sql = "update account_details set balance = balance-%s where cardno=%s"
            cursor.execute(sql, (session["total"], card_no))

            # Add to owner's account
            sql = "update account_details set balance = balance+%s where cardno=%s"
            cursor.execute(sql, (session["total"], '4321'))

            # Insert into order_master
            sql = "insert into order_master (date_of_order, amount, username) values (%s,%s,%s)"
            cursor.execute(sql, (datetime.now().date(), session['total'], session["uname"]))
            order_id = cursor.lastrowid

            # Fetch cart items (JOIN with book to get price)
            sql = """
            select m.book_id, m.qty, b.price, (m.qty * b.price) as subtotal
            from mycart m
            join book b on m.book_id = b.book_id
            where m.username=%s and m.order_id is null
            """
            cursor.execute(sql, (session["uname"],))
            items = cursor.fetchall()

            # Insert into orders table
            for book_id, qty, price, subtotal in items:
                sql = """insert into orders (username, book_id, qty, price, subtotal, order_date) 
                        values (%s,%s,%s,%s,%s,%s)"""
                cursor.execute(sql, (session["uname"], book_id, qty, price, subtotal, datetime.now()))
                # Reduce stock
                sql = "update book set quantity = quantity - %s where book_id = %s"
                cursor.execute(sql, (qty, book_id))

            #  Update cart
            sql = "update mycart set order_id=%s where username=%s and order_id is null"
            cursor.execute(sql, (order_id, session['uname']))

            con.commit()
            session.pop("total")

            return render_template("payment_success.html", order_id=order_id)
        else:
            return redirect(url_for("payment"))

def my_orders():
    if "uname" not in session:
        return redirect("/login")

    uname = session["uname"]
    conn = mysql.connector.connect(
        host="localhost", user="root", password="user", database="onlinebookstore"
    )
    # dictionary cursor use karo
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT 
          o.id AS id,
          b.book_title AS book_title,
          o.qty AS qty,
          o.price AS price,
          o.subtotal AS subtotal,
          o.order_date AS order_date
        FROM orders o
        JOIN book b ON o.book_id = b.book_id
        WHERE o.username = %s
        ORDER BY o.order_date DESC
    """
    cursor.execute(sql, (uname,))
    orders = cursor.fetchall()

    conn.close()

    return render_template("myorders.html", orders=orders)
