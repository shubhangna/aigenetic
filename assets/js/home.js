/* Homepage: aurora field, liquid-glass pointer light, scroll reveal,
   mobile menu, and the original-demo waveform players.
   Booking stays in the page's own openCalendarModalMain / closeCalendarModalMain. */
(function () {
  var root = document.getElementById("root");
  if (!root) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  var glassOk = false;
  try {
    glassOk = CSS.supports("backdrop-filter", "blur(4px)") || CSS.supports("-webkit-backdrop-filter", "blur(4px)");
  } catch (err) {
    glassOk = false;
  }
  if (!glassOk) document.documentElement.classList.add("no-glass");

  var aurora = document.getElementById("aurora");
  if (aurora && aurora.getContext) {
    var actx = aurora.getContext("2d");
    var particles = [];
    var pointer = { x: 0.62, y: 0.28 };
    var pointerTarget = { x: 0.62, y: 0.28 };
    var scrollY = 0;
    var running = false;
    var lastStamp = 0;

    function resizeAurora() {
      var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      var w = Math.max(1, Math.round(window.innerWidth * dpr));
      var h = Math.max(1, Math.round(window.innerHeight * dpr));
      if (aurora.width !== w || aurora.height !== h) {
        aurora.width = w;
        aurora.height = h;
      }
      var count = window.innerWidth < 760 ? 28 : 48;
      if (particles.length !== count) {
        particles = [];
        for (var i = 0; i < count; i++) {
          var angle = Math.random() * Math.PI * 2;
          var speed = 0.00038 + Math.random() * 0.00034;
          particles.push({
            x: Math.random(),
            y: Math.random(),
            z: Math.random(),
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed * 0.72,
            hue: Math.random()
          });
        }
      }
    }

    function blob(x, y, radius, color) {
      var g = actx.createRadialGradient(x, y, 0, x, y, radius);
      g.addColorStop(0, color);
      g.addColorStop(1, "rgba(0,0,0,0)");
      actx.fillStyle = g;
      actx.beginPath();
      actx.arc(x, y, radius, 0, Math.PI * 2);
      actx.fill();
    }

    function mixGlow(from, to, amount, alpha) {
      var r = Math.round(from[0] + (to[0] - from[0]) * amount);
      var g = Math.round(from[1] + (to[1] - from[1]) * amount);
      var b = Math.round(from[2] + (to[2] - from[2]) * amount);
      return "rgba(" + r + "," + g + "," + b + "," + alpha.toFixed(3) + ")";
    }

    function wrap(v) {
      if (v < -0.06) return v + 1.12;
      if (v > 1.06) return v - 1.12;
      return v;
    }

    function paintAurora(time, frameScale) {
      var w = aurora.width;
      var h = aurora.height;
      var t = (time || 0) / 1000;
      var px = pointer.x;
      var py = pointer.y;
      var drift = reduced.matches ? 0 : scrollY * 0.08;
      var breath = 0.5 + 0.5 * Math.sin(t * Math.PI * 2 / 17);
      var step = reduced.matches ? 0 : frameScale;
      actx.clearRect(0, 0, w, h);
      actx.globalCompositeOperation = "lighter";
      /* 16s / 18s / 20s orbits, about 15% of the viewport, with a slow hue breath. */
      blob(
        w * (0.30 + Math.sin(t * Math.PI * 2 / 16) * 0.16 + (px - 0.5) * 0.08),
        h * (0.22 + Math.cos(t * Math.PI * 2 / 18) * 0.14 + (py - 0.5) * 0.06) - drift,
        Math.max(w, h) * (0.38 + breath * 0.05),
        mixGlow([92, 58, 214], [56, 128, 232], breath, 0.22 + breath * 0.10)
      );
      blob(
        w * (0.74 + Math.cos(t * Math.PI * 2 / 18) * 0.15 + (px - 0.5) * -0.07),
        h * (0.28 + Math.sin(t * Math.PI * 2 / 16) * 0.15) - drift * 0.6,
        Math.max(w, h) * (0.32 + (1 - breath) * 0.05),
        mixGlow([24, 168, 198], [72, 214, 196], breath, 0.18 + (1 - breath) * 0.10)
      );
      blob(
        w * (0.48 + Math.sin(t * Math.PI * 2 / 20) * 0.17),
        h * (0.78 + Math.cos(t * Math.PI * 2 / 19) * 0.13 + (py - 0.5) * 0.05) - drift * 0.3,
        Math.max(w, h) * 0.36,
        mixGlow([176, 48, 148], [214, 96, 188], 1 - breath, 0.12 + breath * 0.08)
      );
      /* Soft sweep: a radial glow crosses the field about every 8 seconds. */
      var sweep = (t % 8) / 8;
      var sweepFade = Math.sin(sweep * Math.PI);
      blob(
        w * (-0.18 + sweep * 1.36) + (px - 0.5) * w * 0.05,
        h * (0.32 + Math.sin(sweep * Math.PI * 2) * 0.16) - drift * 0.35,
        Math.max(w, h) * 0.30,
        "rgba(198, 228, 255, " + (sweepFade * 0.11).toFixed(3) + ")"
      );
      actx.globalCompositeOperation = "source-over";

      var pts = [];
      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        if (step) {
          var depthSpeed = 0.62 + p.z * 0.7;
          var flowX = Math.sin(t * 0.65 + p.y * 5.2) * 0.00022;
          var flowY = Math.cos(t * 0.5 + p.x * 4.1) * 0.00016;
          p.x = wrap(p.x + (p.vx + flowX) * depthSpeed * step);
          p.y = wrap(p.y + (p.vy + flowY) * depthSpeed * step);
        }
        var depth = 0.35 + p.z * 0.65;
        var x = (p.x + (px - 0.5) * 0.03 * depth) * w;
        var y = (p.y + (py - 0.5) * 0.02 * depth) * h - drift * depth;
        var edge = Math.min(p.x, p.y, 1 - p.x, 1 - p.y);
        var edgeFade = Math.max(0, Math.min(1, edge / 0.07));
        pts.push({ x: x, y: y, z: p.z, hue: p.hue, fade: edgeFade });
        actx.beginPath();
        actx.fillStyle = p.hue > 0.55 ? "rgba(186, 230, 255, 0.9)" : "rgba(214, 196, 255, 0.85)";
        actx.globalAlpha = (0.28 + p.z * 0.55) * edgeFade;
        actx.arc(x, y, (1.05 + p.z * 1.7) * (w > 1400 ? 1.25 : 1), 0, Math.PI * 2);
        actx.fill();
      }
      actx.globalAlpha = 1;

      var limit = w * 0.13;
      var pulseA = (t % 5.5) / 5.5;
      var pulseB = (pulseA + 0.5) % 1;
      var focus = [
        { x: w * (0.08 + pulseA * 0.84), y: h * (0.34 + Math.sin(pulseA * Math.PI * 2) * 0.16) },
        { x: w * (0.9 - pulseB * 0.72), y: h * (0.62 + Math.cos(pulseB * Math.PI * 2) * 0.12) }
      ];
      var reach = w * 0.16;
      for (var a = 0; a < pts.length; a++) {
        for (var b = a + 1; b < pts.length; b++) {
          if (Math.abs(pts[a].z - pts[b].z) > 0.34) continue;
          var dx = pts[a].x - pts[b].x;
          var dy = pts[a].y - pts[b].y;
          var dist = Math.hypot(dx, dy);
          if (dist >= limit || dist < 0.5) continue;
          var near = 1 - dist / limit;
          var fade = near * near * (3 - 2 * near);
          fade *= Math.min(pts[a].fade, pts[b].fade);
          if (fade < 0.02) continue;
          var mx = (pts[a].x + pts[b].x) * 0.5;
          var my = (pts[a].y + pts[b].y) * 0.5;
          var glow = 0;
          for (var f = 0; f < focus.length; f++) {
            var pd = Math.hypot(mx - focus[f].x, my - focus[f].y);
            if (pd < reach) glow = Math.max(glow, 1 - pd / reach);
          }
          actx.beginPath();
          actx.moveTo(pts[a].x, pts[a].y);
          actx.lineTo(pts[b].x, pts[b].y);
          actx.lineWidth = 1 + fade * 0.8;
          actx.strokeStyle = "rgba(176, 214, 255, " + (fade * 0.34).toFixed(3) + ")";
          actx.stroke();
          if (glow > 0.08) {
            actx.lineWidth = 1.4 + glow * 1.6;
            actx.strokeStyle = "rgba(226, 244, 255, " + (fade * glow * 0.72).toFixed(3) + ")";
            actx.stroke();
          }
        }
      }
    }

    function loop(time) {
      var frameScale = lastStamp ? Math.min(2, (time - lastStamp) / 16.67) : 1;
      lastStamp = time;
      pointer.x += (pointerTarget.x - pointer.x) * 0.04;
      pointer.y += (pointerTarget.y - pointer.y) * 0.04;
      paintAurora(time, frameScale);
      if (!reduced.matches && running) requestAnimationFrame(loop);
    }

    resizeAurora();
    paintAurora(0);
    if (!reduced.matches) {
      running = true;
      requestAnimationFrame(loop);
      window.addEventListener("pointermove", function (event) {
        pointerTarget.x = event.clientX / Math.max(1, window.innerWidth);
        pointerTarget.y = event.clientY / Math.max(1, window.innerHeight);
      }, { passive: true });
      window.addEventListener("scroll", function () {
        scrollY = window.scrollY || 0;
      }, { passive: true });
      document.addEventListener("visibilitychange", function () {
        if (document.hidden) {
          running = false;
        } else if (!running) {
          running = true;
          requestAnimationFrame(loop);
        }
      });
    }
    window.addEventListener("resize", function () {
      resizeAurora();
      if (reduced.matches) paintAurora(0);
    });
  }

  function track(el) {
    el.addEventListener("pointermove", function (event) {
      var rect = el.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      el.style.setProperty("--gx", ((event.clientX - rect.left) / rect.width) * 100 + "%");
      el.style.setProperty("--gy", ((event.clientY - rect.top) / rect.height) * 100 + "%");
    });
    el.addEventListener("pointerleave", function () {
      el.style.removeProperty("--gx");
      el.style.removeProperty("--gy");
    });
  }

  root.querySelectorAll(".glass, .btn, .play-btn, .nav-toggle, .top").forEach(track);
  root.querySelectorAll(".btn, .play-btn, .nav-toggle, .glass").forEach(function (btn) {
    btn.addEventListener("pointerdown", function (event) {
      if (reduced.matches) return;
      if (event.button !== 0) return;
      var rect = btn.getBoundingClientRect();
      var size = Math.max(rect.width, rect.height) * 1.5;
      var ink = document.createElement("span");
      ink.className = "ripple-ink";
      ink.style.width = size + "px";
      ink.style.height = size + "px";
      var clientX = event.clientX || rect.left + rect.width / 2;
      var clientY = event.clientY || rect.top + rect.height / 2;
      ink.style.left = clientX - rect.left - size / 2 + "px";
      ink.style.top = clientY - rect.top - size / 2 + "px";
      btn.appendChild(ink);
      ink.addEventListener("animationend", function () { ink.remove(); });
    });
  });

  var reveals = root.querySelectorAll("[data-reveal]");
  if (reduced.matches || !("IntersectionObserver" in window)) {
    reveals.forEach(function (node) { node.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (node) { io.observe(node); });
  }

  var toggle = root.querySelector(".nav-toggle");
  var panel = root.querySelector("#mobile-nav-panel");
  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      var willOpen = panel.hasAttribute("hidden");
      if (willOpen) panel.removeAttribute("hidden");
      else panel.setAttribute("hidden", "");
      toggle.setAttribute("aria-expanded", willOpen ? "true" : "false");
      toggle.setAttribute("aria-label", willOpen ? "Close menu" : "Open menu");
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        panel.setAttribute("hidden", "");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open menu");
      });
    });
  }

  /* Policy pages: "On this page" feedback. A click always flashes the target
     heading and moves focus to it, even when the section is already on screen
     and the page can't scroll. The link is marked current (.active +
     aria-current) and a scroll-spy keeps that mark in step while reading.
     A mark set by a click or a #hash arrival holds until the reader scrolls. */
  var toc = root.querySelector(".toc");
  if (toc) {
    var tocItems = [];
    toc.querySelectorAll('a[href^="#"]').forEach(function (link) {
      var section = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      var heading = section && section.querySelector("h2");
      if (!heading) return;
      heading.setAttribute("tabindex", "-1");
      var item = { link: link, section: section, heading: heading, timer: 0, inBand: false };
      heading.addEventListener("animationend", function (event) {
        if (event.target === heading && event.animationName === "heading-flash") {
          heading.classList.remove("flash");
        }
      });
      tocItems.push(item);
    });

    var activeItem = null;
    var locked = false;   /* a click or hash arrival owns the mark */
    var settling = false; /* ...and the browser is still carrying out that jump */
    var settledY = 0;
    var jumpId = 0;
    var clickedHash = null;
    var spyOffset = tocItems.length ? parseFloat(getComputedStyle(tocItems[0].section).scrollMarginTop) || 0 : 0;

    var itemFor = function (hash) {
      for (var i = 0; i < tocItems.length; i++) {
        if (tocItems[i].link.hash === hash) return tocItems[i];
      }
      return null;
    };

    var setActive = function (item) {
      if (item === activeItem) return;
      if (activeItem) {
        activeItem.link.classList.remove("active");
        activeItem.link.removeAttribute("aria-current");
      }
      activeItem = item;
      if (!item) return;
      item.link.classList.add("active");
      item.link.setAttribute("aria-current", "true");
      /* On short screens the panel scrolls: keep the current link in view
         (move the panel itself; scrollIntoView would move the page too). */
      if (toc.scrollHeight > toc.clientHeight) {
        var lr = item.link.getBoundingClientRect();
        var tr = toc.getBoundingClientRect();
        if (lr.top < tr.top || lr.bottom > tr.bottom) {
          toc.scrollTop += lr.top - tr.top - (tr.height - lr.height) / 2;
        }
      }
    };

    var flash = function (item) {
      var heading = item.heading;
      clearTimeout(item.timer);
      heading.classList.remove("flash");
      void heading.offsetWidth; /* restart the animation on a repeat click */
      heading.classList.add("flash");
      /* animationend clears it; the timer covers reduced motion (no animation). */
      item.timer = setTimeout(function () { heading.classList.remove("flash"); }, 1250);
    };

    /* Where the page comes to rest for this section: scroll-margin-top
       applied, clamped to the scrollable range (the last sections can't reach the top). */
    var restingY = function (section) {
      var margin = parseFloat(getComputedStyle(section).scrollMarginTop) || 0;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var y = section.getBoundingClientRect().top + window.scrollY - margin;
      return Math.max(0, Math.min(max, y));
    };

    /* Mark the item now. Flash once the jump has finished: right away when
       nothing needs to scroll, or after the smooth scroll arrives. */
    var arrive = function (item, minDelay) {
      var id = ++jumpId;
      var start = 0;
      var lastY = NaN;
      var still = 0;
      locked = true;
      settling = true;
      setActive(item);
      requestAnimationFrame(function check(now) {
        if (id !== jumpId) return;
        if (!start) start = now;
        var y = window.scrollY;
        still = Math.abs(y - lastY) < 0.5 ? still + 1 : 0;
        lastY = y;
        var waited = now - start;
        var there = Math.abs(y - restingY(item.section)) < 2;
        if (waited < minDelay || !((there && still >= 1) || still >= 8 || waited > 2500)) {
          requestAnimationFrame(check);
          return;
        }
        settling = false;
        settledY = y;
        flash(item);
      });
    };

    var spyApply = function () {
      if (locked) return;
      for (var i = 0; i < tocItems.length; i++) {
        if (tocItems[i].inBand) {
          setActive(tocItems[i]);
          return;
        }
      }
      setActive(null); /* above the first section */
    };

    tocItems.forEach(function (item) {
      item.link.addEventListener("click", function (event) {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        /* The default jump still runs (hash, history, smooth scroll); this only adds feedback.
           hashchange fires only if the hash differs; remember it so it isn't handled twice. */
        clickedHash = item.link.hash !== location.hash ? item.link.hash : null;
        item.heading.focus({ preventScroll: true });
        arrive(item, 0);
      });
    });

    window.addEventListener("hashchange", function () {
      var own = location.hash === clickedHash;
      clickedHash = null;
      if (own) return;
      var item = itemFor(location.hash);
      if (item) arrive(item, 150); /* back/forward: let the browser restore the scroll first */
    });

    window.addEventListener("scroll", function () {
      if (locked && !settling && Math.abs(window.scrollY - settledY) > 2) {
        locked = false;
        spyApply();
      }
    }, { passive: true });

    /* Reading band: from just under the sticky header (scroll-margin-top, plus a
       few px so the section above a jump target, whose edge only touches the band, doesn't count)
       down to 45% of the viewport. The first section in the band is the current one. */
    if ("IntersectionObserver" in window && tocItems.length) {
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          tocItems.forEach(function (item) {
            if (item.section === entry.target) item.inBand = entry.isIntersecting;
          });
        });
        spyApply();
      }, { rootMargin: "-" + Math.round(spyOffset + 8) + "px 0px -55% 0px" });
      tocItems.forEach(function (item) { spy.observe(item.section); });
    }

    /* Arriving with a #hash (shared link or reload): flash once the jump has settled. */
    var landing = itemFor(location.hash);
    if (landing) arrive(landing, 450);
  }

  var audioCtx = null;
  var activeAudio = null;

  function getAudioContext() {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    if (!audioCtx) audioCtx = new AC();
    return audioCtx;
  }

  function formatTime(value) {
    if (!isFinite(value) || value < 0) return "00:00";
    var minutes = Math.floor(value / 60);
    var seconds = Math.floor(value % 60).toString().padStart(2, "0");
    return String(minutes).padStart(2, "0") + ":" + seconds;
  }

  function roundRect(ctx, x, y, w, h, r) {
    var radius = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.arcTo(x + w, y, x + w, y + h, radius);
    ctx.arcTo(x + w, y + h, x, y + h, radius);
    ctx.arcTo(x, y + h, x, y, radius);
    ctx.arcTo(x, y, x + w, y, radius);
    ctx.closePath();
  }

  root.querySelectorAll("[data-player]").forEach(function (card, index) {
    var audio = card.querySelector("audio");
    var canvas = card.querySelector("canvas");
    var button = card.querySelector("[data-play]");
    var scrub = card.querySelector("[data-scrub]");
    var currentEl = card.querySelector("[data-current]");
    var durationEl = card.querySelector("[data-duration]");
    var errorEl = card.querySelector("[data-error]");
    if (!audio || !canvas || !button) return;

    var slot = document.createElement("div");
    slot.className = "play-slot";
    button.parentNode.insertBefore(slot, button);
    slot.appendChild(button);
    var ring = document.createElement("canvas");
    ring.className = "ring-canvas";
    ring.setAttribute("aria-hidden", "true");
    slot.insertBefore(ring, button);
    var ringCtx = ring.getContext("2d");
    var chip = document.createElement("p");
    chip.className = "live-chip";
    chip.setAttribute("data-live", "");
    chip.setAttribute("aria-hidden", "true");
    chip.hidden = true;
    chip.innerHTML = "<i></i>LIVE · AI CALL";
    canvas.parentNode.appendChild(chip);

    var ctx2d = canvas.getContext("2d");
    var track = document.createElement("canvas");
    track.className = "track-canvas";
    track.setAttribute("aria-hidden", "true");
    canvas.insertAdjacentElement("afterend", track);
    var trackCtx = track.getContext("2d");
    var bands = { bass: 0.08, mid: 0.06, treble: 0.04, level: 0.14 };
    var bandTargets = { bass: 0.08, mid: 0.06, treble: 0.04, level: 0.14 };
    var player = {
      analyser: null,
      graphTried: false,
      raf: 0,
      seeking: false,
      dragging: false,
      dpr: 1,
      hot: false,
      bass: 0,
      last: 0,
      phase: index * 1.3
    };

    function resize() {
      var rect = canvas.getBoundingClientRect();
      player.dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      var w = Math.max(1, Math.round(rect.width * player.dpr));
      var h = Math.max(1, Math.round((rect.height || 92) * player.dpr));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
      }
      var trackRect = track.getBoundingClientRect();
      var tw = Math.max(1, Math.round((trackRect.width || rect.width) * player.dpr));
      var th = Math.max(1, Math.round((trackRect.height || 40) * player.dpr));
      if (track.width !== tw || track.height !== th) {
        track.width = tw;
        track.height = th;
      }
      var ringSize = Math.round(76 * player.dpr);
      if (ring.width !== ringSize) {
        ring.width = ringSize;
        ring.height = ringSize;
      }
      draw();
    }

    function isLive() {
      return !audio.paused && !audio.ended;
    }

    function drawRing(energy) {
      var size = ring.width;
      var c = ringCtx;
      c.clearRect(0, 0, size, size);
      var cx = size / 2;
      var cy = size / 2;
      var radius = size * (0.39 + energy * 0.035);
      c.beginPath();
      c.arc(cx, cy, radius, 0, Math.PI * 2);
      c.strokeStyle = "rgba(120, 220, 255, 0.28)";
      c.lineWidth = Math.max(1, 1.25 * player.dpr);
      c.stroke();
      if (energy > 0.04) {
        c.beginPath();
        c.arc(cx, cy, radius + energy * size * 0.05, 0, Math.PI * 2);
        c.strokeStyle = "rgba(180, 120, 255, 0.18)";
        c.stroke();
      }
    }

    function taper(t) {
      var edge = Math.min(t, 1 - t) / 0.16;
      if (edge >= 1) return 1;
      if (edge <= 0) return 0;
      return edge * edge * (3 - 2 * edge);
    }

    function strokeWave(color, glow, width, points) {
      ctx2d.beginPath();
      ctx2d.moveTo(points[0], points[1]);
      for (var i = 2; i < points.length; i += 2) ctx2d.lineTo(points[i], points[i + 1]);
      ctx2d.strokeStyle = glow;
      ctx2d.lineWidth = width * 3.2;
      ctx2d.stroke();
      ctx2d.strokeStyle = color;
      ctx2d.lineWidth = width;
      ctx2d.stroke();
    }

    function drawFlow(now) {
      var w = canvas.width;
      var h = canvas.height;
      var dpr = player.dpr || 1;
      var live = isLive();
      var mid = h * 0.5;
      ctx2d.clearRect(0, 0, w, h);
      ctx2d.lineCap = "round";
      ctx2d.lineJoin = "round";
      ctx2d.globalCompositeOperation = "lighter";
      var layers = [
        { color: "rgba(94, 240, 255, 0.92)", glow: "rgba(94, 240, 255, 0.28)", freq: 1.7, phase: 0.2, speed: 1, drive: 0.42 + bands.bass * 1.15 + bands.level * 0.35 },
        { color: "rgba(90, 150, 255, 0.88)", glow: "rgba(90, 150, 255, 0.26)", freq: 2.5, phase: 1.4, speed: 1.25, drive: 0.34 + bands.mid * 1.05 + bands.level * 0.22 },
        { color: "rgba(176, 112, 255, 0.86)", glow: "rgba(176, 112, 255, 0.24)", freq: 3.4, phase: 2.5, speed: 0.85, drive: 0.28 + bands.treble * 1.1 + bands.mid * 0.2 },
        { color: "rgba(255, 96, 196, 0.8)", glow: "rgba(255, 96, 196, 0.22)", freq: 4.3, phase: 3.7, speed: 1.45, drive: 0.24 + bands.bass * 0.35 + bands.treble * 0.7 }
      ];
      var steps = 72;
      for (var layer = 0; layer < layers.length; layer++) {
        var spec = layers[layer];
        var freq = spec.freq * (1 + bands.treble * 0.28 + bands.level * 0.12);
        var points = new Array((steps + 1) * 2);
        for (var s = 0; s <= steps; s++) {
          var t = s / steps;
          var wave = Math.sin(t * Math.PI * 2 * freq + spec.phase + player.phase * spec.speed) * 0.66;
          wave += Math.sin(t * Math.PI * 2 * freq * 1.65 + spec.phase * 1.3 + player.phase * 0.6) * 0.24;
          var shaped = 0;
          if (live && player.time && player.time.length) {
            var idx = Math.min(player.time.length - 1, Math.floor(t * (player.time.length - 1)));
            shaped = (player.time[idx] - 128) / 128;
          }
          var amp = Math.min(1.15, spec.drive) * taper(t);
          var y = mid + (wave * amp + shaped * bands.level * 0.55) * h * 0.34;
          points[s * 2] = t * w;
          points[s * 2 + 1] = y;
        }
        strokeWave(spec.color, spec.glow, Math.max(1.1, 1.35 * dpr), points);
      }
      ctx2d.globalCompositeOperation = "source-over";
    }

    function drawTrack() {
      var w = track.width;
      var h = track.height;
      var dpr = player.dpr || 1;
      var peaks = player.track;
      var count = peaks ? peaks.length : 120;
      var gap = Math.max(1, 1.15 * dpr);
      var barW = Math.max(dpr, (w - gap * (count - 1)) / count);
      var progress = audio.duration ? Math.min(1, audio.currentTime / audio.duration) : 0;
      var mid = h * 0.5;
      trackCtx.clearRect(0, 0, w, h);
      var played = trackCtx.createLinearGradient(0, 0, w, 0);
      played.addColorStop(0, "#5ef0ff");
      played.addColorStop(0.5, "#6aa6ff");
      played.addColorStop(1, "#e15cff");
      for (var i = 0; i < count; i++) {
        var amp = peaks ? Math.max(0.06, peaks[i]) : 0.1;
        var bh = Math.max(dpr * 1.4, amp * h * 0.88);
        var x = i * (barW + gap);
        var lit = (i + 0.5) / count <= progress;
        trackCtx.fillStyle = lit ? played : "rgba(176, 190, 220, 0.28)";
        roundRect(trackCtx, x, mid - bh / 2, barW, bh, barW / 2);
        trackCtx.fill();
      }
      if (audio.duration) {
        var px = progress * w;
        trackCtx.fillStyle = "rgba(170, 230, 255, 0.4)";
        trackCtx.fillRect(px - 2.4 * dpr, dpr, 4.8 * dpr, h - dpr * 2);
        trackCtx.fillStyle = "#f7fdff";
        trackCtx.fillRect(px - 0.7 * dpr, 0, Math.max(1.2 * dpr, 1.5), h);
      }
    }

    function draw(now) {
      drawFlow(now || 0);
      drawTrack();
      drawRing(player.bass);
    }

    function readBands() {
      var freq = player.freq;
      var bins = freq.length;
      function avg(from, to) {
        var start = Math.max(1, Math.floor(from * bins));
        var end = Math.max(start + 1, Math.floor(to * bins));
        var sum = 0;
        for (var i = start; i < end; i++) sum += freq[i];
        return sum / ((end - start) * 255);
      }
      bandTargets.bass = avg(0, 0.08);
      bandTargets.mid = avg(0.08, 0.32);
      bandTargets.treble = avg(0.32, 0.75);
      var rms = 0;
      var count = 0;
      if (player.time) {
        for (var p = 0; p < player.time.length; p += 8) {
          var sample = (player.time[p] - 128) / 128;
          rms += sample * sample;
          count += 1;
        }
      }
      bandTargets.level = Math.min(1, count ? Math.sqrt(rms / count) * 3.4 : 0);
      player.bass = bandTargets.bass;
    }

    function tick(now) {
      var playing = isLive();
      var frame = player.last ? Math.min(2, (now - player.last) / 16.67) : 1;
      player.last = now;
      var engaged = playing || player.hot || card.matches(":focus-within");
      if (playing && !player.seeking) keepVisInSync();
      if (reduced.matches) {
        player.bass = 0.08;
        bands.level = 0.16;
        if (chip) chip.hidden = !playing;
        draw(0);
        player.raf = 0;
        return;
      }
      if (player.analyser && playing && player.freq) {
        player.analyser.getByteFrequencyData(player.freq);
        if (player.time) player.analyser.getByteTimeDomainData(player.time);
        readBands();
      } else {
        bandTargets.bass = 0.1 + 0.035 * Math.sin(now / 980 + index);
        bandTargets.mid = 0.07 + 0.03 * Math.sin(now / 1240 + index * 0.7);
        bandTargets.treble = 0.04 + 0.02 * Math.sin(now / 860 + 1.4);
        bandTargets.level = 0.15;
        player.bass += (bandTargets.bass - player.bass) * 0.08;
      }
      var ease = playing ? 0.22 : 0.08;
      var delta = 0;
      var keys = ["bass", "mid", "treble", "level"];
      for (var k = 0; k < keys.length; k++) {
        var key = keys[k];
        delta += Math.abs(bandTargets[key] - bands[key]);
        bands[key] += (bandTargets[key] - bands[key]) * ease;
      }
      player.phase += (playing ? 0.05 + bands.level * 0.07 : 0.012) * frame;
      if (!player.seeking && scrub && audio.duration) {
        scrub.value = String(Math.round((audio.currentTime / audio.duration) * 1000));
      }
      if (currentEl) currentEl.textContent = formatTime(audio.currentTime || 0);
      if (durationEl && audio.duration) durationEl.textContent = formatTime(audio.duration);
      if (chip) chip.hidden = !playing;
      draw(now);
      if (engaged || delta > 0.03) player.raf = requestAnimationFrame(tick);
      else player.raf = 0;
    }

    function startLoop() {
      if (!player.raf) player.raf = requestAnimationFrame(tick);
    }

    function ensureGraph() {
      if (player.graphTried) return;
      player.graphTried = true;
      var context = getAudioContext();
      if (!context) return;
      try {
        var source = context.createMediaElementSource(audio);
        source.connect(context.destination);
      } catch (err) { /* element audio still plays */ }
      var analyser = context.createAnalyser();
      analyser.fftSize = 1024;
      analyser.smoothingTimeConstant = 0.72;
      var silent = context.createGain();
      silent.gain.value = 0;
      analyser.connect(silent);
      silent.connect(context.destination);
      player.analyser = analyser;
      player.time = new Uint8Array(analyser.fftSize);
      player.freq = new Uint8Array(analyser.frequencyBinCount);
    }

    function rebuildEnvelope(buffer) {
      var channel = buffer.getChannelData(0);
      var count = 160;
      var peaks = new Float32Array(count);
      var chunk = Math.max(1, Math.floor(channel.length / count));
      var max = 0.0001;
      for (var i = 0; i < count; i++) {
        var peak = 0;
        var from = i * chunk;
        var to = Math.min(channel.length, from + chunk);
        var step = Math.max(1, Math.floor((to - from) / 40));
        for (var j = from; j < to; j += step) {
          var sample = Math.abs(channel[j]);
          if (sample > peak) peak = sample;
        }
        peaks[i] = peak;
        if (peak > max) max = peak;
      }
      for (var n = 0; n < count; n++) peaks[n] = Math.min(1, peaks[n] / max);
      player.track = peaks;
    }

    function restartVis() {
      var context = getAudioContext();
      if (!context || !player.audioBuffer || !player.analyser) return;
      if (player.visSource) {
        try { player.visSource.stop(); } catch (err) { /* already stopped */ }
        try { player.visSource.disconnect(); } catch (err) { /* ignore */ }
      }
      var src = context.createBufferSource();
      src.buffer = player.audioBuffer;
      src.connect(player.analyser);
      var offset = Math.max(0, Math.min(audio.currentTime || 0, Math.max(0.05, player.audioBuffer.duration - 0.05)));
      try { src.start(0, offset); } catch (err) { return; }
      player.visSource = src;
      player.visOffset = offset;
      player.visAt = context.currentTime;
    }

    function keepVisInSync() {
      var context = getAudioContext();
      if (!context || !player.visSource || audio.paused) return;
      var expected = player.visOffset + (context.currentTime - player.visAt);
      if (Math.abs(expected - audio.currentTime) > 0.4) restartVis();
    }

    function decodeClip() {
      if (player.audioBuffer || player.decodePromise) return;
      var context = getAudioContext();
      if (!context) return;
      player.decodePromise = fetch(audio.currentSrc || audio.getAttribute("src"))
        .then(function (res) { return res.arrayBuffer(); })
        .then(function (buf) { return context.decodeAudioData(buf); })
        .then(function (decoded) {
          player.audioBuffer = decoded;
          rebuildEnvelope(decoded);
          if (!audio.paused) restartVis();
          startLoop();
        })
        .catch(function () { player.decodePromise = null; });
    }

    function stopVis() {
      if (!player.visSource) return;
      try { player.visSource.stop(); } catch (err) { /* already stopped */ }
      player.visSource = null;
    }

    function setPlaying(on) {
      card.classList.toggle("is-playing", on);
      button.setAttribute("aria-pressed", on ? "true" : "false");
      var name = button.getAttribute("data-label") || "sample";
      button.setAttribute("aria-label", (on ? "Pause " : "Play ") + name);
    }

    button.addEventListener("click", function () {
      if (!audio.paused) {
        audio.pause();
        return;
      }
      if (activeAudio && activeAudio !== audio) activeAudio.pause();
      activeAudio = audio;
      var context = getAudioContext();
      if (context && context.state === "suspended") context.resume();
      ensureGraph();
      decodeClip();
      var attempt = audio.play();
      if (attempt && typeof attempt.catch === "function") {
        attempt.catch(function () { setPlaying(false); });
      }
    });

    audio.addEventListener("play", function () {
      setPlaying(true);
      if (player.audioBuffer) restartVis();
      startLoop();
    });
    audio.addEventListener("pause", function () {
      setPlaying(false);
      stopVis();
      startLoop();
    });
    audio.addEventListener("ended", function () {
      setPlaying(false);
      stopVis();
      startLoop();
    });
    audio.addEventListener("timeupdate", function () {
      if (!reduced.matches) return;
      if (currentEl) currentEl.textContent = formatTime(audio.currentTime || 0);
      if (durationEl && audio.duration) durationEl.textContent = formatTime(audio.duration);
      if (!player.seeking && scrub && audio.duration) {
        scrub.value = String(Math.round((audio.currentTime / audio.duration) * 1000));
      }
      if (chip) chip.hidden = audio.paused || audio.ended;
      draw(0);
    });
    audio.addEventListener("loadedmetadata", function () {
      if (durationEl) durationEl.textContent = formatTime(audio.duration);
      if (scrub) scrub.disabled = false;
    });
    audio.addEventListener("error", function () {
      card.classList.add("is-error");
      if (errorEl) errorEl.hidden = false;
      button.disabled = true;
    });

    if (scrub) {
      scrub.addEventListener("input", function () {
        if (!audio.duration) return;
        player.seeking = true;
        audio.currentTime = (Number(scrub.value) / 1000) * audio.duration;
        if (currentEl) currentEl.textContent = formatTime(audio.currentTime);
        draw();
      });
      scrub.addEventListener("change", function () {
        player.seeking = false;
        if (!audio.paused) restartVis();
      });
    }

    function seekAt(clientX) {
      if (!audio.duration) return;
      var rect = track.getBoundingClientRect();
      var ratio = Math.min(1, Math.max(0, (clientX - rect.left) / rect.width));
      audio.currentTime = ratio * audio.duration;
      if (scrub) scrub.value = String(Math.round(ratio * 1000));
      if (currentEl) currentEl.textContent = formatTime(audio.currentTime);
      draw();
    }

    track.addEventListener("pointerdown", function (event) {
      player.dragging = true;
      player.seeking = true;
      try { track.setPointerCapture(event.pointerId); } catch (err) { /* ignore */ }
      seekAt(event.clientX);
    });
    track.addEventListener("pointermove", function (event) {
      if (!player.dragging) return;
      seekAt(event.clientX);
    });
    track.addEventListener("pointerup", function () {
      player.dragging = false;
      player.seeking = false;
      if (!audio.paused) restartVis();
    });
    track.addEventListener("pointercancel", function () {
      player.dragging = false;
      player.seeking = false;
    });

    function arm() {
      if (!player.audioBuffer) decodeClip();
      if (reduced.matches) return;
      player.hot = true;
      startLoop();
    }
    function disarm() {
      player.hot = card.matches(":hover") || card.matches(":focus-within");
      if (!player.hot && audio.paused) startLoop();
    }
    card.addEventListener("pointerenter", arm);
    card.addEventListener("pointerleave", disarm);
    card.addEventListener("focusin", arm);
    card.addEventListener("focusout", disarm);

    if (typeof ResizeObserver === "function") new ResizeObserver(resize).observe(canvas);
    else window.addEventListener("resize", resize);
    if (currentEl) currentEl.textContent = "00:00";
    if (durationEl) durationEl.textContent = "00:00";
    resize();
  });
})();
