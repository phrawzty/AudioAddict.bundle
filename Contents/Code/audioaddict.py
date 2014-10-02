"""AudioAddict utility class."""

# pylint: disable=line-too-long, old-style-class, broad-except
# This is based entirely on http://tobiass.eu/api-doc.html (thanks!)

import urllib2
import json
import random

class AudioAddict:
    """AudioAddict utility class."""

    def __init__(self):
        """Init. You know."""

        self.listenkey = None

        # Valid streaming services according to audioaddict.com.
        self.validservices = {
            'sky': 'Sky.fm',
            'di': 'DI.fm',
            'jazzradio': 'JazzRadio.com',
            'rockradio': 'RockRadio.com'
        }

        # Each service proposes a selection of stream types.
        # It's worth noting that public3 is the *only* common type.
        self.validstreams = {
            'di': {
                'android_low':              {'codec': 'aac', 'bitrate':  40},
                'android':                  {'codec': 'aac', 'bitrate':  64},
                'android_high':             {'codec': 'mp3', 'bitrate':  96},
                'android_premium_low':      {'codec': 'aac', 'bitrate':  40},
                'android_premium_medium':   {'codec': 'aac', 'bitrate':  64},
                'android_premium':          {'codec': 'aac', 'bitrate': 128},
                'android_premium_high':     {'codec': 'mp3', 'bitrate': 256},
                'public1':                  {'codec': 'aac', 'bitrate':  64},
                'public2':                  {'codec': 'aac', 'bitrate':  40},
                'public3':                  {'codec': 'mp3', 'bitrate':  96},
                'premium_low':              {'codec': 'aac', 'bitrate':  40},
                'premium_medium':           {'codec': 'aac', 'bitrate':  64},
                'premium':                  {'codec': 'aac', 'bitrate': 128},
                'premium_high':             {'codec': 'mp3', 'bitrate': 256}
           },
            'sky': {
                'appleapp_low':             {'codec': 'aac', 'bitrate':  40},
                'appleapp':                 {'codec': 'aac', 'bitrate':  64},
                'appleapp_high':            {'codec': 'mp3', 'bitrate':  96},
                'appleapp_premium_medium':  {'codec': 'aac', 'bitrate':  64},
                'appleapp_premium':         {'codec': 'aac', 'bitrate': 128},
                'appleapp_premium_high':    {'codec': 'mp3', 'bitrate': 256},
                'public1':                  {'codec': 'aac', 'bitrate':  40},
                'public3':                  {'codec': 'mp3', 'bitrate':  96},
                'public5':                  {'codec': 'wma', 'bitrate':  40},
                'premium_low':              {'codec': 'aac', 'bitrate':  40},
                'premium_medium':           {'codec': 'aac', 'bitrate':  64},
                'premium':                  {'codec': 'aac', 'bitrate': 128},
                'premium_high':             {'codec': 'mp3', 'bitrate': 256}
           },
            'jazzradio': {
                'appleapp_low':             {'codec': 'aac', 'bitrate':  40},
                'appleapp':                 {'codec': 'aac', 'bitrate':  64},
                'appleapp_premium_medium':  {'codec': 'aac', 'bitrate':  64},
                'appleapp_premium':         {'codec': 'aac', 'bitrate': 128},
                'appleapp_premium_high':    {'codec': 'mp3', 'bitrate': 256},
                'public1':                  {'codec': 'aac', 'bitrate':  40},
                'public3':                  {'codec': 'mp3', 'bitrate':  64},
                'premium_low':              {'codec': 'aac', 'bitrate':  40},
                'premium_medium':           {'codec': 'aac', 'bitrate':  64},
                'premium':                  {'codec': 'aac', 'bitrate': 128},
                'premium_high':             {'codec': 'mp3', 'bitrate': 256}
           },
            'rockradio': {
                'android_low':              {'codec': 'aac', 'bitrate':  40},
                'android':                  {'codec': 'aac', 'bitrate':  64},
                'android_premium_medium':   {'codec': 'aac', 'bitrate':  64},
                'android_premium':          {'codec': 'aac', 'bitrate': 128},
                'android_premium_high':     {'codec': 'mp3', 'bitrate': 256},
                'public3':                  {'codec': 'mp3', 'bitrate':  96},
           }
        }

        self.streampref = 'public3'
        self.sourcepref = None

        self.service = None
        self.chanlist = []

        # All streaming services use a common API service.
        self.apihost = 'api.audioaddict.com'

        # The batch API endpoint requires a static dummy auth header.
        self.authheader = ['Authorization', 'Basic ZXBoZW1lcm9uOmRheWVpcGgwbmVAcHA=']
        self.batchinfo = {}

    def get_apihost(self, url=True, ssl=False):
        """Get the AA API host; normally used as part of a URL."""

        if url == False:
            return self.apihost

        obj = '://' + self.apihost + '/v1'

        if ssl == True:
            obj = 'https' + obj
        else:
            obj = 'http' + obj

        return obj

    def set_listenkey(self, listenkey=None):
        """Set the listen_key."""

        self.listenkey = listenkey

    def get_listenkey(self, url=True):
        """Get the listen_key; normally used as part of a URL."""

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

        if serv == None:
            serv = self.get_service()

        if not serv in self.get_validservices().keys():
            raise Exception('Invalid service')

        return self.validservices[serv]

    def get_validstreams(self):
        """Get the list of valid streams (extended mix)."""

        return self.validstreams

    def get_serviceurl(self, serv=None, prefix='listen'):
        """Get the service URL for the service we're using."""

        if serv == None:
            serv = self.get_service()

        url = 'http://' + prefix + '.' + self.get_servicename(serv)
        url = url.lower()

        return url

    def set_streampref(self, stream=None):
        """Set the preferred stream (extended mix)."""

        if not stream in self.get_validstreams()[self.get_service()]:
            raise Exception('Invalid stream')

        self.streampref = stream

    def get_streamdetails(self):
        """Get the details for a stream (extended mix)."""

        details = {}
        validstreams = self.get_validstreams()
        stream = self.get_streampref()

        if stream in validstreams[self.get_service()]:
            details = validstreams[self.get_service()][stream]

        return details

    def get_streampref(self):
        """Get the preferred stream."""

        return self.streampref

    def set_sourcepref(self, source=None):
        """Set the preferred source."""

        self.sourcepref = source

    def get_sourcepref(self):
        """Get the preferred source."""

        return self.sourcepref

    def get_chanlist(self, refresh=False):
        """Get the master channel list."""

        if len(self.chanlist) < 1 or refresh == True:
            try:
                data = urllib2.urlopen(self.get_serviceurl() + '/' + self.get_streampref())
                self.chanlist = json.loads(data.read())
            except Exception:
                raise

        return self.chanlist

    def get_chaninfo(self, key):
        """Get the info for a particular channel."""

        chaninfo = None

        for chan in self.get_chanlist():
            if chan['key'] == key:
                chaninfo = chan.copy()

        if chaninfo == None:
            raise Exception('Invalid channel')

        return chaninfo

    def get_streamurl(self, key):
        """Generate a streamable URL for a channel."""

        channelurl = self.get_serviceurl() + '/' + self.get_streampref() + '/' + key + self.get_listenkey()

        data = urllib2.urlopen(channelurl)
        sources = json.loads(data.read())

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

    def get_chanhist(self, key):
        """Get track history for a channel."""

        servurl = self.get_apihost() + '/' + self.get_service() + '/' + 'track_history/channel/' + str(self.get_chaninfo(key)['id'])

        data = urllib2.urlopen(servurl)
        history = json.loads(data.read())

        return history

    def get_nowplaying(self, key):
        """Get current track for a channel."""

        # Normally the current song is position 0, but if an advertisement
        # was played in the public stream, it will pollute the history -
        # in that case, we pick the track from position 1.

        track = 'Unknown - Unknown'

        if not 'ad' in self.get_chanhist(key)[0]:
            track = self.get_chanhist(key)[0]['track']
        else:
            track = self.get_chanhist(key)[1]['track']

        return track

    def get_batchinfo(self, refresh=False):
        """Get the massive batch info blob."""

        if (len(self.batchinfo) > 0) and refresh == False:
            return self.batchinfo

        url = self.get_apihost() + '/' + self.get_service() + '/mobile/batch_update?stream_set_key=' + self.get_streampref()

        req = urllib2.Request(url)
        req.add_header(*self.authheader)
        data = urllib2.urlopen(req).read()

        batch = json.loads(data)

        # Only the "All" channel filter is interesting for now.
        for i in batch['channel_filters']:
            if i['name'] == 'All':
                self.batchinfo = i['channels']
                return self.batchinfo
