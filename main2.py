import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Встановлюємо опції виводу даних
pd.set_option('display.max_columns', None)

# Зчитуємо shape-файл карти України
shapefile_path = 'gadm41_UKR_shp\\gadm41_UKR_2.shp'
ukraine_map = gpd.read_file(shapefile_path)
print(ukraine_map)

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

# Замінюємо значення, щоб вони співпадали в файлах yield.csv і ukraine_map
df['regions'] = df['regions'].replace({'м.Київ': 'Київ'})
df['regions'] = df['regions'].replace({'м.Севастополь': 'Севастополь'})
df['regions'] = df['regions'].replace({'Донецька': 'Доне́цька'})
df['regions'] = df['regions'].replace({'Дніпропетровська': 'Дніпропетро́вська'})

# Зберігаємо змінений DataFrame у CSV-файл
df.to_csv('yield_changed.csv', index=False)

# Перетворення стовпців врожайності у числові значення
for crop_key, crop_value in crops.items():
    df[crop_key] = pd.to_numeric(df[crop_key], errors='coerce')

# Задаємо діапазон років
years = range(2015, 2023)

# Розділяємо DataFrame за кожен рік і зберігаємо в окремий файл
for year in years:
    # Вибираємо дані для поточного року
    df_year = df[df['period'] == year]

    # Зберігаємо дані у файл
    output_file_path = f'yield{year}.csv'
    df_year.to_csv(output_file_path, index=False)

# Об'єднуємо дані
merged_data = ukraine_map.set_index('NL_NAME_1').join(df.set_index('regions'))

# Перетворюємо стовпці врожайності у числові значення
crops = ['grains_and_legumes', 'sugarbeet', 'sunflower', 'soybeans', 'rapeseed', 'potatoes', 'vegetables', 'fruits_and_berries']
for crop in crops:
    merged_data[crop] = pd.to_numeric(merged_data[crop], errors='coerce')

# Графіки для кожного року
years = range(2015, 2023)
for year in years:
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged_data[merged_data['period'] == year].plot(
        column='grains_and_legumes', cmap='viridis', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True
    )
    ax.set_title(f'Врожайність за регіонами України у {year} році')
    ax.set_axis_off()
    plt.show()
