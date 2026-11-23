/* Google Calendar booking dialog shared by the homepage and inner pages.
   The iframe keeps the live appointment URL. Loading is deferred with
   loading="lazy" while the dialog is hidden; opening the dialog shows the
   same frame and focuses the close button. */
var lastCalendarTrigger = null;

function calendarModal() {
  return document.getElementById("calendar-modal-main");
}

function openCalendarModalMain() {
  var modal = calendarModal();
  if (!modal) return;
  modal.style.display = "flex";
  document.body.style.overflow = "hidden";
  var closeBtn = modal.querySelector(".calendar-close");
  if (closeBtn) closeBtn.focus();
}

function closeCalendarModalMain() {
  var modal = calendarModal();
  if (!modal || modal.style.display === "none") return;
  modal.style.display = "none";
  document.body.style.overflow = "";
  if (lastCalendarTrigger && typeof lastCalendarTrigger.focus === "function") {
    lastCalendarTrigger.focus();
  }
}

document.addEventListener("click", function (e) {
  var modal = calendarModal();
  if (!modal) return;
  if (e.target && e.target.id === "calendar-modal-main") {
    closeCalendarModalMain();
    return;
  }
  var trigger = e.target.closest && e.target.closest("[data-open-calendar]");
  if (!trigger) return;
  e.preventDefault();
  lastCalendarTrigger = trigger;
  openCalendarModalMain();
});

document.addEventListener("keydown", function (e) {
  var modal = calendarModal();
  if (!modal || modal.style.display === "none") return;
  if (e.key === "Escape") {
    closeCalendarModalMain();
    return;
  }
  if (e.key !== "Tab") return;
  var items = modal.querySelectorAll("button, [href], iframe");
  if (!items.length) return;
  var first = items[0];
  var last = items[items.length - 1];
  if (e.shiftKey && document.activeElement === first) {
    e.preventDefault();
    last.focus();
  } else if (!e.shiftKey && document.activeElement === last) {
    e.preventDefault();
    first.focus();
  }
});
