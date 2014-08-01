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
ICON = 'icon-default.png'

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
    AA.set_streampref(Prefs['stream_pref'])
    AA.set_sourcepref(Prefs['source_pref'])
    #TODO: Prefs['force_refresh'] boolean which clears the chanlist and
    # the Dict (streamurls).

    oc = ObjectContainer(title1=AA.get_servicename(serv))

    for channel in AA.get_chanlist(refresh=True):
        # Use the handy internal Dict api to avoid re-generating the streamurl
        # over and over.
        if not channel['key'] in Dict:
            Dict[channel['key']] = AA.get_streamurl(channel['key'])

        oc.add(CreateChannelObject(
            url=Dict[channel['key']],
            title=channel['name'],
            summary=channel['key'],
            fmt='mp3',
            thumb=AA.get_batch_chanthumb(channel['key'])
        ))

    return oc

@route(MUSIC_PREFIX + '/channel')
def CreateChannelObject(
        url,
        title,
        summary,
        fmt,
        thumb,
        include_container=False
    ):
    """Build yon streamable object, ye mighty."""

    if fmt == 'mp3':
        container = Container.MP3
        audio_codec = AudioCodec.MP3
    elif fmt == 'aac':      # Maybe this will work in the future.
        container = Container.MP4
        audio_codec = AudioCodec.AAC

    track_object = TrackObject(
        key=Callback(CreateChannelObject,
            url=url,
            title=title,
            summary=summary,
            fmt=fmt,
            include_container=True
            ),
        rating_key=url,
        title=title,
        summary=summary,
        thumb=thumb,
        items=[
            MediaObject(
                parts=[
                    PartObject(key=url)
                ],
                container=container,
                audio_codec=audio_codec,
                bitrate=128,    # this is never correct :P
                audio_channels=2
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects=[track_object])
    else:
        return track_object
