document.addEventListener("DOMContentLoaded", () => {
  // --- CÓDIGO DO MENU HAMBÚRGUER ---
  const hamburger = document.getElementById("hamburger-menu");
  const navLinks = document.getElementById("nav-links");
  const allNavLinks = document.querySelectorAll(".nav-links a"); // Pega todos os links do menu

  // Função para abrir/fechar o menu
  function toggleMenu() {
    navLinks.classList.toggle("active");
    hamburger.classList.toggle("active"); // Também adiciona a classe ao ícone para animá-lo
  }

  // Adiciona o evento de clique ao botão hambúrguer
  if (hamburger) {
    hamburger.addEventListener("click", toggleMenu);
  }

  // Adiciona o evento de clique a CADA link do menu para fechá-lo após o clique
  allNavLinks.forEach((link) => {
    link.addEventListener("click", () => {
      // Se o menu estiver aberto, feche-o
      if (navLinks.classList.contains("active")) {
        toggleMenu();
      }
    });
  });

  // --- CÓDIGO DO SCROLL SUAVE (se você ainda o tiver) ---
  const menuLinksWithHash = document.querySelectorAll('a[href^="#"]');
  menuLinksWithHash.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      const targetSection = document.querySelector(targetId);
      if (targetSection) {
        window.scrollTo({
          top: targetSection.offsetTop - 70, // Desconto para a altura do header
          behavior: "smooth",
        });
      }
    });
  });
});
