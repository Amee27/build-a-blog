from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:test123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text())

    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route('/blog', methods=['POST', 'GET'])
def index():
    post_id = request.args.get('id')
    title = "Build a Blog"

    if post_id:
        blog = Blog.query.filter_by(id = post_id).all()
        return render_template('index.html', title = title, blog = blog, post_id = post_id, list_view=False)
    else:
        blog = Blog.query.order_by(Blog.id.desc()).all()
        return render_template('index.html', title = title, blog = blog, list_view=True)

@app.route('/newpost', methods=['POST', 'GET'])
def create_new_post():
    blog_title = ""
    blog_content = ""
    title_error = ""
    content_error = ""

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']
        new_post = Blog(blog_title, blog_content)

        if blog_title == "":
            title_error = "Please enter a title!"

        if blog_content == "":
            content_error = "Please enter a post!"

        if title_error == "" and content_error == "":
            db.session.add(new_post)
            db.session.commit()

            return redirect('blog?id={}'.format(new_post.id))

    return render_template('newpost.html', title = "Add a new post", blog_title = blog_title, blog_content = blog_content, title_error = title_error, content_error = content_error)

if __name__ == "__main__":
    app.run()