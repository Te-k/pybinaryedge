import requests
import re


class BinaryEdgeException(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, message)


class BinaryEdge(object):
    def __init__(self, key):
        self.key = key
        self.base_url = 'https://api.binaryedge.io/v2/'
        self.ua = 'pybinaryedge https://github.com/Te-k/pybinaryedge'

    def _get(self, url, params={}):
        headers = {'X-Key': self.key, 'User-Agent': self.ua}
        r = requests.get(self.base_url + url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            raise BinaryEdgeException('Invalid return code %i' % r.status_code)

    def _is_ip(self, ip):
        """
        Test that the given string is an IPv4 address
        Otherwise raise ValueError
        Remove brackets around dots added for IOCs
        """
        ip = ip.replace("[.]", ".")
        if not re.match('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', ip):
            raise ValueError('Invalid IP address')
        return ip

    def host(self, ip):
        """
        Details about an Host. List of recent events for the specified host,
        including details of exposed ports and services.
        https://docs.binaryedge.io/api-v2/#host
        """
        return self._get('query/ip/' + self._is_ip(ip))

    def host_historical(self, ip):
        """
        Details about an Host, with data up to 6 months.
        List of events for the specified host, with events for each time that:
        - A port was detected open
        - A service was found running
        - Other modules were successfully executed
        https://docs.binaryedge.io/api-v2/#v2queryiphistoricaltarget
        """
        return self._get('query/ip/historical/' + self._is_ip(ip))

    def host_search(self, query, page=1):
        """
        Events based on a Query. List of recent events for the given query,
            including details of exposed ports and services. Can be used with
            specific parameters and/or full-text search.
        https://docs.binaryedge.io/api-v2/#v2querysearch
        """
        return self._get('query/search', params={'query': query, 'page': page})

    def host_score(self, ip):
        """
        IP Scoring of an host. Scoring is based on all information found on
        our databases regarding an IP and refers to the level of exposure
        of a target, i.e, the higher the score, the greater the risk exposure
        https://docs.binaryedge.io/api-v2/#v2queryscoreiptarget
        """
        return self._get('query/score/ip/' + self._is_ip(ip))

    def image_ip(self, ip):
        """
        Details about Remote Desktops found on an Host. List of screenshots
        and details extracted from them for the specified host, including OCR
        and whether faces were found or not, with data up to 2 months.
        https://docs.binaryedge.io/api-v2/#v2queryimageipip
        """
        return self._get('query/image/ip/' + self._is_ip(ip))

    def image_search(self, query, page=1):
        """
        Remote Desktops based on a Query. List of screenshots and details
        extracted from them for the given query, including OCR and whether
        faces were found or not. Can be used with specific parameters and/or
        full-text search.
        https://docs.binaryedge.io/api-v2/#v2queryimagesearch
        """
        return self._get(
            'query/image/search',
            params={'query': query, 'page': page}
        )

    def image_tags(self):
        """
        Get the list of possible tags for the images
        https://docs.binaryedge.io/api-v2/#v2queryimagetags
        """
        return self._get('query/image/tags')

    def torrent_ip(self, ip):
        """
        Details about torrents transferred by an Host. List of recent
        torrent events for the specified host, including details of the
        peer and torrent.
        https://docs.binaryedge.io/api-v2/#v2querytorrentiptarget
        """
        return self._get('query/torrent/ip/' + self._is_ip(ip))

    def torrent_historical_ip(self, ip):
        """
        Details about torrents transferred by an Host, with data up to 6 months
        List of torrent events for the specified host, with events for each
        time that a new transfer was detected on the DHT.
        https://docs.binaryedge.io/api-v2/#v2querytorrenthistoricaltarget
        """
        return self._get('query/torrent/historical/' + self._is_ip(ip))

    def dataleaks_email(self, email):
        """
        Allows you to search across multiple data breaches to see if any of
        your email addresses has been compromised.
        https://docs.binaryedge.io/api-v2/#v2querydataleaksemailemail
        """
        return self._get('query/dataleaks/email/' + email)

    def dataleaks_organization(self, domain):
        """
        Verify how may emails are affected by dataleaks for a specific domain
        We don't provide the list of affected emails.
        https://docs.binaryedge.io/api-v2/#v2querydataleaksorganizationdomain
        """
        return self._get('query/dataleaks/organization/' + domain)

    def dataleaks_info(self):
        """
        Get the list of dataleaks our platform keeps track.
        https://docs.binaryedge.io/api-v2/#v2querydataleaksinfo
        """
        return self._get('query/dataleaks/info')
