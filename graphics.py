import pandas as pd
import matplotlib.pyplot as plt

# Встановлюємо опції виводу даних
pd.set_option('display.max_columns', None)

# Зчитуємо дані з Excel файлу (xlsx)
xlsx_file_path = 'yield.xlsx'
df = pd.read_excel(xlsx_file_path)

# Зберігаємо дані у форматі CSV
csv_file_path = 'yield.csv'
df.to_csv(csv_file_path, index=False)

# Видаляємо непотрібний рядок
df = df.drop([0])  # 0 - індекс першого рядка

# Створюємо словник для відображення поточних та нових назв стовпців
column_mapping = {
    'data1': 'grains_and_legumes',
    'data2': 'sugarbeet',
    'data3': 'sunflower',
    'data4': 'soybeans',
    'data5': 'rapeseed',
    'data6': 'potatoes',
    'data7': 'vegetables',
    'data8': 'fruits_and_berries',
    'attributes': 'regions'
}

# Перейменовуємо стовпці за допомогою методу rename
df.rename(columns=column_mapping, inplace=True)

# Зберігаємо оновлені дані у CSV файл
output_file_path = 'yield.csv'
df.to_csv(output_file_path, index=False)
print(df.head())

# Список посівних культур
crops = {
    'grains_and_legumes': '«Зернові та бобові»',
    'sugarbeet': '«Цукровий буряк»',
    'sunflower': '«Соняшник»',
    'soybeans': '«Соя»',
    'rapeseed': '«Ріпак»',
    'potatoes': '«Картопля»',
    'vegetables': '«Овочі»',
    'fruits_and_berries': '«Фрукти та ягоди»'
}

# Перетворення стовпців врожайності у числові значення
for crop_key, crop_value in crops.items():
    df[crop_key] = pd.to_numeric(df[crop_key], errors='coerce')

# Графіки для кожної посівної культури
for crop_key, crop_value in crops.items():
    # Фільтруємо дані для конкретної культури
    crop_data = df[['regions', 'period', crop_key]]

    # Перетворюємо дані для того, щоб мати регіони як індекс, роки як стовпці, а врожаї як значення
    crop_data_pivot = crop_data.pivot(index='regions', columns='period', values=crop_key)

    # Побудова графіків
    crop_data_pivot.plot(kind='bar', figsize=(18, 10), title=f'Врожайність {crop_value} за регіонами (2015-2022)')
    plt.xlabel('Регіони')
    plt.ylabel('Врожайність')
    plt.xticks(rotation=45)
    plt.yticks(rotation=90)
    plt.legend(title='Рік')
    plt.show()

