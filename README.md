# Sparsity Thresholding Analysis Automation

## Overview

This project automates the analysis of data sparsity and thresholding for media spend and activity metrics across various brands, channels, and media types. It calculates coverage, applies configurable thresholds, and generates summary statistics to support business decisions in media planning and feature selection.

---

## Key Input Variables

There are six input variables that may vary across brands, channels, or media types.  
Default values are set at the start, and overrides are allowed for specific cases.

1. **Parent_level**
   - **Purpose:** Defines the granularity level at which metrics are calculated (e.g., %Overall Spend Channel, %Year Spend Channel, %Weekly Year Active).
   - **Example:** For Paid Media, the level is 5 (Brand * Paid Media * Product Line * Master Channel * Channel).
   - **Config Location:**  
     - Default: `default_values.parent_level`  
     - Override: `parent_level` (by media type)

2. **granularity_level_after_Parent_level**
   - **Purpose:** Specifies the granularity considered after the parent level.
   - **Example:**  
     - TV: 1 (after Channel, only Platform is considered)  
     - Digital: 2 in PC (Platform and Audience), 3 in B&W (Platform, Audience, Influencer Say)
   - **Config Location:**  
     - Default: `default_values.granularity_lavel_after_Parent_level`  
     - Override: `granularity_lavel_after_Parent_level` (by Master channel/media type or Halo)  
     - Further Override: `granularity_lavel_after_Parent_level.exception_case_in_Next_level` (by Channel)

3. **green_thr**
   - **Purpose:** The minimum percentage of spend in the last one year required within its group to be eligible for feature selection.
   - **Config Location:**  
     - Default: `default_values.green_thr`  
     - Override: `green_thr` (by Master channel/media type or any group)  
     - Further Override: `green_thr.exception_case_in_Next_level` (by Channel or any subgroup)

4. **orange_thr**
   - **Purpose:** The minimum percentage of spend in the overall duration required within its group to be eligible for feature selection.
   - **Config Location:**  
     - Default: `default_values.orange_thr`  
     - Override: `orange_thr` (by Master channel/media type or any group))  
     - Further Override: `orange_thr.exception_case_in_Next_level` (by Channel or any subgroup)

5. **green_active**
   - **Purpose:** The minimum percentage of weekly activation in the last one year required within its group to be eligible for feature selection.
   - **Config Location:**  
     - Default: `default_values.green_active`  
     - Override: `green_active` (by Master channel/media type or any group))  
     - Further Override: `green_active.exception_case_in_Next_level` (by Channel or any subgroup)

6. **orange_active**
   - **Purpose:** The minimum percentage of weekly activation in the overall duration required within its group to be eligible for feature selection.
   - **Config Location:**  
     - Default: `default_values.orange_active`  
     - Override: `orange_active` (by Master channel/media type or any group))  
     - Further Override: `orange_active.exception_case_in_Next_level` (by Channel or any subgroup)

**How to set Variables:**  
Set default values for all six variables at the start.  
Allow updates/overrides only when a brand, channel, or media type requires different values.

---

## Other Configuration Keys

- **input_AIO_file_path:** Path to the main input CSV file.
- **input_Data_summary:** Path to the data summary CSV file.
- **date_filter:** Specifies the date range for filtering data (`start_date`, `end_date`).
- **date_format:** Format of the date in the input files.
- **date_col:** Name of the column containing date information.
- **common_filter:** Dictionary of filters applied to all data (e.g., filter by Business Unit).
- **target_metric:** List of metrics to analyze.
- **prefix:** Optional prefix for output files or columns.

---

## Project Structure

```
Sparsity-Thresholding-Analysis-Automation/
├── config.json
├── utility_thresholding.py
├── New_format_raw_conversion.py
├── utility_automation.py
├── utility_Feature_selaction.py
├── utility_Sparsity.py
└── README.md
```

---

## Module Descriptions

- **utility_thresholding.py:**  
  Contains functions for applying threshold logic, summarizing coverage, and generating pivot tables for spend and activation metrics.

- **New_format_raw_conversion.py:**  
  Handles conversion and preprocessing of raw input data into the required format for analysis.

- **utility_automation.py:**  
  Automates the workflow, orchestrating the application of thresholds, feature selection, and sparsity analysis across datasets.

- **utility_Feature_selaction.py:**  
  Implements logic for selecting features based on coverage, spend, and activation criteria.

- **utility_Sparsity.py:**  
  Analyzes data sparsity, calculates relevant metrics, and supports reporting for decision-making.

---

## Usage Instructions

1. **Configure** input files and parameters in `config.json`.
2. **Run** the main automation script (`utility_automation.py`) to process data and apply analysis.
3. **Review** generated summaries, pivot tables, and feature selection outputs.

---

## Customization

- Adjust parameters in `config.json` to set defaults and overrides for brands, channels, or media types.
- Extend or modify utility modules to support additional analysis or reporting requirements.

---

## Author & Contact

- Surendra Bera 
- surendra.b@datapoem.com

---

## License

Include your license information here.

---

*This documentation provides a comprehensive overview and usage guide for the Sparsity Thresholding Analysis Automation project. Update and expand as needed for your specific workflow and requirements.*


