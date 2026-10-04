/* Small, dependency-free enhancements. Navigation and content also work without JS. */
document.addEventListener('DOMContentLoaded', () => {
    const root = document.documentElement;
    const header = document.getElementById('site-header');
    const menu = document.getElementById('mobile-menu');
    const toggle = document.getElementById('menu-toggle');
    const closeButton = document.getElementById('mobile-menu-close');
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)');

    // Native dialog makes the background inert and restores focus on close.
    if (menu && toggle && typeof menu.showModal === 'function') {
        root.classList.add('js-enabled');
        const closeMenu = () => menu.close();
        toggle.addEventListener('click', () => {
            menu.showModal();
            toggle.setAttribute('aria-expanded', 'true');
            document.body.classList.add('menu-open');
            closeButton?.focus();
        });
        closeButton?.addEventListener('click', closeMenu);
        menu.addEventListener('keydown', event => {
            if (event.key !== 'Tab') return;
            const items = [...menu.querySelectorAll('a[href], button:not([disabled])')]
                .filter(element => element.getClientRects().length > 0);
            const first = items[0];
            const last = items[items.length - 1];
            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last?.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first?.focus();
            }
        });
        menu.addEventListener('close', () => {
            toggle.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('menu-open');
        });
        menu.addEventListener('click', (event) => {
            if (event.target !== menu) return;
            const rect = menu.getBoundingClientRect();
            if (event.clientX < rect.left || event.clientX > rect.right ||
                event.clientY < rect.top || event.clientY > rect.bottom) closeMenu();
        });
        menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
        window.matchMedia('(min-width: 761px)').addEventListener('change', event => {
            if (event.matches && menu.open) closeMenu();
        });
        window.addEventListener('pageshow', () => { if (menu.open) closeMenu(); });
    }

    // Passive scroll listener and a single paint per animation frame.
    let scheduled = false;
    const updateScroll = () => {
        const distance = root.scrollHeight - window.innerHeight;
        header?.classList.toggle('is-scrolled', window.scrollY > 16);
        header?.style.setProperty('--scroll-progress', distance > 0 ? Math.min(1, Math.max(0, window.scrollY / distance)) : 0);
        scheduled = false;
    };
    const scheduleScroll = () => {
        if (!scheduled) {
            scheduled = true;
            window.requestAnimationFrame(updateScroll);
        }
    };
    updateScroll();
    window.addEventListener('scroll', scheduleScroll, { passive: true });
    window.addEventListener('resize', scheduleScroll);
    window.addEventListener('load', scheduleScroll);
    document.querySelectorAll('details').forEach(details => details.addEventListener('toggle', scheduleScroll));

    if ('IntersectionObserver' in window) {
        const revealElements = document.querySelectorAll('.reveal');
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0, rootMargin: '0px 0px -32px 0px' });
        if (!motion.matches) {
            revealElements.forEach(element => {
                // Keep initially visible content stable; reveal later sections only.
                if (element.getBoundingClientRect().top >= window.innerHeight) {
                    observer.observe(element);
                    element.classList.add('reveal-ready');
                }
            });
        }
        motion.addEventListener('change', event => {
            if (event.matches) {
                observer.disconnect();
                revealElements.forEach(element => element.classList.add('is-visible'));
            }
        });
        const sectionLinks = [...document.querySelectorAll('.site-nav a')].filter(link => {
            const url = new URL(link.href);
            return url.pathname === window.location.pathname && url.hash;
        });
        const sectionObserver = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                sectionLinks.forEach(link => {
                    if (new URL(link.href).hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
                    else link.removeAttribute('aria-current');
                });
            });
        }, { rootMargin: '-15% 0px -60% 0px', threshold: 0 });
        document.querySelectorAll('.landing-page > section[id]').forEach(section => sectionObserver.observe(section));
    }
});
