# Excel Dashboard Structure

## Workbook Tabs

| Tab | Purpose |
| --- | --- |
| `README` | Workbook notes, source/API details, and refresh guidance |
| `Source_API_Extract` | Optional imported extract from the CMS Provider Data Catalog API or local filtered CSV |
| `Clean_Data` | Cleaned CMS HCAHPS patient experience file exported from the Python workflow |
| `Data_Dictionary` | Field definitions, source notes, and dashboard use |
| `Pivot_Source` | Pivot-ready tables based on cleaned data |
| `Dashboard` | Stakeholder-facing reporting view |
| `Insights_Brief` | Concise narrative summary area for documented observations |

## Dashboard Sections

- Reporting period and data source note
- Discharge-related measure summary
- Patient experience measure comparison
- Hospital or state filter area
- Notes section for interpretation and data limitations
- Data quality and footnote reminder area

## Suggested Visuals

- Measure summary table
- Horizontal bar chart for selected HCAHPS measures
- Trend or comparison view when multiple reporting periods are available
- Highlight area for documented observations from analysis

## Input File

The Excel workbook uses the cleaned CSV created by the Python preparation script. The default Florida API workflow exports:

```text
data/processed/hcahps_patient_experience_clean.csv
data/processed/hcahps_patient_experience_fl_clean.csv
```

The source extract comes from the CMS Provider Data Catalog API for dataset `dgck-syfz`, or from a manually downloaded filtered CSV placed in `data/raw/`.

The dashboard structure is defined here for reporting design only. The Excel workbook itself is not included at this stage.

## API Refresh Notes

- Default state filter: `FL`
- Dataset: `Patient survey (HCAHPS) - Hospital`
- Dataset ID: `dgck-syfz`
- API workflow: run `python scripts/prepare_hcahps_data.py`
- Local CSV workflow: run `python scripts/prepare_hcahps_data.py --input-mode local`
