document.addEventListener('DOMContentLoaded', () => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const siteHeader = document.getElementById('site-header');
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuClose = document.getElementById('mobile-menu-close');
    const mobileMenuLinks = mobileMenu ? mobileMenu.querySelectorAll('a') : [];
    const sectionElements = document.querySelectorAll('.landing-page > .hero, .landing-page > .section');

    const setViewportHeightVariable = () => {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--app-vh', `${vh}px`);
    };

    setViewportHeightVariable();
    window.addEventListener('resize', setViewportHeightVariable);

    const setHeaderState = () => {
        if (!siteHeader) {
            return;
        }

        if (window.scrollY > 12) {
            siteHeader.classList.add('is-scrolled');
        } else {
            siteHeader.classList.remove('is-scrolled');
        }
    };

    setHeaderState();
    window.addEventListener('scroll', setHeaderState, { passive: true });

    const closeMenu = () => {
        if (!menuToggle || !mobileMenu) {
            return;
        }

        menuToggle.classList.remove('is-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileMenu.classList.remove('is-open');
        mobileMenu.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    };

    const openMenu = () => {
        if (!menuToggle || !mobileMenu) {
            return;
        }

        menuToggle.classList.add('is-open');
        menuToggle.setAttribute('aria-expanded', 'true');
        mobileMenu.classList.add('is-open');
        mobileMenu.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    };

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', () => {
            if (mobileMenu.classList.contains('is-open')) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        mobileMenu.addEventListener('click', (event) => {
            if (event.target === mobileMenu) {
                closeMenu();
            }
        });
    }

    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', closeMenu);
    }

    mobileMenuLinks.forEach((link) => {
        link.addEventListener('click', closeMenu);
    });

    const navLinks = document.querySelectorAll('.site-nav a, .mobile-menu__nav a');
    const currentPath = window.location.pathname;

    navLinks.forEach((link) => {
        const linkUrl = new URL(link.href, window.location.origin);
        if (linkUrl.pathname === currentPath && !linkUrl.hash) {
            link.setAttribute('aria-current', 'page');
        }
    });

    const scrollToHashTarget = (hashValue) => {
        const target = document.querySelector(hashValue);
        if (!target) {
            return;
        }

        const headerHeight = siteHeader ? siteHeader.getBoundingClientRect().height : 0;
        const targetTop = target.getBoundingClientRect().top + window.scrollY - headerHeight - 10;

        window.scrollTo({
            top: targetTop,
            behavior: prefersReducedMotion ? 'auto' : 'smooth'
        });
    };

    navLinks.forEach((link) => {
        const linkUrl = new URL(link.href, window.location.origin);
        const isSamePageHash = linkUrl.pathname === window.location.pathname && !!linkUrl.hash;

        if (!isSamePageHash) {
            return;
        }

        link.addEventListener('click', (event) => {
            event.preventDefault();
            scrollToHashTarget(linkUrl.hash);
            closeMenu();
            history.replaceState(null, '', linkUrl.hash);
        });
    });

    if (window.location.hash) {
        setTimeout(() => {
            scrollToHashTarget(window.location.hash);
        }, 10);
    }

    if (sectionElements.length > 0) {
        sectionElements.forEach((section) => section.classList.add('section-transition'));

        if (!prefersReducedMotion) {
            const sectionObserver = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-inview');
                    } else {
                        entry.target.classList.remove('is-inview');
                    }
                });
            }, {
                threshold: 0.45
            });

            sectionElements.forEach((section) => sectionObserver.observe(section));
        } else {
            sectionElements.forEach((section) => section.classList.add('is-inview'));
        }
    }

    if (!prefersReducedMotion) {
        const revealElements = document.querySelectorAll('.reveal');
        if (revealElements.length > 0) {
            const revealObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.2 });

            revealElements.forEach((el) => revealObserver.observe(el));
        }
    } else {
        document.querySelectorAll('.reveal').forEach((el) => el.classList.add('is-visible'));
    }

    const counterElements = document.querySelectorAll('.counter[data-count]');
    if (counterElements.length > 0) {
        const animateCounter = (el) => {
            const rawValue = Number(el.dataset.count || 0);
            if (!Number.isFinite(rawValue)) {
                return;
            }

            if (prefersReducedMotion) {
                el.textContent = rawValue + (rawValue === 98 ? '%' : '+');
                return;
            }

            const duration = 1100;
            const start = performance.now();
            const step = (timestamp) => {
                const progress = Math.min((timestamp - start) / duration, 1);
                const value = Math.floor(progress * rawValue);
                el.textContent = value + (rawValue === 98 ? '%' : '+');
                if (progress < 1) {
                    requestAnimationFrame(step);
                }
            };
            requestAnimationFrame(step);
        };

        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counterElements.forEach((counter) => counterObserver.observe(counter));
    }
});