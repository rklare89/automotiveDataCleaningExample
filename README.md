# Vehicle Sales Data Cleaning Project

## Overview

This project demonstrates data cleaning techniques for a vehicle sales dataset, showcasing skills in handling both numeric and categorical data. The script, `vehicle_data_cleaning.py`, processes the `syedanwarafridi/vehicle-sales-data` dataset from Kaggle, cleaning columns like `year`, `odometer`, `make`, `model`, `trim`, `transmission`, and `body` to prepare them for analysis.

## Dataset

The dataset used is `syedanwarafridi/vehicle-sales-data` from Kaggle, specifically the `car_details.csv` file. It contains vehicle sales data with columns such as:

- `year`: Model year of the vehicle (numeric).
- `odometer`: Mileage of the vehicle (numeric).
- `make`: Vehicle brand (e.g., Toyota, Ford).
- `model`: Vehicle model (e.g., Camry, F-150).
- `trim`: Vehicle trim level (e.g., LE, XLT).
- `transmission`: Transmission type (e.g., automatic, manual).
- `body`: Body type (e.g., sedan, pickup).

The dataset may contain inconsistencies like missing values, typos, or non-standard formats, which this project addresses through systematic cleaning.

## Prerequisites

To run the script, ensure you have the following:

- **Python 3.8+**: The script uses Python for data processing.
- **Required Libraries**:
  - `pandas`: For data manipulation.
  - `numpy`: For numerical operations.
  - `kagglehub`: For downloading the Kaggle dataset.
  Install them using:
  ```bash
  pip install pandas numpy kagglehub
  ```
- **Kaggle API Credentials**:
  - You need a Kaggle account and API token to download the dataset.
  - Set up your Kaggle API credentials:
    1. Go to your Kaggle account settings and create a new API token. This downloads a `kaggle.json` file.
    2. Place `kaggle.json` in `~/.kaggle/` (Linux/Mac) or `%USERPROFILE%\.kaggle\` (Windows).
    3. Ensure the file has appropriate permissions (`chmod 600 ~/.kaggle/kaggle.json` on Linux/Mac).
  - Alternatively, the script includes `kagglehub.login()` for interactive authentication in environments like Jupyter notebooks.
- **Internet Connection**: Required to download the dataset via `kagglehub`.

## File Description

- **dataCleaningExample.py**: The main script that performs the following tasks:
  1. **Loads the Dataset**: Downloads `car_details.csv` from Kaggle using `kagglehub`.
  2. **Drops Missing Values**: Removes rows with any missing data to ensure quality.
  3. **Cleans Numeric Columns**:
     - Converts `year` and `odometer` to integers.
     - Validates ranges (`year`: 1900–2026, `odometer`: 0–999999).
     - Handles invalid values (e.g., non-numeric entries) by replacing them with `-1`.
     - Logs invalid values for transparency.
  4. **Cleans Categorical Columns**:
     - Standardizes `make`, `model`, `trim`, `transmission`, and `body` by:
       - Converting to lowercase and removing whitespace.
       - Applying mappings to fix typos/synonyms (e.g., `chevy` → `Chevrolet`, `g sedan` → `sedan`).
       - Capitalizing `make`, `model`, `trim`, and `body` for consistency (e.g., `toyota` → `Toyota`).
     - Handles missing values:
       - Drops rows with missing `make` or `model` (critical columns).
       - Imputes missing `trim`, `transmission`, or `body` with `Unknown`.
     - Reduces cardinality for `trim` and `body` by grouping rare values (<1% frequency) into `Other`.
     - Converts columns to `category` type for efficiency.
     - Logs all cleaning actions (e.g., rows dropped, values mapped).
  5. **Displays Results**: Prints the cleaned DataFrame, data types, and logs for numeric and categorical cleaning.

## How to Run

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install pandas numpy kagglehub
   ```

3. **Set Up Kaggle API**:
   - Follow the instructions in the *Prerequisites* section to configure your Kaggle API credentials.
   - If running in an interactive environment (e.g., Jupyter), the script’s `kagglehub.login()` will prompt for credentials if needed.

4. **Run the Script**:
   ```bash
   python dataCleaningExample.py
   ```

5. **Expected Output**:
   - Confirmation of dataset loading.
   - Shape of the DataFrame after dropping missing values.
   - Logs of invalid numeric values (e.g., non-numeric `year` entries).
   - Summaries of categorical cleaning actions (e.g., mappings applied, rows dropped).
   - A preview of the cleaned DataFrame and its data types.

## Example Output

```plaintext
Dataset loaded successfully.
Shape after dropping missing values: (5396, 11)
Column 'year' has invalid values: [(123, 'N/A'), (456, 'invalid')]
Column 'odometer' has invalid values: [(789, 'unknown')]
Cleaning summary for make: ['Applied make mapping: {...}', 'Converted make to category type']
Cleaning summary for body: ['Applied body mapping: {...}', 'Imputed missing body with Unknown', 'Grouped 3 rare body values into Other', 'Converted body to category type']
...
Cleaned DataFrame:
   year  odometer     make   model  trim transmission   body
0  2019    50000   Toyota   Camry    LE   automatic  Sedan
1  2020    60000     Ford   F-150   XLT     manual Pickup
...
Data types:
year             int32
odometer         int32
make          category
model         category
trim          category
transmission  category
body          category
...
```

## Portfolio Highlights

This project showcases the following skills:

- **Data Cleaning**: Handling numeric (`year`, `odometer`) and categorical (`make`, `model`, `trim`, `transmission`, `body`) data with techniques like type conversion, standardization, missing value imputation, and cardinality reduction.
- **Error Handling**: Robust try-except blocks and logging of invalid values and cleaning actions.
- **Domain Knowledge**: Understanding vehicle data nuances (e.g., critical columns like `make`, valid year ranges, body type variants).
- **Modular Code**: Reusable functions (`convert_columns_to_int`, `clean_categorical_columns`) for scalability.
- **Reproducibility**: Clear setup instructions and use of a public Kaggle dataset.

To enhance the project, consider:
- Adding visualizations (e.g., bar plots of `body` or `make` distributions) to show cleaning impact.
- Displaying before-and-after value counts for categorical columns.
- Testing edge cases (e.g., a DataFrame with messy `body` values) to demonstrate robustness.

## Notes

- **Dataset Columns**: The script assumes `car_details.csv` contains `year`, `odometer`, `make`, `model`, `trim`, `transmission`, and `body`. If column names differ, update `col_to_int` or `col_to_clean` accordingly.
- **Kaggle API**: Ensure your environment has internet access and Kaggle credentials to download the dataset.
- **Extensibility**: The `make_map`, `transmission_map`, and `body_map` dictionaries can be expanded for datasets with more inconsistencies.

## License

This project is licensed under the MIT License.

## Contact

For questions or feedback, please contact Allen Klare at allenklare33@gmail.com.
