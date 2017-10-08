N.B. This README reflects the desired state of the project. Do not attempt to use the code at this point in time unless you like stuff that's broken.

zonetruck
=========
"It's not a series of tubes"

Zonetruck is not a series of tubes. It's a magical truck for your DNS zones.

Imagine a truck that comes to your internal corporate DNS server, loads up its DNS zone file while magically leaving behind any DNS records that are not for public consumption, and unloads sanitized copies of your zone file on any number of external DNS providers. Because the truck is magic, it can also fly and make deliveries into the cloud.

Zonetruck lets you forget about managing external DNS, keeping you as an administrator happy, while enabling an low-cost easy multi-provider high-availability strategy for your DNS with no vendor-lock-in, keeping your boss and your customers happy too.

That's also why I've tried to make zonetruck to run on anything that can run Python 3.3, no matter if it's your daughter's Raspberry Pi, your cousin's uncle's AS/400, or a x1.32xlarge Amazon EC2 instance with Windows Server with SQL Enterprise. Some might call it a flexible pay what you want as you go model ready for an accellerated on-premise hybrid cloud platform. I just smile and nod, and don't care what you run it on, but please, don't call me when it breaks when you try running it on jython on your neighbor's set top box.

Because zonetruck does not believe in vendor lock-in, it can ingest data from any system permitting zone transfers. It can live inside of your perimeter or outside, as long as it can get a zone transfer from your internal authoritative DNS server, it's happy.

It can deliver clean zone files to multiple destination systems, using those modern web API:s that all the cool kids are using, while leaving you, the system administrator, to use your existing tools for managing your internal DNS.

Zonetruck is simple and secure. It is configured with a single configuration file that fits on your screen. There is no admin panel, no role-based access control, no daemon, no enterprise middleware, no muss, no fuss. All you need is a Scheduled Task (on Windows) or a Cron Job (on Linux). Because Zonetruck needs no access to anything beyond its configuration file and network access to your authoritative DNS servers and your chosen API endpoints, it's really simple to lock down and secure, if you feel like you have to, despite its minimal attack surface.


Theory of operation
===================

When launched by a cron job, zonetruck will read the configuration file specified on the command line. (There is no reason zonetruck might not be launched manually, or even on receiving a notification from a master DNS server. That functionality will probably never be in zonetruck itself, but could be handled by a helper daemon.)

The configuration file is parsed for information about:

- the input zones to process, and corresponding master DNS servers
- the filters to apply on the zones
- the output external authoritative DNS services to upload the filtered zone to

For more complex scenarios, where you want differerent filtering or external DNS services on different zones, this can be accomplished by running several configuration files. This keeps zonetruck simple for easy use cases (most of them) and makes hard use cases possible.

The serial numbers of each the internal zone are queried by doing a DNS query to the configured master, and the serial numbers of the external zones are queried using functionality in the output plugins. (This could be optimized by caching the serial numbers of the external zones, but that would introduce state into zonetruck, and rob it of some of its magic. It's not like querying a serial number from DNS service is very expensive.)

Zone transfers are performed from a master DNS server, and then filtered on the fly based on the filter criteria.

IP-based filtering is based on a filtered IP/IPv6 address range, to find A and AAAA records to exclude.

Name-based filtering can also be based on a regex match of the name of a record.

Filter exceptions can be defined for both IP-based and name-based filters, using a first-match approach, similar to a firewall.

After the initial filtering pass, zonetruck prunes and CNAMEs, SRV records or MX records that point to filtered A and AAAA records. And because zonetruck does not judge you for pointing a MX, SRV, or CNAME to another CNAME, it will continue pruning until it has nothing left to prune.

With the filtered zones in memory, zonetruck uses the configured output plugins to upload the modified DNS zones to your external DNS services.

That's all. But, not really. I kinda lied. Because zonetruck is magical, all operations are run on multiple workers in a queue to make sure it doesn't take longer than needed to do its job.

If something goes wrong, it will throw a log message. Other than that, that's all. Really.

Configuring zonetruck
=====================

Zonetruck uses YAML for configuration files. Here's an example that should
be self-explanatory. Note that indentation levels matter, so you need to
keep your files nicely indented for zonetruck to understand them.

.. code:: yaml

    ---
    sources:
        -
            masters:
                - ns1.example.com
                - ns2.example.net
            zones:
                - example.com
                - example.net
        -
            masters:
                - ns1.other.example.com
            zones:
                - other.example.com
    filter_rules:
        -
            action: pass
            ip: 192.0.2.192/26
        -
            action: filter
            ip: 192.0.2.0/24
        -
            action: pass
            ipv6: 2001:db8:1234:5678::/64
        -
            action: block
            ipv6: 2001:db8::/32
        -
            action: pass
            fqdn_regex: '^internal.+\.other\.example\.com\.$'
        -
            action: block
            fqdn_regex: '^internal'
        -
            action: block
            fqdn_regex: '^secret'
    outputs:
        -
            type: zonefile
            path: /tmp/zonetruck-output-zone
        -
            type: random-cloud-service
            apikey: 12345 # Same as on my luggage
    ...


About the license
=================

The code is provided under the MIT license, because I believe in as little hassle as possible. If you want to make zonetruck a part of your clusterdumb enterprise bloatware, go right ahead. If you don't want to give your code back, I don't even want your code back. But if you're cool, I know you'll submit a pull request anyway. The last thing I want is for zonetruck to make one fewer sysadmin's life more awesome because of some ridiculous manager who heard something about the GPL being a computer virus.

----

Copyright (c) 2017 Per von Zweigbergk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
