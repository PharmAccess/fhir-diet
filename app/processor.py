import csv

import fhirpathpy
from actions.ttp import expected_params
from deidentify import actions as deident_actions
from deidentify import perform_deidentification
from depseudonymize import depseudo_actions, perform_depseudonymization
from pseudonymize import perform_pseudonymization, pseudo_actions
from rich.progress import track
from utils.logger_wrapper import get_logger
from utils.util import not_implemented

log = get_logger()


def _process_single_resource(resource, settings, mappings):
    result = resource
    for rule in settings.rules:
        fhirpathpy.engine.invocations['log'] = {'fn': lambda ctx, els: [
            {'path': x.path, 'value': x.data} for x in els]}
        matched_elements = fhirpathpy.evaluate(
            resource, rule['match'] + '.log()', [])
        log.debug(f'Matched elements: {matched_elements}')
        for el in matched_elements:
            action = rule['action']
            params = rule['params'] if 'params' in rule.keys() else {}
            if action in list(deident_actions.keys()):
                result = perform_deidentification(action, resource, el, params)
            elif action in list(pseudo_actions.keys()):
                result = perform_pseudonymization(action, resource, el, params, mappings[action])
            elif action in list(depseudo_actions.keys()):
                result = perform_depseudonymization(
                    action, resource, el, params, mappings[action])
            else:
                not_implemented(f'Method {action} is not implemented')
    return result


def _return_action_mappings(settings):
    mappings = {}
    actions_that_require_mapping_file = ['ttp_pseudonymize']
    # Create a dictionary of mappings for each action that requires a mapping file
    mappings = dict((action, {}) for action in actions_that_require_mapping_file)
    
    for rule in settings.rules:
        action = rule['action']
        if action in actions_that_require_mapping_file:
            if 'mapping_file' not in rule['params']:
                raise ValueError(
                    f'Action {action} requires a mapping file to be provided in the params')
            mapping_file = rule['params']['mapping_file']
            params = rule['params']
            separator = params[expected_params[2]] if expected_params[2] in params else ','
            header_lines = params[expected_params[3]] if expected_params[3] in params else 0
            # mappings[action] = _read_mappings(mapping_file, separator, header_lines)
            mappings[action].update(_read_mappings(mapping_file, separator, header_lines))
    return mappings


def _read_mappings(mapping_file, separator=',', header_lines=0) -> dict:
    with (open(mapping_file, 'r')) as fin:
        reader = csv.reader(fin, delimiter=separator)
        rows = [row for row in reader]
        mappings = dict((row[0], row[1]) for row in rows[header_lines:])
    return mappings


def process_data(resource, settings):
    mappings = _return_action_mappings(settings)
    if isinstance(resource, list):
        return [_process_single_resource(res, settings, mappings) for res in track(resource, description="Processing...")]
    return _process_single_resource(resource, settings, mappings)
