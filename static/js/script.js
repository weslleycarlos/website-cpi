document.addEventListener('DOMContentLoaded', () => {
    // Seleciona todos os links do menu que começam com '#'
    const menuLinks = document.querySelectorAll('nav a[href^="#"]');

    function smoothScroll(event) {
        event.preventDefault();
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        window.scrollTo({
            top: targetSection.offsetTop - 70, // -70 para compensar a altura do header
            behavior: 'smooth'
        });
    }

    menuLinks.forEach(link => {
        link.addEventListener('click', smoothScroll);
    });

     const hamburger = document.getElementById('hamburger-menu');
    const navLinks = document.getElementById('nav-links');

    hamburger.addEventListener('click', () => {
        // Adiciona ou remove a classe 'active' na lista de links
        navLinks.classList.toggle('active');
    });
    
});

