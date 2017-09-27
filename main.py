# flask requirements
from flask import Flask
from flask import request
from flask import render_template

# database client
from google.appengine.ext import ndb

# model
class Post(ndb.Model):
	title = ndb.StringProperty()
	content = ndb.StringProperty()
	# returns the title in lowercase with the spaces removed, and limit the
	# length to 20
	slug = ndb.ComputedProperty(lambda self: self.title.replace(" ", "_").lower()[:20])
	# returns the date when created
	published = ndb.DateProperty(auto_now_add=True)


# create our WSGI instance of the app
app = Flask(__name__)

@app.route("/")
def index():
	# return the index template, ordering the posts by date
	return render_template("index.html", posts=Post.query().order(-Post.date))

@app.route("/show_post/<post_slug>")
def show(post_slug):
	# return the specific post which matches the given slug
	return render_template("show_post", post=Post.query(Post.slug == post_slug))

@app.route("/new_post")
def new_post():
	return render_template("new_post.html")

@app.route("/create_post", methods=["POST"])
def create_post():
	# create a new post, based on the given
	# title and content
	n = Post(
		title=request.form["title"],
		content=request.form["content"])
	# save to the database
	n.put()
	return render_template("create_post.html", post=n)

@app.route("/edit_post/<post_slug>")
def edit_post():
	# get the post that matches the slug given
	n = Post.query(Post.slug == post_slug)
	return render_template("edit_post.html", post=n)

@app.route("/update_post/<post_slug>", methods=["POST"])
def update_post():
	# remake the post
	# ndb, instead of making a duplicate
	# post, will update the properties for
	# us
	n = Post.query(Post.slug == post_slug)
	n.title = request.form["title"]
	n.content = request.form["content"]
	n.put()
	return render_template("update_post.html", post=n)

@app.route("/delete_post/<post_slug>")
def delete_post():
	# delete the post using a key
	p_key = ndb.Key(Post, post_slug)
	p_key.delete()
	return render_template("delete_post.html")