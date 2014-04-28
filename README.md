# AudioAddict.bundle

Plex channel plugin for AudioAddict (sky.fm, di.fm, etc.)

# Preferences

There are three preferences that can be set:

* __Listen Key__: Your unique key, functionally used as an auth and ident token. It can be obtained from the "player settings -> hardware player" section of your favourite AA service. Example: http://www.sky.fm/settings
* __Preferred Stream__: This corresponds to the "sound quality & bandwidth" option of the AA service. I haven't been able to get the AAC streams to play in Plex, so your options are `public3` and `premium_high` (except rockradio.com, which uses `android_premium_high` for Premium).
* __Preferred Source__: This corresponds to the regional server that you want to stream. You're not obligated to set this, but if you're having bandwidth issues it might help. Hint: `prem2` is the Premium server in Europe. I don't know what the others are.

# Does it work?

Well it's not pretty, but it works for me just fine. For reference, I run Plex on a Ubuntu 12.04 LTS box, and I access it using the Android client, the Samsung Smart TV app, and via Firefox on my MacBook.

Your mileage may vary.

# AudioAddict API

This is the sum total of all public knowledge concerning the AA API: http://tobiass.eu/api-doc.html 

This plugin would have been impossible without that document, so a big thank-you to whomever wrote it.

