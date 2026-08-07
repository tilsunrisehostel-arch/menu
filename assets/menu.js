/* Mejora progresiva: el menú se lee perfectamente con JavaScript desactivado.
   Esto solo resalta el botón de la sección que estás mirando y lo mantiene
   a la vista dentro de la barra que se desplaza. */
(function () {
  'use strict';

  var nav = document.querySelector('.sectionnav');
  if (!nav) return;

  var scroller = nav.querySelector('.sectionnav__scroll');
  var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'));
  if (!links.length) return;

  var entries = [];
  links.forEach(function (link) {
    var section = document.getElementById(decodeURIComponent(link.getAttribute('href').slice(1)));
    if (section) entries.push({ link: link, section: section });
  });
  if (!entries.length) return;

  var current = null;
  var smooth = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setActive(entry) {
    if (entry.link === current) return;
    current = entry.link;

    links.forEach(function (link) {
      var on = link === entry.link;
      link.classList.toggle('is-active', on);
      if (on) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });

    // Centrar el botón activo dentro de la tira horizontal, sin mover la página.
    // Se mide con rectángulos y no con offsetLeft, que depende del ancestro
    // posicionado y aquí daría una referencia equivocada.
    if (!scroller || scroller.scrollWidth <= scroller.clientWidth) return;
    var linkBox = entry.link.getBoundingClientRect();
    var boxScroller = scroller.getBoundingClientRect();
    var delta = (linkBox.left - boxScroller.left) - (boxScroller.width - linkBox.width) / 2;
    var max = scroller.scrollWidth - scroller.clientWidth;
    scroller.scrollTo({
      left: Math.max(0, Math.min(scroller.scrollLeft + delta, max)),
      behavior: smooth ? 'smooth' : 'auto'
    });
  }

  function update() {
    var doc = document.documentElement;

    // Al llegar al final de la página gana siempre la última sección: si no,
    // la anterior se queda marcada porque ya no se puede desplazar más.
    if (window.innerHeight + window.scrollY >= doc.scrollHeight - 4) {
      setActive(entries[entries.length - 1]);
      return;
    }

    // Línea imaginaria al 30% de la altura de la pantalla: la sección activa es
    // la última cuyo comienzo ya la ha cruzado. Se compara en coordenadas de
    // pantalla, porque offsetTop se mide contra <main> y no contra el documento.
    var line = window.innerHeight * 0.3;
    var found = entries[0];
    for (var i = 0; i < entries.length; i++) {
      if (entries[i].section.getBoundingClientRect().top <= line) found = entries[i];
    }
    setActive(found);
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      ticking = false;
      update();
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();
})();
