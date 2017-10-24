#!/usr/bin/env python
import json
import lxml.etree as ET

from insights import make_response, parser, Parser, run, rule
from insights.core.context import JBossContext, JDRContext
from insights.core.spec_factory import RawFileProvider, SpecFactory

sf = SpecFactory()

activeconfig = sf.simple_file("sos_strings/wildfly_full-10/configuration.json",
                              context=JDRContext,
                              Kind=RawFileProvider,
                              name="active_config")

sacfg = sf.simple_file("$JBOSS_HOME/standalone/configuration/standalone.xml",
                       Kind=RawFileProvider,
                       name="sacfg")

salog = sf.simple_file("$JBOSS_HOME/standalone/log/server.log", name="salog")


@parser(activeconfig)
class ActiveConfig(Parser):
    def parse_content(self, content):
        doc = json.loads(content)
        self.data = doc["result"]


@parser(sacfg)
class StandAloneXML(Parser):
    def parse_content(self, content):
        self.root = ET.fromstring(content)


@rule(salog, StandAloneXML)
def report(log, cfg):
    return make_response("SOMETHING_HAPPENED")


@rule(StandAloneXML)
def report2(cfg):
    return make_response("SOMETHING_ELSE_HAPPENED")


if __name__ == "__main__":
    run(print_summary=True,
        run_context=JBossContext,
        archive_context=JDRContext)
