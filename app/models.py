import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))


class AdminUser(UserMixin, db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    hero_title = db.Column(db.String(200), default='THENELLA')
    hero_subtitle_en = db.Column(db.String(300), default='Cameroonian Gospel Artist · Evangelist · Worship Leader')
    hero_subtitle_fr = db.Column(db.String(300), default='Artiste Gospel Camerounaise · Évangéliste · Leader de Louange')
    hero_description_en = db.Column(db.String(500), default='Ministering through music that transforms hearts and glorifies God')
    hero_description_fr = db.Column(db.String(500), default='Ministère par la musique qui transforme les cœurs et glorifie Dieu')
    hero_image = db.Column(db.String(300), default='seed/OIP (1).webp')
    footer_email = db.Column(db.String(200), default='contact@thenellaministries.com')
    footer_phone = db.Column(db.String(50), default='+237 XXX XXX XXX')
    footer_location_en = db.Column(db.String(200), default='Douala, Cameroon')
    footer_location_fr = db.Column(db.String(200), default='Douala, Cameroun')


class Biography(db.Model):
    __tablename__ = 'biography'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), default='Bonog Thérèse Ornella')
    section_title_en = db.Column(db.String(200), default='Her Story')
    section_title_fr = db.Column(db.String(200), default='Son Histoire')
    paragraph1_en = db.Column(db.Text)
    paragraph1_fr = db.Column(db.Text)
    paragraph2_en = db.Column(db.Text)
    paragraph2_fr = db.Column(db.Text)
    paragraph3_en = db.Column(db.Text)
    paragraph3_fr = db.Column(db.Text)
    image = db.Column(db.String(300), default='seed/OIP.webp')


class Achievement(db.Model):
    __tablename__ = 'achievement'
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(100), nullable=False, default='fas fa-trophy')
    title_en = db.Column(db.String(200), nullable=False)
    title_fr = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text)
    description_fr = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)


class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    description_en = db.Column(db.Text)
    description_fr = db.Column(db.Text)
    cover_image = db.Column(db.String(300))
    listen_url = db.Column(db.String(500))
    audio_file = db.Column(db.String(300))
    sort_order = db.Column(db.Integer, default=0)


class GalleryImage(db.Model):
    __tablename__ = 'gallery_image'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(300), nullable=False)
    caption_en = db.Column(db.String(300))
    caption_fr = db.Column(db.String(300))
    sort_order = db.Column(db.Integer, default=0)


class SocialAccount(db.Model):
    __tablename__ = 'social_account'
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), default='#000000')
    description_en = db.Column(db.String(300))
    description_fr = db.Column(db.String(300))
    links_json = db.Column(db.Text, default='[]')
    sort_order = db.Column(db.Integer, default=0)

    @property
    def links(self):
        return json.loads(self.links_json) if self.links_json else []

    @links.setter
    def links(self, value):
        self.links_json = json.dumps(value, ensure_ascii=False)


class BookingRequest(db.Model):
    __tablename__ = 'booking_request'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50))
    event_type = db.Column(db.String(100))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


def seed_database():
    """Populate the database with original static site content if empty."""
    if AdminUser.query.first():
        return

    # Create admin user
    admin = AdminUser(username='admin')
    admin.set_password('thenella2026')
    db.session.add(admin)

    # Site settings
    settings = SiteSettings()
    db.session.add(settings)

    # Biography
    bio = Biography(
        full_name='Bonog Thérèse Ornella',
        paragraph1_en='Thenella, born Bonog Thérèse Ornella, is a Cameroonian gospel singer, songwriter, worship leader, and evangelist. Her spiritual journey began in a Christian family where her father\'s miraculous healing experience profoundly shaped her faith.',
        paragraph1_fr='Thenella, née Bonog Thérèse Ornella, est une chanteuse de gospel, auteure-compositrice, leader de louange et évangéliste camerounaise. Son parcours spirituel a commencé dans une famille chrétienne où l\'expérience de guérison miraculeuse de son père a profondément façonné sa foi.',
        paragraph2_en='For years, she served as lead vocalist and choir director at various churches, working with gospel groups like No Greater Love Family and Divine Harmonie. In September 2017, she was ordained as an evangelist, expanding her ministry beyond music to include preaching and outreach to vulnerable communities across Africa.',
        paragraph2_fr='Pendant des années, elle a servi comme vocaliste principale et directrice de chœur dans diverses églises, travaillant avec des groupes gospel comme No Greater Love Family et Divine Harmonie. En septembre 2017, elle a été ordonnée évangéliste, élargissant son ministère au-delà de la musique pour inclure la prédication et le soutien aux communautés vulnérables à travers l\'Afrique.',
        paragraph3_en='Married to Dr. Philippe Totto Ndong, Thenella continues to minister through her music and gospel outreach from Douala, Cameroon, touching hearts with worship that bridges earthly experiences and divine encounters.',
        paragraph3_fr='Mariée au Dr. Philippe Totto Ndong, Thenella continue à exercer son ministère à travers sa musique et son évangélisation depuis Douala, Cameroun, touchant les cœurs avec une louange qui relie les expériences terrestres aux rencontres divines.',
        image='seed/OIP.webp'
    )
    db.session.add(bio)

    # Achievements
    achievements = [
        Achievement(icon='fas fa-trophy', title_en='Revelation of the Year', title_fr='Révélation de l\'Année',
                     description_en='Zamba Awards after the release of \'Cœur Nouveau\' album',
                     description_fr='Zamba Awards après la sortie de l\'album \'Cœur Nouveau\'', sort_order=1),
        Achievement(icon='fas fa-music', title_en='Breakthrough Album', title_fr='Album Révélation',
                     description_en='\'Cœur Nouveau\' (2019) with 10 inspirational tracks',
                     description_fr='\'Cœur Nouveau\' (2019) avec 10 titres inspirants', sort_order=2),
        Achievement(icon='fas fa-hands-praying', title_en='Ordained Evangelist', title_fr='Évangéliste Ordonnée',
                     description_en='Officially ordained in September 2017 for ministry work',
                     description_fr='Ordonnée officiellement en septembre 2017 pour le travail ministériel', sort_order=3),
        Achievement(icon='fas fa-record-vinyl', title_en='Multiple Albums', title_fr='Plusieurs Albums',
                     description_en='Released several successful albums and singles since 2017',
                     description_fr='Plusieurs albums et singles à succès depuis 2017', sort_order=4),
    ]
    db.session.add_all(achievements)

    # Albums
    albums = [
        Album(title='Cœur Nouveau', year=2019,
              description_en='Breakthrough album with 10 tracks of spiritual transformation',
              description_fr='Album révélation avec 10 titres de transformation spirituelle',
              cover_image='seed/592x592bb.webp',
              listen_url='https://music.apple.com/us/album/c%C5%93ur-nouveau/1454733587', sort_order=1),
        Album(title='Une Autre Dimension', year=2024,
              description_en='Latest album capturing praise, worship, and testimony themes',
              description_fr='Dernier album capturant des thèmes de louange, d\'adoration et de témoignage',
              cover_image='seed/592x592bb (1).webp',
              listen_url='https://music.apple.com/sn/album/une-autre-dimension/1786566551', sort_order=2),
        Album(title='Je te bénirai (Live)', year=2024,
              description_en='Live single reflecting grateful worship and praise',
              description_fr='Single en direct reflétant une adoration et une louange reconnaissantes',
              cover_image='seed/592x592bb (2).webp',
              listen_url='https://music.apple.com/gb/album/je-te-b%C3%A9nirai-live-single/1755108856', sort_order=3),
    ]
    db.session.add_all(albums)

    # Gallery images
    gallery = [
        GalleryImage(image='seed/OIP.webp', caption_en='Ministry & Worship', caption_fr='Ministère & Adoration', sort_order=1),
        GalleryImage(image='seed/download.webp', caption_en='Live Gospel Performances', caption_fr='Performances Gospel en Direct', sort_order=2),
        GalleryImage(image='seed/OIP (5).webp', caption_en='Music Creation Process', caption_fr='Processus de Création Musicale', sort_order=3),
        GalleryImage(image='seed/OIP (4).webp', caption_en='Community Outreach & Evangelism', caption_fr='Action Communautaire & Évangélisation', sort_order=4),
    ]
    db.session.add_all(gallery)

    # Social accounts
    youtube = SocialAccount(
        platform='youtube', icon='fab fa-youtube', color='#FF0000',
        description_en='Official music videos and worship sessions',
        description_fr='Vidéos musicales officielles et sessions de louange',
        sort_order=1
    )
    youtube.links = [
        {'url': 'https://www.youtube.com/results?search_query=Thenella+Officiel', 'icon': 'fas fa-play-circle', 'label_en': 'Ouvrier de la Moisson', 'label_fr': 'Ouvrier de la Moisson'},
        {'url': 'https://www.youtube.com/results?search_query=Thenella+Officiel', 'icon': 'fas fa-play-circle', 'label_en': 'Seigneur Mon Roi', 'label_fr': 'Seigneur Mon Roi'},
        {'url': 'https://www.youtube.com/results?search_query=Thenella+Officiel', 'icon': 'fas fa-play-circle', 'label_en': 'La Gloire de l\'Éternel', 'label_fr': 'La Gloire de l\'Éternel'},
    ]

    tiktok = SocialAccount(
        platform='tiktok', icon='fab fa-tiktok', color='#000000',
        description_en='Short videos, behind the scenes, and worship clips',
        description_fr='Vidéos courtes, coulisses et clips de louange',
        sort_order=2
    )
    tiktok.links = [
        {'url': 'https://www.tiktok.com/search?q=thenella%20gospel&t=1717758924714', 'icon': 'fas fa-video', 'label_en': 'Worship Moments', 'label_fr': 'Moments de Louange'},
        {'url': 'https://www.tiktok.com/search?q=thenella%20gospel&t=1717758924714', 'icon': 'fas fa-video', 'label_en': 'Ministry Updates', 'label_fr': 'Mises à Jour du Ministère'},
        {'url': 'https://www.tiktok.com/search?q=thenella%20gospel&t=1717758924714', 'icon': 'fas fa-video', 'label_en': 'Daily Inspiration', 'label_fr': 'Inspiration Quotidienne'},
    ]

    facebook = SocialAccount(
        platform='facebook', icon='fab fa-facebook', color='#1877F2',
        description_en='Thenella Ministries official page for updates and events',
        description_fr='Page officielle de Thenella Ministries pour mises à jour et événements',
        sort_order=3
    )
    facebook.links = [
        {'url': 'https://www.facebook.com/search/top?q=thenella%20gospel', 'icon': 'fas fa-newspaper', 'label_en': 'Ministry Publications', 'label_fr': 'Publications du Ministère'},
        {'url': 'https://www.facebook.com/search/top?q=thenella%20gospel', 'icon': 'fas fa-users', 'label_en': 'Community Events', 'label_fr': 'Événements Communautaires'},
        {'url': 'https://www.facebook.com/search/top?q=thenella%20gospel', 'icon': 'fas fa-calendar-alt', 'label_en': 'Concert Announcements', 'label_fr': 'Annonces de Concerts'},
    ]

    instagram = SocialAccount(
        platform='instagram', icon='fab fa-instagram', color='#E4405F',
        description_en='Personal ministry moments and inspirational posts',
        description_fr='Moments personnels du ministère et publications inspirantes',
        sort_order=4
    )
    instagram.links = [
        {'url': 'https://www.instagram.com/explore/tags/thenella/', 'icon': 'fas fa-hashtag', 'label_en': '#ThenellaMinistries', 'label_fr': '#ThenellaMinistries'},
        {'url': 'https://www.instagram.com/explore/tags/thenella/', 'icon': 'fas fa-hashtag', 'label_en': '#CameroonianGospel', 'label_fr': '#CameroonianGospel'},
        {'url': 'https://www.instagram.com/explore/tags/thenella/', 'icon': 'fas fa-hashtag', 'label_en': '#WorshipWithThenella', 'label_fr': '#WorshipWithThenella'},
    ]

    db.session.add_all([youtube, tiktok, facebook, instagram])
    db.session.commit()
