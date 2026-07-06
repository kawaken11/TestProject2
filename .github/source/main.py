"""
================================================================================
ファイル名: main.py
作成者: AI Assistant
作成日: 2026-07-06
更新日: 2026-07-06
バージョン: 1.0
説明: ファイル内の指定文字列を置換して出力するメインプログラム
================================================================================
"""

import sys
import os
from typing import Tuple
from pathlib import Path

# write_logクラスをインポート
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "common"))
from write_log import WriteLog


class StringReplacer:
    """
    ファイル内の文字列を置換するクラス。
    """
    
    def __init__(self) -> None:
        """コンストラクタ"""
        pass
    
    @staticmethod
    def replace_string(
        search_string: str,
        replace_string: str,
        input_file_path: str,
        output_file_path: str
    ) -> Tuple[int, int]:
        """
        ファイル内の指定文字列を置換する。
        
        Args:
            search_string (str): 置換前文字列
            replace_string (str): 置換後文字列
            input_file_path (str): 入力ファイルパス
            output_file_path (str): 出力ファイルパス
        
        Returns:
            Tuple[int, int]: (return_code, replace_count)
                return_code: 0=成功、その他=エラーコード
                replace_count: 置換件数
        """
        # 処理開始ログ
        start_message: str = "処理開始"
        print(start_message)
        WriteLog.write("I", start_message)
        
        try:
            # 入力ファイルと出力ファイルが同じかどうかを確認
            input_path_abs: str = os.path.abspath(input_file_path)
            output_path_abs: str = os.path.abspath(output_file_path)
            
            if input_path_abs == output_path_abs:
                error_message: str = f"エラー内容（return_code=22）"
                print(error_message, file=sys.stderr)
                WriteLog.write("E", error_message)
                end_message: str = "処理終了（return_code=22）"
                print(end_message)
                WriteLog.write("I", end_message)
                return 22, 0
            
            # 置換前文字列が空文字かどうかを確認
            if not search_string:
                error_message = f"エラー内容（return_code=17）"
                print(error_message, file=sys.stderr)
                WriteLog.write("E", error_message)
                end_message = "処理終了（return_code=17）"
                print(end_message)
                WriteLog.write("I", end_message)
                return 17, 0
            
            # 入力ファイルが存在するかどうかを確認
            if not os.path.exists(input_file_path):
                error_message = f"エラー内容（return_code=18）"
                print(error_message, file=sys.stderr)
                WriteLog.write("E", error_message)
                end_message = "処理終了（return_code=18）"
                print(end_message)
                WriteLog.write("I", end_message)
                return 18, 0
            
            # 出力ファイルの格納先ディレクトリが存在するかどうかを確認
            output_dir: str = os.path.dirname(output_file_path)
            if output_dir and not os.path.exists(output_dir):
                error_message = f"エラー内容（return_code=19）"
                print(error_message, file=sys.stderr)
                WriteLog.write("E", error_message)
                end_message = "処理終了（return_code=19）"
                print(end_message)
                WriteLog.write("I", end_message)
                return 19, 0
            
            # 出力ファイルが既に存在するかどうかを確認
            if os.path.exists(output_file_path):
                error_message = f"エラー内容（return_code=20）"
                print(error_message, file=sys.stderr)
                WriteLog.write("E", error_message)
                end_message = "処理終了（return_code=20）"
                print(end_message)
                WriteLog.write("I", end_message)
                return 20, 0
            
            # 入力ファイルを読み込む
            try:
                with open(input_file_path, "r", encoding="utf-8") as input_file:
                    file_content: str = input_file.read()
            except Exception:
                error_message = f"エラー内容（return_code=18）"
                print(error_message, file=sys.stderr)
                WriteLog.write("E", error_message)
                end_message = "処理終了（return_code=18）"
                print(end_message)
                WriteLog.write("I", end_message)
                return 18, 0
            
            # 置換処理を実行
            replaced_content: str = file_content
            replace_count: int = 0
            
            # 置換前文字列の出現位置をすべて探して置換
            start_pos: int = 0
            while True:
                pos: int = replaced_content.find(search_string, start_pos)
                if pos == -1:
                    break
                replaced_content = (
                    replaced_content[:pos] + replace_string +
                    replaced_content[pos + len(search_string):]
                )
                replace_count += 1
                start_pos = pos + len(replace_string)
            
            # 出力ファイルを書き込む
            try:
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(replaced_content)
            except Exception:
                error_message = f"エラー内容（return_code=21）"
                print(error_message, file=sys.stderr)
                WriteLog.write("E", error_message)
                end_message = "処理終了（return_code=21）"
                print(end_message)
                WriteLog.write("I", end_message)
                return 21, 0
            
            # 置換件数をログに出力
            count_message: str = f"置換件数:{replace_count}件"
            print(count_message)
            WriteLog.write("I", count_message)
            
            # 処理終了ログ
            end_message = "処理終了（return_code=0）"
            print(end_message)
            WriteLog.write("I", end_message)
            
            return 0, replace_count
        
        except Exception as error:
            # 想定外のエラー
            error_message = f"エラー内容（return_code=99）"
            print(error_message, file=sys.stderr)
            WriteLog.write("E", error_message)
            end_message = "処理終了（return_code=99）"
            print(end_message)
            WriteLog.write("I", end_message)
            return 99, 0


def main() -> int:
    """
    メイン処理。
    
    Returns:
        int: リターンコード
    """
    # 引数の数を確認
    if len(sys.argv) != 5:
        error_message: str = f"エラー内容（return_code=16）"
        print(error_message, file=sys.stderr)
        WriteLog.write("E", error_message)
        end_message: str = "処理終了（return_code=16）"
        print(end_message)
        WriteLog.write("I", end_message)
        return 16
    
    # 引数を取得
    search_str: str = sys.argv[1]
    replace_str: str = sys.argv[2]
    input_path: str = sys.argv[3]
    output_path: str = sys.argv[4]
    
    # 置換処理を実行
    replacer: StringReplacer = StringReplacer()
    return_code: int
    return_code, _ = replacer.replace_string(
        search_str,
        replace_str,
        input_path,
        output_path
    )
    
    return return_code


if __name__ == "__main__":
    sys.exit(main())
