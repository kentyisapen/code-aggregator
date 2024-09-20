import os
import fnmatch
from pathlib import Path

def load_gitignore(directory):
    gitignore_path = Path(directory) / '.gitignore'
    patterns = []
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns

def find_files(directory, patterns=None, ignore_patterns=None, use_gitignore=False):
    matched_files = []
    ignore = ignore_patterns or []
    if use_gitignore:
        ignore += load_gitignore(directory)
    
    for root, dirs, files in os.walk(directory):
        # 除外ディレクトリの処理
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(os.path.join(root, d), pat) for pat in ignore)]
        
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            
            # パターンマッチング
            if patterns:
                if not any(fnmatch.fnmatch(file, pat) for pat in patterns):
                    continue
            # 除外パターンマッチング
            if ignore:
                if any(fnmatch.fnmatch(relative_path, pat) for pat in ignore):
                    continue
            matched_files.append(file_path)
    return matched_files
