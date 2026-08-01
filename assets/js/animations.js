(function () {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function initNavbarScroll() {
    const navbar = document.getElementById("navbar");
    if (!navbar) return;

    const toggleScrolled = () => {
      navbar.classList.toggle("navbar-scrolled", window.scrollY > 12);
    };

    toggleScrolled();
    window.addEventListener("scroll", toggleScrolled, { passive: true });
  }

  function initRevealOnScroll() {
    const selectors = [
      ".post-header",
      ".profile img",
      ".post article > h2",
      ".post article > h3",
      ".pub-section-heading",
      ".publications ol.bibliography > li",
      ".research-impact-metrics",
      ".research-impact-metric",
      ".teaching-materials-gate",
      ".social .contact-icons a",
    ];

    const elements = [];
    selectors.forEach((selector) => {
      document.querySelectorAll(selector).forEach((element) => {
        element.classList.add("reveal-on-scroll");
        elements.push(element);
      });
    });

    document.querySelectorAll(".publications ol.bibliography > li").forEach((element, index) => {
      element.style.setProperty("--reveal-delay", `${Math.min(index * 40, 400)}ms`);
    });

    document.querySelectorAll(".research-impact-metric").forEach((element, index) => {
      element.style.setProperty("--reveal-delay", `${index * 70}ms`);
    });

    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      elements.forEach((element) => element.classList.add("is-visible"));
      initMetricCounters(true);
      return;
    }

    const markVisible = (element) => {
      element.classList.add("is-visible");
      if (element.classList.contains("research-impact-metrics")) {
        initMetricCounters(false);
      }
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          markVisible(entry.target);
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -5% 0px" },
    );

    elements.forEach((element) => {
      const rect = element.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.92 && rect.bottom > 0) {
        markVisible(element);
        return;
      }
      observer.observe(element);
    });
  }

  function animateCount(element, target, suffix, duration) {
    const start = performance.now();
    const from = 0;

    function frame(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.round(from + (target - from) * eased);
      element.textContent = `${value}${suffix || ""}`;

      if (progress < 1) {
        requestAnimationFrame(frame);
      }
    }

    requestAnimationFrame(frame);
  }

  function initMetricCounters(instant) {
    document.querySelectorAll("[data-count]").forEach((element) => {
      if (element.dataset.counted === "true") return;

      const target = parseInt(element.dataset.count, 10);
      const suffix = element.dataset.suffix || "";
      if (Number.isNaN(target)) return;

      element.dataset.counted = "true";

      if (instant || prefersReducedMotion) {
        element.textContent = `${target}${suffix}`;
        return;
      }

      animateCount(element, target, suffix, 1200);
    });
  }

  function initSmoothAnchors() {
    if (prefersReducedMotion) return;

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", (event) => {
        const id = anchor.getAttribute("href");
        if (!id || id === "#") return;

        const target = document.querySelector(id);
        if (!target) return;

        event.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  function init() {
    initNavbarScroll();
    initRevealOnScroll();
    initSmoothAnchors();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
