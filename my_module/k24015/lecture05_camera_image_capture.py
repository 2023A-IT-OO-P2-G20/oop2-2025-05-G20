import numpy as np
import cv2


class MyVideoCapture:
    """Webカメラから映像を取得し、最後にキャプチャしたフレームを保持するクラス。

    run() を実行して 'q' キーで終了すると、そのときのフレームが get_img() で取得できます。
    このモジュール自身でファイル保存する必要はありません（保存機能は呼ばないで下さい）。
    """

    DELAY: int = 100

    def __init__(self) -> None:
        # カメラを初期化（必要に応じてデバイスIDを変更）
        self.cap: cv2.VideoCapture = cv2.VideoCapture(0)
        # 希望サイズ: 640x480（指定どおり）
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.captured_img: np.ndarray | None = None

    def run(self) -> None:
        """カメラ映像を表示し、'q' キーで終了すると最後のフレームを保持する。"""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # 加工表示は行うが、元のフレームはそのまま保持できるようコピー
            img = np.copy(frame)
            rows, cols, _ = img.shape
            center = (int(cols / 2), int(rows / 2))
            img = cv2.circle(img, center, 30, (0, 0, 255), 3)

            # 左右反転して表示（見た目用）
            disp = cv2.flip(img, 1)
            cv2.imshow('Camera - press q to capture', disp)

            if cv2.waitKey(self.DELAY) & 0xFF == ord('q'):
                # 'q' 押下でその時点のフレームを保存して終了
                self.captured_img = frame
                break

        # 終了処理
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

    def get_img(self) -> np.ndarray | None:
        """最後にキャプチャした画像を返す。未キャプチャの場合は None を返す。"""
        return self.captured_img

    def write_img(self, filepath: str = 'output_images/camera_capture.png') -> None:
        """（補助）キャプチャ画像を保存するユーティリティ。メインからは呼ばないこと。"""
        if self.captured_img is None:
            raise ValueError('キャプチャ画像がありません。')
        cv2.imwrite(filepath, self.captured_img)


if __name__ == '__main__':
    app = MyVideoCapture()
    app.run()
    if app.get_img() is not None:
        print('Captured image available (not saved).')
    else:
        print('No image captured.')
