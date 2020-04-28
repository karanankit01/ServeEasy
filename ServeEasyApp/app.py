from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
import MySQLdb


app=Flask(__name__)

import yaml
db = yaml.load(open('db.yaml'))
app.config['MYSQ_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db'] 
mysql = MySQL(app)


@app.route('/product/all')
def all_product():
    try:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from design_products;")
        design_products = cursor.fetchall()
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from programming_products;")
        programming_products = cursor.fetchall()
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from freestyle_products;")
        freestyle_products = cursor.fetchall()
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from physical_products;")
        physical_products = cursor.fetchall()
        return render_template('all_product.html',physical_products=physical_products,freestyle_products=freestyle_products,design_products=design_products,programming_products=programming_products)
    except Exception as e:
        return str(e)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/home/<int:user_id>')
def user_home(user_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query="SELECT name,username,email,phone from user where user_id = "+str(user_id)
        print(query)
        cursor.execute(query)
        user_details = cursor.fetchall()
        return render_template('home.html',user_details=user_details)
    except Exception as e:
        return str(e)


@app.route('/sign_up',methods=['POST','GET'])
def sign_up():
    if(request.method=='POST'):
        user_details = request.form
        name = user_details['name']
        username = user_details['username']
        email = user_details['email']
        password = user_details['password']
        phone = user_details['phone']
        
        cur = mysql.connection.cursor()
        cur.execute("insert into user value(%s,%s,%s,%s,%s)",(name,0,username,email,phone))
        mysql.connection.commit()
        cur.close()
        
        return redirect('/home')
    return render_template('sign_up.html')

@app.route('/sign_in',methods=['POST','GET'])
def sign_in():
    if(request.method=='POST'):
        user_details = request.form
        username = user_details['username']
        user_password = user_details['password']
        # print(username,password)
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query="SELECT user_id AS user_id ,password AS password FROM user WHERE username ="+"'"+username+"'"
            cursor.execute(query)
            password_id_details = cursor.fetchall()
            print(type(password_id_details))
            if(len(password_id_details)==0):
                return "user dosn't exist try another or sign up"
            else:
                url_for_user_home='/home/'+str(password_id_details[0]['user_id'])
                return redirect(url_for_user_home)
        except Exception as e:
            return str(e)
    return render_template('sign_in.html')


@app.route('/products/programming',methods=['GET'])
def programming_products():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from programming_products;")
        programming_products = cursor.fetchall()
        return render_template('programming_products.html',programming_products=programming_products)
    except Exception as e:
        return str(e)
    
@app.route('/products/freestyle',methods=['GET'])
def freestyle_products():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from freestyle_products;")
        freestyle_products = cursor.fetchall()
        return render_template('freestyle_products.html',freestyle_products=freestyle_products)
    except Exception as e:
        return str(e)

@app.route('/products/design',methods=['GET'])
def design_products():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from design_products;")
        design_products = cursor.fetchall()
        return render_template('design_products.html',design_products=design_products)
    except Exception as e:
        return str(e)

@app.route('/products/physical',methods=['GET'])
def physical_products():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from physical_products;")
        physical_products = cursor.fetchall()
        return render_template('physical_products.html',physical_products=physical_products)
    except Exception as e:
        return str(e)

if __name__=='__main__':
    app.run(debug=True)

