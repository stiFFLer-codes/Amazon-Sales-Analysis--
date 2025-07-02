# AMAZON SALES ANALYSIS - INNOBYTE SERVICES
# Part 2: Data Cleaning and Preparation
# =====================================

# Assuming df is already loaded from Part 1

print("🧹 DATA CLEANING AND PREPARATION")
print("=" * 50)

# 1. Handle missing values
print("\n1️⃣ MISSING VALUES ANALYSIS")
print("-" * 30)
missing_data = df.isnull().sum()
missing_percentage = (missing_data / len(df)) * 100
missing_df = pd.DataFrame({
    'Column': missing_data.index,
    'Missing_Count': missing_data.values,
    'Missing_Percentage': missing_percentage.values
}).sort_values('Missing_Count', ascending=False)

print(missing_df[missing_df['Missing_Count'] > 0])

# 2. Data type conversions and cleaning
print("\n2️⃣ DATA TYPE CONVERSIONS")
print("-" * 30)

# Convert Date column
df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%y', errors='coerce')
print("✅ Date column converted to datetime")

# Clean Amount column (remove any non-numeric values)
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
print("✅ Amount column cleaned and converted to numeric")

# Clean Qty column
df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0).astype(int)
print("✅ Quantity column cleaned")

# Clean string columns
string_columns = ['ship-city', 'ship-state', 'Category', 'Size', 'Status', 'Fulfilment']
for col in string_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()
print("✅ String columns cleaned and standardized")

# 3. Create additional useful columns
print("\n3️⃣ FEATURE ENGINEERING")
print("-" * 30)

# Extract date components
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Weekday'] = df['Date'].dt.day_name()
df['Month_Name'] = df['Date'].dt.month_name()
print("✅ Date components extracted")

# Create revenue per unit
df['Revenue_Per_Unit'] = df['Amount'] / df['Qty'].replace(0, 1)
print("✅ Revenue per unit calculated")

# Categorize order status
def categorize_status(status):
    if pd.isna(status):
        return 'Unknown'
    status = str(status).lower()
    if 'cancelled' in status:
        return 'Cancelled'
    elif 'delivered' in status:
        return 'Delivered'
    elif 'shipped' in status:
        return 'Shipped'
    elif 'pending' in status:
        return 'Pending'
    else:
        return 'Other'

df['Status_Category'] = df['Status'].apply(categorize_status)
print("✅ Order status categorized")

# 4. Filter valid transactions
print("\n4️⃣ DATA FILTERING")
print("-" * 30)

# Remove records with invalid amounts
initial_count = len(df)
df_clean = df[df['Amount'] > 0].copy()
removed_count = initial_count - len(df_clean)

print(f"Initial records: {initial_count:,}")
print(f"Records with Amount > 0: {len(df_clean):,}")
print(f"Removed records: {removed_count:,} ({removed_count/initial_count*100:.1f}%)")

# 5. Data quality summary
print("\n5️⃣ CLEAN DATA SUMMARY")
print("-" * 30)
print(f"✅ Clean dataset shape: {df_clean.shape}")
print(f"✅ Date range: {df_clean['Date'].min().strftime('%Y-%m-%d')} to {df_clean['Date'].max().strftime('%Y-%m-%d')}")
print(f"✅ Total revenue: ₹{df_clean['Amount'].sum():,.2f}")
print(f"✅ Average order value: ₹{df_clean['Amount'].mean():.2f}")
print(f"✅ Total units sold: {df_clean['Qty'].sum():,}")

# Save cleaned data
df_clean.to_csv('Amazon_Sales_Clean.csv', index=False)
print("\n💾 Cleaned data saved as 'Amazon_Sales_Clean.csv'")

print("\n✅ Part 2 Complete: Data cleaning and preparation finished!")
print("Next: Run Part 3 for Sales Overview Analysis")