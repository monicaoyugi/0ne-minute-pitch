from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired


class PitchForm(FlaskForm):
    title = StringField(' Title', validators=[DataRequired()])
    pitch = TextAreaField('Your Pitch', validators=[DataRequired()])
    type = RadioField('Type', choices=[('interview', 'interview_pitch'),('promotion', 'promotion_pitch')])
    submit = SubmitField('Submit')


class CommentsForm(FlaskForm):
    comment = TextAreaField('Comments', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[DataRequired()])
    submit = SubmitField('Submit')
