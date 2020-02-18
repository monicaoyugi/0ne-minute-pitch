from flask import render_template, request, redirect, url_for, abort
from . import main
from flask_login import login_required, current_user
from ..models import Pitch, Comment, User
from .forms import PitchForm, CommentsForm, UpdateProfile
from .. import db, photos


@main.route('/')
def index():
    """
    View root page function that returns the index page and its data
    """
    return render_template('index.html')


@main.route('/category/interview', methods=["GET", "POST"])
def interview():
    '''
    A view function that will return the pitches on a specific kind of view
    '''

    types = Pitch.query.filter_by(type='interview').all()
    # title = f'{types} pitch'

    return render_template('interview.html', types=types)


@main.route('/category/promotion', methods=["GET", "POST"])
def promotion():
    '''
    A view function that will return the pitches on a specific kind of view
    '''

    types = Pitch.query.filter_by(type='promotion').all()
    title = f'{types} pitch'

    return render_template('promotion.html', title=title, types=types)


@main.route('/category/add_pitch', methods=["GET", "POST"])
@login_required
def add_pitch():
    '''
    view function that helps renders theform to create a new pitch
    '''

    pitch_form = PitchForm()

    if pitch_form.validate_on_submit():
        pitch = pitch_form.pitch.data
        title = pitch_form.title.data
        type = pitch_form.type.data

        new_pitch = Pitch(title=title, pitch=pitch, type=type)
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'ADD PITCH'
    return render_template('add_pitch.html', title=title, pitch_form=pitch_form)


@main.route('/comments/new/<int:id>', methods=["GET", "POST"])
@login_required
def comment(id):
    """
    view function that return a form to comment on a given pitch
    """

    form = CommentsForm()
    pitch = Pitch.query.filter_by(id=id).first()
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(comment_post=comment, user=current_user)
        new_comment.save_comments()

        return redirect(url_for('.comments', id=pitch.id))
    title = f'{pitch.title} comments'
    return render_template('new_comment.html', title=title, comment_form=form, pitch=pitch)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, types=types)


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

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))
