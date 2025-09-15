from actions.encrypt import encrypt_by_path
from actions.ttp import list_by_path
from ttp_pseudonymizer import pseudo_actions as ttp_pseudo_actions
from utils.util import not_implemented

actions = {
    "encrypt": encrypt_by_path,
    "ttp_gen_list": list_by_path,
}

pseudo_actions = actions | ttp_pseudo_actions


def perform_pseudonymization(action, resource, el, params, mappings):
    if action in list(actions.keys()):
        actions[action](resource, el, params)
    elif action in list(ttp_pseudo_actions.keys()):  # TTP (gPAS
        ttp_pseudo_actions[action](resource, el, mappings)
    else:
        not_implemented(f'Method {action} is not implemented')
    return resource
