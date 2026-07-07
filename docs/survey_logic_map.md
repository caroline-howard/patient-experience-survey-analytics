# Survey Logic Map

## Embedded Data

| Field | Purpose |
| --- | --- |
| `respondent_id` | Unique respondent tracking field |
| `hospital_id` | Hospital or facility identifier |
| `discharge_date` | Date associated with patient discharge |
| `service_line` | Clinical service or department context |
| `language_preference` | Preferred survey language |
| `follow_up_channel` | Outreach channel used for follow-up |

## Display Logic

| Condition | Displayed Content |
| --- | --- |
| Low rating on discharge understanding | Open-text prompt about unclear instructions |
| Low rating on follow-up support | Follow-up needs detail question |
| Medication instruction concern selected | Medication clarity follow-up prompt |
| Low medication side-effect clarity rating | Side-effect explanation follow-up prompt |
| Home support concern selected | Home resource follow-up prompt |

## Branching Logic

| Branch | Trigger | Purpose |
| --- | --- | --- |
| Discharge clarity branch | Disagree or strongly disagree on instruction clarity | Capture details about unclear discharge guidance |
| Follow-up support branch | Disagree or strongly disagree on support received | Identify unmet post-discharge needs |
| Medication clarity branch | Disagree or strongly disagree on medication purpose or side-effect clarity | Identify gaps in medication explanations after discharge |
| Positive experience branch | Agree or strongly agree across core items | Capture drivers of a supportive experience |
