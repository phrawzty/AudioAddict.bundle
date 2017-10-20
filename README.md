# AudioAddict.bundle

This is a Plex [Channel plugin](https://support.plex.tv/hc/en-us/categories/200109616-Channels) that offers a nice interface to the [AudioAddict](http://www.audioaddict.com/) family of music streaming sites, including [DI.fm](http://di.fm) (aka Digitally Imported), [RadioTunes.com](http://radiotunes.com) (formerly Sky.fm), and others.

# Install

Like most plugins, this is currently "[unsupported](https://support.plex.tv/hc/en-us/articles/201375863-Channels-from-Other-Sources)", so the installation process is manual. See the [official Plex documentation](https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-) for more information.

# Preferences

There are some preferences that can be set:

* __Listen Key__: Your unique key, functionally used as an auth and ident token. It can be obtained from the "player settings → hardware player" section of your favourite AA service. Example: http://www.radiotunes.com/settings
* __Preferred Source__: This corresponds to the regional server that you want to stream. You're not obligated to set this, but if you're having bandwidth issues it might help. `prem1`, `prem3`, and `prem4` are in the USA, while `prem2` is in Europe.
* __Preferred Streams__: These correspond to the "sound quality & bandwidth" option of the AA service. AAC support is sort of wonky (works on some devices, not on others), so your only safe options (read: MP3) are `public3` and `premium_high` (except RockRadio, which uses `android_premium_high` for some reason).
* __Force Refresh__: This will, as the name implies, force a refresh of the service information next time you access it. In practice, this should be used if you modify either (or both) of the _Source_ or _Stream_ preferences at any time. It is possible that this will _appear_ to cause an error of some type (this is due to timeout issues that have been totally ignored. sorry.), but it probably worked. Remember to turn it off when you're done.
* __Debug__: This will cause additional debug output to be generated - some of it will be visible in the interface, but most of it goes into the logs.

# FAQ

##### Where is the Plex Forum post for this plugin?

https://forums.plex.tv/discussion/107801/rel-audioaddict-radiotunes-com-di-fm-etc/p1

##### Do I need a Premium account?

Yes. You need a Premium account in order to get the __Listen Key__. Without that key, all you get are the free streams, which - while technically functional - no longer have music on them (just a message on loop).

##### I can't play the stream and/or I get a codec error - what's the deal?

As noted above, AAC support is inconsistent across devices, browsers, and clients. The only "safe" option is to use an MP3 stream (though AAC does often work).

##### I changed settings such as Preferred Stream in the preferences, but it didn't seem to do anything.

As noted above, any time you change a setting in preferences, you'll need to Force Refresh the service(s) you're interested in. Don't worry if it seems like it timed out the first time, and don't forget to _turn this flag back off when you're done_.

##### Does this work in Chromecast / iPad / HT / (insert whatever architecture you've got)?

Probably (see AAC vs. MP3 above, however).

# AudioAddict API

The sum total of all public knowledge concerning the AA API used to be available [here](http://tobiass.eu/api-doc.html); however, the server disappeared without a trace sometime in 2014.  There is an archived copy available on the [wayback machine](https://web.archive.org/web/20140426192326/http://tobiass.eu/api-doc.html).
