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
print(f"Total Spent: ₼{df['amount'].sum():,.2f}")
print(f"Average Transaction: ₼{df['amount'].mean():.2f}")
print(f"Median Transaction: ₼{df['amount'].median():.2f}")

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
print(f"Average Monthly Spending: ₼{monthly_stats['Total'].mean():,.2f}")
print(f"Highest Month: {monthly_stats['Total'].idxmax()} (₼{monthly_stats['Total'].max():,.2f})")
print(f"Lowest Month: {monthly_stats['Total'].idxmin()} (₼{monthly_stats['Total'].min():,.2f})")

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
            label=f'Average: ₼{monthly_totals.mean():.2f}', linewidth=2)
plt.fill_between(range(len(monthly_totals)), monthly_totals.values,
                 alpha=0.3, color='#2E86AB')
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Total Spending (₼)', fontsize=12, fontweight='bold')
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
plt.ylabel('Spending (₼)', fontsize=12, fontweight='bold')
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
plt.ylabel('Average Spending per Transaction (₼)', fontsize=12, fontweight='bold')
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
plt.xlabel('Total Spending (₼)', fontsize=12, fontweight='bold')
plt.title('Total Spending by Category', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

# Add value labels
for i, (idx, val) in enumerate(top_categories.items()):
    plt.text(val, i, f' ₼{val:,.0f}', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/category_totals.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 6: Spending Heatmap by Hour and Day
plt.figure(figsize=(14, 8))
hourly_daily = df.groupby(['day_of_week', 'hour'])['amount'].sum().unstack(fill_value=0)
hourly_daily = hourly_daily.reindex(day_order)
sns.heatmap(hourly_daily, cmap='YlOrRd', annot=False, fmt='.0f',
            cbar_kws={'label': 'Total Spending (₼)'})
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
ax2.set_xlabel('Average Transaction Amount (₼)', fontsize=12, fontweight='bold')
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
plt.ylabel('Transaction Amount (₼)', fontsize=12, fontweight='bold')
plt.xlabel('Percentile', fontsize=12, fontweight='bold')
plt.title('Spending Distribution by Percentile', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='y', alpha=0.3)

# Add value labels
for i, (p, val) in enumerate(zip(percentiles, percentile_values)):
    plt.text(i, val, f'₼{val:.2f}', ha='center', va='bottom',
             fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/spending_percentiles.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 9: Year-over-Year Comparison
if len(df['year'].unique()) > 1:
    plt.figure(figsize=(14, 7))
    yearly_data = df.groupby(['year', 'month'])['amount'].sum().unstack(fill_value=0)

    for year in yearly_data.index:
        plt.plot(range(1, 13), yearly_data.loc[year], marker='o', linewidth=2.5,
                markersize=8, label=str(year), alpha=0.8)

    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Total Spending (₼)', fontsize=12, fontweight='bold')
    plt.title('Year-over-Year Monthly Spending Comparison', fontsize=16, fontweight='bold', pad=20)
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Year', fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('charts/year_over_year.png', dpi=300, bbox_inches='tight')
    plt.close()

# Chart 10: Quarterly Spending Trends
plt.figure(figsize=(12, 6))
df['quarter'] = df['date'].dt.to_period('Q')
quarterly_data = df.groupby('quarter')['amount'].sum()
quarters_str = [str(q) for q in quarterly_data.index]

bars = plt.bar(range(len(quarterly_data)), quarterly_data.values,
               color=sns.color_palette("viridis", len(quarterly_data)),
               edgecolor='black', linewidth=1.2)
plt.xlabel('Quarter', fontsize=12, fontweight='bold')
plt.ylabel('Total Spending (₼)', fontsize=12, fontweight='bold')
plt.title('Quarterly Spending Trends', fontsize=16, fontweight='bold', pad=20)
plt.xticks(range(len(quarters_str)), quarters_str, rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

# Add value labels
for i, val in enumerate(quarterly_data.values):
    plt.text(i, val, f'₼{val:,.0f}', ha='center', va='bottom',
             fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/quarterly_trends.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 11: Top 15 Most Expensive Transactions
plt.figure(figsize=(12, 8))
top_transactions = df.nlargest(15, 'amount')[['date', 'category', 'amount']].reset_index(drop=True)
colors_top = sns.color_palette("Reds_r", len(top_transactions))

bars = plt.barh(range(len(top_transactions)), top_transactions['amount'],
                color=colors_top, edgecolor='black', linewidth=1.2)
labels = [f"{row['category']} ({row['date'].strftime('%Y-%m-%d')})"
          for _, row in top_transactions.iterrows()]
plt.yticks(range(len(top_transactions)), labels, fontsize=10)
plt.xlabel('Transaction Amount (₼)', fontsize=12, fontweight='bold')
plt.title('Top 15 Most Expensive Transactions', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

# Add value labels
for i, val in enumerate(top_transactions['amount']):
    plt.text(val, i, f' ₼{val:.2f}', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/top_transactions.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 12: Category Spending as Percentage (Donut Chart)
plt.figure(figsize=(10, 8))
category_pct = (category_totals / category_totals.sum()) * 100
colors_donut = sns.color_palette("Set3", len(category_pct))

wedges, texts, autotexts = plt.pie(category_pct, labels=category_pct.index,
                                     autopct='%1.1f%%', startangle=90,
                                     colors=colors_donut, pctdistance=0.85)
# Draw circle for donut
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Add total in center
plt.text(0, 0, f'Total:\n₼{category_totals.sum():,.0f}',
         ha='center', va='center', fontsize=16, fontweight='bold')

plt.title('Category Distribution (% of Total Spending)', fontsize=16,
          fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('charts/category_percentage.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 13: Monthly Growth Rate
plt.figure(figsize=(14, 6))
monthly_growth = monthly_totals.pct_change() * 100
colors_growth = ['green' if x > 0 else 'red' for x in monthly_growth]

plt.bar(range(len(monthly_growth)), monthly_growth.values, color=colors_growth,
        edgecolor='black', linewidth=1.2, alpha=0.7)
plt.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
plt.title('Month-over-Month Spending Growth Rate', fontsize=16, fontweight='bold', pad=20)
plt.xticks(range(len(monthly_growth)), monthly_growth.index.astype(str), rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/growth_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 14: Spending Distribution by Transaction Size
plt.figure(figsize=(12, 6))
bins = [0, 5, 10, 20, 50, 100, 200, 500, df['amount'].max()]
labels = ['<₼5', '₼5-10', '₼10-20', '₼20-50', '₼50-100', '₼100-200', '₼200-500', '>₼500']
df['amount_range'] = pd.cut(df['amount'], bins=bins, labels=labels)
range_counts = df['amount_range'].value_counts().reindex(labels)

colors_range = sns.color_palette("coolwarm", len(range_counts))
bars = plt.bar(range(len(range_counts)), range_counts.values, color=colors_range,
               edgecolor='black', linewidth=1.2)
plt.xlabel('Transaction Size Range', fontsize=12, fontweight='bold')
plt.ylabel('Number of Transactions', fontsize=12, fontweight='bold')
plt.title('Distribution of Transactions by Amount Range', fontsize=16, fontweight='bold', pad=20)
plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

# Add value labels
for i, val in enumerate(range_counts.values):
    plt.text(i, val, f'{val:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/transaction_size_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 15: Average Spending by Month (Across All Years)
plt.figure(figsize=(12, 6))
avg_by_month = df.groupby('month')['amount'].mean()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

colors_months = sns.color_palette("husl", 12)
bars = plt.bar(range(1, 13), avg_by_month.values, color=colors_months,
               edgecolor='black', linewidth=1.2)
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Average Transaction Amount (₼)', fontsize=12, fontweight='bold')
plt.title('Average Transaction Amount by Month (All Years)', fontsize=16, fontweight='bold', pad=20)
plt.xticks(range(1, 13), month_names)
plt.grid(axis='y', alpha=0.3)

# Add value labels
for i, val in enumerate(avg_by_month.values, 1):
    plt.text(i, val, f'₼{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/avg_spending_by_month.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("All 15 charts created successfully in /charts folder!")
print("=" * 60)

# Generate enhanced insights data
top_15_trans = df.nlargest(15, 'amount')[['date', 'category', 'amount']]
yearly_totals = df.groupby('year')['amount'].sum()
quarterly_totals = df.groupby('quarter')['amount'].sum()

insights = {
    'currency': 'AZN (Manat)',
    'summary': {
        'total_spent': float(df['amount'].sum()),
        'total_transactions': int(len(df)),
        'avg_transaction': float(df['amount'].mean()),
        'median_transaction': float(df['amount'].median()),
        'date_range': {
            'start': str(df['date'].min().date()),
            'end': str(df['date'].max().date()),
            'total_days': int((df['date'].max() - df['date'].min()).days)
        }
    },
    'categories': {
        'breakdown': {k: float(v) for k, v in category_totals.to_dict().items()},
        'transaction_counts': {k: int(v) for k, v in df['category'].value_counts().to_dict().items()},
        'top_category': str(category_totals.idxmax()),
        'top_category_amount': float(category_totals.max()),
        'top_category_pct': float((category_totals.max() / df['amount'].sum()) * 100),
        'category_averages': {k: float(v) for k, v in df.groupby('category')['amount'].mean().to_dict().items()}
    },
    'monthly': {
        'avg_spending': float(monthly_totals.mean()),
        'highest_month': str(monthly_totals.idxmax()),
        'highest_month_amount': float(monthly_totals.max()),
        'lowest_month': str(monthly_totals.idxmin()),
        'lowest_month_amount': float(monthly_totals.min()),
        'avg_monthly_transactions': float(df.groupby('year_month').size().mean())
    },
    'yearly': {
        'breakdown': {str(k): float(v) for k, v in yearly_totals.to_dict().items()},
        'avg_yearly_spending': float(yearly_totals.mean())
    },
    'quarterly': {
        'breakdown': {str(k): float(v) for k, v in quarterly_totals.to_dict().items()},
        'avg_quarterly_spending': float(quarterly_totals.mean())
    },
    'daily_patterns': {
        'most_expensive_day': str(daily_spending['mean'].idxmax()),
        'most_expensive_day_avg': float(daily_spending['mean'].max()),
        'cheapest_day': str(daily_spending['mean'].idxmin()),
        'cheapest_day_avg': float(daily_spending['mean'].idxmin()),
        'weekday_avg': float(daily_spending.loc[['Monday', 'Tuesday', 'Wednesday',
                                            'Thursday', 'Friday']]['mean'].mean()),
        'weekend_avg': float(daily_spending.loc[['Saturday', 'Sunday']]['mean'].mean())
    },
    'transaction_analysis': {
        'small_transactions_pct': float((len(df[df['amount'] < 10]) / len(df)) * 100),
        'medium_transactions_pct': float((len(df[(df['amount'] >= 10) & (df['amount'] <= 50)]) / len(df)) * 100),
        'large_transactions_pct': float((len(df[df['amount'] > 50]) / len(df)) * 100),
        'top_15_transactions': [
            {
                'date': str(row['date'].date()),
                'category': str(row['category']),
                'amount': float(row['amount'])
            }
            for _, row in top_15_trans.iterrows()
        ]
    },
    'percentiles': {
        f'{p}th': float(np.percentile(df['amount'], p))
        for p in [10, 25, 50, 75, 90, 95, 99]
    },
    'savings_potential': {
        'if_reduce_restaurant_20pct': float(category_totals.get('Restaurant', 0) * 0.20),
        'if_reduce_coffee_30pct': float(category_totals.get('Coffee', 0) * 0.30),
        'if_reduce_taxi_25pct': float(category_totals.get('Taxi', 0) * 0.25),
        'total_potential_savings': float(
            category_totals.get('Restaurant', 0) * 0.20 +
            category_totals.get('Coffee', 0) * 0.30 +
            category_totals.get('Taxi', 0) * 0.25
        )
    }
}

# Save insights to file
import json
with open('insights.json', 'w') as f:
    json.dump(insights, f, indent=2, default=str)

print("\nInsights saved to insights.json")
