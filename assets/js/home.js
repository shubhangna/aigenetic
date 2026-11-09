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

    function resizeAurora() {
      var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      var w = Math.max(1, Math.round(window.innerWidth * dpr));
      var h = Math.max(1, Math.round(window.innerHeight * dpr));
      if (aurora.width !== w || aurora.height !== h) {
        aurora.width = w;
        aurora.height = h;
      }
      var count = window.innerWidth < 760 ? 28 : 54;
      if (particles.length !== count) {
        particles = [];
        for (var i = 0; i < count; i++) {
          particles.push({
            x: Math.random(),
            y: Math.random(),
            z: Math.random(),
            vx: (Math.random() - 0.5) * 0.00009,
            vy: (Math.random() - 0.5) * 0.00006,
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

    function paintAurora(time) {
      var w = aurora.width;
      var h = aurora.height;
      var t = (time || 0) / 1000;
      var px = pointer.x;
      var py = pointer.y;
      var drift = reduced.matches ? 0 : scrollY * 0.08;
      actx.clearRect(0, 0, w, h);
      actx.globalCompositeOperation = "lighter";
      blob(
        w * (0.22 + Math.sin(t / 17) * 0.06 + (px - 0.5) * 0.08),
        h * (0.18 + Math.cos(t / 21) * 0.05 + (py - 0.5) * 0.06) - drift,
        Math.max(w, h) * 0.42,
        "rgba(98, 62, 210, 0.30)"
      );
      blob(
        w * (0.78 + Math.cos(t / 19) * 0.05 + (px - 0.5) * -0.06),
        h * (0.22 + Math.sin(t / 23) * 0.06) - drift * 0.6,
        Math.max(w, h) * 0.36,
        "rgba(28, 168, 196, 0.26)"
      );
      blob(
        w * (0.5 + Math.sin(t / 29) * 0.08),
        h * (0.82 + Math.cos(t / 26) * 0.04) - drift * 0.3,
        Math.max(w, h) * 0.4,
        "rgba(186, 54, 150, 0.18)"
      );
      actx.globalCompositeOperation = "source-over";

      var pts = [];
      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        if (!reduced.matches) {
          p.x += p.vx * (0.4 + p.z);
          p.y += p.vy * (0.4 + p.z);
          if (p.x < -0.05) p.x = 1.05;
          if (p.x > 1.05) p.x = -0.05;
          if (p.y < -0.05) p.y = 1.05;
          if (p.y > 1.05) p.y = -0.05;
        }
        var depth = 0.35 + p.z * 0.65;
        var x = (p.x + (px - 0.5) * 0.03 * depth) * w;
        var y = (p.y + (py - 0.5) * 0.02 * depth) * h - drift * depth;
        pts.push({ x: x, y: y, z: p.z, hue: p.hue });
        actx.beginPath();
        actx.fillStyle = p.hue > 0.55 ? "rgba(186, 230, 255, 0.75)" : "rgba(214, 196, 255, 0.7)";
        actx.globalAlpha = 0.25 + p.z * 0.55;
        actx.arc(x, y, (0.7 + p.z * 1.5) * (w > 1400 ? 1.3 : 1), 0, Math.PI * 2);
        actx.fill();
      }
      actx.globalAlpha = 1;
      actx.lineWidth = 1;
      var limit = w * 0.12;
      for (var a = 0; a < pts.length; a++) {
        for (var b = a + 1; b < pts.length; b++) {
          if (Math.abs(pts[a].z - pts[b].z) > 0.28) continue;
          var dx = pts[a].x - pts[b].x;
          var dy = pts[a].y - pts[b].y;
          var dist = Math.hypot(dx, dy);
          if (dist > limit) continue;
          actx.strokeStyle = "rgba(170, 210, 255, " + ((1 - dist / limit) * 0.22) + ")";
          actx.beginPath();
          actx.moveTo(pts[a].x, pts[a].y);
          actx.lineTo(pts[b].x, pts[b].y);
          actx.stroke();
        }
      }
    }

    function loop(time) {
      pointer.x += (pointerTarget.x - pointer.x) * 0.04;
      pointer.y += (pointerTarget.y - pointer.y) * 0.04;
      paintAurora(time);
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

  var audioCtx = null;
  var activeAudio = null;

  function getAudioContext() {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    if (!audioCtx) audioCtx = new AC();
    return audioCtx;
  }

  function formatTime(value) {
    if (!isFinite(value) || value < 0) return "0:00";
    var minutes = Math.floor(value / 60);
    var seconds = Math.floor(value % 60).toString().padStart(2, "0");
    return minutes + ":" + seconds;
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

    var ctx2d = canvas.getContext("2d");
    var bars = 56;
    var rest = new Float32Array(bars);
    var levels = new Float32Array(bars);
    var targets = new Float32Array(bars);
    var seed = 1.7 + index * 2.3;
    for (var i = 0; i < bars; i++) {
      var a = Math.abs(Math.sin(seed + i * 0.47));
      var b = Math.abs(Math.sin(seed * 1.3 + i * 0.19));
      var c = Math.abs(Math.sin(seed * 0.4 + i * 0.91));
      rest[i] = 0.16 + 0.55 * (0.5 * a + 0.3 * b + 0.2 * c);
      levels[i] = rest[i];
      targets[i] = rest[i];
    }

    var player = { analyser: null, graphTried: false, raf: 0, seeking: false, dragging: false, dpr: 1 };

    function resize() {
      var rect = canvas.getBoundingClientRect();
      player.dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(1, Math.round(rect.width * player.dpr));
      var h = Math.max(1, Math.round((rect.height || 84) * player.dpr));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
      }
      draw();
    }

    function draw() {
      var w = canvas.width;
      var h = canvas.height;
      var dpr = player.dpr || 1;
      ctx2d.clearRect(0, 0, w, h);
      var gap = 3 * dpr;
      var barW = Math.max(2 * dpr, (w - gap * (bars - 1)) / bars);
      var duration = audio.duration;
      var progress = duration ? Math.min(1, audio.currentTime / duration) : 0;
      var live = !audio.paused && !audio.ended;
      var baseline = h * 0.62;
      for (var n = 0; n < bars; n++) {
        var amp = levels[n];
        var bh = Math.max(2.5 * dpr, amp * h * 0.78);
        var x = n * (barW + gap);
        var played = (n + 0.5) / bars <= progress + (live ? 0.02 : 0.01);
        ctx2d.fillStyle = played ? "rgba(158, 236, 255, 0.95)" : "rgba(176, 186, 230, 0.32)";
        roundRect(ctx2d, x, baseline - bh, barW, bh, barW / 2);
        ctx2d.fill();
      }
      if (duration) {
        ctx2d.fillStyle = "rgba(255,255,255,.85)";
        ctx2d.fillRect(progress * w, h * 0.18, Math.max(1.5 * dpr, 2), h * 0.64);
      }
    }

    function tick() {
      var playing = !audio.paused && !audio.ended;
      if (playing && !player.seeking) keepVisInSync();
      if (player.analyser && playing && player.time && player.envelope) {
        player.analyser.getByteTimeDomainData(player.time);
        var energy = 0;
        var samples = 0;
        for (var probe = 0; probe < player.time.length; probe += 8) {
          energy += Math.abs(player.time[probe] - 128);
          samples += 1;
        }
        var loudness = samples ? Math.min(1, (energy / samples) / 22) : 0;
        for (var n = 0; n < bars; n++) targets[n] = Math.min(1, player.envelope[n] * (0.78 + loudness * 0.7));
      } else if (player.envelope) {
        for (var env = 0; env < bars; env++) targets[env] = player.envelope[env];
      } else {
        for (var r = 0; r < bars; r++) targets[r] = rest[r];
      }
      var ease = reduced.matches ? 1 : (playing ? 0.7 : 0.22);
      var delta = 0;
      for (var k = 0; k < bars; k++) {
        delta += Math.abs(targets[k] - levels[k]);
        levels[k] += (targets[k] - levels[k]) * ease;
      }
      if (!player.seeking && scrub && audio.duration) {
        scrub.value = String(Math.round((audio.currentTime / audio.duration) * 1000));
      }
      if (currentEl) currentEl.textContent = formatTime(audio.currentTime);
      draw();
      if (playing || delta > 0.35) player.raf = requestAnimationFrame(tick);
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
      analyser.fftSize = 2048;
      analyser.smoothingTimeConstant = 0.62;
      var silent = context.createGain();
      silent.gain.value = 0;
      analyser.connect(silent);
      silent.connect(context.destination);
      player.analyser = analyser;
      player.time = new Uint8Array(analyser.fftSize);
    }

    function rebuildEnvelope(buffer) {
      var channel = buffer.getChannelData(0);
      var envelope = new Float32Array(bars);
      var chunk = Math.max(1, Math.floor(channel.length / bars));
      for (var i = 0; i < bars; i++) {
        var peak = 0;
        var from = i * chunk;
        var to = Math.min(channel.length, from + chunk);
        for (var j = from; j < to; j += 12) {
          var sample = Math.abs(channel[j]);
          if (sample > peak) peak = sample;
        }
        envelope[i] = Math.min(1, 0.12 + peak * 1.65);
      }
      player.envelope = envelope;
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
      var rect = canvas.getBoundingClientRect();
      var ratio = Math.min(1, Math.max(0, (clientX - rect.left) / rect.width));
      audio.currentTime = ratio * audio.duration;
      if (scrub) scrub.value = String(Math.round(ratio * 1000));
      if (currentEl) currentEl.textContent = formatTime(audio.currentTime);
      draw();
    }

    canvas.addEventListener("pointerdown", function (event) {
      player.dragging = true;
      player.seeking = true;
      try { canvas.setPointerCapture(event.pointerId); } catch (err) { /* ignore */ }
      seekAt(event.clientX);
    });
    canvas.addEventListener("pointermove", function (event) {
      if (!player.dragging) return;
      seekAt(event.clientX);
    });
    canvas.addEventListener("pointerup", function () {
      player.dragging = false;
      player.seeking = false;
      if (!audio.paused) restartVis();
    });
    canvas.addEventListener("pointercancel", function () {
      player.dragging = false;
      player.seeking = false;
    });

    if (typeof ResizeObserver === "function") new ResizeObserver(resize).observe(canvas);
    else window.addEventListener("resize", resize);
    resize();
  });
})();
