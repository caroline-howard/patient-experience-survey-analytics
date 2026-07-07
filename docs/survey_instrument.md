# Qualtrics Follow-Up Survey Instrument

## Survey Purpose

The follow-up survey captures additional patient-reported context about discharge experience, medication clarity, and post-discharge support needs. It complements public CMS HCAHPS reporting by demonstrating survey design, respondent context fields, Likert-scale questions, branching logic, and open-text feedback prompts.

The current CMS HCAHPS dashboard identifies medicine communication, especially explanation of possible side effects, as the clearest follow-up area. The survey design should therefore prioritize medication understanding and post-discharge contact/support questions.

## Embedded Respondent Context Fields

- `respondent_id`
- `hospital_id`
- `discharge_date`
- `service_line`
- `language_preference`
- `follow_up_channel`

## Example Survey Sections

### Discharge Understanding

- I understood the instructions I received before leaving the hospital.
- I knew whom to contact if I had questions after discharge.
- I understood how to take my medications after discharge.

Response scale: Strongly disagree, Disagree, Neither agree nor disagree, Agree, Strongly agree

### Follow-Up Support

- I received the follow-up support I needed after leaving the hospital.
- My follow-up appointment instructions were clear.
- I had access to the resources I needed at home.

Response scale: Strongly disagree, Disagree, Neither agree nor disagree, Agree, Strongly agree

### Medication Clarity

- I understood what each new medication was for.
- I understood possible side effects of my medications.
- I knew whom to contact if I had medication questions after leaving the hospital.

Response scale: Strongly disagree, Disagree, Neither agree nor disagree, Agree, Strongly agree

### Open-Text Feedback

- What would have made your discharge experience clearer or more supportive?
- What would have made your medication instructions clearer?
- Is there anything else you would like the care team to know about your experience after discharge?
