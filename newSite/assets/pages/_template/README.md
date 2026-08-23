# Pattern stub for a new vertical page's assets

This folder is a placeholder showing the shape to copy when you start a new
vertical (e.g. `realestate`). It intentionally holds no real files.

When you build a new vertical page:

1. Duplicate this folder: `newSite/assets/pages/_template/` → `newSite/assets/pages/<verticalName>/`.
2. Inside it, create `audio/` and/or `images/` subfolders only for assets that
   are **unique to this page** or that you're deliberately duplicating out of
   `assets/common/` for a page-local reference (see template.json's
   `assets.audio.pages.healthcare` for the pattern — it duplicates one clip
   out of `assets/common/audio/` because the page only ever plays that one).
3. Anything reused identically across pages (logos, favicon, the full 6-clip
   shared audio showcase set) stays in `assets/common/` — do not copy it here.
4. Register the new files in `template.json` under a new
   `assets.audio.pages.<verticalName>` (or `assets.images.pages.<verticalName>`)
   block, mirroring the existing `healthcare` entry.
