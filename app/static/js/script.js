document.addEventListener('DOMContentLoaded', () => {

    // --- LÓGICA DA SIDEBAR ATIVA (DESKTOP) ---
    const sections = document.querySelectorAll('.main-content .full-screen-section');
    const navLinks = document.querySelectorAll('.sidebar-nav a[data-section]');

    if (sections.length > 0 && navLinks.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.5
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    navLinks.forEach(link => link.classList.remove('active'));
                    const sectionId = entry.target.id;
                    const activeLink = document.querySelector(`.sidebar-nav a[data-section="${sectionId}"]`);
                    if (activeLink) activeLink.classList.add('active');
                }
            });
        }, observerOptions);

        sections.forEach(section => observer.observe(section));
    }

    // --- SMOOTH SCROLL para links internos (sidebar e mobile) ---
    const allLinks = document.querySelectorAll('.sidebar-nav a[data-section], .mobile-nav-panel a');
    allLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) { // só scroll para links internos
                e.preventDefault();
                const targetSection = document.querySelector(href);
                if (targetSection) {
                    targetSection.scrollIntoView({ behavior: 'smooth' });
                }
            }
            // links externos continuam funcionando normalmente
        });
    });

    // --- LÓGICA DO MENU HAMBÚRGUER (MOBILE) ---
    const hamburger = document.getElementById('hamburger-menu');
    const mobileNavPanel = document.getElementById('mobile-nav-panel');
    const mobileOverlay = document.getElementById('mobile-overlay');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-panel a');

    if (hamburger && mobileNavPanel && mobileOverlay) {
        function toggleMenu() {
            const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
            hamburger.setAttribute('aria-expanded', !isExpanded);
            hamburger.classList.toggle('active');
            mobileNavPanel.classList.toggle('active');
            mobileOverlay.classList.toggle('active');
        }

        // Clique no hambúrguer
        hamburger.addEventListener('click', toggleMenu);

        // Clique no overlay fecha o menu
        mobileOverlay.addEventListener('click', toggleMenu);

        // Fecha o menu ao clicar em qualquer link mobile
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (mobileNavPanel.classList.contains('active')) toggleMenu();
            });
        });
    }

});