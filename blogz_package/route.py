from flask import render_template, request, url_for, flash, redirect, session
from blogz_package.models import Blog, User
from blogz_package import app, db
from sqlalchemy import desc
from blogz_package.hashutils import make_pw_hash, check_pw_hash

# blog.id AS blog_id, 
# blog.title AS blog_title, 
# blog.text AS blog_text, 
# blog.completed AS blog_completed, 
# blog.moment AS blog_moment, 
# blog.owner_id AS blog_owner_id 

# user.id AS user_id, 
# user.email AS user_email, 
# user.username AS user_username, 
# user.pw_hash AS user_pw_hash 


@app.before_request
def require_login():
    allowed_routes = ['index', ' blog', 'login', 'register', 'static']  
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect(url_for('login'))



@app.route("/", methods=['POST', 'GET'])
def index():
    users = User.query.order_by(-User.id, User.username)
    return render_template('index.html', users=users)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']              # data sent in a post request
        user = User.query.filter_by(username=username).first() #query email from db, 1 item return
        if user and check_pw_hash(password, user.pw_hash):           # if user and check_pw_hash(password, user.pw_hash):
            session['email'] = email                     #remembers the user is logged in
            flash("Logged in", 'info')
            return redirect(url_for('blog'))

        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template("login.html")



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if len(username) <3 or len(username) >20 or " " in username:  
            flash('Invalid: 3-20 characters', 'error') 
        if len(password) <3 or len(password) >20 or " " in password:
            flash('InValid: 3-20 characters', 'error')
        if password != verify:
            flash('User password does not match', 'error')
        if email != '' and len(email) <3 or len(email) >20 and ("@" or "." not in email):
            flash('InValid email', 'error')    
            email = ''


        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(username, email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect(url_for('blog'))
        else:
            flash("The email <strong>{0}</strong> is already registered".format(email), 'error')
            
    return render_template("register.html")



@app.route('/logout')   #, methods=['POST'])
def logout():
    del session['email']
    return redirect(url_for('index'))



@app.route("/blog")
def blog():
    blog_id = Blog.query.order_by(-Blog.id)
    users = User.query.all()
    id = request.args.get("id")
    user_id = request.args.get("user_id")

    if user_id:
        user = User.query.filter_by(id=user_id).first()
        blog_id = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('userpost.html',blog_id=blog_id,user=user)
    
    elif id:
        post_id = request.args.get('id')
        blog_id = Blog.query.filter_by(id=post_id).first()
        user = User.query.filter_by(id=user_id).first()
        users = Blog.query.filter_by(owner_id=user_id).all()
        return render_template("viewpost.html", blog_id=blog_id, users=users, user=user)

    else:
        return render_template('blog.html', blog_id=blog_id,users=users)



@app.route("/addpost", methods=['GET', 'POST'])
def addpost():

    owner = User.query.filter_by(email=session['email']).first()

    if request.method == "POST":
        title = request.form['blog-title']
        text = request.form['blog-text']

        if not title:
            flash("Title field is empty", category="title")
            return redirect(url_for('addpost'))
        elif not text:
            flash("Post field is empty", category="text")
            return redirect(url_for('addpost'))
        else:
            new_post = Blog(title, text, owner)
            db.session.add(new_post)
            db.session.commit()
        view_post = Blog.query.order_by(-Blog.id).first()
        #view_post = Blog.query.order_by(desc(Blog.id)).first()
        return redirect("/blog?id={}".format(view_post.id))

    return render_template("addpost.html")


# @app.route('/delete-post', methods=['POST'])
# def delete_post():
#     post_id = int(request.form['post-id'])
#     post = Blog.query.get(post_id)
#     post.completed = False
#     db.session.delete(post)
#     db.session.commit()

#     return redirect('/blog')



######################### Notes #########################
#https://www.programcreek.com/python/example/51530/flask.request.args
# http://flask.pocoo.org/docs/1.0/quickstart/#accessing-request-data
# http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
#http://flask.pocoo.org/docs/1.0/api/#message-flashing
#http://flask.pocoo.org/docs/1.0/patterns/flashing/#flashing-with-categories
# https://www.tutorialspoint.com/flask/flask_message_flashing.htm
# http://flask.pocoo.org/docs/1.0/quickstart/?highlight=cookies#message-flashing
# nice examples ######### https://teamtreehouse.com/community/how-to-add-comments-to-post-in-flask-application
# http://flask.pocoo.org/docs/1.0/api/#sessions #users
#######https://www.tutorialspoint.com/flask/flask_sessions.htm
# http://flask.pocoo.org/docs/1.0/quickstart/#sessions
# http://flask.pocoo.org/docs/1.0/quickstart/?highlight=cookies#sessions
# http://www.sqlitetutorial.net/sqlite-date/
#http://flask-sqlalchemy.pocoo.org/2.3/queries/
#https://flask-login.readthedocs.io/en/latest/#your-user-class
#