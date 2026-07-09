# HCAHPS Favorable Metric Validation

## Data Source
- Source file: `data/processed/hcahps_patient_experience_fl_clean.csv`
- Dataset: public CMS HCAHPS hospital-level patient survey data.

## Scope
- Rows: 11,460
- Columns: 33
- Facilities: 191
- States present: FL (11,460)
- Reporting periods: 07/01/2024 to 06/30/2025 (11,460)

## Required Columns
- All required columns are present.

## Favorable-Response Definitions
- Discharge Information: `Yes`
- Nurse Communication: `Always`
- Doctor Communication: `Always`
- Medicine Communication: `Always`
- Overall Rating: `9 or 10`
- Recommendation: `Definitely yes`

## Weighting Method
- `favorable_percent = hcahps_answer_percent_numeric`
- `survey_weight = number_of_completed_surveys_numeric`
- Weighted favorable percent = `sum(favorable_percent * survey_weight) / sum(survey_weight)`.
- Included rows must be favorable-response rows with numeric favorable percent and numeric survey weight greater than zero.
- If a denominator is zero, missing, or invalid, the result is left blank/null rather than emitting an invalid value.

## Category Results
| Measure group | Favorable % | Expected % | Difference | Included rows | Excluded rows | Matches expected |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Discharge Information | 84.27 | 84.27 | -0.00 | 521 | 52 | Yes |
| Nurse Communication | 76.39 | 76.39 | 0.00 | 694 | 70 | Yes |
| Doctor Communication | 74.82 | 74.82 | 0.00 | 694 | 70 | Yes |
| Recommendation | 70.01 | 70.01 | 0.00 | 175 | 16 | Yes |
| Overall Rating | 69.07 | 69.07 | 0.00 | 175 | 16 | Yes |
| Medicine Communication | 58.01 | 58.01 | -0.00 | 521 | 52 | Yes |

## Submeasure Results
| Measure group | Submeasure | Favorable % | Included rows | Excluded rows |
| --- | --- | ---: | ---: | ---: |
| Discharge Information | given recovery information | 84.23 | 175 | 16 |
| Discharge Information | staff discussed help after discharge | 82.82 | 173 | 18 |
| Discharge Information | written symptoms to watch for | 85.75 | 173 | 18 |
| Nurse Communication | overall nurse communication | 76.37 | 175 | 16 |
| Nurse Communication | explained clearly | 72.19 | 173 | 18 |
| Nurse Communication | listened carefully | 73.33 | 173 | 18 |
| Nurse Communication | courtesy/respect | 83.68 | 173 | 18 |
| Doctor Communication | overall doctor communication | 74.87 | 175 | 16 |
| Doctor Communication | explained clearly | 69.79 | 173 | 18 |
| Doctor Communication | listened carefully | 72.81 | 173 | 18 |
| Doctor Communication | courtesy/respect | 81.82 | 173 | 18 |
| Medicine Communication | overall medicine communication | 58.03 | 175 | 16 |
| Medicine Communication | new medication purpose | 72.22 | 173 | 18 |
| Medicine Communication | side effects | 43.78 | 173 | 18 |
| Overall Rating | overall rating 9 or 10 | 69.07 | 175 | 16 |
| Recommendation | definitely recommend | 70.01 | 175 | 16 |

## Excluded Rows And Missing Values
- Favorable rows excluded from category calculations: 276
- Missing favorable percent: 276
- Invalid favorable percent: 0
- Missing survey weight: 0
- Invalid survey weight: 0
- Nonpositive survey weight: 0

## Expected-Metric Check
- Category values match the provided expected metrics within 0.05 percentage points: Yes.
- Side-effect explanation favorable percent: 43.78% versus expected about 43.78%.

## Limitations
- CMS hospital-level percentages are already rounded by the source data; weighted summaries therefore inherit that rounding.
- Survey weights use the hospital-level completed survey count repeated across HCAHPS measure rows, not patient-level microdata.
- Hospitals with missing percentages or missing/nonpositive completed-survey counts are excluded from the relevant weighted calculation.
