"""
================================================================================
ファイル名: write_log.py
作成者: システム開発チーム
作成日: 2026-07-06
更新日: 2026-07-06
バージョン: 1.0
説明: ログファイルへメッセージを出力するクラス
================================================================================
"""

from datetime import datetime
from pathlib import Path
import sys
from typing import Literal


class WriteLog:
    """
    ログファイルへメッセージを出力するクラス。

    ログファイルを「c:\\temp\\testproject2.log」に作成・追記し、
    指定されたメッセージを所定の形式で出力します。
    """

    # ログレベルのマッピング
    LOG_LEVELS: dict[str, str] = {
        "I": "INFO",
        "W": "WARN",
        "E": "ERR ",
        "C": "CRIT"
    }

    # ログファイルのパス
    LOG_FILE_PATH: str = r"c:\temp\testproject2.log"

    def write(self, level: str, message: str) -> None:
        """
        ログメッセージをファイルに出力する。

        Args:
            level (str): ログレベル（I/W/E/C）
            message (str): 出力メッセージ

        Returns:
            None

        Raises:
            None（内部で例外を処理）
        """
        # 処理日時の取得
        now: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        # ログレベルの検証
        if level not in self.LOG_LEVELS:
            # 不正なログレベルの場合
            self._output_log(now, "WARN", f"メッセージ区分指定に誤りがあります（{level}）")
            if message == "":
                self._output_log(now, "CRIT", "メッセージが指定されていません。")
            else:
                self._output_log(now, "CRIT", message)
            return

        # メッセージが空文字の場合
        if message == "":
            message = "メッセージが指定されていません。"

        # ログを出力
        log_level: str = self.LOG_LEVELS[level]
        self._output_log(now, log_level, message)

    def _output_log(self, timestamp: str, level: str, message: str) -> None:
        """
        ログメッセージをファイルに出力する内部メソッド。

        Args:
            timestamp (str): 処理日時（yyyy/mm/dd hh:mm:ss形式）
            level (str): ログレベル（INFO/WARN/ERR /CRIT）
            message (str): 出力メッセージ

        Returns:
            None
        """
        log_entry: str = f"{timestamp} {level} {message}"

        try:
            # ログファイルの親ディレクトリを作成
            log_file: Path = Path(self.LOG_FILE_PATH)
            log_file.parent.mkdir(parents=True, exist_ok=True)

            # ログファイルに追記
            with open(log_file, mode="a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            # ログファイル出力失敗時
            error_timestamp: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            error_message: str = f"{error_timestamp} CRIT ログファイルの出力に失敗しました。\n" \
                                 f"{error_timestamp} {level} {message}"
            sys.stderr.write(error_message + "\n")
