from flask import Flask, render_template, request, redirect, url_for,flash, session,jsonify
from flask_mysqldb import MySQL
from spellchecker import SpellChecker
import MySQLdb
import os
from PIL import Image
import sys
import yaml
import random
import string
from form_validation import SignupForm

spell = SpellChecker()


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


app = Flask(__name__)

local_dir = os.getcwd()
print(local_dir)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)


user_details=()
@app.route('/')
def home2():
    return redirect(url_for('home'))
    

def ifUsernameNotAvailable(user_id):
    cursor = mysql.connection.cursor()
    query = "select user_id from user where user_id = %s"
    cursor.execute(query,[user_id])
    result = cursor.fetchall()
    return result

def ifEmailOccupied(email):
    cursor = mysql.connection.cursor()
    query = "select email from user where email = %s"
    cursor.execute(query,[email])
    result = cursor.fetchall()
    return result

def ifphoneOccupied(phone):
    cursor = mysql.connection.cursor()
    query = "select phone from user where phone = %s"
    cursor.execute(query,[phone])
    result = cursor.fetchall()
    return result

@app.route('/home')
def home():
    if 'user_id' in session:
        return redirect(url_for('user_home'))
    return render_template('home.html', user_details=())



@app.route('/username',methods=["POST"])
def username():
    if request.method == "POST":
        username = request.form['username']
        if ifUsernameNotAvailable(username):
            return jsonify(result="username not available")
        return jsonify(result="username available")



@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/user')
def user_home():
    try:
        # print(session)
        # sys.stdout.flush()
        if 'user_id' in session:
            user_id = session['user_id']
           # user_id = request.form('user_id')
          #  print(user_id)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + "'"+str(user_id)+"'"
            cursor.execute(query)
            user_details = cursor.fetchall()
            return render_template('home.html', user_details=user_details)
        else:
            return render_template('home.html', user_details=())
           # return 5
    except Exception as e:
        return str(e)


@app.route('/about')
def about():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + \
            str(user_id)
        cursor.execute(query)
        user_details = cursor.fetchall()
    else:
        user_details = ()
    return render_template('about.html', user_details=user_details)


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    form = SignupForm()
    if(request.method == 'POST'):
        if form.validate_on_submit():
            name = form.name.data
            user_id = form.username.data
            email = form.email.data
            password = form.password.data
            phone = form.phone.data
            if(ifUsernameNotAvailable(user_id)):
                flash( "try different username")
                return render_template('sign_up.html',form=form)
            if(ifEmailOccupied(email)):
                flash("this email already exists")
                return render_template('sign_up.html',form=form)
            cur = mysql.connection.cursor()
            cur.execute("insert into user value(%s,%s,%s,%s,%s,%s,%s)",(name, user_id,email, phone, password, '', ''))
            mysql.connection.commit()
            cur.close()
            return redirect('/home')
        return render_template('sign_up.html',form=form)
    return render_template('sign_up.html',form=form)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if(request.method == 'POST'):
        user_details = request.form
        user_id = user_details['username']
        user_password = user_details['password']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT user_id,password  FROM user WHERE user_id ="+"'"+user_id+"'"
            cursor.execute(query)
            password_id_details = cursor.fetchall()
            print(password_id_details,len(password_id_details))
            if(len(password_id_details) == 0):
                return "user dosn't exist try another or sign up"
            else:
                if(user_password == password_id_details[0]['password']):
                    #  url_for_user_home='/home/'+str(password_id_details[0]['user_id'])
                    user_id = str(password_id_details[0]['user_id'])
                    session['user_id'] = user_id
                    return redirect(url_for('user_home'))
                else:
                    return "wrong password try again"
        except Exception as e:
            return str(e)
    return render_template('sign_in.html')


@app.route('/my_products/add_new_product', methods=['POST', 'GET'])
def add_new_product():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + \
            str(user_id)
        cursor.execute(query)
        user_details = cursor.fetchall()
        if(request.method == 'POST'):
            new_product_details = request.form
            owner_id = int(user_id)
            product_name = new_product_details['product_name']
            est_price = int(new_product_details['est_price'])
            short_discription = new_product_details['short_discription']
            full_discription = new_product_details['full_discription']
            product_type = new_product_details['type']
            average_rating = 0
            NO_OF_TIME = 0
            product_id = ''
            if(product_type == '1'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "select * from physical_products ORDER BY product_id DESC LIMIT 1;"
                cursor.execute(query)
                last_row = cursor.fetchall()
                product_id_no = int(
                    (last_row[0]['product_id']).split("-")[1])+1
                product_id = (last_row[0]['product_id']).split(
                    "-")[0] + '-' + str(product_id_no)
                query = "insert into physical_products value(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, [owner_id, product_name, est_price, product_id,
                                       average_rating, NO_OF_TIME, full_discription, short_discription])
                query = "insert into all_products value(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, [owner_id, product_name, est_price, product_id,
                                       average_rating, NO_OF_TIME, full_discription, short_discription])
                mysql.connection.commit()
                cursor.close()
            elif(product_type == '2'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "select * from programming_products ORDER BY product_id DESC LIMIT 1;"
                cursor.execute(query)
                last_row = cursor.fetchall()
                product_id_no = int(
                    (last_row[0]['product_id']).split("-")[1])+1
                product_id = (last_row[0]['product_id']).split(
                    "-")[0] + '-' + str(product_id_no)
                query = "insert into programming_products value(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, [owner_id, product_name, est_price, product_id,
                                       average_rating, NO_OF_TIME, full_discription, short_discription])
                query = "insert into all_products value(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, [owner_id, product_name, est_price, product_id,
                                       average_rating, NO_OF_TIME, full_discription, short_discription])
                mysql.connection.commit()
                cursor.close()
            elif(product_type == '3'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "select * from design_products ORDER BY product_id DESC LIMIT 1;"
                cursor.execute(query)
                last_row = cursor.fetchall()
                product_id_no = int(
                    (last_row[0]['product_id']).split("-")[1])+1
                product_id = (last_row[0]['product_id']).split(
                    "-")[0] + '-' + str(product_id_no)
                query = "insert into design_products value(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, [owner_id, product_name, est_price, product_id,
                                       average_rating, NO_OF_TIME, full_discription, short_discription])
                query = "insert into all_products value(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, [owner_id, product_name, est_price, product_id,
                                       average_rating, NO_OF_TIME, full_discription, short_discription])
                mysql.connection.commit()
                cursor.close()
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "select * from freestyle_products ORDER BY product_id DESC LIMIT 1;"
                cursor.execute(query)
                last_row = cursor.fetchall()
                product_id_no = int(
                    (last_row[0]['product_id']).split("-")[1])+1
                product_id = (last_row[0]['product_id']).split(
                    "-")[0] + '-' + str(product_id_no)
                query = "insert into freestyle_products value(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, [owner_id, product_name, est_price, product_id,
                                       average_rating, NO_OF_TIME, full_discription, short_discription])
                query = "insert into all_products value(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, [owner_id, product_name, est_price, product_id,
                                       average_rating, NO_OF_TIME, full_discription, short_discription])
                mysql.connection.commit()
                cursor.close()
            try:
                redirect_url = '/my_products'
                return redirect(redirect_url)
            except Exception as e:
                return str(e)
        return render_template('add_new_product.html', user_details=user_details)
    else:
        redirect('/sign_in')


@app.route('/profile/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' in session:
        user_id = session['user_id']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if(request.method == 'POST'):
                pic = request.files['file']
                file_name = pic.filename

                file_extension = os.path.splitext(file_name)[1]

                file_path = local_dir + \
                    "/static/image/profile_pic/profile"+str(user_id)
                new_path = file_path+file_extension
                file_name = "profile"+str(user_id)+file_extension

                query = "select profile_pic from user where user_id = " + \
                    str(user_id)
                cursor.execute(query)
                pic_status = cursor.fetchall()[0]['profile_pic']
                if pic_status:
                    pic_extension = os.path.splitext(pic_status)[1]
                    temp_path = file_path+pic_extension
                    os.remove(temp_path)
                    pic.save(new_path)
                else:
                    pic.save(new_path)

                query = "update user set profile_pic = %s where user_id = " + \
                    str(user_id)
                cursor.execute(query, [file_name])
                mysql.connection.commit()
                cursor.close()
            return redirect('/profile')
        except Exception as e:
            return str(e)
    else:
        return redirect('/profile')


@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' in session:
        try:
            user_id = session['user_id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if(user_id != -1):
                query = "SELECT discribe_yourself,profile_pic,name,user_id as username,email,phone,user_id from user where user_id = " + \
                    str(user_id)
                cursor.execute(query)
                user_details = cursor.fetchall()
            #  user_details[0]['profile_pic'].show()

            #  print("s = ",user_details[0]['name'])
            else:
                user_details = ()
            query = "SELECT product_id as product_id, product_name as product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from all_products where owner_id = " + \
                str(user_id)
            cursor.execute(query)
            my_products = cursor.fetchall()
            # print(user_details)
            return render_template('profile.html', my_products=my_products, user_details=user_details)

        except Exception as e:
            return str(e)
    else:
        redirect('/sign_in')


@app.route('/product/<product_id>', methods=['POST', 'GET'])
def product(product_id):
    # try:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "select * from all_products inner join user on all_products.owner_id = user.user_id inner join product_display_pic on all_products.product_id = product_display_pic.product_id   where all_products.product_id  = %s", [product_id])
    product_and_owner_description = cursor.fetchall()
    cursor.execute(
        "select * from gallary where product_id  = %s", [product_id])
    product_gallary = cursor.fetchall()
    # print(product_and_owner_description)
    if 'user_id' in session:
        user_id = session['user_id']
        if(request.method == 'POST'):
            pic = request.files['file']
            file_name = pic.filename

            file_extension = os.path.splitext(file_name)[1]

            file_path = local_dir + \
                "/static/image/product_display_pic/product_"+str(product_id)
            new_path = file_path+file_extension
            file_name = "product_"+str(product_id)+file_extension

            query = "select * from product_display_pic where product_display_pic.product_id = '" + \
                str(product_id)+"'"
            print(query)
            cursor.execute(query)
            pic_status = cursor.fetchall()[0]['display_pic']
            # print(pic_status,"*************************")
            # print(new_path)
            # print(file_name)
            if pic_status:
                pic_extension = os.path.splitext(pic_status)[1]
                temp_path = file_path+pic_extension
                os.remove(temp_path)
                pic.save(new_path)
            else:
                pic.save(new_path)
            query = "update product_display_pic set product_display_pic.display_pic = %s where product_id = '" + \
                str(product_id)+"'"
            cursor.execute(query, [file_name])
            mysql.connection.commit()
        query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + \
            str(user_id)
        cursor.execute(query)
        user_details = cursor.fetchall()
        cursor.close()
        return render_template('product.html', product_gallary=product_gallary, user_details=user_details, product_and_owner_description=product_and_owner_description)
    return redirect('/sign_in')
    # except Exception as e:
    #     return str(e)


@app.route('/product_gallary_uploads/<product_id>', methods=['POST', 'GET'])
def gallary(product_id):
    try:
        if request.method == 'POST':
            file = request.files['file']
            file_name = file.filename

            file_extension = os.path.splitext(file_name)[1]
            if file_extension == '':
                return redirect('/product/'+str(product_id))
            file_dir = local_dir + "/static/image/gallary/" + str(product_id)

            if (os.path.isdir(file_dir) == False):
                os.mkdir(file_dir)
            file_name = randomString(16) + file_extension
            file_path = file_dir + "/" + file_name
            file.save(file_path)
            print(file_path)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "insert into gallary value(%s,%s)"
            cursor.execute(query, [product_id, file_name])
            mysql.connection.commit()
            return redirect('/product/'+str(product_id))
        else:
            return redirect('/product/'+str(product_id))
    except Exception as e:
        return str(e)


@app.route('/delete/product/gallary/<product_id>/<media_name>')
def delete_from_gallary(product_id, media_name):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "delete from gallary where media_name = '"+str(media_name)+"'"
        cursor.execute(query)
        mysql.connection.commit()
        file_dir = local_dir + "/static/image/gallary/" + \
            str(product_id)+"/"+str(media_name)
        os.remove(file_dir)
        return redirect('/product/'+str(product_id))
    except Exception as e:
        return str(e)


@app.route('/my_products', methods=['GET'])
def my_products():
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + \
                str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
            query = "SELECT * from all_products inner join product_display_pic on all_products.product_id = product_display_pic.product_id where owner_id = "+"'"+user_id+"'"
            cursor.execute(query)
            my_products = cursor.fetchall()
            return render_template('my_products.html', my_products=my_products, user_details=user_details)
        else:
            redirect('/sign_in')
    except Exception as e:
        return str(e)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        search_spell = spell.correction(search)
        search_similar = spell.candidates(search)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * from all_products inner join product_display_pic on all_products.product_id = product_display_pic.product_id WHERE LOWER(product_name) LIKE "+"'"+"%"+search.lower(
        )+"%"+"'"+" or LOWER(product_name) LIKE "+"'"+"%"+search_spell.lower()+"%"+"'"
        for word in search_similar:
            query = query+" or LOWER(product_name) LIKE " + \
                "'"+"%"+word.lower()+"%"+"'"
        cursor.execute(query)
        all_products = cursor.fetchall()
        if (len(search) == 0 and search == 'all') or len(all_products) == 0:
            cursor.execute(
                "SELECT * from all_products inner join product_display_pic on all_products.product_id = product_display_pic.product_id")
            all_products = cursor.fetchall()
        return render_template('all_product.html', user_details=user_details, all_products=all_products)
    return redirect('/product/all')


@app.route('/products/all', methods=['GET'])
def all_product():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * from all_products inner join product_display_pic on all_products.product_id = product_display_pic.product_id")
        all_products = cursor.fetchall()
        # print(user_id)
        if 'user_id' in session:
            user_id = session['user_id']
            query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + \
                str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details = ()
        return render_template('all_product.html', user_details=user_details, all_products=all_products)
    except Exception as e:
        return str(e)


@app.route('/products/programming', methods=['GET'])
def programming_products():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * from programming_products inner join product_display_pic on programming_products.product_id = product_display_pic.product_id")
        programming_products = cursor.fetchall()
        if 'user_id' in session:
            user_id = session['user_id']
            query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + \
                str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details = ()
        return render_template('programming_products.html', user_details=user_details, programming_products=programming_products)
    except Exception as e:
        return str(e)


@app.route('/products/freestyle', methods=['GET'])
def freestyle_products():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * from freestyle_products inner join product_display_pic on freestyle_products.product_id = product_display_pic.product_id")
        freestyle_products = cursor.fetchall()
        if 'user_id' in session:
            user_id = session['user_id']
            query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + \
                str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:

            user_details = ()
        return render_template('freestyle_products.html', user_details=user_details, freestyle_products=freestyle_products)
    except Exception as e:
        return str(e)


@app.route('/products/design', methods=['GET'])
def design_products():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * from design_products inner join product_display_pic on design_products.product_id = product_display_pic.product_id")
        design_products = cursor.fetchall()
        if 'user_id' in session:
            user_id = session['user_id']
            query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + \
                str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details = ()
        return render_template('design_products.html', user_details=user_details, design_products=design_products)
    except Exception as e:
        return str(e)


@app.route('/products/physical', methods=['GET'])
def physical_products():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * from physical_products inner join product_display_pic on physical_products.product_id = product_display_pic.product_id")
        physical_products = cursor.fetchall()
        if 'user_id' in session:
            user_id = session['user_id']
            query = "SELECT name,user_id as username,email,phone,user_id from user where user_id = " + \
                str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details = ()
        return render_template('physical_products.html', user_details=user_details, physical_products=physical_products)
    except Exception as e:
        return str(e)


app.secret_key = 'os.urandom(16)'
if __name__ == '__main__':
    app.run(debug=True)
