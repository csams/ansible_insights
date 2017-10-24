#!/usr/bin/env python
from __future__ import print_function
from collections import namedtuple

from insights import get_active_lines, parser, Parser
from insights import make_response, rule
from insights.core.spec_factory import SpecFactory
from insights.parsers.redhat_release import RedhatRelease

sf = SpecFactory()
hosts = sf.simple_file("/etc/hosts", name="hosts")


@parser(hosts)
class HostParser(Parser):
    Host = namedtuple("Host", ["ip", "host", "aliases"])

    def parse_content(self, content):
        self.hosts = []
        for line in get_active_lines(content):
            # remove inline comments
            line = line.partition("#")[0].strip()

            # break the line into parts
            parts = line.split()
            ip, host = parts[:2]
            aliases = parts[2:]

            self.hosts.append(HostParser.Host(ip, host, aliases))

    def __repr__(self):
        me = self.__class__.__name__
        msg = "%s([" + ", ".join([str(d) for d in self.hosts]) + "])"
        return msg % me


@rule(HostParser, RedhatRelease)
def report(hp, rhr):
    if len(hp.hosts) > 1:
        return make_response("ERROR_KEY_TOO_MANY_HOSTS",
                             number=len(hp.hosts),
                             product=rhr.product)


if __name__ == "__main__":
    from insights import run
    run(report, print_summary=True)
