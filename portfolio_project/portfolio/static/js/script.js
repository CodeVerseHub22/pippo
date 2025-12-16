/* ============================================
   MODERN DARK PORTFOLIO - JAVASCRIPT
   Premium Interactions & Animations
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // PARTICLE ANIMATION SYSTEM
    // ============================================
    const particleCanvas = document.getElementById('particleCanvas');
    if (particleCanvas) {
        const ctx = particleCanvas.getContext('2d');
        let particles = [];
        let animationId;
        
        function resizeCanvas() {
            particleCanvas.width = window.innerWidth;
            particleCanvas.height = window.innerHeight;
        }
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        class Particle {
            constructor() {
                this.x = Math.random() * particleCanvas.width;
                this.y = Math.random() * particleCanvas.height;
                this.size = Math.random() * 2 + 0.5;
                this.speedX = (Math.random() - 0.5) * 0.5;
                this.speedY = (Math.random() - 0.5) * 0.5;
                this.opacity = Math.random() * 0.5 + 0.2;
                this.color = Math.random() > 0.5 ? '#00d4ff' : '#7c3aed';
            }
            
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                
                if (this.x > particleCanvas.width) this.x = 0;
                if (this.x < 0) this.x = particleCanvas.width;
                if (this.y > particleCanvas.height) this.y = 0;
                if (this.y < 0) this.y = particleCanvas.height;
            }
            
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = this.opacity;
                ctx.fill();
                ctx.globalAlpha = 1;
            }
        }
        
        function initParticles() {
            particles = [];
            const particleCount = Math.min(100, Math.floor(window.innerWidth / 15));
            for (let i = 0; i < particleCount; i++) {
                particles.push(new Particle());
            }
        }
        
        function connectParticles() {
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < 150) {
                        ctx.beginPath();
                        ctx.strokeStyle = '#00d4ff';
                        ctx.globalAlpha = 0.1 * (1 - distance / 150);
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                        ctx.globalAlpha = 1;
                    }
                }
            }
        }
        
        function animateParticles() {
            ctx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
            
            particles.forEach(particle => {
                particle.update();
                particle.draw();
            });
            
            connectParticles();
            animationId = requestAnimationFrame(animateParticles);
        }
        
        initParticles();
        animateParticles();
        
        // Mouse interaction
        let mouse = { x: null, y: null };
        document.addEventListener('mousemove', function(e) {
            mouse.x = e.x;
            mouse.y = e.y;
            
            particles.forEach(particle => {
                const dx = mouse.x - particle.x;
                const dy = mouse.y - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 100) {
                    const angle = Math.atan2(dy, dx);
                    particle.x -= Math.cos(angle) * 2;
                    particle.y -= Math.sin(angle) * 2;
                }
            });
        });
    }
    
    // ============================================
    // TYPING EFFECT
    // ============================================
    const typingElement = document.querySelector('.typing-text');
    if (typingElement) {
        const words = JSON.parse(typingElement.dataset.words || '["Developer", "Designer", "Creator"]');
        let wordIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typeSpeed = 100;
        
        function typeEffect() {
            const currentWord = words[wordIndex];
            
            if (isDeleting) {
                typingElement.textContent = currentWord.substring(0, charIndex - 1);
                charIndex--;
                typeSpeed = 50;
            } else {
                typingElement.textContent = currentWord.substring(0, charIndex + 1);
                charIndex++;
                typeSpeed = 100;
            }
            
            if (!isDeleting && charIndex === currentWord.length) {
                isDeleting = true;
                typeSpeed = 2000; // Pause at end
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                typeSpeed = 500; // Pause before next word
            }
            
            setTimeout(typeEffect, typeSpeed);
        }
        
        setTimeout(typeEffect, 1000);
    }
    
    // ============================================
    // SCROLL ANIMATIONS
    // ============================================
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Trigger counter animation if present
                const counter = entry.target.querySelector('[data-count]');
                if (counter && !counter.classList.contains('counted')) {
                    animateCounter(counter);
                }
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        scrollObserver.observe(el);
    });
    
    // ============================================
    // COUNTER ANIMATION
    // ============================================
    function animateCounter(element) {
        element.classList.add('counted');
        const target = parseInt(element.dataset.count);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        function updateCounter() {
            current += step;
            if (current < target) {
                element.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target + '+';
            }
        }
        
        updateCounter();
    }
    
    // Also observe stat values directly
    document.querySelectorAll('.stat-value[data-count]').forEach(el => {
        const parent = el.closest('.animate-on-scroll');
        if (!parent) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !el.classList.contains('counted')) {
                        animateCounter(el);
                    }
                });
            }, observerOptions);
            observer.observe(el);
        }
    });
    
    // ============================================
    // NAVBAR SCROLL EFFECT
    // ============================================
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (navbar) {
            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            
            // Hide/show on scroll direction
            if (currentScroll > lastScroll && currentScroll > 200) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
        }
        
        lastScroll = currentScroll;
    });
    
    // ============================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ============================================
    // SKILL BARS ANIMATION
    // ============================================
    const skillBars = document.querySelectorAll('.progress-bar');
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Get width from data-width attribute
                const targetWidth = entry.target.dataset.width;
                if (targetWidth) {
                    entry.target.style.width = '0%';
                    setTimeout(() => {
                        entry.target.style.width = targetWidth + '%';
                    }, 100);
                }
                skillObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    skillBars.forEach(bar => skillObserver.observe(bar));
    
    // ============================================
    // FORM INTERACTIONS
    // ============================================
    const formInputs = document.querySelectorAll('.form-input');
    
    formInputs.forEach(input => {
        // Add focus class on parent
        input.addEventListener('focus', function() {
            this.closest('.input-wrapper').classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.closest('.input-wrapper').classList.remove('focused');
            if (this.value) {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
        
        // Check on load
        if (input.value) {
            input.classList.add('has-value');
        }
    });
    
    // ============================================
    // PROJECT CARDS TILT EFFECT
    // ============================================
    const projectCards = document.querySelectorAll('.project-card-modern');
    
    projectCards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });
        
        card.addEventListener('mouseleave', function() {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });
    
    // ============================================
    // MOBILE NAV TOGGLE
    // ============================================
    const navToggle = document.querySelector('.navbar-toggler');
    const navMenu = document.querySelector('.navbar-collapse');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            document.body.classList.toggle('nav-open');
        });
        
        // Close on link click
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                document.body.classList.remove('nav-open');
                navMenu.classList.remove('show');
            });
        });
    }
    
    // ============================================
    // GLOW CURSOR EFFECT
    // ============================================
    const cursor = document.createElement('div');
    cursor.classList.add('glow-cursor');
    document.body.appendChild(cursor);
    
    let cursorX = 0, cursorY = 0;
    let targetX = 0, targetY = 0;
    
    document.addEventListener('mousemove', (e) => {
        targetX = e.clientX;
        targetY = e.clientY;
    });
    
    function animateCursor() {
        cursorX += (targetX - cursorX) * 0.1;
        cursorY += (targetY - cursorY) * 0.1;
        
        cursor.style.left = cursorX + 'px';
        cursor.style.top = cursorY + 'px';
        
        requestAnimationFrame(animateCursor);
    }
    
    animateCursor();
    
    // Cursor effects on interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .project-card-modern, .skill-category-card');
    
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.classList.add('cursor-hover');
        });
        
        el.addEventListener('mouseleave', () => {
            cursor.classList.remove('cursor-hover');
        });
    });
    
    // ============================================
    // PARALLAX EFFECT ON FLOATING SHAPES
    // ============================================
    const shapes = document.querySelectorAll('.floating-shape');
    
    window.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        shapes.forEach((shape, index) => {
            const speed = (index + 1) * 20;
            const moveX = (x - 0.5) * speed;
            const moveY = (y - 0.5) * speed;
            
            shape.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    });
    
    // ============================================
    // LAZY LOADING IMAGES
    // ============================================
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
    
    // ============================================
    // TESTIMONIALS CAROUSEL - DISABLED (showing all cards in grid)
    // ============================================
    // Carousel functionality disabled to show all testimonials at once
    
    // ============================================
    // LOADING SCREEN
    // ============================================
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
        
        const loader = document.querySelector('.page-loader');
        if (loader) {
            setTimeout(() => {
                loader.classList.add('hidden');
                setTimeout(() => loader.remove(), 500);
            }, 500);
        }
    });
    
    // ============================================
    // SCROLL TO TOP BUTTON
    // ============================================
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.classList.add('scroll-top-btn');
    scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(scrollTopBtn);
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 500) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    });
    
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // ============================================
    // MAGNETIC BUTTONS
    // ============================================
    const magneticBtns = document.querySelectorAll('.btn-glow, .submit-btn');
    
    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', function(e) {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
        });
        
        btn.addEventListener('mouseleave', function() {
            btn.style.transform = '';
        });
    });
    
    // ============================================
    // PREFERS REDUCED MOTION
    // ============================================
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    if (prefersReducedMotion.matches) {
        // Disable animations
        document.documentElement.style.setProperty('--animation-duration', '0.01s');
        
        // Stop particle animation
        if (typeof animationId !== 'undefined') {
            cancelAnimationFrame(animationId);
        }
    }
    
    console.log('🚀 Portfolio initialized successfully!');
});

// ============================================
// UTILITY FUNCTIONS
// ============================================

function debounce(func, wait = 100) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function throttle(func, limit = 100) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
