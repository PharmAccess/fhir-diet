# Running locally

## De-identifying FHIR data

To de-identify COT data:

1. copy the COT data to the `data` directory as ndjsons
2. create config for each Resource in the `config` directory.
    1. check `config/cot_deid.yaml` for an example
3. if you need to pseudonymize the data, create a `pseudonymize` directory in the `data` directory and add the pseudonymization mapping file
    1. check `pseudonymization/cot_pseudonym_mapping.csv` for an example
    2. update the `config/cot_deid.yaml` to include the pseudonymization mapping file
    3. we use [gpas-tool](https://github.com/PharmAccess/gpas-tool) to create the pseudonymization mapping file
    4. COT mapping can be found in [archive container](https://cotarchive.blob.core.windows.net/cot-pseudo-ids/cot_pseudonym_mapping.csv)
4. run the de-identification script from the root directory on each resource

    ```bash
    python3 cli.py test/data/cot/patient.json test/config/cot_deid.yaml
    ```
