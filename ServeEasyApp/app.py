from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL


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
    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def login():
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
    return render_template('login.html')


if __name__=='__main__':
    app.run(debug=True)

