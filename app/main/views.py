from ..import db, photos
from flask import render_template, redirect, url_for, abort
from . import main
from .forms import UpdateProfile, ReviewForm, BlogForm, CategoryForm, CommentForm
from flask_login import login_required, current_user
from ..models import Review, User, Blog, Category, Comments
from ..requests import get_quotes

@main.route('/')
def index():
    '''
    View function to route to index page
    '''

    #Getting popular movi
    title = 'Home'
    allBlogs = Blog.query.all()
    reviewz = Review.query.all()

    quote = get_quotes()

    return render_template('index.html', title=title, quote=quote, blogs=allBlogs, reviewz=reviewz)


@main.route('/user/<uname>')
def profile(uname):
    '''
    view function of the user profile page
    '''
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, Blog=Blog)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form, user=user)




@main.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    '''
    Function to route user to the form page to create new blog
    '''

    form = BlogForm()
    blog = Blog()

    if form.validate_on_submit():

        title = form.blog.data
        id = form.category_id.data
        new_blog = Blog(title=title, id=id)

        db.session.add(new_blog)
        db.session.commit()

        return redirect(url_for('.index'))

    return render_template('new_blog.html', BlogForm=form)

@main.route('/user/<uname>/update/pic', methods=['GET', 'POST'])
@login_required
def update_pic(uname):

    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_photo_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))

@main.route('/category/<int:id>')
def blogs(category):
    '''
    category route function returns a list of blogs in the category chosen
    '''
    title = Blog.query.filter_by(
        blog_id=blog.id).order_by(Blog.posted.desc())
    blogs = Blog.query.filter_by(
        category=category).order_by(Blog.posted.desc())
    comments = Review.query.filter_by(
        blog_id=blog.id).order_by(Review.posted.desc())

    return render_template("blogs.html", blogs=blogs, category=category,comments=comments,title=title)


@main.route('/reviews/<blog_id>')
@login_required
def reviews(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    reviews = Review.query.filter_by(
        blog_id=blog.id).order_by(Review.posted.desc())

    return render_template('reviews.html', blog=blog, reviews=reviews)

@main.route('/add/category', methods=['GET', 'POST'])
@login_required
def new_category():
    '''
    View new group route function that returns a page with a form to create a category
    '''
    form = CategoryForm()
    blog = Blog.query.all()

    if form.validate_on_submit():
        name = form.blog.data
        new_category = Category(name=name)
        new_category.save_category()

        return redirect(url_for('main.index'))

    title = 'New category'
    return render_template('new_category.html', category_form=form, title=title, blogs=blog)

@main.route('/blog/review/new/<blog_id>', methods=['GET', 'POST'])
@login_required
def new_review(blog_id):
    form = ReviewForm()
    blog = Blog.query.filter_by(id=blog_id).first()
    review = Review()

    if form.validate_on_submit():
        review.blog_review_title = form.title.data
        review.blog_review = form.review.data
        review.blog_id = blog_id
        review.user_id = current_user.id

        db.session.add(review)
        db.session.commit()

        return redirect(url_for('main.reviews', blog_id=blog.id))

    return render_template('new_review.html', review_form=form)


@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    ''' function to post comments '''
    form = CommentForm()
    title = 'post comment'
    blogs = Blog.query.filter_by(id=id).first()
    comments = Comments.query.filter_by().all()

    if blogs is None:
         abort(404)

    if form.validate_on_submit():
        feedback = form.feedback.data
        new_comment = Comments(
            feedback=feedback, user_id=current_user.id, blogs_id=blogs.id)
        new_comment.save_comment()
        
        return redirect(url_for('main.index', id=blogs.id))

    return render_template('post_comment.html', comment_form=form, title=title,comments=comments)


