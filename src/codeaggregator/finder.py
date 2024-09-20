# ./src/codeaggregator/finder.py

import os
import fnmatch
from pathlib import Path
import logging

# ロガーの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_gitignore(directory):
    """
    指定されたディレクトリから .gitignore ファイルを読み込み、パターンをリストとして返します。
    """
    gitignore_path = Path(directory) / '.gitignore'
    patterns = []
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # 末尾のスラッシュを除去
                    if line.endswith('/'):
                        line = line.rstrip('/')
                    patterns.append(line)
    return patterns

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

def find_files(directory, patterns=None, ignore_patterns=None, use_gitignore=False):
    """
    指定されたディレクトリ内のファイルを検索します。

    Args:
        directory (str): 検索対象のディレクトリパス。
        patterns (list, optional): インクルードするファイルパターンのリスト。デフォルトは None（すべてのファイルを含む）。
        ignore_patterns (list, optional): 除外するファイル/ディレクトリパターンのリスト。デフォルトは None。
        use_gitignore (bool, optional): .gitignore のパターンを除外に使用するかどうか。デフォルトは False。

    Returns:
        list: マッチしたファイルのパスのリスト。
    """
    matched_files = []
    ignore = []

    # 追加の除外パターンがあれば正規化して追加
    if ignore_patterns:
        normalized_ignore = normalize_patterns(ignore_patterns)
        ignore += normalized_ignore
        logger.debug(f"Normalized ignore patterns: {normalized_ignore}")

    # .gitignore のパターンを除外に追加
    if use_gitignore:
        gitignore_patterns = load_gitignore(directory)
        ignore += gitignore_patterns
        logger.debug(f"Loaded .gitignore patterns: {gitignore_patterns}")

    logger.info(f"Final ignore patterns: {ignore}")

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
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)

            # インクルードパターンの適用
            if patterns:
                if not any(fnmatch.fnmatch(file, pat) for pat in patterns):
                    logger.debug(f"Excluded by include pattern: {relative_path}")
                    continue  # インクルードパターンに一致しない場合、スキップ

            # エクスクルードパターンの適用
            if ignore:
                if any(fnmatch.fnmatch(relative_path, pat) for pat in ignore):
                    logger.debug(f"Excluded by ignore pattern: {relative_path}")
                    continue  # エクスクルードパターンに一致する場合、スキップ

            matched_files.append(file_path)
            logger.info(f"Included: {relative_path}")

    return matched_files
