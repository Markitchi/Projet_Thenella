import os
import uuid
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.admin import bp
from app.models import (AdminUser, SiteSettings, Biography, Achievement,
                        Album, GalleryImage, SocialAccount, BookingRequest)
from app.forms import (LoginForm, SiteSettingsForm, BiographyForm, AchievementForm,
                        AlbumForm, GalleryForm, SocialAccountForm)
from app import db


def save_upload(file_field):
    """Save an uploaded file and return its relative path."""
    if file_field and file_field.filename:
        filename = secure_filename(file_field.filename)
        # Add UUID to prevent collisions
        unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        file_field.save(filepath)
        return unique_name
    return None


# ─── Authentication ────────────────────────────────────────────────
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('admin/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('admin.login'))


# ─── Dashboard ─────────────────────────────────────────────────────
@bp.route('/')
@login_required
def dashboard():
    stats = {
        'total_bookings': BookingRequest.query.count(),
        'unread_bookings': BookingRequest.query.filter_by(is_read=False).count(),
        'total_albums': Album.query.count(),
        'total_achievements': Achievement.query.count(),
        'total_gallery': GalleryImage.query.count(),
    }
    recent_bookings = BookingRequest.query.order_by(BookingRequest.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_bookings=recent_bookings)


# ─── Site Settings ─────────────────────────────────────────────────
@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    site = SiteSettings.query.first()
    form = SiteSettingsForm(obj=site)
    if form.validate_on_submit():
        form.populate_obj(site)
        img = save_upload(form.hero_image.data)
        if img:
            site.hero_image = img
        db.session.commit()
        flash('Settings updated!', 'success')
        return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html', form=form, site=site)


# ─── Biography ─────────────────────────────────────────────────────
@bp.route('/biography', methods=['GET', 'POST'])
@login_required
def biography():
    bio = Biography.query.first()
    form = BiographyForm(obj=bio)
    if form.validate_on_submit():
        form.populate_obj(bio)
        img = save_upload(form.image.data)
        if img:
            bio.image = img
        db.session.commit()
        flash('Biography updated!', 'success')
        return redirect(url_for('admin.biography'))
    return render_template('admin/biography.html', form=form, bio=bio)


# ─── Achievements ──────────────────────────────────────────────────
@bp.route('/achievements')
@login_required
def achievements():
    items = Achievement.query.order_by(Achievement.sort_order).all()
    return render_template('admin/achievements.html', items=items)


@bp.route('/achievements/add', methods=['GET', 'POST'])
@login_required
def achievement_add():
    form = AchievementForm()
    if form.validate_on_submit():
        item = Achievement()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash('Achievement added!', 'success')
        return redirect(url_for('admin.achievements'))
    return render_template('admin/achievement_form.html', form=form, title='Add Achievement')


@bp.route('/achievements/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def achievement_edit(id):
    item = Achievement.query.get_or_404(id)
    form = AchievementForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('Achievement updated!', 'success')
        return redirect(url_for('admin.achievements'))
    return render_template('admin/achievement_form.html', form=form, title='Edit Achievement')


@bp.route('/achievements/<int:id>/delete', methods=['POST'])
@login_required
def achievement_delete(id):
    item = Achievement.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Achievement deleted.', 'success')
    return redirect(url_for('admin.achievements'))


# ─── Albums ────────────────────────────────────────────────────────
@bp.route('/albums')
@login_required
def albums():
    items = Album.query.order_by(Album.sort_order).all()
    return render_template('admin/albums.html', items=items)


@bp.route('/albums/add', methods=['GET', 'POST'])
@login_required
def album_add():
    form = AlbumForm()
    if form.validate_on_submit():
        item = Album()
        form.populate_obj(item)
        img = save_upload(form.cover_image.data)
        if img:
            item.cover_image = img
        audio = save_upload(form.audio_file.data)
        if audio:
            item.audio_file = audio
        db.session.add(item)
        db.session.commit()
        flash('Album added!', 'success')
        return redirect(url_for('admin.albums'))
    return render_template('admin/album_form.html', form=form, title='Add Album')


@bp.route('/albums/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def album_edit(id):
    item = Album.query.get_or_404(id)
    form = AlbumForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        img = save_upload(form.cover_image.data)
        if img:
            item.cover_image = img
        audio = save_upload(form.audio_file.data)
        if audio:
            item.audio_file = audio
        db.session.commit()
        flash('Album updated!', 'success')
        return redirect(url_for('admin.albums'))
    return render_template('admin/album_form.html', form=form, title='Edit Album', item=item)


@bp.route('/albums/<int:id>/delete', methods=['POST'])
@login_required
def album_delete(id):
    item = Album.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Album deleted.', 'success')
    return redirect(url_for('admin.albums'))


# ─── Gallery ───────────────────────────────────────────────────────
@bp.route('/gallery')
@login_required
def gallery():
    items = GalleryImage.query.order_by(GalleryImage.sort_order).all()
    return render_template('admin/gallery.html', items=items)


@bp.route('/gallery/add', methods=['GET', 'POST'])
@login_required
def gallery_add():
    form = GalleryForm()
    if form.validate_on_submit():
        item = GalleryImage()
        form.populate_obj(item)
        img = save_upload(form.image.data)
        if img:
            item.image = img
        db.session.add(item)
        db.session.commit()
        flash('Image added!', 'success')
        return redirect(url_for('admin.gallery'))
    return render_template('admin/gallery_form.html', form=form, title='Add Gallery Image')


@bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def gallery_edit(id):
    item = GalleryImage.query.get_or_404(id)
    form = GalleryForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        img = save_upload(form.image.data)
        if img:
            item.image = img
        db.session.commit()
        flash('Image updated!', 'success')
        return redirect(url_for('admin.gallery'))
    return render_template('admin/gallery_form.html', form=form, title='Edit Gallery Image', item=item)


@bp.route('/gallery/<int:id>/delete', methods=['POST'])
@login_required
def gallery_delete(id):
    item = GalleryImage.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Image deleted.', 'success')
    return redirect(url_for('admin.gallery'))


# ─── Social Accounts ──────────────────────────────────────────────
@bp.route('/socials')
@login_required
def socials():
    items = SocialAccount.query.order_by(SocialAccount.sort_order).all()
    return render_template('admin/socials.html', items=items)


@bp.route('/socials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def social_edit(id):
    item = SocialAccount.query.get_or_404(id)
    form = SocialAccountForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('Social account updated!', 'success')
        return redirect(url_for('admin.socials'))
    return render_template('admin/social_form.html', form=form, title=f'Edit {item.platform.title()}', item=item)


# ─── Bookings ──────────────────────────────────────────────────────
@bp.route('/bookings')
@login_required
def bookings():
    items = BookingRequest.query.order_by(BookingRequest.created_at.desc()).all()
    return render_template('admin/bookings.html', items=items)


@bp.route('/bookings/<int:id>/read', methods=['POST'])
@login_required
def booking_read(id):
    item = BookingRequest.query.get_or_404(id)
    item.is_read = True
    db.session.commit()
    return redirect(url_for('admin.bookings'))


@bp.route('/bookings/<int:id>/delete', methods=['POST'])
@login_required
def booking_delete(id):
    item = BookingRequest.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Booking deleted.', 'success')
    return redirect(url_for('admin.bookings'))
