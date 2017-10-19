#!/usr/bin/env python
from ansible.module_utils.basic import AnsibleModule
from insights import run
from insights.core import dr
from insights.core.serde import get_serializer


def get_name(o):
    return "_".join([dr.get_base_module_name(o), dr.get_simple_name(o)])


def serialize(_type, obj):
    if not obj:
        return {}

    if isinstance(obj, dict):
        return {get_name(_type): obj}

    is_list = isinstance(obj, list)
    if is_list:
        instance = obj[0]
    else:
        instance = obj

    ser = get_serializer(instance)
    if not ser:
        return {}

    raw = [ser(o) for o in obj] if is_list else ser(obj)

    if raw and raw is not obj:
        name = get_name(type(instance))
        return {name: raw}

    return {}


def main():
    module_args = dict(plugins=dict(type="dict", required=True))
    module = AnsibleModule(argument_spec=module_args)

    plugins = module.params["plugins"] or {}
    components = []
    for p, meta in plugins.items():
        plugin = dr.get_component(p)
        components.append(plugin)
        if meta:
            dr.COMPONENT_METADATA[plugin] = meta

    results = run(components)
    response = {}
    for p in components:
        r = results.get(p)
        if r:
            response.update(serialize(p, r))

    result = {"ansible_facts": {"insights": response}}
    module.exit_json(changed=False, **result)


if __name__ == '__main__':
    main()
