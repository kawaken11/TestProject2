"""
================================================================================
ファイル名: write_log.py
作成者: AI Assistant
作成日: 2026-07-06
更新日: 2026-07-06
バージョン: 1.0
説明: ログメッセージをファイルに出力するクラス
================================================================================
"""

from datetime import datetime
from typing import Literal
import sys


class WriteLog:
    """
    ログメッセージをファイルに出力するクラス。
    
    Args:
        区分 (Literal["I", "W", "E", "C"]): ログレベル
            - I: 情報（INFO）
            - W: 警告（WARN）
            - E: エラー（ERR）
            - C: 致命的エラー（CRIT）
        message (str): 出力メッセージ
    """
    
    # ログファイルパス
    LOG_FILE_PATH: str = r"c:\temp\testproject2.log"
    
    # 区分とログレベルのマッピング
    LEVEL_MAP: dict[str, str] = {
        "I": "INFO",
        "W": "WARN",
        "E": "ERR ",
        "C": "CRIT"
    }
    
    @classmethod
    def write(cls, division: str, message: str) -> None:
        """
        ログメッセージをファイルに出力する。
        
        Args:
            division (str): メッセージ区分（I/W/E/C）
            message (str): 出力メッセージ
        
        Returns:
            None
        """
        try:
            # 現在時刻を取得
            current_time: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            
            # メッセージが空文字かどうかを確認
            if not message:
                message = "メッセージが指定されていません。"
            
            # 区分が有効かどうかを確認
            if division not in cls.LEVEL_MAP:
                # 区分指定誤りの警告メッセージを出力
                warning_log: str = (
                    f"{current_time} WARN メッセージ区分指定に誤りがあります"
                    f"（{division}）\n"
                )
                # ファイルに書き込み
                with open(cls.LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
                    log_file.write(warning_log)
                
                # 本メッセージをCRITで出力
                critical_log: str = f"{current_time} CRIT {message}\n"
                with open(cls.LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
                    log_file.write(critical_log)
            else:
                # 通常のログ出力
                log_level: str = cls.LEVEL_MAP[division]
                log_line: str = f"{current_time} {log_level} {message}\n"
                with open(cls.LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
                    log_file.write(log_line)
        
        except Exception as error:
            # ファイル操作失敗時はstderrに出力
            current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            error_message: str = f"{current_time} CRIT ログファイルの出力に失敗しました。\n"
            sys.stderr.write(error_message)
            sys.stderr.write(
                f"{current_time} {cls.LEVEL_MAP.get(division, 'CRIT')} {message}\n"
            )
