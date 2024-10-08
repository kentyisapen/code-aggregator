# finder.py

import os
import fnmatch
from pathlib import Path
import logging
import sys

# ロガーの設定
logger = logging.getLogger(__name__)

def normalize_patterns(patterns):
    """
    パターンの末尾に '/' があれば除去します。
    """
    normalized = []
    for pat in patterns:
        if pat.endswith('/'):
            pat = pat.rstrip('/')
        normalized.append(pat)
    return normalized

def expand_or_patterns(patterns):
    """
    パターン内の '|' を分割し、フラットなパターンリストを返します。
    例: ["*.py|*.txt", "*.md"] -> ["*.py", "*.txt", "*.md"]
    """
    expanded = []
    for pat in patterns:
        split_pats = pat.split('|')
        expanded.extend(split_pats)
    return expanded

def find_files(directory, patterns=None, ignore_patterns=None, fromfile=None, include_hidden=False):
    """
    指定されたディレクトリ内のファイルを検索します。

    Args:
        directory (str): 検索対象のディレクトリパス。
        patterns (list, optional): インクルードするファイルパターンのリスト。デフォルトは None（すべてのファイルを含む）。
        ignore_patterns (list, optional): 除外するファイル/ディレクトリパターンのリスト。デフォルトは None。
        fromfile (str, optional): ファイルリストを指定。"." を指定すると標準入力から読み取ります。デフォルトは None。
        include_hidden (bool, optional): 先頭に '.' が付くファイルやフォルダを含めるかどうか。デフォルトは False。

    Returns:
        list: マッチしたファイルのパスのリスト。
    """
    matched_files = []
    ignore = []

    # 隠しファイル/フォルダを除外するパターンを追加
    if not include_hidden:
        ignore.append('.*')  # 先頭に '.' が付くファイルやフォルダを無視

    # 追加の除外パターンがあれば正規化して追加
    if ignore_patterns:
        normalized_ignore = normalize_patterns(ignore_patterns)
        ignore += normalized_ignore
        logger.debug(f"Normalized ignore patterns: {normalized_ignore}")

    # パターンの展開（ORパターンを分割）
    if patterns:
        expanded_patterns = expand_or_patterns(patterns)
        patterns = expanded_patterns
        logger.debug(f"Expanded include patterns: {patterns}")

    # エクスクルードパターンも展開（必要に応じて）
    if ignore:
        expanded_ignore = expand_or_patterns(ignore)
        ignore += expanded_ignore
        logger.debug(f"Expanded ignore patterns: {ignore}")

    logger.info(f"Final include patterns: {patterns}")
    logger.info(f"Final ignore patterns: {ignore}")

    if fromfile:
        if fromfile == '.':
            # 標準入力からファイルリストを取得
            logger.info("Reading file list from stdin.")
            file_list = [line.strip() for line in sys.stdin if line.strip()]
        else:
            # 指定されたファイルからファイルリストを取得
            logger.info(f"Reading file list from {fromfile}.")
            try:
                with open(fromfile, 'r', encoding='utf-8') as f:
                    file_list = [line.strip() for line in f if line.strip()]
            except Exception as e:
                logger.error(f"Error reading from file {fromfile}: {e}")
                return matched_files
    else:
        # 通常のファイル検索
        file_list = []
        for root, dirs, files in os.walk(directory):
            # 除外ディレクトリの処理
            dirs_to_remove = []
            for d in dirs:
                # ディレクトリ名のみでマッチング
                if any(fnmatch.fnmatch(d, pat) for pat in ignore):
                    dirs_to_remove.append(d)
                    logger.debug(f"Excluding directory: {os.path.join(root, d)}")
            for d in dirs_to_remove:
                dirs.remove(d)

            for file in files:
                if not include_hidden and file.startswith('.'):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                file_list.append(rel_path)

    
    for rel_file_path in file_list:
        abs_file_path = os.path.join(directory, rel_file_path)
        print(rel_file_path)

        # インクルードパターンの適用
        if patterns:
            if not any(fnmatch.fnmatch(rel_file_path, pat) for pat in patterns):
                logger.debug(f"Excluded by include pattern: {rel_file_path}")
                continue  # インクルードパターンに一致しない場合、スキップ

        # エクスクルードパターンの適用
        if ignore:
            if any(fnmatch.fnmatch(rel_file_path, pat) for pat in ignore):
                logger.debug(f"Excluded by ignore pattern: {rel_file_path}")
                continue  # エクスクルードパターンに一致する場合、スキップ

        matched_files.append(abs_file_path)

    return matched_files
