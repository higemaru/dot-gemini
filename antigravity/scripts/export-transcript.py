#!/usr/bin/env python3
"""
Antigravity の会話 JSONL を Markdown に変換してエクスポートするスクリプト。
usage: python3 export-transcript.py <project_dir> [output_dir]
  project_dir: プロジェクトのルートディレクトリ（絶対パス）
  output_dir:  出力先ディレクトリ（省略時は project_dir/transcripts/）
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

def get_current_conversation_dir():
    """現在のセッション、もしくは最新のセッションのログディレクトリを取得する"""
    gemini_home = os.path.expanduser("~/.gemini/antigravity")
    brain_dir = os.path.join(gemini_home, "brain")

    # 1. 環境変数 ANTIGRAVITY_SOURCE_METADATA から conversationId を探す
    metadata_str = os.environ.get("ANTIGRAVITY_SOURCE_METADATA")
    if metadata_str:
        try:
            metadata = json.loads(metadata_str)
            conv_id = metadata.get("tool", {}).get("conversationId")
            if conv_id:
                conv_path = os.path.join(brain_dir, conv_id)
                log_file = os.path.join(conv_path, ".system_generated", "logs", "transcript.jsonl")
                if os.path.isfile(log_file):
                    return conv_id, log_file
        except Exception:
            pass

    # 2. 環境変数がない場合、または見つからない場合は、最も更新日時が新しい transcript.jsonl を探す
    if not os.path.isdir(brain_dir):
        return None, None

    latest_mtime = 0
    latest_log_file = None
    latest_conv_id = None

    for conv_id in os.listdir(brain_dir):
        conv_path = os.path.join(brain_dir, conv_id)
        if not os.path.isdir(conv_path):
            continue
        log_file = os.path.join(conv_path, ".system_generated", "logs", "transcript.jsonl")
        if os.path.isfile(log_file):
            mtime = os.path.getmtime(log_file)
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest_log_file = log_file
                latest_conv_id = conv_id

    return latest_conv_id, latest_log_file

def clean_user_content(content):
    """ユーザーメッセージから <USER_REQUEST> タグの内容を抽出する"""
    if not content:
        return ""
    # <USER_REQUEST> タグがある場合はその中身を抽出
    match = re.search(r'<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return content.strip()

def jsonl_to_markdown(jsonl_path, conversation_id):
    """JSONL ファイルを Markdown に変換する"""
    messages = []
    first_ts = None

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            source = entry.get("source")
            entry_type = entry.get("type")
            content = entry.get("content", "")
            ts_raw = entry.get("created_at")

            # タイムスタンプのパース
            ts_str = ""
            if ts_raw:
                try:
                    dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).astimezone()
                    ts_str = dt.strftime("%H:%M")
                    if first_ts is None:
                        first_ts = dt
                except Exception:
                    pass

            # ツール実行履歴の処理
            tool_calls = entry.get("tool_calls", [])
            if tool_calls and isinstance(tool_calls, list):
                for tool in tool_calls:
                    tool_name = tool.get("name", "tool")
                    messages.append(("tool", ts_str, f"*[{tool_name} を実行]*"))

            # メッセージ履歴の処理
            if source == "USER_EXPLICIT" or entry_type == "USER_INPUT":
                text = clean_user_content(content)
                if text:
                    messages.append(("user", ts_str, text))
            elif source == "MODEL" and entry_type == "PLANNER_RESPONSE":
                if content:
                    messages.append(("assistant", ts_str, content.strip()))

    if not messages:
        return None, None

    date_str = first_ts.strftime("%Y-%m-%d") if first_ts else datetime.now().strftime("%Y-%m-%d")
    
    lines = [f"# トランスクリプト {date_str}", ""]
    for role, ts, text in messages:
        ts_part = f" {ts}" if ts else ""
        if role == "user":
            header = f"## ユーザー{ts_part}"
        elif role == "assistant":
            header = f"## Antigravity{ts_part}"
        elif role == "tool":
            header = f"### システム（ツール実行）{ts_part}"
        
        lines.append(header)
        lines.append("")
        lines.append(text)
        lines.append("")

    return date_str, "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <project_dir> [output_dir]", file=sys.stderr)
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) >= 3 else os.path.join(project_dir, "transcripts")
    os.makedirs(output_dir, exist_ok=True)

    conv_id, log_file = get_current_conversation_dir()
    if not log_file:
        print("エラー: 会話ログ (transcript.jsonl) が見つかりませんでした。", file=sys.stderr)
        sys.exit(1)

    print(f"対象セッションID: {conv_id}")
    print(f"読み込み元: {log_file}")

    date_str, md = jsonl_to_markdown(log_file, conv_id)
    if md is None:
        print("エラー: 会話履歴の変換に失敗したか、中身が空です。", file=sys.stderr)
        sys.exit(1)

    short_id = conv_id[:8] if conv_id else "session"
    out_name = f"{date_str}_{short_id}.md"
    out_path = os.path.join(output_dir, out_name)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"保存完了: {out_path}")

if __name__ == "__main__":
    main()
