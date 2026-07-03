import os
import sys
from datetime import datetime
from typing import ClassVar, Dict


class FileLogger:
    """メッセージを指定のログファイルに出力するクラス。"""

    LOG_PATH: ClassVar[str] = r"c:\temp\testproject2.log"
    LEVEL_MAP: ClassVar[Dict[str, str]] = {
        "I": "INFO",
        "W": "WARN",
        "E": "ERR ",
        "C": "CRIT",
    }
    EMPTY_MESSAGE: ClassVar[str] = "メッセージが指定されていません。"

    @classmethod
    def write(cls, level: str, message: str) -> None:
        """指定された区分とメッセージをログファイルに追記する。"""
        timestamp: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        actual_message: str = message if message != "" else cls.EMPTY_MESSAGE

        if level not in cls.LEVEL_MAP:
            cls._append_line(timestamp, "WARN", f"メッセージ区分指定に誤りがあります（{level}）")
            cls._append_line(timestamp, "CRIT", actual_message)
            return

        log_level: str = cls.LEVEL_MAP[level]
        cls._append_line(timestamp, log_level, actual_message)

    @classmethod
    def _append_line(cls, timestamp: str, level: str, message: str) -> None:
        """ログファイルに1行を追記する。"""
        try:
            log_dir: str = os.path.dirname(cls.LOG_PATH)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            with open(cls.LOG_PATH, "a", encoding="utf-8") as log_file:
                log_file.write(f"{timestamp} {level} {message}\n")
        except OSError:
            error_timestamp: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            sys.stderr.write(f"{error_timestamp} CRIT ログファイルの出力に失敗しました。\n")
