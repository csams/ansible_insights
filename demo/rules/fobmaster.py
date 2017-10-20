#!/usr/bin/env python
from insights import make_response, rule, run
from insights.core.dr import get_metadata


@rule(metadata={"foo": 10})
def report():
    meta = get_metadata(report)
    if meta["foo"] < 5:
        return make_response("LESS_THAN_5")
    else:
        return make_response("GREATER_EQUAL_5")


if __name__ == "__main__":
    run(report, print_summary=True)
