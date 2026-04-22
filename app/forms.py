from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Optional, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class BookingForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=200)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=200)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=50)])
    event_type = SelectField('Type of Event', choices=[
        ('', 'Select an option'),
        ('concert', 'Concert'),
        ('church-service', 'Church Service'),
        ('conference', 'Conference'),
        ('wedding', 'Wedding'),
        ('other', 'Other'),
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[Optional()])
    submit = SubmitField('Send Booking Request')


class SiteSettingsForm(FlaskForm):
    hero_title = StringField('Hero Title', validators=[DataRequired()])
    hero_subtitle_en = StringField('Hero Subtitle (EN)', validators=[DataRequired()])
    hero_subtitle_fr = StringField('Hero Subtitle (FR)', validators=[DataRequired()])
    hero_description_en = StringField('Hero Description (EN)')
    hero_description_fr = StringField('Hero Description (FR)')
    hero_image = FileField('Hero Background Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'])])
    footer_email = StringField('Footer Email')
    footer_phone = StringField('Footer Phone')
    footer_location_en = StringField('Location (EN)')
    footer_location_fr = StringField('Location (FR)')
    submit = SubmitField('Save Settings')


class BiographyForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    section_title_en = StringField('Section Title (EN)', validators=[DataRequired()])
    section_title_fr = StringField('Section Title (FR)', validators=[DataRequired()])
    paragraph1_en = TextAreaField('Paragraph 1 (EN)', validators=[DataRequired()])
    paragraph1_fr = TextAreaField('Paragraph 1 (FR)', validators=[DataRequired()])
    paragraph2_en = TextAreaField('Paragraph 2 (EN)')
    paragraph2_fr = TextAreaField('Paragraph 2 (FR)')
    paragraph3_en = TextAreaField('Paragraph 3 (EN)')
    paragraph3_fr = TextAreaField('Paragraph 3 (FR)')
    image = FileField('Biography Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'])])
    submit = SubmitField('Save Biography')


class AchievementForm(FlaskForm):
    icon = StringField('Icon Class (e.g. fas fa-trophy)', validators=[DataRequired()])
    title_en = StringField('Title (EN)', validators=[DataRequired()])
    title_fr = StringField('Title (FR)', validators=[DataRequired()])
    description_en = TextAreaField('Description (EN)')
    description_fr = TextAreaField('Description (FR)')
    sort_order = IntegerField('Sort Order', default=0)
    submit = SubmitField('Save')


class AlbumForm(FlaskForm):
    title = StringField('Album Title', validators=[DataRequired()])
    year = IntegerField('Year', validators=[Optional()])
    description_en = TextAreaField('Description (EN)')
    description_fr = TextAreaField('Description (FR)')
    cover_image = FileField('Cover Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'])])
    audio_file = FileField('Audio File (MP3)', validators=[FileAllowed(['mp3', 'wav', 'ogg', 'm4a'])])
    listen_url = StringField('Apple Music URL (fallback)')
    sort_order = IntegerField('Sort Order', default=0)
    submit = SubmitField('Save')


class GalleryForm(FlaskForm):
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'])])
    caption_en = StringField('Caption (EN)')
    caption_fr = StringField('Caption (FR)')
    sort_order = IntegerField('Sort Order', default=0)
    submit = SubmitField('Save')


class SocialAccountForm(FlaskForm):
    platform = StringField('Platform', validators=[DataRequired()])
    icon = StringField('Icon Class', validators=[DataRequired()])
    color = StringField('Color (hex)', default='#000000')
    description_en = StringField('Description (EN)')
    description_fr = StringField('Description (FR)')
    sort_order = IntegerField('Sort Order', default=0)
    submit = SubmitField('Save')
