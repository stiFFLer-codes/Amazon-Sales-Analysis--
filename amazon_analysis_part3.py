# AMAZON SALES ANALYSIS - INNOBYTE SERVICES
# Part 3: Sales Overview Analysis (Objective 1)
# =============================================

# Assuming df_clean is available from Part 2

print("🎯 OBJECTIVE 1: SALES OVERVIEW ANALYSIS")
print("=" * 50)

# 1. Key Performance Indicators (KPIs)
print("\n1️⃣ KEY PERFORMANCE INDICATORS")
print("-" * 35)

total_revenue = df_clean['Amount'].sum()
total_orders = len(df_clean)
total_units = df_clean['Qty'].sum()
avg_order_value = df_clean['Amount'].mean()
avg_units_per_order = df_clean['Qty'].mean()
revenue_per_unit = total_revenue / total_units

print(f"💰 Total Revenue: ₹{total_revenue:,.2f}")
print(f"📦 Total Orders: {total_orders:,}")
print(f"🛍️  Total Units Sold: {total_units:,}")
print(f"💳 Average Order Value: ₹{avg_order_value:.2f}")
print(f"📊 Average Units per Order: {avg_units_per_order:.2f}")
print(f"💵 Revenue per Unit: ₹{revenue_per_unit:.2f}")

# 2. Monthly Sales Trends
print("\n2️⃣ MONTHLY SALES PERFORMANCE")
print("-" * 35)

monthly_sales = df_clean.groupby(['Year', 'Month']).agg({
    'Amount': ['sum', 'mean', 'count'],
    'Qty': 'sum'
}).round(2)

monthly_sales.columns = ['Total_Revenue', 'Avg_Order_Value', 'Total_Orders', 'Total_Units']
monthly_sales = monthly_sales.reset_index()
monthly_sales['Month_Name'] = pd.to_datetime(monthly_sales[['Year', 'Month']].assign(day=1)).dt.strftime('%B %Y')

print("📈 Monthly Performance Summary:")
print(monthly_sales[['Month_Name', 'Total_Revenue', 'Total_Orders', 'Avg_Order_Value']].head(10))

# 3. Daily Sales Patterns
print("\n3️⃣ DAILY SALES PATTERNS")
print("-" * 35)

daily_pattern = df_clean.groupby('Weekday').agg({
    'Amount': ['sum', 'mean', 'count'],
    'Qty': 'sum'
}).round(2)

daily_pattern.columns = ['Total_Revenue', 'Avg_Order_Value', 'Total_Orders', 'Total_Units']
daily_pattern = daily_pattern.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

print("📅 Sales by Day of Week:")
print(daily_pattern)

# 4. Order Status Analysis
print("\n4️⃣ ORDER STATUS ANALYSIS")
print("-" * 35)

status_analysis = df_clean.groupby('Status_Category').agg({
    'Amount': ['sum', 'count'],
    'Qty': 'sum'
}).round(2)

status_analysis.columns = ['Total_Revenue', 'Order_Count', 'Total_Units']
status_analysis['Revenue_Percentage'] = (status_analysis['Total_Revenue'] / total_revenue * 100).round(2)
status_analysis['Order_Percentage'] = (status_analysis['Order_Count'] / total_orders * 100).round(2)

print("📊 Performance by Order Status:")
print(status_analysis.sort_values('Total_Revenue', ascending=False))

# 5. Revenue Distribution Analysis
print("\n5️⃣ REVENUE DISTRIBUTION ANALYSIS")
print("-" * 35)

# Order value ranges
def categorize_order_value(amount):
    if amount < 300:
        return 'Low (< ₹300)'
    elif amount < 600:
        return 'Medium (₹300-600)'
    elif amount < 1000:
        return 'High (₹600-1000)'
    else:
        return 'Premium (₹1000+)'

df_clean['Order_Value_Category'] = df_clean['Amount'].apply(categorize_order_value)

value_distribution = df_clean.groupby('Order_Value_Category').agg({
    'Amount': ['sum', 'count', 'mean'],
    'Qty': 'sum'
}).round(2)

value_distribution.columns = ['Total_Revenue', 'Order_Count', 'Avg_Amount', 'Total_Units']
value_distribution['Revenue_Share'] = (value_distribution['Total_Revenue'] / total_revenue * 100).round(2)

print("💎 Revenue Distribution by Order Value:")
print(value_distribution)

# 6. Growth Analysis (if multiple months available)
print("\n6️⃣ GROWTH TRENDS")
print("-" * 35)

if len(monthly_sales) > 1:
    monthly_sales['Revenue_Growth'] = monthly_sales['Total_Revenue'].pct_change() * 100
    monthly_sales['Order_Growth'] = monthly_sales['Total_Orders'].pct_change() * 100
    
    print("📈 Month-over-Month Growth:")
    growth_summary = monthly_sales[['Month_Name', 'Revenue_Growth', 'Order_Growth']].dropna()
    print(growth_summary.round(2))
else:
    print("⚠️ Insufficient data for growth analysis (single month)")

# 7. Summary Insights
print("\n7️⃣ KEY SALES INSIGHTS")
print("-" * 35)

best_day = daily_pattern['Total_Revenue'].idxmax()
worst_day = daily_pattern['Total_Revenue'].idxmin()
best_status = status_analysis['Total_Revenue'].idxmax()
dominant_value_category = value_distribution['Revenue_Share'].idxmax()

print(f"🏆 Best performing day: {best_day}")
print(f"📉 Lowest performing day: {worst_day}")
print(f"✅ Most successful order status: {best_status}")
print(f"💰 Dominant order value category: {dominant_value_category}")
print(f"📊 Revenue concentration: {value_distribution.loc[dominant_value_category, 'Revenue_Share']:.1f}% in {dominant_value_category}")

print("\n✅ Part 3 Complete: Sales Overview Analysis finished!")
print("Next: Run Part 4 for Product Analysis")