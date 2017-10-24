#!/usr/bin/env python
from insights import make_response, rule
from insights.core.dr import get_metadata


@rule(metadata={"foo": 10})
def report():
    meta = get_metadata(report)
    foo = meta["foo"]

    if foo < 5:
        return make_response("LESS_THAN_5", foo=foo)
    else:
        return make_response("GREATER_EQUAL_5", foo=foo)


if __name__ == "__main__":
    from insights import run
    run(report, print_summary=True)
