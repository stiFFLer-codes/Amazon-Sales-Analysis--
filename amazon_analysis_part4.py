# AMAZON SALES ANALYSIS - INNOBYTE SERVICES
# Part 4: Product Analysis (Objective 2)
# ======================================

# Assuming df_clean is available from previous parts

print("🎯 OBJECTIVE 2: PRODUCT ANALYSIS")
print("=" * 50)

# 1. Product Category Performance
print("\n1️⃣ PRODUCT CATEGORY ANALYSIS")
print("-" * 35)

category_analysis = df_clean.groupby('Category').agg({
    'Amount': ['sum', 'mean', 'count'],
    'Qty': ['sum', 'mean'],
    'Revenue_Per_Unit': 'mean'
}).round(2)

category_analysis.columns = ['Total_Revenue', 'Avg_Order_Value', 'Total_Orders', 'Total_Units', 'Avg_Units_Per_Order', 'Revenue_Per_Unit']
category_analysis['Revenue_Share'] = (category_analysis['Total_Revenue'] / df_clean['Amount'].sum() * 100).round(2)
category_analysis['Order_Share'] = (category_analysis['Total_Orders'] / len(df_clean) * 100).round(2)

# Sort by revenue
category_analysis = category_analysis.sort_values('Total_Revenue', ascending=False)

print("🏆 Product Category Performance (by Revenue):")
print(category_analysis)

# Top and bottom performing categories
top_category = category_analysis.index[0]
bottom_category = category_analysis.index[-1]
print(f"\n🥇 Top Category: {top_category} (₹{category_analysis.loc[top_category, 'Total_Revenue']:,.2f})")
print(f"🔻 Bottom Category: {bottom_category} (₹{category_analysis.loc[bottom_category, 'Total_Revenue']:,.2f})")

# 2. Size Analysis
print("\n2️⃣ SIZE VARIANT ANALYSIS")
print("-" * 35)

size_analysis = df_clean.groupby('Size').agg({
    'Amount': ['sum', 'mean', 'count'],
    'Qty': 'sum'
}).round(2)

size_analysis.columns = ['Total_Revenue', 'Avg_Order_Value', 'Total_Orders', 'Total_Units']
size_analysis['Revenue_Share'] = (size_analysis['Total_Revenue'] / df_clean['Amount'].sum() * 100).round(2)
size_analysis = size_analysis.sort_values('Total_Revenue', ascending=False)

print("👕 Size Performance (Top 10):")
print(size_analysis.head(10))

most_popular_size = size_analysis.index[0]
print(f"\n📏 Most Popular Size: {most_popular_size} ({size_analysis.loc[most_popular_size, 'Revenue_Share']:.1f}% of revenue)")

# 3. Category-Size Cross Analysis
print("\n3️⃣ CATEGORY × SIZE CROSS ANALYSIS")
print("-" * 35)

category_size = df_clean.groupby(['Category', 'Size']).agg({
    'Amount': 'sum',
    'Qty': 'sum'
}).round(2)

print("🔍 Top Category-Size Combinations:")
top_combinations = category_size.sort_values('Amount', ascending=False).head(10)
print(top_combinations)

# 4. Product Performance Metrics
print("\n4️⃣ PRODUCT PERFORMANCE METRICS")
print("-" * 35)

# Calculate key metrics per category
performance_metrics = df_clean.groupby('Category').agg({
    'Amount': ['sum', 'mean', 'std', 'min', 'max'],
    'Qty': ['sum', 'mean'],
}).round(2)

performance_metrics.columns = ['Total_Revenue', 'Avg_Revenue', 'Revenue_Std', 'Min_Revenue', 'Max_Revenue', 'Total_Qty', 'Avg_Qty']

# Calculate coefficient of variation (risk measure)
performance_metrics['Revenue_CV'] = (performance_metrics['Revenue_Std'] / performance_metrics['Avg_Revenue'] * 100).round(2)

print("📊 Product Performance Metrics:")
print(performance_metrics)

# 5. Quantity Analysis
print("\n5️⃣ QUANTITY ANALYSIS")
print("-" * 35)

# Quantity distribution
qty_stats = df_clean['Qty'].describe()
print("📦 Quantity Statistics:")
print(qty_stats)

# Most common quantities
qty_distribution = df_clean['Qty'].value_counts().head(10)
print(f"\n🔢 Most Common Order Quantities:")
print(qty_distribution)

# Category with highest average quantity
highest_qty_category = df_clean.groupby('Category')['Qty'].mean().sort_values(ascending=False)
print(f"\n📈 Categories by Average Quantity per Order:")
print(highest_qty_category.round(2))

# 6. Revenue Efficiency Analysis
print("\n6️⃣ REVENUE EFFICIENCY ANALYSIS")
print("-" * 35)

# Revenue per unit by category
revenue_per_unit = df_clean.groupby('Category')['Revenue_Per_Unit'].agg(['mean', 'median', 'std']).round(2)
revenue_per_unit.columns = ['Avg_Revenue_Per_Unit', 'Median_Revenue_Per_Unit', 'Std_Revenue_Per_Unit']

print("💰 Revenue Efficiency by Category:")
print(revenue_per_unit)

most_efficient = revenue_per_unit['Avg_Revenue_Per_Unit'].idxmax()
least_efficient = revenue_per_unit['Avg_Revenue_Per_Unit'].idxmin()

print(f"\n🏆 Most Efficient Category: {most_efficient} (₹{revenue_per_unit.loc[most_efficient, 'Avg_Revenue_Per_Unit']:.2f}/unit)")
print(f"📉 Least Efficient Category: {least_efficient} (₹{revenue_per_unit.loc[least_efficient, 'Avg_Revenue_Per_Unit']:.2f}/unit)")

# 7. Product Portfolio Analysis
print("\n7️⃣ PRODUCT PORTFOLIO ANALYSIS")
print("-" * 35)

# Categorize products by performance
def categorize_product_performance(category_data):
    revenue_threshold = category_data['Total_Revenue'].quantile(0.7)
    order_threshold = category_data['Total_Orders'].quantile(0.7)
    
    def classify(row):
        if row['Total_Revenue'] >= revenue_threshold and row['Total_Orders'] >= order_threshold:
            return 'Star Products'
        elif row['Total_Revenue'] >= revenue_threshold:
            return 'Cash Cows'
        elif row['Total_Orders'] >= order_threshold:
            return 'Popular Products'
        else:
            return 'Question Marks'
    
    return category_data.apply(classify, axis=1)

category_analysis['Product_Type'] = categorize_product_performance(category_analysis)
portfolio_summary = category_analysis['Product_Type'].value_counts()

print("🎯 Product Portfolio Classification:")
print(portfolio_summary)

print(f"\n⭐ Star Products: {', '.join(category_analysis[category_analysis['Product_Type'] == 'Star Products'].index.tolist())}")
print(f"🐄 Cash Cows: {', '.join(category_analysis[category_analysis['Product_Type'] == 'Cash Cows'].index.tolist())}")

# 8. Key Product Insights
print("\n8️⃣ KEY PRODUCT INSIGHTS")
print("-" * 35)

total_categories = len(category_analysis)
top_3_revenue_share = category_analysis.head(3)['Revenue_Share'].sum()

print(f"📊 Total Product Categories: {total_categories}")
print(f"🏆 Top 3 categories account for: {top_3_revenue_share:.1f}% of total revenue")
print(f"📏 Most popular size overall: {most_popular_size}")
print(f"💎 Highest value category: {category_analysis.index[0]} (₹{category_analysis.iloc[0]['Avg_Order_Value']:.2f} AOV)")
print(f"🔄 Most frequently ordered: {category_analysis.sort_values('Total_Orders', ascending=False).index[0]}")

print("\n✅ Part 4 Complete: Product Analysis finished!")
print("Next: Run Part 5 for Fulfilment Analysis")