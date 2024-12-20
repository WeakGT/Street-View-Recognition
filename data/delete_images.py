import os
import pandas as pd

# 定義路徑
data_folder = 'processed/test'
csv_path = os.path.join(data_folder, 'test.csv')
txt_path = 'bad_coords.txt'

while input('Have you closed the file "test.csv" yet? (y/n)') != 'y':
    continue    
print('Start progressing...')

# 讀取要刪除的 index
with open(txt_path, 'r') as f:
    indices_to_delete = set(int(line.strip()) for line in f if line.strip().isdigit())

# 讀取 csv 檔
df = pd.read_csv(csv_path)

# 過濾掉要刪除的 rows 並刪除對應的圖片
deleted_images = 0
for index in indices_to_delete:
    row = df[df['index'] == index]
    if not row.empty:
        image_name = row['image'].values[0]
        image_path = os.path.join(data_folder, image_name)
        if os.path.exists(image_path):
            os.remove(image_path)
            deleted_images += 1
            # print(f"Deleted image: {image_path}")

# 更新 DataFrame，刪除指定的 rows
df = df[~df['index'].isin(indices_to_delete)].reset_index(drop=True)

# 將最後的資料往前遞補，並更新 index 與圖片檔名
for new_index, row in df.iterrows():
    current_image_name = row['image']
    expected_image_name = f"streetview{new_index}_{current_image_name.split('_')[1]}"
    
    # 如果圖片名稱不同，進行重新命名
    if current_image_name != expected_image_name:
        current_image_path = os.path.join(data_folder, current_image_name)
        new_image_path = os.path.join(data_folder, expected_image_name)
        
        # 重新命名圖片
        if os.path.exists(current_image_path):
            os.rename(current_image_path, new_image_path)
            # print(f"Renamed image: {current_image_path} -> {new_image_path}")
        else:
            print('    Error: Original file doesn\'t exist')
        
        # 更新 DataFrame 中的圖片名稱
        df.at[new_index, 'image'] = expected_image_name

# 儲存更新後的 CSV 檔案
df['index'] = df.index  # 更新 index 欄位
df.to_csv(csv_path, index=False)
print(f"Updated CSV saved to {csv_path}.")
print(f"Deleted {deleted_images} images, updated indices, and renamed image files.")
print('\nPlease remember to truncate the "bad_coords.txt" file.')
