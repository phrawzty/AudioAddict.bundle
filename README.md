# AudioAddict.bundle

Plex channel plugin for AudioAddict (sky.fm, di.fm, etc.)

# Preferences

There are some preferences that can be set:

* __Listen Key__: Your unique key, functionally used as an auth and ident token. It can be obtained from the "player settings -> hardware player" section of your favourite AA service. Example: http://www.radiotunes.com/settings
* __Preferred Streams__: These corresponds to the "sound quality & bandwidth" option of the AA service. AAC support is sort of wonky (works on some devices, not on others), so your only safe options (read: MP3) are `public3` and `premium_high` (except RockRadio, which uses `android_premium_high` for some reason).
* __Preferred Source__: This corresponds to the regional server that you want to stream. You're not obligated to set this, but if you're having bandwidth issues it might help. `pub` and `prem1` are in the USA, `prem2` is in Europe, and `prem3` is in SE Asia (possibly Singapore).

# Does it work?

Well it's not pretty, but it works for me just fine. For reference, I run Plex on a Ubuntu 14.04 LTS box, and I access it using the Android client, the Samsung Smart TV app, and via Firefox on my MacBook.

Your mileage may vary.

# AudioAddict API

The sum total of all public knowledge concerning the AA API used to be available [here](http://tobiass.eu/api-doc.html); however, the server disappeared without a trace sometime in 2014.  There is an archived copy available on the [wayback machine](https://web.archive.org/web/20140426192326/http://tobiass.eu/api-doc.html).
This plugin would have been impossible without that document, so a big thank-you to whomever wrote it in the first place.
