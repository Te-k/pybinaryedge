# pybinaryedge

Python 3 Wrapper for the binary edge API https://www.binaryedge.io/

See the [APIv2 documentation](https://docs.binaryedge.io/api-v2/)

## Install

To install this tool :
```
git clone https://github.com/Te-k/pybinaryedge.git
cd pybinaryedge
pip install -r requirements.txt
```

You need to have an account on the [Binary Edge platform](https://www.binaryedge.io/), create an API key, and configure the CLI tool to use it with `binaryedge config --key KEY`

## API

Example :
```python
from pybinaryedge import BinaryEdge

be = BinaryEdge(API_KEY)
# Iterate over the first page of IPs having specific ssh configuration
search = 'ssh.algorithms.encryption.keyword:"aes256-cbc" ssh.banner.keyword:"SSH-2.0-OpenSSH_LeadSec"'
for ip in be.host_search(search):
    print('%s': % ip['origin']['ip'])
```

List of functions implemented :
* `host(IP)` : [Details about an Host](https://docs.binaryedge.io/api-v2/#v2queryiptarget)
* `host_historical(IP)` : [Details about an Host, with data up to 6 months](https://docs.binaryedge.io/api-v2/#v2queryiphistoricaltarget)
* `host_search(QUERY, PAGE)` : [List of recent events for the given query](https://docs.binaryedge.io/api-v2/#v2querysearch)
* `host_score(IP)` : [IP Scoring of an host.](https://docs.binaryedge.io/api-v2/#v2queryscoreiptarget)
* `image_ip(IP)` : [Details about Remote Desktops found on an Host](https://docs.binaryedge.io/api-v2/#v2queryimageipip)
* `image_search(QUERY, PAGE)` : [Remote Desktops based on a Query](https://docs.binaryedge.io/api-v2/#v2queryimagesearch)
* `image_tags()` : [Get the list of possible tags for the images](https://docs.binaryedge.io/api-v2/#v2queryimagetags)
* `torrent_ip(IP)` : [Details about torrents transferred by an Host](https://docs.binaryedge.io/api-v2/#v2querytorrentiptarget)
* `torrent_historical_ip(IP)` : [Details about torrents transferred by an Host, with data up to 6 months](https://docs.binaryedge.io/api-v2/#v2querytorrenthistoricaltarget)
* `dataleaks_email(EMAIL)` : [Verify which dataleaks affect the target email](https://docs.binaryedge.io/api-v2/#v2querydataleaksemailemail)
* `dataleaks_organization(DOMAIN)` : [Verify how many emails are affected by dataleaks for a specific domain](https://docs.binaryedge.io/api-v2/#v2querydataleaksorganizationdomain)
* `dataleaks_info()` : [Get the list of dataleaks our platform keeps track.](https://docs.binaryedge.io/api-v2/#v2querydataleaksinfo)

## CLI

This library also implements a CLI binaryedge tool :
```
binaryedge -h
usage: binaryedge [-h] {config,ip,search} ...

Request BinaryEdge API

positional arguments:
  {config,ip,search}  Commands
    config            Configure pybinary edge
    ip                Query an IP address
    search            Search in the database

optional arguments:
  -h, --help          show this help message and exit
```

Example :
```
$ binaryedge config --key KEY
$ binaryedge ip -i 149.202.178[.]130
{
    "events": [
        {
            "port": 27017,
            "results": [
                {
                    "origin": {
                        "country": "sg",
                        "ip": "172.104.173.35",
                        "module": "grabber",
                        "ts": 1536782325059,
                        "type": "service-simple"
[SNIP]
```

## License

This code is published under MIT license
