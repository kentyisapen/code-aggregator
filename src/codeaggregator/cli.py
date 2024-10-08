# cli.py

import argparse
import logging
from codeaggregator.finder import find_files
from codeaggregator.output import output_files

def main():
    parser = argparse.ArgumentParser(
        description='生成AI用にコードファイルをまとめて出力するツール'
    )
    # 'directory' 引数をオプションの位置引数に変更
    parser.add_argument(
        'directory',
        nargs='?',  # 0または1の引数を受け取る
        default='.',  # デフォルト値をカレントディレクトリに設定
        help='検索対象のディレクトリ (デフォルト: カレントディレクトリ)'
    )
    parser.add_argument(
        '-P', '--pattern',
        help='対象とするファイルパターンを指定 (例: *.py|*.txt)'
    )
    parser.add_argument(
        '-I', '--ignore',
        help='除外するファイル/ディレクトリパターンを指定 (例: node_modules/|__pycache__/)'
    )
    parser.add_argument(
        '--fromfile',
        metavar='FILE',
        nargs='?',
        const='.',
        help='ファイルリストを指定。パイプ入力の場合は何も指定せずに使用。例: --fromfile, --fromfile=path.txt'
    )
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='隠しファイルやフォルダも含める'
    )
    parser.add_argument(
        '-o', '--output',
        help='出力先を指定（デフォルトは標準出力）'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='CodeAggregator 0.1.0',
        help='バージョン情報を表示'
    )
    parser.add_argument(
        '-i', '--info',
        action='store_true',  # フラグとして定義
        help='詳細情報の表示 (INFOレベルのログを有効にします)'
    )

    args = parser.parse_args()

    # ログレベルの設定
    if args.info:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

    # パターンをリストに変換
    patterns = expand_patterns(args.pattern) if args.pattern else None
    ignore_patterns = expand_patterns(args.ignore) if args.ignore else None

    # ファイル検索
    files = find_files(
        directory=args.directory,
        patterns=patterns,
        ignore_patterns=ignore_patterns,
        fromfile=args.fromfile,
        include_hidden=args.all  # -a オプションに基づき隠しファイルを含める
    )

    # 検索結果の出力
    output_files(files, args.output)

def expand_patterns(pattern_str):
    """
    パターン文字列をリストに変換し、ORパターンを展開します。
    """
    patterns = pattern_str.split(',')
    expanded = []
    for pat in patterns:
        expanded.extend(pat.split('|'))
    return expanded
