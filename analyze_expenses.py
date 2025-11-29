import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Read data
df = pd.read_csv('budget.csv')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['year_month'] = df['date'].dt.to_period('M')
df['day_of_week'] = df['date'].dt.day_name()
df['hour'] = df['date'].dt.hour

# Print basic statistics
print("=" * 60)
print("EXPENSE DATA ANALYSIS")
print("=" * 60)
print(f"\nTotal Transactions: {len(df):,}")
print(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Total Spent: ${df['amount'].sum():,.2f}")
print(f"Average Transaction: ${df['amount'].mean():.2f}")
print(f"Median Transaction: ${df['amount'].median():.2f}")

# Category breakdown
print("\n" + "=" * 60)
print("SPENDING BY CATEGORY")
print("=" * 60)
category_stats = df.groupby('category').agg({
    'amount': ['sum', 'count', 'mean']
}).round(2)
category_stats.columns = ['Total', 'Count', 'Avg']
category_stats = category_stats.sort_values('Total', ascending=False)
print(category_stats)

# Monthly statistics
monthly_stats = df.groupby('year_month')['amount'].agg(['sum', 'count', 'mean']).round(2)
monthly_stats.columns = ['Total', 'Transactions', 'Average']

print("\n" + "=" * 60)
print("MONTHLY SPENDING TRENDS")
print("=" * 60)
print(f"Average Monthly Spending: ${monthly_stats['Total'].mean():,.2f}")
print(f"Highest Month: {monthly_stats['Total'].idxmax()} (${monthly_stats['Total'].max():,.2f})")
print(f"Lowest Month: {monthly_stats['Total'].idxmin()} (${monthly_stats['Total'].min():,.2f})")

# Chart 1: Total Spending by Category (Pie Chart)
plt.figure(figsize=(10, 8))
category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
colors = sns.color_palette("husl", len(category_totals))
plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%',
        startangle=90, colors=colors)
plt.title('Spending Distribution by Category', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('charts/spending_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 2: Monthly Spending Trend
plt.figure(figsize=(14, 6))
monthly_totals = df.groupby('year_month')['amount'].sum()
plt.plot(monthly_totals.index.astype(str), monthly_totals.values,
         marker='o', linewidth=2, markersize=6, color='#2E86AB')
plt.axhline(y=monthly_totals.mean(), color='r', linestyle='--',
            label=f'Average: ${monthly_totals.mean():.2f}', linewidth=2)
plt.fill_between(range(len(monthly_totals)), monthly_totals.values,
                 alpha=0.3, color='#2E86AB')
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Total Spending ($)', fontsize=12, fontweight='bold')
plt.title('Monthly Spending Trend', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/monthly_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 3: Category Spending Over Time (Stacked Area)
plt.figure(figsize=(14, 7))
category_monthly = df.groupby(['year_month', 'category'])['amount'].sum().unstack(fill_value=0)
category_monthly.plot(kind='area', stacked=True, alpha=0.7,
                     colormap='tab10', ax=plt.gca())
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Spending ($)', fontsize=12, fontweight='bold')
plt.title('Category Spending Trends Over Time', fontsize=16, fontweight='bold', pad=20)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/category_trends.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 4: Average Daily Spending by Day of Week
plt.figure(figsize=(12, 6))
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_spending = df.groupby('day_of_week')['amount'].agg(['sum', 'count', 'mean'])
daily_spending = daily_spending.reindex(day_order)
colors_week = ['#FF6B6B' if day in ['Saturday', 'Sunday'] else '#4ECDC4'
               for day in day_order]
bars = plt.bar(range(len(day_order)), daily_spending['mean'], color=colors_week,
               edgecolor='black', linewidth=1.2)
plt.xlabel('Day of Week', fontsize=12, fontweight='bold')
plt.ylabel('Average Spending per Transaction ($)', fontsize=12, fontweight='bold')
plt.title('Average Spending by Day of Week', fontsize=16, fontweight='bold', pad=20)
plt.xticks(range(len(day_order)), day_order, rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/spending_by_day.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 5: Top Categories Bar Chart
plt.figure(figsize=(12, 7))
top_categories = df.groupby('category')['amount'].sum().sort_values(ascending=True)
colors_bar = sns.color_palette("RdYlGn_r", len(top_categories))
bars = plt.barh(range(len(top_categories)), top_categories.values, color=colors_bar,
                edgecolor='black', linewidth=1.2)
plt.yticks(range(len(top_categories)), top_categories.index, fontsize=11)
plt.xlabel('Total Spending ($)', fontsize=12, fontweight='bold')
plt.title('Total Spending by Category', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

# Add value labels
for i, (idx, val) in enumerate(top_categories.items()):
    plt.text(val, i, f' ${val:,.0f}', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/category_totals.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 6: Spending Heatmap by Hour and Day
plt.figure(figsize=(14, 8))
hourly_daily = df.groupby(['day_of_week', 'hour'])['amount'].sum().unstack(fill_value=0)
hourly_daily = hourly_daily.reindex(day_order)
sns.heatmap(hourly_daily, cmap='YlOrRd', annot=False, fmt='.0f',
            cbar_kws={'label': 'Total Spending ($)'})
plt.xlabel('Hour of Day', fontsize=12, fontweight='bold')
plt.ylabel('Day of Week', fontsize=12, fontweight='bold')
plt.title('Spending Patterns by Day and Hour', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('charts/spending_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 7: Transaction Count vs Amount by Category
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Transaction count
category_counts = df['category'].value_counts().sort_values(ascending=True)
colors_count = sns.color_palette("viridis", len(category_counts))
ax1.barh(range(len(category_counts)), category_counts.values,
         color=colors_count, edgecolor='black', linewidth=1.2)
ax1.set_yticks(range(len(category_counts)))
ax1.set_yticklabels(category_counts.index)
ax1.set_xlabel('Number of Transactions', fontsize=12, fontweight='bold')
ax1.set_title('Transaction Frequency by Category', fontsize=14, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Average amount
category_avg = df.groupby('category')['amount'].mean().sort_values(ascending=True)
colors_avg = sns.color_palette("plasma", len(category_avg))
ax2.barh(range(len(category_avg)), category_avg.values,
         color=colors_avg, edgecolor='black', linewidth=1.2)
ax2.set_yticks(range(len(category_avg)))
ax2.set_yticklabels(category_avg.index)
ax2.set_xlabel('Average Transaction Amount ($)', fontsize=12, fontweight='bold')
ax2.set_title('Average Spending per Transaction', fontsize=14, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('charts/transaction_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 8: Spending Percentile Distribution
plt.figure(figsize=(12, 6))
percentiles = [10, 25, 50, 75, 90, 95, 99]
percentile_values = [np.percentile(df['amount'], p) for p in percentiles]

bars = plt.bar([f'{p}th' for p in percentiles], percentile_values,
               color=sns.color_palette("coolwarm", len(percentiles)),
               edgecolor='black', linewidth=1.2)
plt.ylabel('Transaction Amount ($)', fontsize=12, fontweight='bold')
plt.xlabel('Percentile', fontsize=12, fontweight='bold')
plt.title('Spending Distribution by Percentile', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='y', alpha=0.3)

# Add value labels
for i, (p, val) in enumerate(zip(percentiles, percentile_values)):
    plt.text(i, val, f'${val:.2f}', ha='center', va='bottom',
             fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/spending_percentiles.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("All charts created successfully in /charts folder!")
print("=" * 60)

# Generate insights data
insights = {
    'total_spent': df['amount'].sum(),
    'total_transactions': len(df),
    'avg_transaction': df['amount'].mean(),
    'top_category': category_totals.idxmax(),
    'top_category_amount': category_totals.max(),
    'top_category_pct': (category_totals.max() / df['amount'].sum()) * 100,
    'monthly_avg': monthly_totals.mean(),
    'highest_month': str(monthly_totals.idxmax()),
    'highest_month_amount': monthly_totals.max(),
    'lowest_month': str(monthly_totals.idxmin()),
    'lowest_month_amount': monthly_totals.min(),
    'most_expensive_day': daily_spending['mean'].idxmax(),
    'most_expensive_day_avg': daily_spending['mean'].max(),
    'small_transactions_pct': (len(df[df['amount'] < 10]) / len(df)) * 100,
    'large_transactions_pct': (len(df[df['amount'] > 50]) / len(df)) * 100,
    'weekday_avg': daily_spending.loc[['Monday', 'Tuesday', 'Wednesday',
                                        'Thursday', 'Friday']]['mean'].mean(),
    'weekend_avg': daily_spending.loc[['Saturday', 'Sunday']]['mean'].mean(),
    'categories': category_totals.to_dict(),
    'category_counts': df['category'].value_counts().to_dict(),
}

# Save insights to file
import json
with open('insights.json', 'w') as f:
    json.dump(insights, f, indent=2, default=str)

print("\nInsights saved to insights.json")
