import pandas as pd

# ==========================================
# SELF-ASSESSMENT REFLECTIONS (Lab 14)
# 1. Dropping rows vs filling missing values feels most ambiguous when dealing 
#    with essential IDs or dates. Without business context, deciding whether to 
#    drop an entire transaction or impute a default can alter financial totals.
# 2. Comments are written to explain the 'why' behind dropping rows, coercing 
#    types, and cleaning duplicates, making the data pipeline transparent.
# 3. Running describe() revealed negative revenues and incorrectly parsed quantities 
#    that standard imports wouldn't flag automatically.
# ==========================================

# EXERCISE 1: Inspect
df = pd.read_csv('data/messy_sales.csv')
print("--- EXERCISE 1: INFO & NULLS ---")
print(df.info())
print(df.isnull().sum())
# Data Quality Issues observed:
# 1. 'unit_price' has 1 missing value and is stored as string due to '$' signs.
# 2. 'order_date' contains an invalid string format entry ('invalid_date').
# 3. 'quantity_sold' has non-numeric entries ('abc') forcing object dtype.

# EXERCISE 2: Standardize column names
df.columns = df.columns.str.lower().str.replace(' ', '_')
print("\n--- EXERCISE 2: STANDARDIZED COLUMNS ---")
print(df.columns.tolist())

# EXERCISE 3: Handle missing values
print(f"\nShape before dropping essential rows: {df.shape}")
df = df.dropna(subset=['order_id'] if 'order_id' in df.columns else ['customer_id', 'order_date'])
print(f"Shape after dropping essential rows: {df.shape}")
# Fill remaining missing numeric values with column mean if applicable
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_cols:
    df[col] = df[col].fillna(df[col].mean())

# EXERCISE 4: Fix types
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
# Clean unit_price by stripping '$' if present and converting to numeric
if df['unit_price'].dtype == 'object':
    df['unit_price'] = df['unit_price'].astype(str).str.replace('$', '', regex=False)
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
print("\n--- EXERCISE 4: FIXED DTYPES ---")
print(df.dtypes)

# EXERCISE 5: Check duplicates
print(f"\nDuplicate count: {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"Shape after dropping duplicates: {df.shape}")

# EXERCISE 6: Describe
print("\n--- EXERCISE 6: DESCRIBE STATS ---")
print(df.describe())
# Suspicious items: Negative revenue/prices could represent returns or data entry errors.

# EXERCISE 7: Save and reload
df.to_csv('data/clean_sales.csv', index=False)
reloaded_df = pd.read_csv('data/clean_sales.csv')
print("\n--- EXERCISE 7: RELOADED INFO ---")
print(reloaded_df.info())