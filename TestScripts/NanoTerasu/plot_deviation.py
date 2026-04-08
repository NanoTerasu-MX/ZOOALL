import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
import os

# --- 1. 画像処理関数 (前回の回答のものを流用・float計算を維持) ---

def find_first_rectangle_center(image: np.ndarray) -> Optional[Tuple[float, float]]:
    """
    入力画像から、最初に見つかった四角形の重心座標 (cX, cY) をfloatで計算して返します。

    Args:
        image (np.ndarray): OpenCVで読み込まれた画像データ。

    Returns:
        Optional[Tuple[float, float]]: 重心座標 (cX, cY) のタプル。四角形が見つからない場合は None。
    """
    if image is None:
        return None

    # 2. 前処理 (グレースケール変換と閾値処理)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 3. 輪郭の検出
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 4. 輪郭のフィルタリングと重心の計算
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        
        # 頂点の数が4つであるか確認 (四角形と判断)
        if len(approx) == 4:
            M = cv2.moments(contour)
            
            if M["m00"] != 0:
                # 重心座標をfloatで計算
                cX_float = M["m10"] / M["m00"]
                cY_float = M["m01"] / M["m00"]
                
                # 最初に見つかった四角形の重心を返して終了
                return (cX_float, cY_float)
    
    return None

# --- 2. 連番画像処理とデータ収集 ---

def process_image_sequence(base_dir: str, base_name: str, start_index: int, end_index: int) -> Tuple[List[float], List[float]]:
    """
    連番画像を読み込み、各フレームの四角形重心X, Y座標を収集します。

    Args:
        base_name (str): ファイル名のベース ('nocross').
        start_index (int): 処理を開始する連番インデックス (例: 0).
        end_index (int): 処理を終了する連番インデックス (例: 100).

    Returns:
        Tuple[List[float], List[float]]: (重心X座標のリスト, 重心Y座標のリスト).
    """
    center_x_list = []
    center_y_list = []
    
    for i in range(start_index, end_index + 1):
        # ファイル名を 'nocross_000.ppm', 'nocross_001.ppm' の形式で生成
        filename = os.path.join(base_dir,
                                f"{base_name}_{i:03d}.ppm")
        
        image = cv2.imread(filename)
        
        if image is None:
            # ファイルが見つからないか、読み込みエラー
            print(f"警告: ファイル '{filename}' を読み込めませんでした。処理を終了します。")
            break
            
        # 最初の四角形の重心を計算
        center = find_first_rectangle_center(image)
        
        if center:
            cX, cY = center
            center_x_list.append(cX)
            center_y_list.append(cY)
        else:
            # 四角形が見つからなかった場合、直前の値を使用するか、NaNを追加するなどの処理が可能
            # ここでは、簡単のためリストをそのままにする（データがスキップされる）
            print(f"情報: フレーム {i:03d} で四角形が見つかりませんでした。")

    return center_x_list, center_y_list

# --- 3. プロット処理 ---

def plot_center_changes(center_x_list: List[float], center_y_list: List[float]):
    """
    重心X, Y座標の変化をプロットします。
    """
    if not center_x_list:
        print("プロットするデータがありません。")
        return

    frames = range(len(center_x_list))
    
    # 2つのサブプロットを作成 (X軸の変化とY軸の変化)
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle('Change in Center of Gravity (X and Y)', fontsize=16)

    # X座標の変化をプロット
    axes[0].plot(frames, center_x_list, color='blue', label='Center X')
    axes[0].set_title('Center X Coordinate over Time (Frame Index)')
    axes[0].set_xlabel('Frame Index')
    axes[0].set_ylabel('X Coordinate (pixels)')
    axes[0].grid(True)
    axes[0].legend()

    # Y座標の変化をプロット
    axes[1].plot(frames, center_y_list, color='red', label='Center Y')
    axes[1].set_title('Center Y Coordinate over Time (Frame Index)')
    axes[1].set_xlabel('Frame Index')
    axes[1].set_ylabel('Y Coordinate (pixels)')
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # タイトルが重ならないように調整
    plt.show()

# --- 4. メイン処理 ---

if __name__ == '__main__':
    # --- 設定 ---
    BASE_DIRECTORY = '/data/mxstaff/AlignmentData/2025B/251108/monitor_beam'  # 画像が保存されているディレクトリ
    BASE_FILENAME = 'nocross'
    START_FRAME = 1   # 開始連番
    END_FRAME = 550    # 終了連番 (例: nocross_099.ppmまで処理する場合)
    
    print(f"連番画像 '{BASE_FILENAME}_{START_FRAME:03d}.ppm' から '{BASE_FILENAME}_{END_FRAME:03d}.ppm' までを処理します。")

    # データ収集
    x_data, y_data = process_image_sequence(BASE_DIRECTORY, BASE_FILENAME, START_FRAME, END_FRAME)

    # グラフプロット
    plot_center_changes(x_data, y_data)
    
    print("処理が完了しました。")