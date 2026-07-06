# Data Source Notes

## Primary Source

CMS HCAHPS patient experience data serves as the public data source for the reporting workflow. The project uses the CMS Provider Data Catalog API to retrieve a filtered extract from the hospital-level HCAHPS dataset.

## Dataset Details

| Item | Value |
| --- | --- |
| Dataset | Patient survey (HCAHPS) - Hospital |
| Dataset ID | `dgck-syfz` |
| Source | CMS Provider Data Catalog |
| Data dictionary file reference | `HCAHPS-HOSPITAL.CSV` |
| CMS landing page | `https://data.cms.gov/provider-data/dataset/dgck-syfz` |

The raw full CSV is not committed to this repository because the dataset is large. The workflow uses the CMS API to pull only the fields needed for the dashboard and applies a configurable state filter.

## API-Based Workflow

The default workflow queries the CMS Provider Data Catalog API for Florida (`FL`) records:

```bash
python scripts/prepare_hcahps_data.py
```

The default state filter supports the first portfolio dashboard version. To change the state:

```bash
python scripts/prepare_hcahps_data.py --state GA
```

To pull all states, use:

```bash
python scripts/prepare_hcahps_data.py --all-states
```

Pulling all states may create a large output file.

## Local CSV Option

The script also supports a manually downloaded or filtered CSV extract saved in `data/raw/`:

```bash
python scripts/prepare_hcahps_data.py --input-mode local
```

This option is useful when working from a CMS export or a pre-filtered extract. The full raw CMS file should remain outside the repository unless it is small enough and appropriate to version.

## Data Handling Notes

- API extracts and local CSV inputs are processed through the same cleaning workflow.
- No synthetic records or placeholder results are included.
- The workflow does not invent findings or fill missing CMS values with artificial results.
- Facility IDs are preserved as text so leading zeroes are not lost.
- Numeric fields are converted where possible while original CMS text values are retained.
- CMS footnote fields are kept when available.

## Relevant Measure Areas

- Discharge information
- Communication with nurses
- Communication with doctors
- Communication about medicines
- Overall hospital rating
- Willingness to recommend
- Summary star rating

## Output Files

The workflow exports:

```text
data/processed/hcahps_patient_experience_clean.csv
data/processed/hcahps_patient_experience_fl_clean.csv
```

The Florida-specific file is exported when the default `FL` filter is used.
