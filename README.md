#  HOW TO USE:

This configuration file contains parameters for the Sparsity Thresholding Analysis Automation project.

## Key Input Variables

There are six input variables that may vary across brands, channels, or media types.  
Default values are set at the start, and overrides are allowed for specific cases.

### 1. Parent_level
- **Purpose:** Defines the granularity level at which metrics are calculated (e.g., %Overall Spend Channel, %Year Spend Channel, %Weekly Year Active).
- **Example:** For Paid Media, the level is 5 (Brand * Paid Media * Product Line * Master Channel * Channel).
- **Config Location:**  
  - Default: `default_values.parent_level`
  - Override: `parent_level` (by media type)

### 2. granularity_level_after_Parent_level
- **Purpose:** Specifies the granularity considered after the parent level.
- **Example:**  
  - TV: 1 (after Channel, only Platform is considered)
  - Digital: 2 in PC (Platform and Audience), 3 in B&W (Platform, Audience, Influencer Say)
- **Config Location:**  
  - Default: `default_values.granularity_lavel_after_Parent_level`
  - Override: `granularity_lavel_after_Parent_level` (by Mater channel/media type or Halo..)
  - Further Override: `granularity_lavel_after_Parent_level.exception_case_in_Next_level` (by Channel)

### 3. green_thr
- **Purpose:** The minimum percentage of spend in the last one year that is required within its group to be eligiable for Feature.
- **Config Location:**  
  - Default: `default_values.green_thr`
  - Override: `green_thr` (by Mater channel/media type)
  - Further Override: `green_thr.exception_case_in_Next_level` (by Channel)

### 4. orange_thr
- **Purpose:** The minimum percentage of spend in Overall duration that is required within its group to be eligiable for Feature.
- **Config Location:**  
  - Default: `default_values.orange_thr`
  - Override: `orange_thr` (by Mater channel/media type)
  - Further Override: `orange_thr.exception_case_in_Next_level` (by Channel)

### 5. green_active
- **Purpose:** The minimum percentage of Weekly Activation in the last one year that is required within its group to be eligiable for Feature.
- **Config Location:**  
  - Default: `default_values.green_active`
  - Override: `green_active` (by Mater channel/media type)
  - Further Override: `green_active.exception_case_in_Next_level` (by Channel)

### 6. orange_active
- **Purpose:** The minimum percentage of Weekly Activation in the Overall duration that is required within its group to be eligiable for Feature.
- **Config Location:**  
  - Default: `default_values.orange_active`
  - Override: `orange_active` (by Mater channel/media type)
  - Further Override: `orange_activee.exception_case_in_Next_level` (by Channel)

**How to set Variables:**  
Set default values for all six variables at the start.  
Allow updates/overrides only when a brand, channel, or media type requires different values.

---

## Other Configuration Keys

- **input_AIO_file_path**: Path to the main input CSV file.
- **input_Data_summary**: Path to the data summary CSV file.
- **date_filter**: Specifies the date range for filtering data (`start_date`, `end_date`).
- **date_format**: Format of the date in the input files.
- **date_col**: Name of the column containing date information.
- **common_filter**: Dictionary of filters applied to all data (e.g., filter by Business Unit).
- **target_metric**: List of metrics to analyze.
- **prefix**: Optional prefix for output files or columns.

---


