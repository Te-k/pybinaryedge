How to
======

Pybinaryedge is a python 3 Wrapper for the `BinaryEdge API <https://www.binaryedge.io/>`_, see the `APIv2 documentation <https://docs.binaryedge.io/api-v2/>`_ for more information.

Quick Start
-----------

Fist install the package through `Pypi <https://pypi.org/>`_ ``pip install pybinaryedge``, then configure the CLI tool and request your first IP::

    $ binaryedge config --key KEY
    $ binaryedge ip -i 149.202.178[.]130


Installation
------------

To install this tool, it is recommended to use `virtual environments <https://docs.python.org/3/tutorial/venv.html>`_.

You can install it directly from `pypi <https://pypi.org/>`_ wit
h ``pip install pybinaryedge``

You can Then you can install it directly from sources ::

    git clone https://github.com/Te-k/pybinaryedge.git
    cd pybinaryedge
    pip install .

If you use `pipenv <https://pipenv.readthedocs.io/en/latest/>`_, you can run instead ::

    git clone https://github.com/Te-k/pybinaryedge.git
    cd pybinaryedge
    pipenv install

You need to have an account on the `BinaryEdge platform <https://www.binaryedge.io/>`_, create an API key, and configure the CLI tool to use it with ``binaryedge config --key KEY``

API
---

Here is a quick example, see the full API documentation for more informationon all the functions available::

    from pybinaryedge import BinaryEdge

    be = BinaryEdge(API_KEY)
    # Iterate over the first page of IPs having specific ssh configuration
    search = 'ssh.algorithms.encryption.keyword:"aes256-cbc" ssh.banner.keyword:"SSH-2.0-OpenSSH_LeadSec"'
    for ip in be.host_search(search):
        print('%s': % ip['origin']['ip'])


Command-Line Interface
----------------------

This library also implement a command-line interface tool called ``binaryedge`` ::

    usage: binaryedge [-h] {config,ip,search,dataleaks} ...

    Request BinaryEdge API

    positional arguments:
      {config,ip,search,dataleaks}
                        Commands
        config              Configure pybinary edge
        ip                  Query an IP address
        search              Search in the database
        dataleaks           Search in the leaks database
	domains             Search information on a domain

    optional arguments:
      -h, --help            show this help message and exit

