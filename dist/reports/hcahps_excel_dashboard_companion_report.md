# HCAHPS Excel Dashboard Companion Report

## Patient Discharge Experience & Follow-Up Support Analytics

### Reporting period

07/01/2024-06/30/2025

### Scope

This report accompanies the Excel dashboard `excel_dashboard/patient_discharge_experience_dashboard.xlsx`. It summarizes public CMS HCAHPS hospital-level patient experience results for Florida hospitals and translates the dashboard findings into an implementation-focused rationale for a future Qualtrics follow-up survey.

The dashboard and this report use hospital-level public reporting data. That hospital-level view is the starting point: it identifies where hospitals may need to invest in staff education, role clarity, discharge workflow, and patient-facing medication communication. The future Qualtrics survey should then collect patient-level detail to explain the hospital-level pattern.

## Executive Summary

The statewide HCAHPS dashboard shows a clear pattern: Florida hospitals perform strongest on Discharge Information, while Medicine Communication is the weakest major patient experience category. The most specific gap is side-effect explanation, where favorable performance is substantially lower than the broader category results.

This does not necessarily mean that general doctor or nurse communication is weak. Nurse Communication and Doctor Communication are both notably higher than the side-effect explanation measure. The more useful interpretation is that side-effect education may depend on a specific implementation workflow that is not being delivered, owned, timed, or remembered consistently.

The future Qualtrics survey should therefore be designed as a hospital implementation and improvement diagnostic. It should help answer where hospitals should invest: staff education, role clarity, pharmacist involvement, discharge checklist design, written materials, teach-back, or post-discharge support.

## Dashboard Findings

| Dashboard category | Favorable-response definition | Survey-weighted favorable response rate |
| --- | --- | ---: |
| Discharge Information | Yes | 84.27% |
| Nurse Communication | Always | 76.39% |
| Doctor Communication | Always | 74.82% |
| Recommendation | Definitely yes | 70.01% |
| Overall Rating | 9 or 10 | 69.07% |
| Medicine Communication | Always | 58.01% |

### Main finding

Medicine Communication is the clearest statewide improvement opportunity. At 58.01%, it trails the other major dashboard categories and points to a more specific patient education gap around medication guidance.

### Strongest area

Discharge Information is the strongest major category at 84.27%. This suggests that broad discharge information processes may be more reliable than medication-specific education, or at least more consistently reported as favorable by patients.

### Moderate global experience measures

Recommendation and Overall Rating are moderate, at 70.01% and 69.07%. These measures are useful context, but they are less diagnostic than the communication-specific categories. They show that overall experience is not the lowest signal; the more actionable gap is medication communication.

## Submeasure Findings

The submeasure results sharpen the main dashboard story.

| Category | Submeasure | Favorable response rate |
| --- | --- | ---: |
| Medicine Communication | Overall medicine communication | 58.01% |
| Medicine Communication | New medication purpose | 72.20% |
| Medicine Communication | Side effects | 43.78% |

Side-effect explanation is the lowest specific measure in the validated breakdown, at 43.78%. This is the most important finding for the next phase of work because it identifies a concrete follow-up topic rather than a broad satisfaction issue.

## Interpretation

The dashboard does not suggest that all discharge communication is equally weak. Instead, it points to a narrower issue: patients are less consistently reporting that medication-related information, especially side effects, was explained in the most favorable way.

This distinction matters. If discharge information overall is relatively strong, then the improvement opportunity may not be the existence of discharge instructions in general. It may be the clarity, timing, ownership, and usefulness of medication explanations.

The gap between new medication purpose and side-effect explanation is especially important. Patients may be more likely to hear what a medication is for than what side effects to watch for, what symptoms should trigger follow-up, or whom to contact after discharge.

The contrast with Nurse Communication and Doctor Communication is also important. Patients can report that nurses and doctors listened carefully, explained things clearly, or treated them with respect while still leaving without a clear understanding of medication side effects. Those broader communication measures may reflect interpersonal quality, while side-effect education depends on a more specific clinical process.

For hospital improvement, the core implementation question is:

**If doctor and nurse communication are relatively stronger, why is side-effect explanation so much lower?**

Possible implementation explanations include:

- No clear owner for side-effect education across doctors, nurses, pharmacists, and discharge staff.
- Medication purpose is explained, but side effects and warning signs are not consistently covered.
- Side-effect education happens too late in the discharge process, when patients are overwhelmed.
- Information is included in written paperwork but not verbally reinforced.
- Patients hear the information but do not retain it or cannot translate it into action at home.
- Staff communication training emphasizes courtesy and listening but not medication-specific teach-back.
- High-risk or new medications do not trigger a consistent counseling workflow.

## From Dashboard Finding to Survey Design

The Qualtrics follow-up should be designed as a hospital implementation and improvement survey, not a duplicate HCAHPS instrument. The Excel dashboard identifies the problem area: Medicine Communication, especially side-effect explanation. The Qualtrics survey should explain how that gap happens from the patient perspective.

The survey should therefore focus on implementation conditions that hospitals can change: who owns side-effect education, when it happens, how it is delivered, whether patients understand what to do, and which supports would make the discharge medication process clearer.

This keeps the follow-up survey tied to hospital action. Rather than asking only whether patients were satisfied, it should identify whether the improvement opportunity is staff education, role clarity, pharmacist involvement, discharge workflow, written materials, teach-back, or post-discharge support.

## Recommended Qualtrics Survey Direction

The follow-up survey should prioritize medication communication implementation and post-discharge patient understanding. A practical survey structure would include:

1. **Screening and context**
   Identify whether the patient was discharged with a new medicine, changed medicine, or medication instructions.

2. **Role ownership**
   Ask who explained side effects: doctor, nurse, pharmacist, discharge planner, written instructions only, no one, or not sure.

3. **Medication purpose**
   Ask whether the patient understood what the medicine was for and whether the explanation was clear.

4. **Side-effect explanation**
   Ask whether side effects were explained, whether the patient understood what to watch for, and whether the explanation was specific enough.

5. **Workflow timing and format**
   Ask when the explanation happened and whether information was delivered verbally, in writing, through the patient portal, or only if the patient asked.

6. **Patient understanding and teach-back**
   Ask whether the patient could identify urgent side effects, knew what action to take, and was asked to confirm understanding.

7. **Post-discharge support**
   Ask whether the patient knew whom to contact and what follow-up support would have been helpful.

8. **Implementation improvement target**
   Ask what would have helped most: clearer verbal explanation, simpler written instructions, pharmacist counseling, more time before discharge, caregiver involvement, follow-up call or text, or clearer contact information.

9. **Open-ended improvement item**
   Capture patient language about what would have made medication side-effect instructions clearer.

## Hospital Improvement Questions

The Qualtrics survey should produce results that hospital leaders can connect to implementation decisions. Each survey domain should map to an improvement lever.

| Survey domain | What it diagnoses | Possible hospital investment |
| --- | --- | --- |
| Role ownership | Whether patients know who explained side effects | Clarify doctor, nurse, pharmacist, and discharge staff responsibilities |
| Timing | Whether education happens early enough to absorb | Move medication counseling earlier in discharge workflow |
| Format | Whether patients receive verbal, written, or portal-based guidance | Standardize verbal explanation plus plain-language written materials |
| Content completeness | Whether purpose, side effects, warning signs, and next steps are covered | Add side-effect prompts to discharge checklist |
| Patient understanding | Whether patients know what to do after discharge | Staff teach-back training |
| Follow-up support | Whether patients know who to contact | Post-discharge call, text, portal message, or hotline workflow |

## How to Use the Excel Dashboard With This Report

Use the Excel dashboard as the quantitative reference and this report as the interpretation layer.

- Use the **Dashboard** sheet for the statewide category story.
- Use **Category_Detail** to inspect submeasure results, especially Medicine Communication and side effects.
- Use **Hospital_Detail** to compare individual hospitals with the Florida average by category.
- Use **README** for scope, definitions, and navigation.
- Use this companion report to explain why the Qualtrics follow-up should focus on hospital implementation improvement rather than broad satisfaction alone.

## Scope and Transition to Qualtrics

- The source data is public CMS HCAHPS hospital-level reporting data. This is intentional: the hospital-level findings identify where patient-level follow-up should focus.
- Results are limited to Florida hospitals in the 07/01/2024-06/30/2025 reporting period.
- Favorable response rates are survey-volume weighted and depend on valid completed survey counts.
- The Excel dashboard does not show monthly trends because the HCAHPS source is a reporting-period extract.
- The Qualtrics survey has not yet been fielded. Its purpose is to collect patient-level detail that can help explain the hospital-level HCAHPS pattern, especially whether the Medicine Communication and side-effect explanation gap reflects staff education needs, role ownership gaps, timing issues, or discharge workflow design.

## Conclusion

The Excel dashboard identifies Medicine Communication, and especially side-effect explanation, as the strongest candidate for follow-up investigation. The next phase should convert this insight into a targeted Qualtrics implementation survey that asks patients who explained side effects, when and how the explanation happened, whether they understood what to do after discharge, and what hospital process would have made the information clearer.
