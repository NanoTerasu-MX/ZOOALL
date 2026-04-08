import cv2
import numpy as np
from typing import Optional, Tuple

def find_first_rectangle_center(image_path: str) -> Optional[Tuple[int, int]]:
    """
    指定された画像ファイルから、最初に見つかった四角形の重心座標 (cX, cY) を計算して返します。

    Args:
        image_path (str): 画像ファイルへのパス。

    Returns:
        Optional[Tuple[int, int]]: 重心座標 (cX, cY) のタプル。四角形が見つからない場合は None。
    """
    # 1. 画像の読み込み
    image = cv2.imread(image_path)
    if image is None:
        print(f"エラー: 画像 '{image_path}' を読み込めませんでした。")
        return None

    # 2. 前処理 (グレースケール変換と閾値処理)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ぼかし処理を加えることで、ノイズによる誤検出を減らすこともできます
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 3. 輪郭の検出
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 4. 輪郭のフィルタリングと重心の計算
    for contour in contours:
        # 輪郭の周囲長を計算
        peri = cv2.arcLength(contour, True)
        
        # 輪郭を近似して頂点の数を取得
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        
        # 頂点の数が4つであるか確認 (四角形と判断)
        if len(approx) == 4:
            # --- 重心計算 ---
            M = cv2.moments(contour)
            
            # モーメントがゼロでないことを確認 (有効な輪郭であること)
            if M["m00"] != 0:
                cX = M["m10"] / M["m00"]
                cY = M["m01"] / M["m00"]
                
                # 最初に見つかった四角形の重心を返して関数を終了
                return (cX, cY)
    
    # ループが終了しても四角形が見つからなかった場合
    return None

# --- 使用例 ---
if __name__ == '__main__':
    # 'test_image.jpg'を実際に存在する画像ファイル名に置き換えてください

    import os
    import matplotlib.pyplot as plt
    import numpy as np

    i = 1
    x = np.array([])
    y = np.array([])

    image_dir = '/data/mxstaff/AlignmentData/2025B/251108/monitor_beam/'
    while True:
        if not os.path.exists(os.path.join(image_dir, f'nocross_{i:03d}.ppm')):
            print("No more images to process.")
            break
        image_file = os.path.join(image_dir, f'nocross_{i:03d}.ppm')
        center_coords = find_first_rectangle_center(image_file)
        x = np.append(x, center_coords[0] if center_coords else np.nan)
        y = np.append(y, center_coords[1] if center_coords else np.nan)
        i += 1
        
    plt.plot(x, 'o-', label='X Coordinate')
    plt.plot(y, 'o-', label='Y Coordinate')
    plt.xlabel('Image Index')
    plt.ylabel('Coordinate Value')
    plt.title('Center Coordinates of Detected Rectangles')
    plt.legend()
    plt.show() 
    
    print("Finished processing images.")