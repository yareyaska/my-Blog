from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import Required


class ReviewForm(FlaskForm):
    title = StringField('Review title', validators=[Required()])
    review = TextAreaField('Blog review')
    submit = SubmitField('Submit')


class BlogForm(FlaskForm):
    '''
    Class to create a wtf form for creating a blog
    '''
    title = StringField('Blog title',validators=[Required()])
    category_id = SelectField("Select Category :", choices=[('c', 'select'), (
        '1', 'Educational'), ('2', 'Agricultural'), ('3', 'Sports'), ('4', 'Science'), ('5', 'Technology')])
    blog = TextAreaField(" Post your blog", validators=[Required()])
    submit = SubmitField("Create Blog ")


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    '''
    Class to create a wtf form for creating a blog
    '''
    feedback = TextAreaField('WRITE COMMENT',validators=[Required()])
    submit = SubmitField('SUBMIT')

class CategoryForm(FlaskForm):
    '''
    Class to create a wtf form for creating a blog
    '''
    category_id = SelectField("Select Category :", choices=[('c', 'select'), (
        '1', 'Health Related'), ('2', 'Robotics'), ('3', 'Manufacturing'), ('4', 'IoT'), ('5', 'Life inspiring')])
    blog = TextAreaField(" Post your blog", validators=[Required()])
    submit = SubmitField("Add Blog")
