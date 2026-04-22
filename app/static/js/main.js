// DOM Elements
const header = document.getElementById('header');
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

// Navigation scroll effect
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
});

// Mobile navigation toggle
if (hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.innerHTML = navLinks.classList.contains('active')
            ? '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
    });
}
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        if (navLinks) { navLinks.classList.remove('active'); if (hamburger) hamburger.innerHTML = '<i class="fas fa-bars"></i>'; }
    });
});

// ═══════════════════════════════════════════════════════════════
//  GALLERY LIGHTBOX
// ═══════════════════════════════════════════════════════════════
let lightboxIndex = 0;
const galleryCards = document.querySelectorAll('.gallery-card');
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const lightboxCaption = document.getElementById('lightbox-caption');

function openLightbox(index) {
    lightboxIndex = index;
    const card = galleryCards[index];
    if (!card) return;
    lightboxImg.src = card.querySelector('img').src;
    lightboxCaption.textContent = card.querySelector('.gallery-card-caption h3')?.textContent || '';
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

function lightboxNav(dir) {
    lightboxIndex = (lightboxIndex + dir + galleryCards.length) % galleryCards.length;
    openLightbox(lightboxIndex);
}

// Close on background click & Escape key
if (lightbox) {
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });
    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') lightboxNav(-1);
        if (e.key === 'ArrowRight') lightboxNav(1);
    });
}

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const id = this.getAttribute('href');
        if (id === '#') return;
        const el = document.querySelector(id);
        if (el) window.scrollTo({ top: el.offsetTop - 80, behavior: 'smooth' });
    });
});

// Flash messages auto-dismiss
document.querySelectorAll('.flash-msg').forEach(msg => {
    setTimeout(() => { msg.style.animation = 'slideIn 0.4s ease reverse'; setTimeout(() => msg.remove(), 400); }, 5000);
});
document.querySelectorAll('.close-flash').forEach(btn => {
    btn.addEventListener('click', () => { const m = btn.parentElement; m.style.animation = 'slideIn 0.4s ease reverse'; setTimeout(() => m.remove(), 400); });
});

// ═══════════════════════════════════════════════════════════════
//  CUSTOM MUSIC PLAYER
// ═══════════════════════════════════════════════════════════════
(function() {
    const player = document.getElementById('music-player');
    if (!player) return;

    const audio = new Audio();
    const artImg = player.querySelector('.player-art img');
    const trackTitle = player.querySelector('.player-track-info h4');
    const trackArtist = player.querySelector('.player-track-info span');
    const btnPrev = player.querySelector('.btn-prev');
    const btnNext = player.querySelector('.btn-next');
    const btnPlayPause = player.querySelector('.btn-play-pause');
    const playIcon = btnPlayPause.querySelector('i');
    const timeCurrent = player.querySelector('.time-current');
    const timeTotal = player.querySelector('.time-total');
    const progressWrap = player.querySelector('.progress-bar-wrap');
    const progressFill = player.querySelector('.progress-bar-fill');
    const volumeSlider = player.querySelector('.volume-slider');
    const volumeBtn = player.querySelector('.btn-volume');
    const closeBtn = player.querySelector('.player-close');

    let playlist = [];
    let currentIndex = -1;
    let isPlaying = false;

    // Build playlist from data attributes on music cards
    document.querySelectorAll('.music-card[data-audio]').forEach((card, i) => {
        playlist.push({
            title: card.dataset.title || 'Unknown',
            artist: 'THENELLA',
            audioUrl: card.dataset.audio,
            coverUrl: card.dataset.cover || '',
            listenUrl: card.dataset.listenUrl || ''
        });
    });

    function formatTime(s) {
        if (isNaN(s)) return '0:00';
        const m = Math.floor(s / 60);
        const sec = Math.floor(s % 60);
        return m + ':' + (sec < 10 ? '0' : '') + sec;
    }

    function loadTrack(index) {
        if (index < 0 || index >= playlist.length) return;
        currentIndex = index;
        const track = playlist[currentIndex];
        audio.src = track.audioUrl;
        artImg.src = track.coverUrl;
        trackTitle.textContent = track.title;
        trackArtist.textContent = track.artist;
        progressFill.style.width = '0%';
        timeCurrent.textContent = '0:00';
        timeTotal.textContent = '0:00';

        // Show player
        player.classList.add('active');
        document.body.classList.add('player-active');

        // Highlight active card
        document.querySelectorAll('.music-card').forEach(c => c.style.outline = 'none');
        const activeCard = document.querySelectorAll('.music-card[data-audio]')[index];
        if (activeCard) activeCard.style.outline = '3px solid var(--secondary)';
    }

    function playTrack() {
        audio.play().then(() => {
            isPlaying = true;
            playIcon.className = 'fas fa-pause';
        }).catch(() => {});
    }

    function pauseTrack() {
        audio.pause();
        isPlaying = false;
        playIcon.className = 'fas fa-play';
    }

    function togglePlay() {
        if (currentIndex === -1 && playlist.length > 0) { loadTrack(0); playTrack(); return; }
        if (isPlaying) pauseTrack(); else playTrack();
    }

    function prevTrack() {
        if (playlist.length === 0) return;
        let idx = (currentIndex - 1 + playlist.length) % playlist.length;
        loadTrack(idx);
        playTrack();
    }

    function nextTrack() {
        if (playlist.length === 0) return;
        let idx = (currentIndex + 1) % playlist.length;
        loadTrack(idx);
        playTrack();
    }

    // Events
    btnPlayPause.addEventListener('click', togglePlay);
    btnPrev.addEventListener('click', prevTrack);
    btnNext.addEventListener('click', nextTrack);

    audio.addEventListener('timeupdate', () => {
        if (audio.duration) {
            progressFill.style.width = (audio.currentTime / audio.duration * 100) + '%';
            timeCurrent.textContent = formatTime(audio.currentTime);
        }
    });

    audio.addEventListener('loadedmetadata', () => {
        timeTotal.textContent = formatTime(audio.duration);
    });

    audio.addEventListener('ended', nextTrack);

    progressWrap.addEventListener('click', (e) => {
        const rect = progressWrap.getBoundingClientRect();
        const pct = (e.clientX - rect.left) / rect.width;
        audio.currentTime = pct * audio.duration;
    });

    if (volumeSlider) {
        audio.volume = 0.7;
        volumeSlider.value = 70;
        volumeSlider.addEventListener('input', (e) => {
            audio.volume = e.target.value / 100;
            updateVolumeIcon();
        });
    }

    if (volumeBtn) {
        volumeBtn.addEventListener('click', () => {
            audio.muted = !audio.muted;
            updateVolumeIcon();
        });
    }

    function updateVolumeIcon() {
        if (!volumeBtn) return;
        const icon = volumeBtn.querySelector('i');
        if (audio.muted || audio.volume === 0) icon.className = 'fas fa-volume-mute';
        else if (audio.volume < 0.5) icon.className = 'fas fa-volume-down';
        else icon.className = 'fas fa-volume-up';
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            pauseTrack();
            player.classList.remove('active');
            document.body.classList.remove('player-active');
            document.querySelectorAll('.music-card').forEach(c => c.style.outline = 'none');
        });
    }

    // Click handlers on music cards and play buttons
    document.querySelectorAll('.music-card[data-audio] .play-overlay, .music-card[data-audio] .btn-play-track').forEach(el => {
        el.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const card = el.closest('.music-card[data-audio]');
            const idx = [...document.querySelectorAll('.music-card[data-audio]')].indexOf(card);
            if (idx === currentIndex && isPlaying) { pauseTrack(); }
            else { loadTrack(idx); playTrack(); }
        });
    });
})();
