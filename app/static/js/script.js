// script.js - Awwwards Refactor

document.addEventListener('DOMContentLoaded', () => {
    // Verificar preferência de movimento reduzido
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Inicializar GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    if (!prefersReducedMotion) {
        // 1. HERO ANIMATIONS (Load intro)
        if (document.querySelector('.hero-bg')) {
            const heroTimeline = gsap.timeline();

            heroTimeline
                .to('.hero-bg', {
                    scale: 1.1,
                    duration: 10,
                    ease: "none",
                    repeat: -1,
                    yoyo: true
                }, 0)
                .to('.fade-up', {
                    y: 0,
                    opacity: 1,
                    duration: 1,
                    stagger: 0.2,
                    ease: "power3.out"
                }, 0.5);
        }

        // 2. PARALLAX GENÉRICO
        gsap.utils.toArray('[data-speed]').forEach(el => {
            gsap.to(el, {
                y: (i, target) => -ScrollTrigger.maxScroll(window) * target.dataset.speed * 0.05,
                ease: "none",
                scrollTrigger: {
                    trigger: el,
                    start: "top bottom",
                    end: "bottom top",
                    scrub: 0
                }
            });
        });

        // 3. REVEAL SECTIONS (Fade in on scroll)
        gsap.utils.toArray('section').forEach(section => {
            const targets = section.querySelectorAll('.fade-up-scroll, .step-card, .testimonial-item, .about-text > *');

            if (targets.length > 0) {
                gsap.fromTo(targets,
                    { y: 50, opacity: 0 },
                    {
                        y: 0,
                        opacity: 1,
                        duration: 1,
                        stagger: 0.1,
                        scrollTrigger: {
                            trigger: section,
                            start: "top 75%"
                        }
                    }
                );
            }
        });

        // 4. IMAGE REVEAL ANIMATION (About Section)
        const revealContainers = document.querySelectorAll(".reveal-image");
        revealContainers.forEach((container) => {
            let image = container.querySelector("img");
            let tl = gsap.timeline({
                scrollTrigger: {
                    trigger: container,
                    start: "top 80%",
                    toggleActions: "play none none reverse"
                }
            });
            tl.from(container, { autoAlpha: 0, duration: 1.5, ease: "power2.out" })
                .from(image, { scale: 1.4, duration: 2.5, ease: "power2.out" }, "-=1.5");
        });

    } else {
        // Reduced motion: mostrar elementos fade-up imediatamente
        document.querySelectorAll('.fade-up').forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'none';
        });
    }

    // 5. STATS COUNTER (mantido independente de reduced-motion)
    const stats = document.querySelectorAll('.stat-number');
    stats.forEach(stat => {
        const target = +stat.getAttribute('data-count');

        ScrollTrigger.create({
            trigger: stat,
            start: "top 85%",
            onEnter: () => {
                if (prefersReducedMotion) {
                    stat.innerHTML = target + (target === 98 ? "%" : "+");
                } else {
                    gsap.to(stat, {
                        innerHTML: target,
                        duration: 2,
                        snap: { innerHTML: 1 },
                        modifiers: {
                            innerHTML: val => Math.floor(val) + (target === 98 ? "%" : "+")
                        }
                    });
                }
            },
            once: true
        });
    });

    // 6. HEADER MOBILE TOGGLE
    const hamburger = document.getElementById('hamburger-menu');
    const navPanel = document.getElementById('mobile-nav-panel');
    const closeBtn = document.getElementById('mobile-nav-close');

    function closeMobileMenu() {
        if (hamburger) {
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        }
        if (navPanel) navPanel.classList.remove('active');
    }

    function openMobileMenu() {
        hamburger.classList.add('active');
        hamburger.setAttribute('aria-expanded', 'true');
        navPanel.classList.add('active');
    }

    if (hamburger && navPanel) {
        // Abrir/fechar ao clicar no hamburguer
        hamburger.addEventListener('click', () => {
            const isOpen = navPanel.classList.contains('active');
            isOpen ? closeMobileMenu() : openMobileMenu();
        });

        // Fechar ao clicar no botão ×
        if (closeBtn) {
            closeBtn.addEventListener('click', closeMobileMenu);
        }

        // Fechar ao clicar em qualquer link do painel
        navPanel.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMobileMenu);
        });

        // Fechar ao clicar fora do painel (na overlay)
        document.addEventListener('click', (e) => {
            if (navPanel.classList.contains('active') &&
                !navPanel.contains(e.target) &&
                !hamburger.contains(e.target)) {
                closeMobileMenu();
            }
        });
    }

    // 7. ACTIVE NAV LINK — marcar link ativo na sidebar e adicionar aria-current
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-nav ul a');

    sidebarLinks.forEach(link => {
        const linkPath = new URL(link.href, window.location.origin).pathname;
        // Verificar correspondência exata (ex: /blog, /eventos) ou homepage
        const isActive = linkPath === currentPath ||
            (currentPath === '/' && linkPath === '/');

        if (isActive && linkPath !== '/') {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });
});