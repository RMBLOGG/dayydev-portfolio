/* === LOADER === */
window.addEventListener('load', () => {
  setTimeout(() => { document.getElementById('loader').classList.add('hidden'); }, 1600);
});

/* === PARTICLES === */
const particlesEl = document.getElementById('particles');
for (let i = 0; i < 40; i++) {
  const p = document.createElement('div');
  p.className = 'particle';
  p.style.cssText = `left:${Math.random()*100}%;animation-duration:${6+Math.random()*14}s;animation-delay:${Math.random()*12}s;width:${1+Math.random()*3}px;height:${1+Math.random()*3}px;background:${Math.random()>.5?'#a78bfa':'#ff6b9d'};opacity:${0.2+Math.random()*0.6};`;
  particlesEl.appendChild(p);
}

/* === SAKURA PETALS === */
const sakuraEl = document.getElementById('sakura');
for (let i = 0; i < 18; i++) {
  const petal = document.createElement('div');
  petal.className = 'petal';
  petal.style.cssText = `left:${Math.random()*100}%;animation-duration:${8+Math.random()*14}s;animation-delay:${Math.random()*15}s;transform:scale(${0.5+Math.random()});`;
  sakuraEl.appendChild(petal);
}

/* === SCROLL REVEAL === */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right').forEach((el, i) => {
  const siblings = Array.from(el.parentElement.children).filter(c =>
    c.classList.contains('reveal-up') || c.classList.contains('reveal-left') || c.classList.contains('reveal-right')
  );
  const idx = siblings.indexOf(el);
  el.style.transitionDelay = (idx * 0.09) + 's';
  revealObserver.observe(el);
});

/* === COUNTER === */
function animateCounter(el) {
  const target = parseInt(el.dataset.target);
  const dur = 1500;
  const start = performance.now();
  const tick = (now) => {
    const p = Math.min((now - start) / dur, 1);
    const e = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.floor(e * target).toLocaleString();
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
const statsObs = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    document.querySelectorAll('.stat-num').forEach(animateCounter);
    statsObs.disconnect();
  }
}, { threshold: 0.5 });
const sb = document.querySelector('.stats-bar');
if (sb) statsObs.observe(sb);

/* === SKILL BARS === */
const skillObs = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    document.querySelectorAll('.skill-fill').forEach(bar => {
      setTimeout(() => { bar.style.width = bar.dataset.width + '%'; }, 400);
    });
    skillObs.disconnect();
  }
}, { threshold: 0.3 });
const ac = document.querySelector('.about-card');
if (ac) skillObs.observe(ac);

/* === NAVBAR === */
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 60) {
    navbar.style.background = 'rgba(5,5,16,0.97)';
    navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.5)';
  } else {
    navbar.style.background = 'rgba(5,5,16,0.8)';
    navbar.style.boxShadow = 'none';
  }
}, { passive: true });

/* === ACTIVE NAV LINK === */
const navLinks = document.querySelectorAll('.nav-links a');
const navObs = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + entry.target.id) link.classList.add('active');
      });
    }
  });
}, { threshold: 0.4 });
document.querySelectorAll('section[id]').forEach(s => navObs.observe(s));

/* === CARD TILT === */
document.querySelectorAll('.project-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    card.style.transform = `translateY(-6px) rotateX(${-y*5}deg) rotateY(${x*5}deg)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
  });
});

/* === SMOOTH SCROLL === */
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
  });
});

/* === CURSOR GLOW (desktop only) === */
if (window.innerWidth > 768) {
  const glow = document.createElement('div');
  glow.style.cssText = 'position:fixed;pointer-events:none;z-index:9998;width:350px;height:350px;border-radius:50%;background:radial-gradient(circle,rgba(255,107,157,0.04),transparent 70%);transform:translate(-50%,-50%);transition:left 0.1s,top 0.1s;';
  document.body.appendChild(glow);
  document.addEventListener('mousemove', e => {
    glow.style.left = e.clientX + 'px';
    glow.style.top = e.clientY + 'px';
  });
}

/* === NAV ACTIVE STYLE === */
const style = document.createElement('style');
style.textContent = '.nav-links a.active { color: var(--pink) !important; }';
document.head.appendChild(style);
