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
