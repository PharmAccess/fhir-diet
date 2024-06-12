import typer

import config
from processor import process_data
from utils.logger_wrapper import init_logger, get_logger
from utils.util import read_resource_from_file, write_resource_to_file

app = typer.Typer()
log = get_logger()


@app.command()
def process(
        resource_filename: str,
        config_filename: str = typer.Argument("config.yaml"),
        output_to_file: bool = False
):
    resource = read_resource_from_file(resource_filename)
    settings = config.Settings(config_filename)
    ret = process_data(resource, settings)
    log.debug(f'CLI Process Result={ret}')
    if output_to_file:
        write_resource_to_file(resource_filename, ret)


if __name__ == "__main__":
    init_logger(5)
    app()
