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
    4. hint use [gpas-web](http://localhost:8080/gpas-web/)
    5. COT mapping can be found in [archive container](https://cotarchive.blob.core.windows.net/cot-pseudo-ids/cot_pseudonym_mapping.csv)
4. run the de-identification script from the app directory on each resource

    ```bash
    python cli.py --resource-filename patient.json --resource-dir test/data/cot --config-filename test/config/cot_deid.yaml --output-to-file
    ```

# FHIR Diet CLI Usage

## Command Structure

The CLI provides direct options without subcommands:

```bash
python cli.py [OPTIONS]
```

## Available Options

- `--resource-filename TEXT`: Path to the resource file to process (default: "")
- `--resource-dir TEXT`: Directory containing the resource files (default: "")
- `--config-filename TEXT`: Configuration file to use (default: "config.yaml")
- `--output-to-file / --no-output-to-file`: Write processed output to file (default: False)
- `--parquet / --no-parquet`: Process parquet format files (default: False)
- `--help`: Show help message and exit

## Terminal Command Examples

### Basic Processing
Process with default config:
```bash
python cli.py
```

### Process Single JSON File
```bash
python cli.py --resource-filename simple_patient.json --resource-dir test/sample_fhir_data --config-filename config.yaml
```

### Process NDJSON (Bulk) File with Output
```bash
python cli.py --resource-filename patient.ndjson --resource-dir test/sample_fhir_data --config-filename test/config/safe_harbor_redact.yaml --output-to-file
```

### Process Parquet Files
```bash
python cli.py --resource-dir data/Patient --parquet --output-to-file
```

### Advanced Configuration Examples

#### De-identification with Safe Harbor Rules
```bash
python cli.py --resource-filename synthea_patient_sample.json --resource-dir test/sample_fhir_data --config-filename test/config/safe_harbor_redact.yaml --output-to-file
```

#### Cryptographic Hashing
```bash
python cli.py --resource-filename patient.ndjson --resource-dir test/sample_fhir_data --config-filename test/config/cryptohash.yaml --output-to-file
```

#### Encryption/Decryption
```bash
# Encryption
python cli.py --resource-filename simple_patient.json --resource-dir test/sample_fhir_data --config-filename test/config/encrypt.yaml --output-to-file

# Decryption
python cli.py --resource-filename simple_patient_deid.json --resource-dir test/sample_fhir_data --config-filename test/config/decrypt.yaml --output-to-file
```

#### TTP Pseudonymization
```bash
python cli.py --resource-filename patient.ndjson --resource-dir test/sample_fhir_data --config-filename test/config/ttp_pseudonymize.yaml --output-to-file
```

#### Data Perturbation
```bash
python cli.py --resource-filename synthea_patient_sample.json --resource-dir test/sample_fhir_data --config-filename test/config/perturb.yaml --output-to-file
```

#### Multiple Rule Processing
```bash
python cli.py --resource-filename patient.ndjson --resource-dir test/sample_fhir_data --config-filename test/config/multi_rule.yaml --output-to-file
```

## Configuration Files Available

The following configuration files are available in `test/config/`:

- `cot_deid.yaml` - COT-specific de-identification
- `cryptohash.yaml` - Cryptographic hashing
- `decrypt.yaml` - Data decryption
- `encrypt.yaml` - Data encryption
- `keep.yaml` - Keep specific fields
- `momcare_ke_deid.yaml` - MomCare Kenya de-identification
- `multi_rule.yaml` - Multiple processing rules
- `perturb.yaml` - Data perturbation
- `redact.yaml` - Data redaction
- `safe_harbor_redact.yaml` - HIPAA Safe Harbor redaction
- `substitute.yaml` - Data substitution
- `ttp_depseudonymize.yaml` - TTP de-pseudonymization
- `ttp_gen_list.yaml` - TTP list generation
- `ttp_pseudonymize.yaml` - TTP pseudonymization

## Sample Data Files

Test with sample data from `test/sample_fhir_data/`:

- `simple_patient.json` - Basic patient record
- `patient.ndjson` - Bulk patient data
- `synthea_patient_sample.json` - Synthea-generated patient
- `sample.json` - General sample data
- Files in `synthea_sample_fhir_data/` - Multiple Synthea patient records

## Output Files

When using `--output-to-file`, processed files are saved with `_deid` suffix:
- `patient.json` → `patient_deid.json`
- `patient.ndjson` → `patient_deid.ndjson`
