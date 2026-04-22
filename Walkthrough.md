# Walkthrough: THENELLA Static → Dynamic Flask Conversion

## What Was Done

Converted the single-file static HTML website (`thella2.html`) for **THENELLA** (Cameroonian Gospel Artist) into a fully dynamic **Flask 3.1 + Flask-SQLAlchemy** web application.

## Project Structure Created

```
thella2/
├── app.py                          # Entry point (port 5001)
├── config.py                       # Config (SQLite, uploads, secret key)
├── requirements.txt                # Dependencies
├── instance/thenella.db            # SQLite database (auto-created)
├── app/
│   ├── __init__.py                 # App factory
│   ├── models.py                   # 8 models + seed_database()
│   ├── forms.py                    # WTForms for admin & booking
│   ├── main/                       # Public blueprint
│   │   ├── __init__.py
│   │   └── routes.py               # /, /contact, /lang/<lang>
│   ├── admin/                      # Admin blueprint
│   │   ├── __init__.py
│   │   └── routes.py               # Full CRUD for all content
│   ├── static/
│   │   ├── css/style.css           # Extracted original styles
│   │   ├── js/main.js              # Extracted original scripts
│   │   └── uploads/seed/           # Original .webp images
│   └── templates/
│       ├── base.html               # Base template
│       ├── index.html              # Public page (all sections)
│       └── admin/                  # 12 admin templates
```

## Database Models

| Model | Purpose |
|-------|---------|
| `AdminUser` | Admin authentication (login/logout) |
| `SiteSettings` | Hero section & footer config (EN/FR) |
| `Biography` | Bio text + photo (EN/FR) |
| `Achievement` | Achievement cards with icons |
| `Album` | Discography with cover images |
| `GalleryImage` | Gallery slider images |
| `SocialAccount` | Social media cards with nested links (JSON) |
| `BookingRequest` | Contact form submissions |

## Key Features

- **All content is database-driven** — editable via admin panel
- **Admin panel** at `/admin/` with sidebar navigation
- **Contact form saves to DB** instead of just `alert()`
- **Cookie-based language switching** (EN/FR) — persists across visits
- **Image uploads** for gallery, albums, biography, hero
- **CSRF protection** on all forms
- **Flash messages** for user feedback
- **Fixed hero image** (was using hardcoded `C:\Users\STABY\...` path)

## Design Preservation

✅ Same CSS variables, fonts, colors, animations, hover effects, responsive breakpoints — exact visual match to the original static site.

## Credentials

- **Admin URL**: http://127.0.0.1:5001/admin/login
- **Username**: `admin`
- **Password**: `thenella2026`

## Verification

- Server runs on `http://127.0.0.1:5001`
- All routes return HTTP 200
- All images load correctly (304 from cache)
- Admin login page renders correctly
