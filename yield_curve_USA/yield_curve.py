import pandas as pd
import matplotlib.pyplot as plt
import datetime

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y"


try:
    df = pd.read_csv(url, 
                     index_col=0, 
                     parse_dates=True, 
                     storage_options={'User-Agent': 'Mozilla/5.0'})
except Exception as e:
    print(f"ダウンロードエラー: {e}")
    exit()

# 1980年以降
df = df[df.index >= '1980-01-01']


target_col = df.columns[0] 
df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
df = df.dropna()


plt.figure(figsize=(12, 6))


plt.plot(df.index, df[target_col], color='black', linewidth=1, label='10Y-2Y Spread')


plt.fill_between(df.index, df[target_col], 0, where=(df[target_col] >= 0), 
                 facecolor='blue', alpha=0.1, interpolate=True)
plt.fill_between(df.index, df[target_col], 0, where=(df[target_col] < 0), 
                 facecolor='red', alpha=0.5, interpolate=True, label='Recession Signal (Inverted Yield)')

plt.axhline(0, color='black', linewidth=1, linestyle='--')


plt.title('US Treasury Yield Spread (10Y - 2Y): The Recession Predictor', fontsize=14)
plt.ylabel('Spread (%)')
plt.grid(True, alpha=0.3)
plt.legend(loc='upper left')


plt.tight_layout()

plt.savefig('yield_curve_analysis.png')
