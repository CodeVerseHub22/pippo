/**
 * PREMIUM PORTFOLIO INTERACTION ENGINE
 * Scroll Animations | Interaction Effects | Performance Optimized
 */

document.addEventListener('DOMContentLoaded', () => {

    // 1. Navbar Scroll Effect
    window.addEventListener('scroll', () => {
        const nav = document.getElementById('navbar');
        if (nav && window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else if (nav) {
            nav.classList.remove('scrolled');
        }
    });

    // 2. Intersection Observer for Scroll Animations
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Apply observer to all animated elements
    const animatedElements = document.querySelectorAll('[data-animate]');
    animatedElements.forEach(el => animationObserver.observe(el));

    // 3. Performance: Lazy loading images with fade-in
    const lazyImages = document.querySelectorAll('img');
    const imgOptions = { threshold: 0, rootMargin: '0px 0px 200px 0px' };

    const imgObserver = new IntersectionObserver((entries, self) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.style.opacity = '1';
                self.unobserve(img);
            }
        });
    }, imgOptions);

    lazyImages.forEach(img => {
        img.style.transition = 'opacity 1s ease-in-out';
        img.style.opacity = '0';
        imgObserver.observe(img);
    });

    // 4. Smooth Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // 5. Parallax effect for Hero Blob (Gentle movement)
    const heroBlob = document.querySelector('.hero-blob');
    if (heroBlob) {
        window.addEventListener('mousemove', (e) => {
            const { clientX, clientY } = e;
            const moveX = (clientX - window.innerWidth / 2) * 0.01;
            const moveY = (clientY - window.innerHeight / 2) * 0.01;
            heroBlob.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    }

    // 6. Set progress bar widths from data attributes
    const progressBars = document.querySelectorAll('.progress-bar-custom[data-width], .skill-bar-fill[data-width]');
    
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.getAttribute('data-width');
                setTimeout(() => {
                    bar.style.width = `${width}%`;
                }, 100);
                progressObserver.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => {
        bar.style.width = '0%';
        progressObserver.observe(bar);
    });

    // 7. Form Handling Feedback
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', () => {
            const btn = contactForm.querySelector('button');
            if (btn) {
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Invio in corso...';
                btn.style.opacity = '0.7';
                btn.style.pointerEvents = 'none';
            }
        });
    }

    // 8. Chiudi navbar hamburger se clicchi fuori
    document.addEventListener('click', function (e) {
        const navbarCollapse = document.querySelector('.navbar-collapse');
        const navbarToggler = document.querySelector('.navbar-toggler');
        if (
            navbarCollapse &&
            navbarCollapse.classList.contains('show') &&
            !navbarCollapse.contains(e.target) &&
            !navbarToggler.contains(e.target)
        ) {
            const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
            if (bsCollapse) {
                bsCollapse.hide();
            }
        }
    });
});
