HERO BACKGROUND VIDEO
=====================

Drop the files here, then flip one attribute in index.html:

    <video class="hero__video" data-hero-video="off"   ->   data-hero-video="on"

Files expected (names are referenced in index.html):
    video/hero.mp4     H.264 / AAC-free, no audio track
    video/hero.webm    optional, served first where supported

Specs that keep it fast:
    1920 x 1080, 24-30fps
    8-15 seconds, cut so the last frame matches the first (seamless loop)
    NO audio track at all (not just muted)
    Target under 5 MB for the mp4. Over ~8 MB and it hurts more than it helps.

The poster is images/projects/oak-point-lg.jpg. It shows:
    - before the video loads
    - if the file is missing or fails
    - under prefers-reduced-motion
    - on screens 760px and under (video is never even requested)
    - when the browser blocks autoplay
    - when the visitor has Data Saver on

There is no ffmpeg on this machine, so compression has to happen
wherever the clip is sourced or via an online encoder (Handbrake works).

LICENSING: this goes on a paying client's site. Use footage cleared for
commercial use and keep a record of the licence.
