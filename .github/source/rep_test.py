#!/usr/bin/env python3
"""
文字列置換スクリプト

指定ファイル内の文字列を別の文字列に置換し、結果を出力ファイルに保存します。
"""

import os
import sys
from typing import Tuple

from common.write_log import FileLogger


def main() -> int:
    """メイン処理を実行し、適切な終了コードを返す。"""
    return_code: int = 0

    try:
        # 引数チェック
        if len(sys.argv) != 5:
            error_message: str = f"引数が4個以外です（return_code=16）"
            sys.stderr.write(error_message + "\n")
            FileLogger.write("E", error_message)
            return 16

        before_str: str = sys.argv[1]
        after_str: str = sys.argv[2]
        input_file_path: str = sys.argv[3]
        output_file_path: str = sys.argv[4]

        # 処理開始メッセージを出力
        start_message: str = "処理開始"
        print(start_message)
        FileLogger.write("I", start_message)

        # 置換前文字列のチェック
        if before_str == "":
            error_message = f"置換前文字列に空文字を指定されました（return_code=17）"
            sys.stderr.write(error_message + "\n")
            FileLogger.write("E", error_message)
            end_message: str = f"処理終了（return_code=17）"
            print(end_message)
            FileLogger.write("I", end_message)
            return 17

        # 入力ファイルのチェック
        if not os.path.exists(input_file_path):
            error_message = f"入力ファイルが存在しません（return_code=18）"
            sys.stderr.write(error_message + "\n")
            FileLogger.write("E", error_message)
            end_message = f"処理終了（return_code=18）"
            print(end_message)
            FileLogger.write("I", end_message)
            return 18

        # 出力ファイルの格納先ディレクトリのチェック
        output_dir: str = os.path.dirname(output_file_path)
        if output_dir and not os.path.exists(output_dir):
            error_message = f"出力ファイルの格納先ディレクトリが存在しません（return_code=19）"
            sys.stderr.write(error_message + "\n")
            FileLogger.write("E", error_message)
            end_message = f"処理終了（return_code=19）"
            print(end_message)
            FileLogger.write("I", end_message)
            return 19

        # 出力ファイルの存在チェック
        if os.path.exists(output_file_path):
            error_message = f"出力ファイルが既に存在します（return_code=20）"
            sys.stderr.write(error_message + "\n")
            FileLogger.write("E", error_message)
            end_message = f"処理終了（return_code=20）"
            print(end_message)
            FileLogger.write("I", end_message)
            return 20

        # 入力ファイルの読み込みと置換処理
        try:
            with open(input_file_path, "r", encoding="utf-8") as input_file:
                content: str = input_file.read()
        except OSError as e:
            error_message = f"入力ファイルの読み込みに失敗しました: {str(e)}（return_code=99）"
            sys.stderr.write(error_message + "\n")
            FileLogger.write("E", error_message)
            end_message = f"処理終了（return_code=99）"
            print(end_message)
            FileLogger.write("I", end_message)
            return 99

        # 置換処理を実行
        replaced_content: str = content
        replacement_count: int = count_and_replace(content, before_str, after_str)
        replaced_content = content.replace(before_str, after_str)

        # 出力ファイルへの書き込み
        try:
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(replaced_content)
        except OSError as e:
            error_message = f"出力ファイルのオープンに失敗しました: {str(e)}（return_code=21）"
            sys.stderr.write(error_message + "\n")
            FileLogger.write("E", error_message)
            end_message = f"処理終了（return_code=21）"
            print(end_message)
            FileLogger.write("I", end_message)
            return 21

        # 置換件数の出力
        replacement_message: str = f"置換件数:{replacement_count}件"
        print(replacement_message)
        FileLogger.write("I", replacement_message)

        # 処理終了メッセージ
        return_code = 0
        end_message = f"処理終了（return_code={return_code}）"
        print(end_message)
        FileLogger.write("I", end_message)

    except Exception as e:
        # 想定外エラー
        error_message = f"想定外のエラーが発生しました: {str(e)}（return_code=99）"
        sys.stderr.write(error_message + "\n")
        FileLogger.write("E", error_message)
        end_message = f"処理終了（return_code=99）"
        print(end_message)
        FileLogger.write("I", end_message)
        return 99

    return return_code


def count_and_replace(text: str, before_str: str, after_str: str) -> int:
    """文字列内で置換前文字列が何回出現するかをカウントする。
    
    Args:
        text: 検索対象のテキスト
        before_str: 検索文字列
        after_str: 置換文字列
    
    Returns:
        置換回数
    """
    count: int = 0
    start: int = 0

    while True:
        pos: int = text.find(before_str, start)
        if pos == -1:
            break
        count += 1
        start = pos + len(before_str)

    return count


if __name__ == "__main__":
    exit_code: int = main()
    sys.exit(exit_code)
