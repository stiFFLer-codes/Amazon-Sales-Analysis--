# AMAZON SALES ANALYSIS - INNOBYTE SERVICES
# Part 1: Data Loading and Initial Setup
# ===========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("🔍 AMAZON SALES ANALYSIS - INNOBYTE SERVICES")
print("=" * 60)

# Load the dataset
try:
    df = pd.read_csv('Amazon Sale Report.csv')
    print(f"✅ Dataset loaded successfully!")
    print(f"📊 Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
except FileNotFoundError:
    print("❌ Error: Please ensure 'Amazon Sale Report.csv' is in the same directory")
    exit()

# Display basic info
print("\n📋 DATASET OVERVIEW")
print("-" * 40)
print(f"Total Records: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Column information
print("\n📝 COLUMN INFORMATION")
print("-" * 40)
for i, col in enumerate(df.columns, 1):
    dtype = df[col].dtype
    null_count = df[col].isnull().sum()
    null_pct = (null_count / len(df)) * 100
    print(f"{i:2d}. {col:<20} | {str(dtype):<10} | Nulls: {null_count:>6} ({null_pct:>5.1f}%)")

# First few rows
print("\n🔍 SAMPLE DATA (First 5 rows)")
print("-" * 40)
print(df.head())

print("\n✅ Part 1 Complete: Data successfully loaded and explored!")
print("Next: Run Part 2 for Data Cleaning and Preparation")