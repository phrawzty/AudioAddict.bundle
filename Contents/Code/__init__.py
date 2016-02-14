"""Plex plugin for AudioAddict (sky.fm, di.fm, etc)."""
# pylint: disable=undefined-variable, relative-import, invalid-name, line-too-long

# Utility class
from audioaddict import AudioAddict
# Instantiate the utility object
AA = AudioAddict()

# Plex
MUSIC_PREFIX = '/music/audioaddict'

NAME = 'AudioAddict'

# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART = 'art-default.jpg'
ICON = 'icon-default.jpg'

####################################################################################################

def Start():
    """This is called when the plugin is loaded."""

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    ## see also:
    ##  http://dev.plexapp.com/docs/Objects.html
    ObjectContainer.title1 = NAME
    DirectoryObject.thumb = R(ICON)

    HTTP.CacheTime = CACHE_1HOUR

def ValidatePrefs():
    """This doesn't do anything useful yet."""

    pass


@handler(MUSIC_PREFIX, NAME, art=ART, thumb=ICON)
def MusicMainMenu():
    """The desired service is selected here."""

    oc = ObjectContainer()

    services = AA.get_validservices()

    for serv in sorted(services, key=services.get):
        oc.add(DirectoryObject(
            key=Callback(GetChannels, serv=serv),
            title=services[serv]
        ))

    return oc

@route(MUSIC_PREFIX + '/service')
def GetChannels(serv):
    """This produces the list of channels for a given service."""

    # Set some preferences. It really makes life easier if they're set.
    AA.set_service(serv)
    AA.set_listenkey(Prefs['listen_key'])
    AA.set_streampref(Prefs['stream_pref_' + serv])
    AA.set_sourcepref(Prefs['source_pref'])

    oc = ObjectContainer(title1=AA.get_servicename(serv))

    fmt = AA.get_streamdetails()['codec']
    bitrate = AA.get_streamdetails()['bitrate']

    for channel in AA.get_batchinfo(refresh=True):
        # Use the handy internal Dict api to avoid re-generating the streamurl
        # over and over.
        if (not channel['key'] in Dict) or (Prefs['force_refresh'] == True):
            Dict[channel['key']] = AA.get_streamurl(channel['key'])
            if Prefs['debug']:
                Log.Debug('saving %s' % Dict[channel['key']])

        oc.add(CreateChannelObject(
            url=Dict[channel['key']],
            title=channel['name'],
            summary=channel['description'],
            fmt=fmt,
            bitrate=bitrate,
            thumb='http:' + channel['asset_url']
        ))

    oc.objects.sort(key=lambda obj: obj.title)
    return oc

@route(MUSIC_PREFIX + '/channel')
def CreateChannelObject(
        url,
        title,
        summary,
        fmt,
        bitrate,
        thumb,
        include_container=False
    ):
    """Build yon streamable object, ye mighty."""

    if fmt == 'mp3':
        container = Container.MP3
        audio_codec = AudioCodec.MP3
    elif fmt == 'aac':
        container = Container.MP4
        audio_codec = AudioCodec.AAC

    # Display details for debugging purposes.
    debug_summary = []
    debug_summary.append(summary)
    if Prefs['debug']:
        debug_summary.append('[%s, %s]' % (fmt, bitrate))
        debug_summary.append('[%s]' % url)

    track_object = TrackObject(
        key=Callback(CreateChannelObject,
            url=url,
            title=title,
            summary=' '.join(debug_summary),
            fmt=fmt,
            bitrate=bitrate,
            thumb=thumb,
            include_container=True
            ),
        rating_key=url,
        title=title,
        summary=' '.join(debug_summary),
        thumb=thumb,
        items=[
            MediaObject(
                parts=[
                    PartObject(key=url)
                ],
                container=container,
                audio_codec=audio_codec,
                bitrate=bitrate,
                audio_channels=2,
                optimized_for_streaming=True
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects=[track_object])
    else:
        return track_object
