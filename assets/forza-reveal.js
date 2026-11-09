(function () {
  // No actuar dentro del editor del tema ni si el usuario prefiere menos movimiento
  if (window.Shopify && Shopify.designMode) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) return;

  function init() {
    // La primera sección (slideshow) no se anima
    var sections = /** @type {HTMLElement[]} */ ([].slice.call(document.querySelectorAll('main .shopify-section, #MainContent > *')).slice(1));
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('fz-in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08 });

    sections.forEach(function (s) {
      if (s.getBoundingClientRect().top < window.innerHeight) return; // ya visible al cargar
      s.classList.add('fz-reveal');
      io.observe(s);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();