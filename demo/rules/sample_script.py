#!/usr/bin/env python
from insights import run
from insights.core.plugins import make_response, rule
from insights.parsers.redhat_release import RedhatRelease


@rule(RedhatRelease)
def report(rel):
    if "Fedora" in rel.product:
        return make_response("IS_FEDORA")


if __name__ == "__main__":
    run(report, print_summary=True)
