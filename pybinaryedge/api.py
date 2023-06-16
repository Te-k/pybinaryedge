#! /usr/bin/env python3

"""
    pybinaryedge
    ~~~~~~~~~~~~

    Python 3 Wrapper for the BinaryEdge API https://www.binaryedge.io/
    https://github.com/Te-k/pybinaryedge

    :copyright: Tek
    :license: MIT Licence

"""

import requests
import ipaddress
import urllib3

class BinaryEdgeException(Exception):
    """
    Exception raised if a request to BinaryEdge returns anything else than 200
    """

    def __init__(self, message):
        self.message = message
        Exception.__init__(self, message)


class BinaryEdgeNotFound(BinaryEdgeException):
    """
    Exception raised if a request to BinaryEdge returns a 404 code
    """

    def __init__(self):
        self.message = 'Search term not found'
        BinaryEdgeException.__init__(self, self.message)


class BinaryEdge(object):
    """
    Initializes a new instance of the BinaryEdge class.

    Args:
        key: The BinaryEdge API key
        verify: Enable or disable SSL verification. Default is enabled.
    """

    def __init__(self, key, verify=True):
        self.key = key
        self.base_url = 'https://api.binaryedge.io/v2/'
        self.ua = 'pybinaryedge https://github.com/Te-k/pybinaryedge'
        self.requests = requests.Session()
        self.requests.verify = verify
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _get(self, url, params={}):
        headers = {'X-Key': self.key, 'User-Agent': self.ua}
        r = self.requests.get(self.base_url + url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            if r.status_code == 404:
                raise BinaryEdgeNotFound()
            else:
                raise BinaryEdgeException(
                    'Invalid return code %i' % r.status_code
                )

    def _is_ip(self, ip):
        """
        Test that the given string is an IPv4/IPv6 address or CIDR

        Args:
            ip: IP address

        Returns:
            a string containing the IP address without bracket

        Raises:
            ValueError: if the string given is not a valid IPv4 address
        """
        try:
            return str(ipaddress.ip_address(ip))
        except:
            pass

        try:
            return str(ipaddress.ip_network(ip, strict=False))
        except:
            raise ValueError('Invalid IP address')

    def host(self, ip):
        """
        Details about an Host. List of recent events for the specified host,
        including details of exposed ports and services.
        https://docs.binaryedge.io/api-v2/#host

        Args:
            ip: IP address (string)

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/ip/' + self._is_ip(ip))

    def host_vulnerabilities(self, ip):
        """
        Give list of CVE vulnerabilities that may affect a given IP

        Args:
            ip: IP address (string)

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/cve/ip/' + self._is_ip(ip))

    def host_historical(self, ip):
        """
        Details about an Host, with data up to 6 months.
        List of events for the specified host, with events for each time that:
        * A port was detected open
        * A service was found running
        * Other modules were successfully executed
        https://docs.binaryedge.io/api-v2/#v2queryiphistoricaltarget

        Args:
            ip: IPv4 address

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/ip/historical/' + self._is_ip(ip))

    def host_search(self, query, page=1):
        """
        Events based on a Query. List of recent events for the given query,
        including details of exposed ports and services. Can be used with
        specific parameters and/or full-text search.
        https://docs.binaryedge.io/api-v2/#v2querysearch

        Args:
            query: Search query in BinaryEdge
            page: page number

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/search', params={'query': query, 'page': page})

    def host_score(self, ip):
        """
        IP Risk Score. Scoring is based on all information found on our
        databases regarding an IP and refers to the level of exposure of
        a target, i.e, the higher the score, the greater the risk of
        exposure. https://docs.binaryedge.io/api-v2/#v2queryscoreiptarget

        Args:
            ip: IPv4 address

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/score/ip/' + self._is_ip(ip))

    def image_ip(self, ip):
        """
        Details about Remote Desktops found on an Host. List of screenshots
        and details extracted from them for the specified host, including OCR
        and whether faces were found or not, with data up to 2 months.
        https://docs.binaryedge.io/api-v2/#v2queryimageipip

        Args:
            ip: IPv4 address

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/image/ip/' + self._is_ip(ip))

    def image_search(self, query, page=1):
        """
        Remote Desktops based on a Query. List of screenshots and details
        extracted from them for the given query, including OCR and whether
        faces were found or not. Can be used with specific parameters and/or
        full-text search.
        https://docs.binaryedge.io/api-v2/#v2queryimagesearch

        Args:
            query: Search query in BinaryEdge
            page: page number

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get(
            'query/image/search',
            params={'query': query, 'page': page}
        )

    def image_tags(self):
        """
        Get the list of possible tags for the images
        https://docs.binaryedge.io/api-v2/#v2queryimagetags

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/image/tags')

    def torrent_ip(self, ip):
        """
        Details about torrents transferred by an Host. List of recent
        torrent events for the specified host, including details of the
        peer and torrent.
        https://docs.binaryedge.io/api-v2/#v2querytorrentiptarget

        Args:
            ip: IPv4 address

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/torrent/ip/' + self._is_ip(ip))

    def torrent_historical_ip(self, ip):
        """
        Details about torrents transferred by an Host, with data up to 6 months
        List of torrent events for the specified host, with events for each
        time that a new transfer was detected on the DHT.
        https://docs.binaryedge.io/api-v2/#v2querytorrenthistoricaltarget

        Args:
            ip: IPv4 address

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/torrent/historical/' + self._is_ip(ip))

    def dataleaks_email(self, email):
        """
        Allows you to search across multiple data breaches to see if any of
        your email addresses has been compromised.
        https://docs.binaryedge.io/api-v2/#v2querydataleaksemailemail

        Args:
            email: email address

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeNotFound: if the email address is not found by BE
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/dataleaks/email/' + email)

    def dataleaks_organization(self, domain):
        """
        Verify how may emails are affected by dataleaks for a specific domain
        We don't provide the list of affected emails.
        https://docs.binaryedge.io/api-v2/#v2querydataleaksorganizationdomain

        Args:
            email: email address

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/dataleaks/organization/' + domain)

    def dataleaks_info(self):
        """
        Get the list of dataleaks our platform keeps track.
        https://docs.binaryedge.io/api-v2/#v2querydataleaksinfo

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned by BE
        """
        return self._get('query/dataleaks/info')

    def domain_subdomains(self, domain, page=1):
        """
        Get a list of known subdomains for this domain
        https://docs.binaryedge.io/api-v2/#v2querydomainssubdomaintarget

        Args:
            domain: domain queried
            page: page result (default is 1)

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned
        """
        return self._get(
            'query/domains/subdomain/' + domain,
            params={'page': page}
        )

    def domain_dns(self, domain, page=1):
        """
        Return list of dns results known from the target domain.
        https://docs.binaryedge.io/api-v2/#v2querydomainsdnstarget

        Args:
            domain: domain queried
            page: page result (default is 1)

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned
        """
        return self._get('query/domains/dns/' + domain, params={'page': page})

    def domain_ip(self, ip, page=1):
        """
        Return records that have the specified IP in their A or AAAA records.
        https://docs.binaryedge.io/api-v2/#v2querydomainsiptarget

        Args:
            IP: IP address queried
            page: page result (default is 1)

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned
        """
        return self._get(
            'query/domains/ip/' + self._is_ip(ip),
            params={'page': page}
        )

    def domain_search(self, query, page=1):
        """
        List of Domains/DNS data based on a Query.
        Can be used with specific parameters and/or full-text search.
        https://docs.binaryedge.io/api-v2/#v2querydomainssearch

        Args:
            query: Search query in BinaryEdge
            page: page result (default is 1)

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned
        """
        return self._get(
            'query/domains/search',
            params={'query': query, 'page': page}
        )

    def sensor_ip(self, target):
        """
        Details about an Scanner. List of recent events form the specified host,
        including details of scanned ports, payloads and tags.
        https://docs.binaryedge.io/api-v2/#v2querysensorsiptarget

        Args:
            target: [String] target IP address or CIDR up to /24

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned
            BinaryEdgeNotFound: if the target has not been seen by sensors
        """
        return self._get('query/sensors/ip/%s' % target)

    def sensor_search(self, query, page=1):
        """
        Events based on a Query. List of recent events for the given query,
        including details of scanned ports, payloads and tags. Can be used
        with specific parameters and/or full-text search.
        https://docs.binaryedge.io/api-v2/#v2querysensorssearch

        Args:
            query: [String] String used to query our data. If no filters are
                used, it will perform a full-text search on the entire events
            page: [Int] Optional. Default 1, Maximum: 500 (10,000 results)

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned

        Example:
            be.sensor_search('tags:ssh_scanner')
        """
        return self._get(
            'query/sensors/search',
            params={'query': query, 'page': page}
        )

    def sensor_search_stats(self, query, type, days=60):
        """
        Statistics of events for the given query. Can be used with specific
        parameters and/or full-text search.
        https://docs.binaryedge.io/api-v2/#v2querysensorssearchstats

        Args:
            query: [String] String used to query our data. If no filters are
                used, it will perform a full-text search on the entire events.
            type: [String] Type of statistic we want to obtain.
                Possible types include: ports, tags, countries, asn, ips,
                payloads, http_path.
            days: [Integer] Number of days to get the stats for.
                For example days=1 for the last day of data.

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned
                or if type is not correct

        Example:
            be.sensor_search_stats('tags:ssh_scanner', 'ports')
        """
        if type not in ['ports', 'tags', 'countries', 'asn', 'ips',
                    'payloads', 'http_path']:
            raise BinaryEdgeException('Invalid type')
        return self._get('query/sensors/search/stats',
                params={
                    'query': query,
                    'type': type,
                    'days': days
                }
        )

    def stats(self, query, type, page=1):
        """
        Statistics of recent events for the given query. Can be used with
        specific parameters and/or full-text search.
        https://docs.binaryedge.io/api-v2/#v2querysearchstats

        Args:
            query: String used to query our data
            type: Type of statistic we want to obtain. Possible types include:
                ports, products, versions, tags, services, countries, asn.
            page: page result (default is 1)

        Returns:
            A dict created from the JSON returned by BinaryEdge

        Raises:
            BinaryEdgeException: if anything else than 200 is returned
        """
        if type not in ['ports', 'products', 'versions', 'tags', 'services',
                'countries', 'asn']:
            raise BinaryEdgeException('Invalid type')
        return self._get(
            'query/search/stats',
            params={
                'query': query,
                'type': type,
                'page': page
            }
        )
