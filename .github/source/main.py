"""
================================================================================
ファイル名: main.py
作成者: システム開発チーム
作成日: 2026-07-06
更新日: 2026-07-06
バージョン: 1.0
説明: 入力ファイル内の指定文字列を置換するメインプログラム
================================================================================
"""

import sys
from pathlib import Path
from typing import Tuple

# common.write_logモジュールをインポート
sys.path.insert(0, str(Path(__file__).parent))
from common.write_log import WriteLog


class StringReplacer:
    """
    ファイル内の文字列を置換するクラス。
    """

    # 戻り値コード
    RETURN_CODE_SUCCESS: int = 0
    RETURN_CODE_INVALID_ARGS: int = 16
    RETURN_CODE_EMPTY_FROM_STRING: int = 17
    RETURN_CODE_INPUT_FILE_NOT_FOUND: int = 18
    RETURN_CODE_OUTPUT_DIR_NOT_FOUND: int = 19
    RETURN_CODE_OUTPUT_FILE_EXISTS: int = 20
    RETURN_CODE_OUTPUT_FILE_OPEN_FAILED: int = 21
    RETURN_CODE_SAME_FILE_PATH: int = 22
    RETURN_CODE_UNEXPECTED_ERROR: int = 99

    def __init__(self) -> None:
        """StringReplacerクラスの初期化。"""
        self.logger: WriteLog = WriteLog()
        self.return_code: int = self.RETURN_CODE_SUCCESS
        self.replacement_count: int = 0

    def run(self, args: list[str]) -> int:
        """
        メインプログラムの実行。

        Args:
            args (list[str]): コマンドライン引数

        Returns:
            int: 戻り値コード
        """
        try:
            self.logger.write("I", "処理開始")
            print("処理開始")

            # 引数の検証
            if len(args) != 4:
                self.return_code = self.RETURN_CODE_INVALID_ARGS
                error_msg: str = f"エラー内容（return_code={self.return_code}）"
                self.logger.write("E", error_msg)
                sys.stderr.write(error_msg + "\n")
                return self.return_code

            from_string: str = args[0]
            to_string: str = args[1]
            input_file_path: str = args[2]
            output_file_path: str = args[3]

            # 置換前文字列が空文字か確認
            if from_string == "":
                self.return_code = self.RETURN_CODE_EMPTY_FROM_STRING
                error_msg = f"エラー内容（return_code={self.return_code}）"
                self.logger.write("E", error_msg)
                sys.stderr.write(error_msg + "\n")
                return self.return_code

            # 入力ファイルと出力ファイルが同じパスか確認
            if input_file_path == output_file_path:
                self.return_code = self.RETURN_CODE_SAME_FILE_PATH
                error_msg = f"エラー内容（return_code={self.return_code}）"
                self.logger.write("E", error_msg)
                sys.stderr.write(error_msg + "\n")
                return self.return_code

            # 入力ファイルが存在するか確認
            input_file: Path = Path(input_file_path)
            if not input_file.exists():
                self.return_code = self.RETURN_CODE_INPUT_FILE_NOT_FOUND
                error_msg = f"エラー内容（return_code={self.return_code}）"
                self.logger.write("E", error_msg)
                sys.stderr.write(error_msg + "\n")
                return self.return_code

            # 出力ファイルのディレクトリが存在するか確認
            output_file: Path = Path(output_file_path)
            if not output_file.parent.exists():
                self.return_code = self.RETURN_CODE_OUTPUT_DIR_NOT_FOUND
                error_msg = f"エラー内容（return_code={self.return_code}）"
                self.logger.write("E", error_msg)
                sys.stderr.write(error_msg + "\n")
                return self.return_code

            # 出力ファイルが既に存在するか確認
            if output_file.exists():
                self.return_code = self.RETURN_CODE_OUTPUT_FILE_EXISTS
                error_msg = f"エラー内容（return_code={self.return_code}）"
                self.logger.write("E", error_msg)
                sys.stderr.write(error_msg + "\n")
                return self.return_code

            # 入力ファイルを読み込み
            with open(input_file, mode="r", encoding="utf-8") as f:
                file_content: str = f.read()

            # 置換処理を実行
            replaced_content: str = file_content
            self.replacement_count = self._count_and_replace(
                file_content, from_string, to_string
            )
            replaced_content = file_content.replace(from_string, to_string)

            # 出力ファイルに書き込み
            try:
                with open(output_file, mode="w", encoding="utf-8") as f:
                    f.write(replaced_content)
            except Exception as e:
                self.return_code = self.RETURN_CODE_OUTPUT_FILE_OPEN_FAILED
                error_msg = f"エラー内容（return_code={self.return_code}）"
                self.logger.write("E", error_msg)
                sys.stderr.write(error_msg + "\n")
                return self.return_code

            # 成功時のログ出力
            replacement_msg: str = f"置換件数:{self.replacement_count}件"
            self.logger.write("I", replacement_msg)
            print(replacement_msg)

            self.return_code = self.RETURN_CODE_SUCCESS
            finish_msg: str = f"処理終了（return_code={self.return_code}）"
            self.logger.write("I", finish_msg)
            print(finish_msg)

            return self.return_code

        except Exception as e:
            self.return_code = self.RETURN_CODE_UNEXPECTED_ERROR
            error_msg = f"エラー内容（return_code={self.return_code}）"
            self.logger.write("C", error_msg)
            sys.stderr.write(error_msg + "\n")
            return self.return_code

    def _count_and_replace(self, text: str, from_string: str, to_string: str) -> int:
        """
        置換回数をカウント（オーバーラップは考慮しない）。

        Args:
            text (str): 対象テキスト
            from_string (str): 置換前文字列
            to_string (str): 置換後文字列

        Returns:
            int: 置換回数
        """
        count: int = 0
        pos: int = 0

        while True:
            pos = text.find(from_string, pos)
            if pos == -1:
                break
            count += 1
            pos += len(from_string)

        return count


def main() -> None:
    """
    プログラムのエントリーポイント。
    """
    replacer: StringReplacer = StringReplacer()
    return_code: int = replacer.run(sys.argv[1:])
    sys.exit(return_code)


if __name__ == "__main__":
    main()
