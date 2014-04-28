"""AudioAddict utility class."""

# pylint: disable=line-too-long, old-style-class, broad-except
# This is based entirely on http://tobiass.eu/api-doc.html (thanks!)

import urllib
import json
import random

class AudioAddict:
    """AudioAddict utility class."""


    def __init__(self):
        """Init. You know."""


        self.listenkey = None
        self.validservices = {
                'sky': 'Sky.fm',
                'di': 'DI.fm',
                'jazz': 'JazzRadio.com',
                'rock': 'RockRadio.com'
                }
        self.service = None
        self.streamlist = []
        # Can't get AAC to play back, so MP3-only for now.
        self.validstreams = [
                'public3',
                'premium_high',
                'android_premium_high' # rockradio only
                ]
        # public3 is the only endpoint common to all services.
        self.streampref = 'public3'
        self.sourcepref = None

    def set_listenkey(self, listenkey=None):
        """Set the listen_key."""

        self.listenkey = listenkey

    def get_listenkey(self, url=True):
        """Get the listen_key; generally only used as part of a URL."""

        if self.listenkey == None:
            return ''
        elif url == False:
            return self.listenkey
        else:
            return '?listen_key=' + self.listenkey

    def get_validservices(self):
        """Get list of valid services."""

        return self.validservices

    def set_service(self, serv=None):
        """Set which service we're using."""

        if not serv in self.validservices.keys():
            raise Exception('Invalid service')

        self.service = serv

    def get_service(self):
        """Get which service we're using."""

        return self.service

    def get_servicename(self, serv=None):
        """Get the name of a given service."""

        if not serv in self.get_validservices().keys():
            raise Exception('Invalid service')

        return self.validservices[serv]

    def get_validstreams(self):
        """Get the list of valid streams."""

        return self.validstreams

    def get_serviceurl(self):
        """Get the service URL for the service we're using."""

        if self.get_service() == 'di':
            return 'http://listen.di.fm'
        elif self.get_service() == 'sky':
            return 'http://listen.sky.fm'
        elif self.get_service() == 'rock':
            return 'http://listen.rockradio.com'
        elif self.get_service() == 'jazz':
            return 'http://listen.jazzradio.com'

    def set_streampref(self, stream=None):
        """Set the preferred stream."""

        if not stream in self.get_validstreams():
            raise Exception('Invalid stream')

        self.streampref = stream

    def get_streampref(self):
        """Get the preferred stream."""

        return self.streampref

    def set_sourcepref(self, source=None):
        """Set the preferred source."""

        self.sourcepref = source

    def get_sourcepref(self):
        """Get the preferred source."""

        return self.sourcepref

    def get_streamlist(self, refresh=False):
        """Get the master channel (stream) list."""

        if len(self.streamlist) < 1 or refresh == True:
            try:
                # Pull from public3 because it's the only endpoint common to
                # all services.
                data = urllib.urlopen(self.get_serviceurl() + '/' + self.get_streampref())
                self.streamlist = json.loads(data.read())
            except Exception:
                raise

        return self.streamlist

    def get_streamurl(self, key):
        """Generate a streamable URL for a channel."""

        channelurl = self.get_serviceurl() + '/' + self.get_streampref() + '/' + key + self.get_listenkey()

        data = urllib.urlopen(channelurl)
        sources = json.loads(data.read())

        # If there's no preferred source, just pick one at random.
        # Otherwise, look through the list for a match to the preferred source.
        # Fallback to random.
        streamurl = None

        # Look through the list for the preferred source.
        if not self.get_sourcepref() == None:
            for source in sources:
                if self.get_sourcepref() in source:
                    streamurl = source

        # If there is no preferred source or one was not found, pick at random.
        if streamurl == None:
            streamurl = (random.choice(sources))

        return streamurl
