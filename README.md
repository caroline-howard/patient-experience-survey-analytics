# Patient Discharge Experience & Follow-Up Support Analytics

## Overview

This project uses public CMS HCAHPS patient experience data and a Qualtrics follow-up survey design to demonstrate a survey-to-insights workflow focused on discharge experience and follow-up support needs.

The workflow combines public benchmark data, survey instrument design, Python data preparation, and Excel reporting structure. The repository includes documentation for the data source, survey logic, data dictionary, dashboard layout, and insights brief format.

## Purpose

This repository presents a clean portfolio foundation for evaluating patient discharge experience using structured survey data and practical reporting artifacts. It emphasizes the connection between respondent experience, survey design, and stakeholder-ready reporting.

## Data Source: CMS HCAHPS Patient Experience Data

The reporting workflow uses public CMS HCAHPS patient experience data as the primary source for hospital patient experience measures. The data preparation script is structured for loading raw CMS files from `data/raw/`, standardizing fields, filtering discharge-related patient experience measures, and exporting cleaned files to `data/processed/`.

## Qualtrics Follow-Up Survey Design

The Qualtrics follow-up survey design demonstrates survey logic for collecting additional discharge and post-discharge support information. It includes embedded respondent context fields, Likert-scale measures, branching and display logic, and open-text feedback prompts.

## Excel Reporting Workflow

The Excel reporting workflow organizes cleaned CMS HCAHPS data into a dashboard-ready structure. The dashboard summarizes patient experience and discharge-related measures for review, comparison, and communication.

## Repository Structure

```text
data/
  raw/                Source CMS HCAHPS files
  processed/          Cleaned analysis-ready files
docs/                 Project documentation and templates
scripts/              Python data preparation scripts
notebooks/            Exploratory analysis notebooks
excel_dashboard/      Excel workbook assets and dashboard files
reports/              Briefs and reporting outputs
assets/               Supporting images and portfolio assets
```

## Tools

- Python
- pandas
- Excel
- Qualtrics
- CMS HCAHPS

## Portfolio/Resume Framing

This project highlights applied survey analytics skills across public data use, survey instrument design, data preparation, dashboard structuring, and insights communication. It is framed for patient experience analytics, healthcare quality reporting, and survey-to-insights portfolio presentation.
