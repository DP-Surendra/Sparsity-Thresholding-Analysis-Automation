# config.json Documentation

This configuration file contains parameters for the Sparsity Thresholding Analysis Automation project.  
Below is a description of each key:

## File Paths
- **input_AIO_file_path**: Path to the main input CSV file.
- **input_Data_summary**: Path to the data summary CSV file.

## Date Filters
- **date_filter**: Specifies the date range for filtering data.
  - `start_date`: Start date (format: YYYY-MM-DD).
  - `end_date`: End date (format: YYYY-MM-DD).
- **date_format**: Format of the date in the input files.
- **date_col**: Name of the column containing date information.

## Common Filters
- **common_filter**: Dictionary of filters applied to all data (e.g., filter by Business Unit).

## Metrics
- **target_metric**: List of metrics to analyze.

## Prefix
- **prefix**: Optional prefix for output files or columns.

## Default Values
- **default_values**: Default thresholds and levels used in analysis.
  - `parent_level`: Default parent level value.
  - `granularity_lavel_after_Parent_level`: Default granularity after parent level.
  - `green_thr`: Default green threshold.
  - `orange_thr`: Default orange threshold.
  - `green_active`: Default green active value.
  - `orange_active`: Default orange active value.

## Parent Level Overrides
- **parent_level**: Specific parent level values for different media types.

## Granularity Level After Parent Level
- **granularity_lavel_after_Parent_level**: Exceptions for granularity at next level.

## Thresholds
- **green_thr**: Green threshold values for each media type.
- **orange_thr**: Orange threshold values for each media type.

## Active Values
- **green_active**: Green active values for each media type.
- **orange_active**: Orange active values for each media type.

## Exception Cases
- **exception_case_in_Next_level**: Used to specify exceptions for thresholds or granularity at the next level.

---

**Note:**  
Adjust these parameters as needed for your analysis requirements.
