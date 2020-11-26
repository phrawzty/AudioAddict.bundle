"""AudioAddict utility class."""

# pylint: disable=line-too-long, old-style-class, broad-except, too-many-instance-attributes

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
            'radiotunes': 'RadioTunes.com',
            'di': 'DI.fm',
            'jazzradio': 'JazzRadio.com',
            'rockradio': 'RockRadio.com',
            'classicalradio': 'ClassicalRadio.com',
            'zenradio': 'ZenRadio.com',
        }

        # Each service proposes a selection of stream types.
        # It's worth noting that public3 is the *only* common type.
        self.validstreams = {
            'premium_medium':           {'codec': 'aac', 'bitrate':  64},
            'premium':                  {'codec': 'aac', 'bitrate': 128},
            'premium_high':             {'codec': 'mp3', 'bitrate': 320},
        }

        self.streampref = 'premium_high'
        self.sourcepref = None

        self.service = None
        self.chanlist = []

        # All streaming services use a common API service.
        self.apihost = 'api.audioaddict.com'

        # The batch API endpoint requires a static dummy auth header.
        self.authheader = ['Authorization', 'Basic ZXBoZW1lcm9uOmRheWVpcGgwbmVAcHA=']
        self.batchinfo = {}

    def get_apihost(self, host_only=False, ssl=False):
        """Get the AA API host; normally used as part of a URL."""

        if host_only:
            return self.apihost

        obj = '://' + self.apihost + '/v1'

        if ssl:
            obj = 'https' + obj
        else:
            obj = 'http' + obj

        return obj

    def set_listenkey(self, listenkey=None):
        """Set the listen_key."""

        self.listenkey = listenkey

    def get_listenkey(self, key_only=False):
        """Get the listen_key; normally used as part of a URL."""

        if not self.listenkey:
            return ''
        elif key_only:
            return self.listenkey
        else:
            return '?listen_key=' + self.listenkey

    def get_validservices(self):
        """Get list of valid services."""

        return self.validservices

    def set_service(self, serv=None):
        """Set which service we're using."""

        if serv not in self.validservices.keys():
            raise Exception('Invalid service')

        self.service = serv

    def get_service(self):
        """Get which service we're using."""

        return self.service

    def get_servicename(self, serv=None):
        """Get the name of a given service."""

        if not serv:
            serv = self.get_service()

        if serv not in self.get_validservices().keys():
            raise Exception('Invalid service')

        return self.validservices[serv]

    def get_validstreams(self):
        """Get the list of valid streams."""

        return self.validstreams

    def get_serviceurl(self, serv=None, prefix='listen'):
        """Get the service URL for the service we're using."""

        if not serv:
            serv = self.get_service()

        url = 'http://' + prefix + '.' + self.get_servicename(serv)
        url = url.lower()

        return url

    def set_streampref(self, stream=None):
        """Set the preferred stream."""

        if stream not in self.get_validstreams():
            raise Exception('Invalid stream')

        self.streampref = stream

    def get_streamdetails(self):
        """Get the details for a stream."""

        details = {}
        stream = self.get_streampref()

        if stream in self.get_validstreams():
            details = self.get_validstreams()[stream]

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

        if not self.chanlist or refresh:
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

        if not chaninfo:
            raise Exception('Invalid channel')

        return chaninfo

    def get_chanhist(self, key):
        """Get track history for a channel."""

        servurl = self.get_apihost() + '/' + self.get_service() + '/track_history/channel/' + \
            str(self.get_chaninfo(key)['id'])

        data = urllib2.urlopen(servurl)
        history = json.loads(data.read())

        return history

    def get_nowplaying(self, key):
        """Get current track for a channel."""

        # Normally the current song is position 0, but if an advertisement
        # was played in the public stream, it will pollute the history -
        # in that case, we pick the track from position 1.

        track = 'Unknown - Unknown'

        if 'ad' not in self.get_chanhist(key)[0]:
            track = self.get_chanhist(key)[0]['track']
        else:
            track = self.get_chanhist(key)[1]['track']

        return track

    def get_batchinfo(self, refresh=False):
        """Get the massive batch info blob."""

        if self.batchinfo and not refresh:
            return self.batchinfo

        url = self.get_apihost() + '/' + self.get_service() + '/mobile/batch_update?stream_set_key=' + \
            self.get_streampref()

        req = urllib2.Request(url)
        req.add_header(*self.authheader)
        # AA started gzip compressing (just) this response in June 2017.
        req.add_header('Accept-Encoding', 'gzip')

        response = urllib2.urlopen(req)

        # This may or may not be a permanent change, so we'll wrap this in a
        # conditional for now. Also, if other endpoints start returning gzip'd
        # data, this should be implemented more generically. OK for today tho.
        if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO(response.read())
            obj = gzip.GzipFile(fileobj=buf)
            data = obj.read()

        batch = json.loads(data)

        # Only the "All" channel filter is interesting for now.
        for i in batch['channel_filters']:
            if i['name'] == 'All':
                batchinfo = i['channels']
                for channel in batchinfo:
                    for ss_channel in batch['stream_sets'][0]['streamlist']['channels']:
                        if channel['id'] == ss_channel['id']:
                            streamurl = None
                            # Look through the list for the preferred source.
                            if self.get_sourcepref():
                                for stream in ss_channel['streams']:
                                    if self.get_sourcepref() in stream['url']:
                                        streamurl = stream['url']

                            # If there is no preferred source or one was not found, pick at random.
                            if not streamurl:
                                streamurl = random.choice([x['url'] for x in ss_channel['streams']])

                            if streamurl:
                                channel['streamurl'] = streamurl + '?' + self.get_listenkey(key_only=True)

                self.batchinfo = batchinfo
                return self.batchinfo
