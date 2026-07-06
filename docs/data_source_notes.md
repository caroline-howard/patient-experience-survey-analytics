# Data Source Notes

## Primary Source

CMS HCAHPS patient experience data serves as the public data source for the reporting workflow.

## Source Use

The project structure supports placing downloaded CMS HCAHPS files in `data/raw/`. The preparation script is organized to standardize column names, identify discharge-related patient experience measures, and create cleaned outputs in `data/processed/`.

## Data Handling Notes

- Raw source files remain unchanged in `data/raw/`.
- Processed files are generated from scripted cleaning steps.
- No synthetic records or placeholder results are included.
- Source metadata, file names, and download dates should be documented when data files are added.

## Relevant Measure Areas

- Communication with nurses and doctors
- Responsiveness of hospital staff
- Discharge information
- Care transition
- Overall hospital rating
- Willingness to recommend
