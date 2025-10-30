import numpy as np
import cv2
from pathlib import Path
from my_module.k24015.lecture05_camera_image_capture import MyVideoCapture

def k24015_lecture05_01():
    # スクリプトの場所を基準にしたパスを設定
    script_dir = Path(__file__).parent.parent
    images_dir = script_dir / 'images'
    output_dir = script_dir / 'output_images'
    
    # --- カメラからキャプチャ
    app = MyVideoCapture()
    print("カメラを起動します。キャプチャしたいフレームのときにウィンドウで 'q' を押してください。")
    app.run()

    # get_img() でキャプチャ画像を取得
    capture_img = app.get_img()

    # 実行環境でカメラが無い場合のフォールバック
    if capture_img is None:
        print('capture_img is None -> fallback to images/camera_capture.png')
        capture_img = cv2.imread(str(images_dir / 'camera_capture.png'))
        if capture_img is None:
            raise RuntimeError('カメラキャプチャ失敗。fallback 画像も見つかりません。')

    # --- 元画像を読み込む ---
    google_img = cv2.imread(str(images_dir / 'google.png'))
    if google_img is None:
        raise FileNotFoundError('images/google.png が見つかりません')

    # OpenCV 画像は numpy.ndarray
    print('type(google_img)=', type(google_img))
    rows, cols, channels = google_img.shape
    print(f'画像の縦{rows}px, 画像の横{cols}px, カラーチャンネル数{channels}')

    # サンプルピクセル表示 x=640, y=140
    sample_x, sample_y = 640, 140
    if sample_x < cols and sample_y < rows:
        print('sample pixel (B,G,R)=', google_img[sample_y, sample_x])

    # キャプチャ画像サイズ
    c_h, c_w, c_ch = capture_img.shape
    print('capture image size =', capture_img.shape)

    # --- capture_img をグリッド状に並べる ---
    print('グリッド状にタイリングを開始...')
    # 新しいキャンバスを用意してループでコピーする
    tiles_x = (cols + c_w - 1) // c_w
    tiles_y = (rows + c_h - 1) // c_h
    print(f'タイル数: {tiles_x} x {tiles_y}')
    tiled = np.zeros((rows, cols, channels), dtype=np.uint8)

    for ty in range(tiles_y):
        for tx in range(tiles_x):
            sx = tx * c_w
            sy = ty * c_h
            ex = min(sx + c_w, cols)
            ey = min(sy + c_h, rows)
            # コピー元の矩形幅・高さ
            w = ex - sx
            h = ey - sy
            tiled[sy:ey, sx:ex] = capture_img[0:h, 0:w]

    print('タイリング完了')
    # --- 白色ピクセル(255,255,255)をキャプチャで置き換える ---
    print('白色ピクセルの置換を開始...')
    out = google_img.copy()
    for y in range(rows):
        for x in range(cols):
            b, g, r = google_img[y, x]
            if (b, g, r) == (255, 255, 255):
                out[y, x] = tiled[y, x]

    print('白色ピクセルの置換完了')
    # --- 保存 ---
    out_filename = output_dir / 'lecture05_01_k24015.png'
    print(f'保存先: {out_filename}')
    result = cv2.imwrite(str(out_filename), out)
    if result:
        print(f'✓ Saved: {out_filename}')
    else:
        print(f'✗ Failed to save: {out_filename}')


if __name__ == '__main__':
    k24015_lecture05_01
