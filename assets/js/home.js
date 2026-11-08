/* Homepage behavior: liquid-glass pointer light, mobile menu,
   calendar dialog, and the demo-audio waveform player.
   Scoped to #root so vertical pages (?mode=) keep their own scripts. */
(function () {
  if (document.documentElement.classList.contains("mode-pending")) return;

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

  root.querySelectorAll(".btn, .play-btn").forEach(function (btn) {
    btn.addEventListener("pointermove", function (event) {
      var rect = btn.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      var x = ((event.clientX - rect.left) / rect.width) * 100;
      var y = ((event.clientY - rect.top) / rect.height) * 100;
      btn.style.setProperty("--gx", x + "%");
      btn.style.setProperty("--gy", y + "%");
    });
    btn.addEventListener("pointerleave", function () {
      btn.style.setProperty("--gx", "28%");
      btn.style.setProperty("--gy", "0%");
    });
    btn.addEventListener("pointerdown", function (event) {
      if (reduced.matches) return;
      var rect = btn.getBoundingClientRect();
      var size = Math.max(rect.width, rect.height) * 1.45;
      var ink = document.createElement("span");
      ink.className = "ripple-ink";
      ink.style.width = size + "px";
      ink.style.height = size + "px";
      var clientX = event.clientX || rect.left + rect.width / 2;
      var clientY = event.clientY || rect.top + rect.height / 2;
      ink.style.left = clientX - rect.left - size / 2 + "px";
      ink.style.top = clientY - rect.top - size / 2 + "px";
      btn.appendChild(ink);
      ink.addEventListener("animationend", function () {
        ink.remove();
      });
    });
  });

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

  var modal = root.querySelector("#calendar-modal-main");
  if (modal) {
    var iframe = modal.querySelector("iframe");
    var lastFocus = null;

    function openCalendar() {
      if (iframe && !iframe.getAttribute("src")) iframe.setAttribute("src", iframe.getAttribute("data-src"));
      lastFocus = document.activeElement;
      modal.hidden = false;
      document.body.style.overflow = "hidden";
      var closeBtn = modal.querySelector("[data-close-calendar]");
      if (closeBtn) closeBtn.focus();
    }

    function closeCalendar() {
      if (modal.hidden) return;
      modal.hidden = true;
      document.body.style.overflow = "";
      if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
    }

    root.querySelectorAll("[data-open-calendar]").forEach(function (el) {
      el.addEventListener("click", function (event) {
        event.preventDefault();
        openCalendar();
      });
    });

    modal.addEventListener("click", function (event) {
      if (event.target === modal) closeCalendar();
    });

    modal.querySelectorAll("[data-close-calendar]").forEach(function (el) {
      el.addEventListener("click", closeCalendar);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeCalendar();
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
      rest[i] = 0.18 + 0.68 * (0.5 * a + 0.3 * b + 0.2 * c);
      levels[i] = rest[i];
      targets[i] = rest[i];
    }

    var player = {
      analyser: null,
      freq: null,
      graphTried: false,
      raf: 0,
      seeking: false,
      dragging: false,
      dpr: 1
    };

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
        var played = live || (duration ? (n + 0.5) / bars <= progress + 0.01 : false);
        ctx2d.fillStyle = played ? "rgba(37, 77, 206, 0.95)" : "rgba(37, 77, 206, 0.28)";
        roundRect(ctx2d, x, baseline - bh, barW, bh, barW / 2);
        ctx2d.fill();
        ctx2d.globalAlpha = played ? 0.28 : 0.12;
        roundRect(ctx2d, x, baseline + 4 * dpr, barW, Math.max(2 * dpr, bh * 0.38), barW / 2);
        ctx2d.fill();
        ctx2d.globalAlpha = 1;
      }
      if (!live && duration) {
        ctx2d.fillStyle = "#14202d";
        ctx2d.fillRect(progress * w, h * 0.16, Math.max(1.5 * dpr, 2), h * 0.68);
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
        for (var n = 0; n < bars; n++) {
          targets[n] = Math.min(1, player.envelope[n] * (0.78 + loudness * 0.7));
        }
      } else if (player.analyser && playing && player.time) {
        player.analyser.getByteTimeDomainData(player.time);
        var len = player.time.length;
        for (var live = 0; live < bars; live++) {
          var start = Math.floor(live / bars * len);
          var end = Math.max(start + 1, Math.floor((live + 1) / bars * len));
          var peak = 0;
          for (var s = start; s < end; s++) {
            var dev = Math.abs(player.time[s] - 128);
            if (dev > peak) peak = dev;
          }
          targets[live] = Math.min(1, 0.06 + (peak / 128) * 1.55);
        }
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
      if (playing || delta > 0.35) {
        player.raf = requestAnimationFrame(tick);
      } else {
        player.raf = 0;
      }
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
      } catch (err) {
        /* Element audio still plays if the graph could not be attached. */
      }
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
      var offset = Math.max(0, Math.min(audio.currentTime || 0, player.audioBuffer.duration - 0.05));
      src.start(0, offset);
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
      player.decodePromise = fetch(audio.getAttribute("src"))
        .then(function (res) { return res.arrayBuffer(); })
        .then(function (buf) { return context.decodeAudioData(buf); })
        .then(function (decoded) {
          player.audioBuffer = decoded;
          rebuildEnvelope(decoded);
          if (!audio.paused) restartVis();
          startLoop();
        })
        .catch(function () {
          player.decodePromise = null;
        });
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
        attempt.catch(function () {
          setPlaying(false);
        });
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
      scrub.addEventListener("pointerup", function () {
        player.seeking = false;
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

    if (typeof ResizeObserver === "function") {
      new ResizeObserver(resize).observe(canvas);
    } else {
      window.addEventListener("resize", resize);
    }
    resize();
  });
})();
