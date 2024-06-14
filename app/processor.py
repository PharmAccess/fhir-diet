import fhirpathpy

from utils.logger_wrapper import get_logger
from deidentify import actions as deident_actions, perform_deidentification
from depseudonymize import actions as depseudo_actions, perform_depseudonymization
from pseudonymize import actions as pseudo_actions, perform_pseudonymization
from utils.util import not_implemented

log = get_logger()


def _process_single_resource(resource, settings):
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
                result = perform_pseudonymization(action, resource, el, params)
            elif action in list(depseudo_actions.keys()):
                result = perform_depseudonymization(
                    action, resource, el, params)
            else:
                not_implemented(f'Method {action} is not implemented')
    return result


def process_data(resource, settings):
    if isinstance(resource, list):
        return [_process_single_resource(res, settings) for res in resource]
    return _process_single_resource(resource, settings)
