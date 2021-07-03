# imagedata
Detecting boundaries of the image and calculate the area of each.

---

このPythonプログラムは材料科学実験のX線回析のレポートのために作成しました．


# 仕様
- 実行のためには`os`，`cv2`，`numpy`，`scipy`，`pandas`のパッケージが必要です．適宜導入してください．
- 最初に画像のファイルパスの入力を要求します．次のように入力してください：
  - 同じディレクトリにあれば`chart.bmp`のように名前のみ
  - そうでなければフルパス：`C:\Users\...\chart.bmp`
  - bmp形式以外にもjpg，png形式なども対応
- 次の作業を行います：
  - 画像を処理し，`filename + '_thresholds.jpg'`に保存
  - 画像欠けを塗りつぶし，`filename + '_thresholds_fill.jpg'`に保存
  - 境界を検出して描画し，`filename + '_counter.jpg'`に保存
  - **各境界内の面積を計算**
  - 計算結果は
    - 画像として`filename + (領域数) + '.jpg'`に保存
    - 面積・重心についてデータを`basename + '_data.csv'`及びbasename + '_data_2.csv'に保存

以上のようにして，画像から境界を検出して内部の面積を計算します．

# 処理例
(チャートは一部分のみ拡大)
|元の画像|処理後|
|---|---|
|![1](https://user-images.githubusercontent.com/83168581/124359995-566fb800-dc62-11eb-96cf-4be32decdd44.jpg)|![2](https://user-images.githubusercontent.com/83168581/124360004-5cfe2f80-dc62-11eb-8a90-d943609a0a34.jpg)|

この部分に該当するcsvファイルは次のようになります：
| ID  | Area    | x_center_of_gravity | y_center_of_gravity | Perimeter | 
| --- | ------- | ------------------- | ------------------- | --------- | 
| 1   | 0.004   | 9415                | 9025                | 8         | 
| ... |         |                     |                     |           | 
| 177 | 0.02    | 2707                | 5462                | 18        | 
| 178 | 97.5875 | 2707                | 7841                | 7884      | 
|...|||||
