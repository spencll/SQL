"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route("/")
def home():
    # Way to reset everything by going to route origin
    with app.app_context():
        db.drop_all()
        db.create_all()

    app.logger.info('hello')
    return render_template("home.html")
    
@app.route("/users")
def list_users():
    """List users"""
    users = User.query.all()
    tags= Tag.query.all()
    return render_template("home.html", tags= tags, users= users)

@app.route("/users/new",)
def show_form():
    """Shows form"""
    return render_template("add_form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user and redirect to user info"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>")
def show_userinfo(user_id):

    '''Show information/posts on user'''
    user = User.query.get_or_404(user_id)
    all_posts = Post.query.all()

    return render_template("detail.html", user=user, all_posts=all_posts)

@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):
    '''Show edit form'''
    user = User.query.get_or_404(user_id)
    return render_template("edit_form.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=['POST'])
def edit_user(user_id):

    '''Edit user'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    '''Finding user and making edits'''
    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    '''Commiting changes'''
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    '''Delete user'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(f"/users")  

# POSTING

@app.route("/users/<int:user_id>/posts/new")
def show_postform(user_id):
    '''Show form'''
    tags = Tag.query.all()
    return render_template('post_form.html', tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def submit_post(user_id):

    title = request.form['title']
    post = request.form['content']
    # List of tagged tag names
    tagged = request.form.getlist('tag')
    # Pulling tagged tags from tag table column
    tags = Tag.query.filter(Tag.name.in_(tagged)).all()

    user_post = Post(title = title, content=post, user_id=user_id, tags=tags)
    db.session.add(user_post)
    db.session.commit() 

    return redirect(f"/posts/{user_post.id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get(post_id)
    author = User.query.get(post.user_id)
    tags = post.tags

    return render_template('post.html',post=post, tags=tags, author=author)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Show edit post form"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html',post=post, tags=tags)
    
@app.route("/posts/<int:post_id>/edit", methods=['POST'])   
def edit_post(post_id):
    '''Edit post'''
    title = request.form['title']
    content = request.form['content']

    '''Finding post and making edits'''
    post = Post.query.get(post_id)
    post.title = title
    post.content = content
 
    '''Commiting changes'''
    db.session.add(post)
    db.session.commit() 

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    '''Delete post'''
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")  

#tagging

# **GET */tags :*** Lists all tags, with links to the tag detail page.
@app.route("/tags")
def list_tags():
    tags = Tag.query.all()

    return render_template('tags.html',tags=tags)

# **GET */tags/[tag-id] :*** Show detail about a tag. Have links to edit form and to delete.

@app.route('/tags/<int:tag_id>')
def show_taginfo(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_info.html',tag=tag)

# **GET */tags/new :*** Shows a form to add a new tag.

@app.route('/tags/new')
def show_tagform():

    return render_template('tag_add.html')

# **POST */tags/new :*** Process add form, adds tag, and redirect to tag list.

@app.route('/tags/new', methods=['POST'])
def submit_tag():

    name = request.form['name']
    # Creating post list in tag

    
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit() 

    return redirect("/tags")

# **GET */tags/[tag-id]/edit :*** Show edit form for a tag.

@app.route('/tags/<int:tag_id>')

def show_edit_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_info.html',tag=tag)

# **POST */tags/[tag-id]/edit :*** Process edit form, edit tag, and redirects to the tags list.

@app.route("/tags/<int:tag_id>/edit", methods=['POST'])   
def edit_tag(tag_id):
    '''Edit post'''
    name = request.form['name']

    '''Finding tag and making edits'''
    tag = Tag.query.get(tag_id)
    tag.name= name
 
    '''Commiting changes'''
    db.session.add(tag)
    db.session.commit() 

    return redirect(f"/tags/{tag_id}")

# **POST */tags/[tag-id]/delete :*** Delete a tag.

@app.route("/tags/<int:tag_id>/delete", methods=['POST'])
def delete_tag(tag_id):
    '''Delete tag'''
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")  






