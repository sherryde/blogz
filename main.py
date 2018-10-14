from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
import cgi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogit-basic:root@localhost:8889/blogit-basic'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)  # interface with db via python code
app.secret_key = 'p9Rv4A4HnSvV'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    # self.completed = False # delete or archiving
    moment = db.Column(db.DateTime, default=datetime.utcnow)  # possible hour ajustment fix: DateTime.UtcNow.ToLocalTime because I'm 7 hours off stl time.

    def __init__(self, title, text, moment=None):
        self.title = title
        self.text = text
        self.moment = moment


@app.route("/blog")
def index():
    if request.args:
        post_id = request.args.get('id')
        post = Blog.query.filter_by(id=post_id).first()
        return render_template("viewpost.html", post=post)

    posts = Blog.query.order_by(desc(Blog.id))
    return render_template("blog.html", posts=posts)


@app.route("/addpost", methods=['GET', 'POST'])
def addpost():
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
            new_post = Blog(title, text)
            db.session.add(new_post)
            db.session.commit()

        view_post = Blog.query.order_by(desc(Blog.id)).first()
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


if __name__ == '__main__':
    app.run(debug=True)
######################### Notes #########################
#local time
#login/hashing
#register/hashing
#Users/session/
#edit/delete or archive
# http://flask.pocoo.org/docs/1.0/quickstart/#accessing-request-data
# http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
#http://flask.pocoo.org/docs/1.0/api/#message-flashing
#http://flask.pocoo.org/docs/1.0/patterns/flashing/#flashing-with-categories
# https://www.tutorialspoint.com/flask/flask_message_flashing.htm
# http://flask.pocoo.org/docs/1.0/quickstart/?highlight=cookies#message-flashing
# nice examples ######### https://teamtreehouse.com/community/how-to-add-comments-to-post-in-flask-application
# http://flask.pocoo.org/docs/1.0/api/#sessions #users
# http://flask-sqlalchemy.pocoo.org/2.3/queries/
# http://flask.pocoo.org/docs/1.0/quickstart/?highlight=cookies#sessions
# http://www.sqlitetutorial.net/sqlite-date/
#{{ url_for('addpost') }}

# get_flashed_messages(): This function gets all of the flash messages stored in the session.
#{% with %}: The Flask template version of Python's with block. Let's you temporarily define a variable. Must be closed with {% endwith %}.
#.order_by("[tablename] desc") ex: .order_by("name desc")
# more specific: .order_by("TableName.name desc")
#.filter_by()