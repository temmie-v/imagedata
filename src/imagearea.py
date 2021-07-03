# https://hk29.hatenablog.jp/entry/2021/04/10/184155

import os
import cv2
import numpy as np
import scipy.ndimage as ndimage
import pandas as pd

file_path = input('Enter filepath of image : ') 
# like... 'chart.bmp' or 'C:\Users\...\chart.bmp'
basename = os.path.splitext(os.path.basename(file_path))[0]

### 画像読み込み
print('Reading...')
img = cv2.imread(file_path, 1)
# 画像の高さと幅を取得
h, w, c = img.shape
# 拡大(拡大することで輪郭がぼやける。このぼやけにより境界を識別しやすくする)
scale = 3
img_resize = cv2.resize(img, (w * scale, h * scale))

### 画像処理
print('Processing...')
# グレースケールに変換
img_gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
# ガウシアンによるスムージング処理（ぼかし）
img_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
# 二値化と大津処理
r, dst = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# モルフォロジー膨張処理
kernel = np.ones((3,3), np.uint8)
dst = cv2.dilate(dst, kernel, iterations = 1)
# 画像ファイルに保存
cv2.imwrite(basename + '_thresholds.jpg', dst)
# もし画像欠けがあった場合に塗りつぶす処理
dst_fill = ndimage.binary_fill_holes(dst).astype(int) * 255
cv2.imwrite(basename + '_thresholds_fill.jpg', dst_fill)

# 境界を検出して描画する
print('Detecting boundaries...')
contours, _ = cv2.findContours(dst_fill.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img_contour = cv2.drawContours(img_resize, contours, -1, (0,0,255), 1)
cv2.imwrite(basename + '_counter.jpg', img_contour)

# 面積、重心、輪郭長さを抽出する
print('Calculating area...')
Areas = []
with open(basename + '_data.csv', 'w') as f:
    for i, contour in enumerate(contours):
        # 面積
        area = cv2.contourArea(contour)
        area = area / 1000
        Areas.append(area)
        # 輪郭の重心
        M = cv2.moments(contour)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])  
        #輪郭（境界）の長さ
        perimeter = cv2.arcLength(contours[i],True)        
        # 画像に出力する
        #img2 = img_resize.copy()
        img2 = cv2.drawContours(img_resize, contours, i, (0, 0, 255), 3)
        cv2.putText(img2, str('{:.1f}'.format(area)), (cx, cy),
                    cv2.FONT_HERSHEY_PLAIN, # フォントタイプ
                    3, # 文字サイズ
                    (0, 0, 0), # 文字色：白(255, 255, 255)　黒(0, 0, 0)
                    2, # 文字太さ
                    cv2.LINE_AA)
        if i == (len(contours)-1):
            img2_resize = cv2.resize(img2, (w, h))
            cv2.imwrite(basename + '_' + str(i) + '.jpg', img2_resize)
        # csvファイルに保存
        if i == 0:
            my_columns_list = ['ID', 'Area', 'x_center_of_gravity', 'y_center_of_gravity', 'Perimeter']
            my_columns_str = ','.join(my_columns_list)
            f.write(my_columns_str + '\n')
        else:
            my_data_list = [str(i), str(area), str(cx), str(cy), str(perimeter)]
            my_data_str = ','.join(my_data_list)
            f.write(my_data_str + '\n')

Area_sum = sum(Areas)

# 面積を割合で出力する
print('Exporting data...')
df = pd.read_csv(basename + '_data.csv')
df[r'Area[%]'] = df['Area'] / Area_sum * 100
df.to_csv(basename + '_data_2.csv')

print('Done.')
