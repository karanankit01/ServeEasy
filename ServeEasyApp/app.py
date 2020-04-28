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


@app.route('/home')
def home():
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
        return render_template('home.html',physical_products=physical_products,freestyle_products=freestyle_products,design_products=design_products,programming_products=programming_products)
    except Exception as e:
        return str(e)

@app.route('/sign_in',methods=['POST','GET'])
def sign_in():
    if(request.method=='POST'):
        user_details = request.form
        name = user_details['name']
        username = user_details['username']
        email = user_details['email']
        phone = user_details['phone']
        
        cur = mysql.connection.cursor()
        cur.execute("insert into user value(%s,%s,%s,%s,%s)",(name,0,username,email,phone))
        mysql.connection.commit()
        cur.close()
        
        return redirect('/home')
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

