import argparse
from codeaggregator.finder import find_files
from codeaggregator.output import output_files

def main():
    parser = argparse.ArgumentParser(
        description='生成AI用にコードファイルをまとめて出力するツール'
    )
    parser.add_argument('directory', help='検索対象のディレクトリ')
    parser.add_argument('-P', '--pattern', help='対象とするファイルパターンを指定（カンマ区切り）')
    parser.add_argument('-I', '--ignore', help='除外するファイル/ディレクトリパターンを指定（カンマ区切り）')
    parser.add_argument('--gitignore', action='store_true', help='.gitignoreを基に除外パターンを適用')
    parser.add_argument('-o', '--output', help='出力先を指定（デフォルトは標準出力）')
    parser.add_argument('-v', '--version', action='version', version='CodeAggregator 0.1.0')

    args = parser.parse_args()

    files = find_files(
        directory=args.directory,
        patterns=args.pattern.split(',') if args.pattern else None,
        ignore_patterns=args.ignore.split(',') if args.ignore else None,
        use_gitignore=args.gitignore
    )
    output_files(files, args.output)
