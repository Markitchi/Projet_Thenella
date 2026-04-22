from flask import render_template, request, redirect, url_for, flash, make_response
from app.main import bp
from app.models import SiteSettings, Biography, Achievement, Album, GalleryImage, SocialAccount, BookingRequest
from app.forms import BookingForm
from app import db


@bp.route('/')
def index():
    lang = request.cookies.get('lang', 'en')
    settings = SiteSettings.query.first()
    bio = Biography.query.first()
    achievements = Achievement.query.order_by(Achievement.sort_order).all()
    albums = Album.query.order_by(Album.sort_order).all()
    gallery = GalleryImage.query.order_by(GalleryImage.sort_order).all()
    socials = SocialAccount.query.order_by(SocialAccount.sort_order).all()
    form = BookingForm()

    return render_template('index.html',
                           lang=lang,
                           settings=settings,
                           bio=bio,
                           achievements=achievements,
                           albums=albums,
                           gallery=gallery,
                           socials=socials,
                           form=form)


@bp.route('/contact', methods=['POST'])
def contact():
    lang = request.cookies.get('lang', 'en')
    form = BookingForm()
    if form.validate_on_submit():
        booking = BookingRequest(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            event_type=form.event_type.data,
            message=form.message.data
        )
        db.session.add(booking)
        db.session.commit()
        if lang == 'fr':
            flash('Merci ! Votre demande de réservation a été reçue. Nous vous contacterons bientôt.', 'success')
        else:
            flash('Thank you! Your booking request has been received. We\'ll contact you shortly.', 'success')
    else:
        if lang == 'fr':
            flash('Veuillez remplir tous les champs obligatoires.', 'error')
        else:
            flash('Please fill in all required fields.', 'error')
    return redirect(url_for('main.index') + '#contact')


@bp.route('/lang/<lang>')
def set_language(lang):
    if lang not in ('en', 'fr'):
        lang = 'en'
    referrer = request.referrer or url_for('main.index')
    response = make_response(redirect(referrer))
    response.set_cookie('lang', lang, max_age=365 * 24 * 60 * 60)
    return response
