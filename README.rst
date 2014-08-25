========
NameSilo
========

A simple wrapper for the NameSilo API_.

.. _API: https://www.namesilo.com/api_reference.php

Install
--------

To install via pip:

    pip install namesilo

Usage
------

Instantiating the client:

    import namesilo

    # By default the client initializes in sandbox mode
    ns = namesilo.NameSilo('API KEY HERE')

    # Instantitate in live mode
    ns = namesilo.NameSilo('API KEY HERE', live=True)

From here you can call operations like so:

    ns.register_domain(domain='yourdomain.com', years='1')

Operations
----------

This client renames the operations to follow a more consistent convention of
(verb)_(subject). See *namesilo.NAMESILO_OPERATIONS* to seehow these method
names map to their NameSilo counterparts. The goal of this mapping its to make
the API more intuitive.
