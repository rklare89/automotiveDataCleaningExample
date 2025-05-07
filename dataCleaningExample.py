import pandas as pd
import numpy as np
import kagglehub
from kagglehub import KaggleDatasetAdapter

# This project uses the 'syedanwarafridi/vehicle-sales-data' dataset from Kaggle
# to demonstrate data cleaning methods for vehicle sales analysis.
# The dataset contains vehicle details like year, odometer, make, model, trim, transmission, body, etc.

# Authenticate with Kaggle API (if not already configured)
# Note: Ensure Kaggle API credentials are set up (e.g., ~/.kaggle/kaggle.json) or run interactively
kagglehub.login()

# Load the dataset from Kaggle
try:
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "syedanwarafridi/vehicle-sales-data",
        file_name="car_details.csv",  # Main file in the dataset
    )
    print("Dataset loaded successfully.")
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = pd.DataFrame()  # Fallback empty DataFrame

# Drop rows with any missing values to ensure data quality
new_df = df.dropna(axis=0, how='any')
print(f"Shape after dropping missing values: {new_df.shape}")

# Define columns to convert to integer and their valid ranges
col_to_int = ['year', 'odometer']
valid_ranges = {
    'year': (1900, 2026),  # Vehicle years from 1900 to future year
    'odometer': (0, 999999)  # Mileage from 0 to reasonable max
}

# Convert specified columns to integers and capture invalid values
new_df, invalid_values = convert_columns_to_int(
    new_df,
    col_to_int,
    valid_ranges=valid_ranges,
    default_value=-1,
    verbose=True
)

# Clean categorical columns (make, model, trim, transmission, body)
col_to_clean = ['make', 'model', 'trim', 'transmission', 'body']
new_df, cleaning_log = clean_categorical_columns(
    new_df,
    col_to_clean,
    verbose=True
)

# Display results
print("\nCleaned DataFrame:")
print(new_df.head())
print("\nData types:")
print(new_df.dtypes)
print("\nNumeric invalid values:")
for col, values in invalid_values.items():
    print(f"{col}: {values}")
print("\nCategorical cleaning log:")
for col, log in cleaning_log.items():
    print(f"{col}: {log}")

def convert_columns_to_int(df, columns, valid_ranges=None, default_value=-1, verbose=False):
    """
    Convert specified DataFrame columns to integer type, handling errors and validating ranges.
    
    Parameters:
    - df: pandas DataFrame
    - columns: list of column names to convert
    - valid_ranges: dict mapping column names to (min, max) tuples (optional)
    - default_value: value to replace NaN/invalid values (default: -1)
    - verbose: if True, print details of invalid values (default: False)
    
    Returns:
    - df: DataFrame with converted columns
    - invalid_values: dict mapping column names to lists of (index, original_value) for invalid entries
    """
    invalid_values = {}
    valid_ranges = valid_ranges or {}  # Default to empty dict if None
    
    for col in columns:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame.")
            continue
        
        try:
            # Store original values for logging
            original_values = df[col].copy()
            
            # Convert to numeric, coercing errors to NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Log invalid values (NaN after coercion)
            if df[col].isna().any():
                invalid_indices = df[df[col].isna()].index
                invalid_values[col] = [(idx, original_values[idx]) for idx in invalid_indices]
                if verbose:
                    print(f"Column '{col}' has invalid values: {invalid_values[col]}")
                
                # Replace NaN with default_value
                df[col] = df[col].fillna(default_value)
            
            # Cast to int
            df[col] = df[col].astype(int)
            
            # Validate range if specified for this column
            if col in valid_ranges:
                min_val, max_val = valid_ranges[col]
                if not df[col].between(min_val, max_val).all():
                    out_of_range = df[~df[col].between(min_val, max_val)][col]
                    if verbose:
                        print(f"Column '{col}' has values outside range {valid_ranges[col]}: {out_of_range.values}")
                    df.loc[~df[col].between(min_val, max_val), col] = default_value
            
        except Exception as e:
            print(f"Error converting column '{col}': {e}")
            invalid_values[col] = invalid_values.get(col, []) + [("error", str(e))]
    
    return df, invalid_values

def clean_categorical_columns(df, columns, verbose=False):
    """
    Clean specified categorical DataFrame columns by standardizing text, handling missing values,
    reducing cardinality, and converting to category type.
    
    Parameters:
    - df: pandas DataFrame
    - columns: list of column names to clean
    - verbose: if True, print details of cleaning actions (default: False)
    
    Returns:
    - df: DataFrame with cleaned columns
    - cleaning_log: dict mapping column names to lists of cleaning actions and issues
    """
    cleaning_log = {}
    
    # Common mappings for different ways to label a transmission
    transmission_map = {
        'auto': 'automatic',
        'at': 'automatic',
        '6sp': 'automatic',
        '10sp': 'automatic',
        'man': 'manual',
        'mt': 'manual'
    }
    # Mapping for vehicle makes (expandable for datasets with more inconsistent brand names)
    make_map = {
        'chevy': 'Chevrolet',
        'merc': 'Mercedes-Benz',
        'vw': 'Volkswagen'
    }
    
    # Mapping for vehicle body types to standardize variants
    body_map = {
        'g sedan': 'sedan',
        'hatchback': 'sedan',
        'crew cab': 'pickup',
        'regular cab': 'pickup',
        'extended cab': 'pickup',
        'double cab': 'pickup'
    }
    
    for col in columns:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame.")
            continue
        
        cleaning_log[col] = []
        try:
            # Store original values for logging
            original_values = df[col].copy()
            
            # Standardize text
            df[col] = df[col].str.lower().str.strip()  # Lowercase and remove whitespace
            
            # Apply specific mappings for potential typos/synonyms
            if col == 'transmission':
                df[col] = df[col].replace(transmission_map)
                cleaning_log[col].append(f"Applied transmission mapping: {transmission_map}")
            elif col == 'make':
                df[col] = df[col].replace(make_map)
                cleaning_log[col].append(f"Applied make mapping: {make_map}")
            elif col == 'body':
                df[col] = df[col].replace(body_map)
                cleaning_log[col].append(f"Applied body mapping: {body_map}")
            
            # Capitalize for consistency
            if col in ['make', 'model', 'trim', 'body']:
                df[col] = df[col].str.title()
            
            # Handle missing values
            if df[col].isna().any():
                if col in ['make', 'model']:
                    # Drop rows with missing make or model (critical columns)
                    initial_len = len(df)
                    df = df.dropna(subset=[col])
                    cleaning_log[col].append(f"Dropped {initial_len - len(df)} rows with missing {col}")
                else:
                    # Impute missing trim, transmission, or body with 'Unknown'
                    df[col] = df[col].fillna('Unknown')
                    cleaning_log[col].append(f"Imputed missing {col} with 'Unknown'")
            
            # Reduce cardinality for high-cardinality columns (trim, body)
            if col in ['trim', 'body']:
                # Group rare values (<1% frequency) into 'Other'
                value_counts = df[col].value_counts()
                rare_values = value_counts[value_counts / len(df) < 0.01].index
                if rare_values.any():
                    df.loc[df[col].isin(rare_values), col] = 'Other'
                    cleaning_log[col].append(f"Grouped {len(rare_values)} rare {col} values into 'Other'")
            
            # Convert to category type
            df[col] = df[col].astype('category')
            cleaning_log[col].append(f"Converted {col} to category type")
            
            if verbose:
                print(f"Cleaning summary for {col}: {cleaning_log[col]}")
                
        except Exception as e:
            print(f"Error cleaning column '{col}': {e}")
            cleaning_log[col].append(f"Error: {str(e)}")
    
    return df, cleaning_log