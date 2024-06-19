from actions.substitute import _substitute_nodes
from utils.util import find_nodes

expected_params = ['output_file', 'mapping_file', 'separator', 'header_lines']


def _find_pseudonym(mappings, value='', reverse=False):
    if reverse:
        key_value = {i for i in mappings if mappings[i] == value}
        return key_value.pop()
    return mappings[value]


def list_by_path(resource, el, params):
    outfile = params[expected_params[0]
    ] if expected_params[0] in params else './list.csv'
    with (open(outfile, 'a+')) as fin:
        fin.write(f"{str(el['value'])}\n")


def pseudonymize_by_path(resource, el, mappings):
    ret = resource
    path = el['path']  # "Patient.name"
    path = path.split('.')[1:]  # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    pseudonym = _find_pseudonym(mappings, el['value'])
    _substitute_nodes(ret, path[-1], el['value'], pseudonym)


def depseudonymize_by_path(resource, el, mappings):
    ret = resource
    path = el['path']  # "Patient.name"
    path = path.split('.')[1:]  # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    depseudonym = _find_pseudonym(mappings, el['value'], True)
    _substitute_nodes(ret, path[-1], el['value'], depseudonym)
