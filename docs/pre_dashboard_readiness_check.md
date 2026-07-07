# Pre-Dashboard Readiness Check

Date checked: 2026-07-07

Branch checked: `codex/fix-hcahps-dashboard-metrics`

## 1. Git Diff / Changed Files

The working tree was clean before this readiness report was created.

Current branch changes compared with `main`:

| File | Change type | Notes |
| --- | --- | --- |
| `README.md` | Modified | Updated project scope, source, reporting period, dashboard metric logic, and Qualtrics role. |
| `scripts/prepare_hcahps_data.py` | Modified | Added source column normalization and favorable-response fields. |
| `data/processed/hcahps_patient_experience_fl_clean.csv` | Modified | Regenerated Florida processed dataset with favorable-response fields. |
| `excel_dashboard/patient_discharge_experience_dashboard.xlsx` | Modified | Workbook was refreshed to use corrected favorable-response metrics. |
| `docs/data_source_notes.md` | Modified | Clarified CMS API paging plus local Florida filtering. |
| `docs/data_dictionary.md` | Modified | Added current processed fields and favorable-response definitions. |
| `docs/excel_dashboard_structure.md` | Modified | Updated workbook structure and metric logic notes. |
| `docs/insights_brief_template.md` | Modified | Updated findings and suggested follow-up questions. |
| `docs/project_overview.md` | Modified | Updated current scope and role of deliverables. |
| `docs/survey_instrument.md` | Modified | Added medication clarity and side-effect emphasis. |
| `docs/survey_logic_map.md` | Modified | Added medication side-effect follow-up logic. |
| `docs/project_status_and_api_inventory.md` | Added | Full project status and API/data inventory. |
| `docs/pre_dashboard_readiness_check.md` | Added | This validation report. |

The Excel workbook did change in the prior correction pass. The workbook currently contains the expected tabs and two dashboard charts. No new dashboard layout or visual redesign changes were made during this readiness validation pass.

The prior changes were limited to corrected metric logic, processed data refresh, documentation/source clarity, and workbook metric refresh.

## 2. Data Workflow Validation

The HCAHPS processing workflow was rerun using local CSV mode:

```bash
.venv/bin/python scripts/prepare_hcahps_data.py --input-mode local
```

Result:

| Check | Result |
| --- | --- |
| Raw local file used | `data/raw/HCAHPS-Hospital.csv` |
| Florida rows after state filter | 12,988 |
| Rows after relevant-measure filter | 11,460 |
| Output file | `data/processed/hcahps_patient_experience_fl_clean.csv` |
| Output exists | Yes |
| Final row count | 11,460 |
| Final column count | 33 |
| State scope | Florida only (`FL`) |
| Facility count | 191 facilities |
| Reporting period | 07/01/2024-06/30/2025 |

Workflow behavior confirmed from `scripts/prepare_hcahps_data.py`:

- API mode uses CMS dataset `dgck-syfz`.
- API requests use `limit` and `offset` pagination.
- The script does not currently request a Florida-only API response.
- The Florida filter is applied locally in pandas after source rows are loaded.
- Local CSV mode reads the first CSV found in `data/raw/`.

## 3. Favorable-Response Metric Validation

Final favorable-response logic:

| Dashboard category | Favorable response rule |
| --- | --- |
| Discharge Information | Answer description starts with `Yes` |
| Nurse Communication | Answer description contains `Always` |
| Doctor Communication | Answer description contains `Always` |
| Medicine Communication | Answer description contains `Always` |
| Overall Rating | Measure ID equals `H_HSP_RATING_9_10` |
| Recommendation | Measure ID equals `H_RECMND_DY` |

Weighting field:

```text
number_of_completed_surveys_numeric
```

Weighted metric formula:

```text
sum(favorable_response_percent_numeric * number_of_completed_surveys_numeric)
/ sum(number_of_completed_surveys_numeric)
```

Missing scores or missing survey counts are excluded from the weighted metric because blank/non-numeric values are converted to null numeric values and do not contribute to the scored rows.

Confirmed headline values from `data/processed/hcahps_patient_experience_fl_clean.csv`:

| Metric | Survey-weighted favorable % | Scored favorable rows | Simple favorable average | Survey-count weight |
| --- | ---: | ---: | ---: | ---: |
| Discharge Information | 84.27 | 521 | 83.19 | 626,423 |
| Nurse Communication | 76.39 | 694 | 75.90 | 835,207 |
| Doctor Communication | 74.82 | 694 | 74.97 | 835,207 |
| Recommendation | 70.01 | 175 | 68.21 | 208,855 |
| Overall Rating | 69.07 | 175 | 67.61 | 208,855 |
| Medicine Communication | 58.01 | 521 | 57.78 | 626,423 |
| Side-effect explanation | 43.78 | 173 | 43.91 | 208,784 |

These values match the expected corrected findings. No discrepancy was found.

## 4. Findings Readiness

The repo now has an updated findings-oriented brief at:

```text
docs/insights_brief_template.md
```

The main finding is clearly documented:

> Florida hospitals perform relatively well on discharge information and general communication, but medicine communication, especially explaining side effects, is the clearest improvement opportunity.

This finding is also reflected in:

- `README.md`
- `docs/excel_dashboard_structure.md`
- `docs/survey_instrument.md`
- `docs/survey_logic_map.md`
- `docs/project_status_and_api_inventory.md`

Remaining issue: `docs/insights_brief_template.md` is now more than a blank template, but it is still written as a reusable brief/template rather than a polished final portfolio report with screenshots and finished narrative exhibits.

## 5. Qualtrics Readiness

The Qualtrics survey documentation now reflects the HCAHPS findings.

Confirmed follow-up survey content:

| Follow-up theme | Present? | Location |
| --- | --- | --- |
| Medication purpose | Yes | `docs/survey_instrument.md` |
| Medication side effects | Yes | `docs/survey_instrument.md`; `docs/survey_logic_map.md` |
| Discharge confidence / understanding | Yes | `docs/survey_instrument.md`; `docs/survey_logic_map.md` |
| Who to contact after discharge | Yes | `docs/survey_instrument.md` |
| Who to contact with medication questions | Yes | `docs/survey_instrument.md` |

The survey is ready to inform dashboard design and portfolio framing. It remains a documented Qualtrics follow-up survey design only; no actual Qualtrics response export is present.

## 6. Documentation Readiness

Documentation now accurately states:

| Documentation requirement | Confirmed? | Notes |
| --- | --- | --- |
| CMS HCAHPS Hospital patient survey data | Yes | `README.md`; `docs/data_source_notes.md` |
| Florida hospitals | Yes | `README.md`; `docs/data_source_notes.md`; processed CSV validation |
| Reporting period 07/01/2024-06/30/2025 | Yes | `README.md`; `docs/data_source_notes.md`; processed CSV validation |
| Qualtrics is a follow-up survey design, not the HCAHPS source | Yes | `README.md`; `docs/insights_brief_template.md`; `docs/data_dictionary.md` |
| Excel dashboard/reporting is a reporting phase, not the source of findings | Mostly yes | Docs identify CMS HCAHPS as the data source and Excel as reporting output. |

## Remaining Issues Before Dashboard Design

| Issue | Impact | Recommended action |
| --- | --- | --- |
| Workbook visual QA was not completed in this pass | The workbook structure and values are validated, but final visual polish still needs review. | Perform visual dashboard design/QA in the next phase. |
| `docs/insights_brief_template.md` is not a final polished report | Findings are present, but portfolio narrative and screenshots are not final. | Convert into a final brief after dashboard layout is finalized. |
| Facility comparison logic should be reviewed during design | Headline KPIs are survey-weighted; facility comparison views may use simple facility averages for readability. | Label metric methodology clearly in the dashboard. |
| API-side Florida filtering is not implemented | Current workflow downloads/pages source rows then filters locally. | Keep documented as-is unless adding API-side filtering becomes a future requirement. |

## Readiness Decision

The project is ready to move into Excel dashboard design.

The data workflow, processed file, favorable-response logic, weighted headline metrics, source documentation, and Qualtrics follow-up survey framing are now aligned. The next phase should focus on dashboard layout, visual hierarchy, stakeholder-facing labels, screenshots, and a final findings brief.
