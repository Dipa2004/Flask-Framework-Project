from main import app
import category_op as cat
import book_op as book
import admin 
import user

###-----------------------Category----------------------###
app.add_url_rule("/addCategory",view_func=cat.addCategory,methods=["GET","POST"])
app.add_url_rule("/showAllCategory",view_func=cat.showAllCategory)
app.add_url_rule("/deleteCategory/<cid>",view_func=cat.deleteCategory,methods=["GET","POST"])
app.add_url_rule("/editCategory/<cid>",view_func=cat.editCategory,methods=["GET","POST"])

###----------------------Book---------------------------###
app.add_url_rule("/addBook",view_func=book.addBook,methods=["GET","POST"])
app.add_url_rule("/showAllBooks",view_func=book.showAllBooks)

# ----------------------Admin-------------------
app.add_url_rule("/adminLogin",view_func=admin.adminlogin,methods=["GET","POST"])
app.add_url_rule("/adminDashboard",view_func=admin.adminDashboard)

#--------------------User-----------------------
app.add_url_rule("/",view_func=user.homepage)
app.add_url_rule("/ViewBooks/<bid>",view_func=user.ViewBooks)
app.add_url_rule("/ViewDetails/<book_id>",view_func=user.ViewDetails,methods=["GET","POST"])
app.add_url_rule("/signup",view_func=user.signup,methods=["GET","POST"])
app.add_url_rule("/login",view_func=user.login,methods=["GET","POST"])
app.add_url_rule("/logout",view_func=user.logout)
app.add_url_rule("/cart",view_func=user.showcart,methods=["GET","POST"])
app.add_url_rule("/payment",view_func=user.payment,methods=["GET","POST"])
app.add_url_rule("/myorders", view_func=user.my_orders)
