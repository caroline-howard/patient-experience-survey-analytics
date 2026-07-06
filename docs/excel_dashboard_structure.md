# Excel Dashboard Structure

## Workbook Tabs

| Tab | Purpose |
| --- | --- |
| `README` | Workbook notes, source details, and refresh guidance |
| `Clean_Data` | Imported cleaned CMS HCAHPS patient experience file |
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

The Excel workbook uses the cleaned CSV created by the Python preparation script:

```text
data/processed/hcahps_patient_experience_clean.csv
```

The dashboard structure is defined here for reporting design only. The Excel workbook itself is not included at this stage.
