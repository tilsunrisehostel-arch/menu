/* Progressive enhancement only — the menu is fully readable with JS disabled.
   Highlights the section chip you are currently scrolled to and keeps it in view. */
(function () {
  'use strict';

  var nav = document.querySelector('.sectionnav');
  if (!nav || !('IntersectionObserver' in window)) return;

  var scroller = nav.querySelector('.sectionnav__scroll');
  var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'));
  if (!links.length) return;

  var linkFor = {};
  var sections = [];

  links.forEach(function (link) {
    var id = decodeURIComponent(link.getAttribute('href').slice(1));
    var section = document.getElementById(id);
    if (!section) return;
    linkFor[id] = link;
    sections.push(section);
  });
  if (!sections.length) return;

  var visible = new Set();
  var current = null;

  function setActive(id) {
    if (id === current) return;
    current = id;
    links.forEach(function (link) { link.classList.remove('is-active'); });

    var link = linkFor[id];
    if (!link) return;
    link.classList.add('is-active');

    // Keep the active chip inside the horizontal strip without scrolling the page.
    if (!scroller || scroller.scrollWidth <= scroller.clientWidth) return;
    var target = link.offsetLeft - (scroller.clientWidth - link.offsetWidth) / 2;
    var max = scroller.scrollWidth - scroller.clientWidth;
    scroller.scrollTo({
      left: Math.max(0, Math.min(target, max)),
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
    });
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) visible.add(entry.target);
        else visible.delete(entry.target);
      });

      if (!visible.size) return;
      // Topmost section currently on screen wins.
      var top = null;
      visible.forEach(function (section) {
        if (!top || section.offsetTop < top.offsetTop) top = section;
      });
      if (top) setActive(top.id);
    },
    { rootMargin: '-30% 0px -55% 0px', threshold: 0 }
  );

  sections.forEach(function (section) { observer.observe(section); });
})();
