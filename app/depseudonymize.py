from actions.decrypt import decrypt_by_path
from ttp_pseudonymizer import depseudo_actions as ttp_depseudo_actions
from utils.util import not_implemented

actions = {
    "decrypt": decrypt_by_path,
}

depseudo_actions = actions | ttp_depseudo_actions


def perform_depseudonymization(action, resource, el, params, mappings):
    if action in list(actions.keys()):
        actions[action](resource, el, params)
    elif action in list(ttp_depseudo_actions.keys()):  # TTP (gPAS)
        ttp_depseudo_actions[action](resource, el, mappings)
    else:
        not_implemented(f'Method {action} is not implemented')
    return resource
