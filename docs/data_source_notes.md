# Data Source Notes

## Primary Source

CMS HCAHPS patient experience data serves as the public data source for the reporting workflow. The dataset is available through the CMS Provider Data Catalog and includes hospital-level patient survey measures used for patient experience reporting.

## Obtaining the Data

1. Go to the CMS Provider Data Catalog.
2. Search for HCAHPS patient survey or hospital HCAHPS data.
3. Select the current HCAHPS patient survey dataset.
4. Download the CSV file from the catalog.
5. Save the raw CSV in `data/raw/`.

The preparation script does not download data automatically. This keeps the workflow transparent and avoids relying on an unstable direct download URL. If CMS provides a stable direct CSV download link in the future, that link can be documented here before adding any automated download step.

## Source Use

The project structure supports placing downloaded CMS HCAHPS CSV files in `data/raw/`. The preparation script loads the raw file, standardizes column names, identifies discharge and patient experience measures, assigns dashboard categories, and creates a cleaned output in `data/processed/`.

## Data Handling Notes

- Raw source files remain unchanged in `data/raw/`.
- Processed files are generated from scripted cleaning steps.
- No synthetic records or placeholder results are included.
- Source metadata, file names, and download dates should be documented when data files are added.
- The workflow does not invent findings or fill missing CMS values with artificial results.

## Relevant Measure Areas

- Communication with nurses and doctors
- Responsiveness of hospital staff
- Discharge information
- Care transition
- Communication about medicines
- Overall hospital rating
- Willingness to recommend

## Expected Raw File Location

Place the CMS HCAHPS CSV in:

```text
data/raw/
```

The cleaned dashboard-ready file is exported to:

```text
data/processed/hcahps_patient_experience_clean.csv
```
