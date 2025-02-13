import pandas as pd
import matplotlib.pyplot as plt

file_path = 'data.csv'
data = pd.read_csv(file_path, delimiter=';', header=None)

data.columns = ['Year', 'Month', 'Day', 'Decimal_Year', 'Value_2', 'dsfdgs', 'Value_3', 'Flag']
filtered_data = data[data['Value_2'] != -1]
mean_values_by_year = filtered_data.groupby('Year')['Value_2'].mean()
print(mean_values_by_year)
plt.figure(figsize=(12, 6))
plt.plot(mean_values_by_year.index, mean_values_by_year.values, marker='o', label='Среднее значение')
plt.xticks(ticks=range(int(mean_values_by_year.index.min()), int(mean_values_by_year.index.max()) + 4, 4), rotation=45)

plt.title('Средние значения по годам')
plt.xlabel('Год')
plt.ylabel('Среднее значение (пятый столбец)')
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()
