# ./tests/test_finder.py

import unittest
import os
from codeaggregator.finder import find_files
from pathlib import Path

class TestFinder(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = 'test_env'
        os.makedirs(self.test_dir, exist_ok=True)
        
        # テストファイルとディレクトリを作成
        os.makedirs(os.path.join(self.test_dir, 'src'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'node_modules'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'tests', '__pycache__'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, '.hidden_dir'), exist_ok=True)
        
        with open(os.path.join(self.test_dir, 'src', 'file1.py'), 'w') as f:
            f.write('print("Hello, World!")')
        with open(os.path.join(self.test_dir, 'src', 'file2.js'), 'w') as f:
            f.write('console.log("Hello, World!");')
        with open(os.path.join(self.test_dir, 'src', 'file3.txt'), 'w') as f:
            f.write('This is a text file.')
        with open(os.path.join(self.test_dir, 'node_modules', 'file4.py'), 'w') as f:
            f.write('print("This should be ignored")')
        with open(os.path.join(self.test_dir, 'tests', '__pycache__', 'cached_file.pyc'), 'w') as f:
            f.write('This is a cached file.')
        with open(os.path.join(self.test_dir, 'tests', 'test1.py'), 'w') as f:
            f.write('def test_example(): pass')
        with open(os.path.join(self.test_dir, '.hidden_file'), 'w') as f:
            f.write('This is a hidden file.')
        with open(os.path.join(self.test_dir, '.hidden_dir', 'hidden_inside.py'), 'w') as f:
            f.write('print("Hidden inside directory")')
        with open(os.path.join(self.test_dir, '.gitignore'), 'w') as f:
            f.write('*.js\nnode_modules/\n__pycache__/\n')
        with open(os.path.join(self.test_dir, 'src', 'file5.cpp'), 'w') as f:
            f.write('// C++ file')
        with open(os.path.join(self.test_dir, 'src', 'file6.dpp'), 'w') as f:
            f.write('// DPP file')
        with open(os.path.join(self.test_dir, 'src', 'file7.wpp'), 'w') as f:
            f.write('// WPP file')

    def tearDown(self):
        # テスト用の一時ディレクトリを削除
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.test_dir)

    def test01_find_files_include_all(self):
        """
        何も指定しなければ、隠しファイルを除くすべてのファイルが含まれることを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=None, use_gitignore=False, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'src', 'file5.cpp'),
            os.path.join(self.test_dir, 'src', 'file6.dpp'),
            os.path.join(self.test_dir, 'src', 'file7.wpp'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', '__pycache__', 'cached_file.pyc'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # 隠しファイル/ディレクトリは含まれない
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test02_find_files_with_ignore_pattern_top_level(self):
        """
        -I "node_modules/" オプションを使用し、node_modules ディレクトリを除外することを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=["node_modules/"], use_gitignore=False, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'src', 'file5.cpp'),
            os.path.join(self.test_dir, 'src', 'file6.dpp'),
            os.path.join(self.test_dir, 'src', 'file7.wpp'),
            os.path.join(self.test_dir, 'tests', '__pycache__', 'cached_file.pyc'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # node_modules/file4.py は除外されるべき
            # 隠しファイル/ディレクトリも除外される
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test03_find_files_with_ignore_pattern_nested(self):
        """
        -I "__pycache__/" オプションを使用し、任意の階層にある __pycache__ ディレクトリを除外することを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=["__pycache__/"], use_gitignore=False, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'src', 'file5.cpp'),
            os.path.join(self.test_dir, 'src', 'file6.dpp'),
            os.path.join(self.test_dir, 'src', 'file7.wpp'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # tests/__pycache__/cached_file.pyc は除外されるべき
            # 隠しファイル/ディレクトリも除外される
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test04_find_files_include_multiple_patterns(self):
        """
        -P "*.py", "*.txt" オプションを使用し、特定のパターンに一致するファイルのみを含めることを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=["*.py", "*.txt"], ignore_patterns=None, use_gitignore=False, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # .gitignore と tests/__pycache__/cached_file.pyc は除外されるべき
            # 隠しファイル/ディレクトリも除外される
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test05_find_files_with_gitignore(self):
        """
        --gitignore オプションを使用し、.gitignore ファイルのパターンに基づいてファイルを除外することを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=None, use_gitignore=True, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'src', 'file5.cpp'),
            os.path.join(self.test_dir, 'src', 'file6.dpp'),
            os.path.join(self.test_dir, 'src', 'file7.wpp'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            
            # node_modules/file4.py と tests/__pycache__/cached_file.pyc は除外されるべき
            # 隠しファイル/ディレクトリも除外される
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test06_find_files_include_with_gitignore_and_patterns(self):
        """
        -P "*.py", "*.txt" --gitignore オプションを使用し、インクルードパターンと .gitignore の除外パターンが正しく適用されることを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=["*.py", "*.txt"], ignore_patterns=None, use_gitignore=True, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # node_modules/file4.py と tests/__pycache__/cached_file.pyc は .gitignore により除外されるため含まれません
            # 隠しファイル/ディレクトリも除外される
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test07_find_files_hidden_directories_excluded(self):
        """
        隠しディレクトリ（例: .hidden_dir）および隠しファイル（例: .hidden_file）が正しく除外されることを確認します。
        """
        # デフォルトで隠しファイル/ディレクトリを除外
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=None, use_gitignore=False, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'src', 'file5.cpp'),
            os.path.join(self.test_dir, 'src', 'file6.dpp'),
            os.path.join(self.test_dir, 'src', 'file7.wpp'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', '__pycache__', 'cached_file.pyc'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # .gitignore と .hidden_file と .hidden_dir/hidden_inside.py は除外されるべき
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test08_find_files_include_hidden_with_a_option(self):
        """
        -a オプションを使用し、先頭に '.' が付くファイルやフォルダも含めることを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=None, use_gitignore=False, include_hidden=True)
        expected = [
            os.path.join(self.test_dir, '.gitignore'),
            os.path.join(self.test_dir, '.hidden_file'),
            os.path.join(self.test_dir, '.hidden_dir', 'hidden_inside.py'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'src', 'file5.cpp'),
            os.path.join(self.test_dir, 'src', 'file6.dpp'),
            os.path.join(self.test_dir, 'src', 'file7.wpp'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', '__pycache__', 'cached_file.pyc'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # .hidden_file と .hidden_dir/hidden_inside.py が含まれる
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test09_find_files_include_hidden_with_a_option_and_patterns(self):
        """
        -P "*.py", "*.txt" -a オプションを使用し、インクルードパターンと共に隠しファイル/ディレクトリも含めることを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=["*.py", "*.txt"], ignore_patterns=None, use_gitignore=False, include_hidden=True)
        expected = [
            os.path.join(self.test_dir, '.hidden_dir', 'hidden_inside.py'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # .hidden_file は *.py や *.txt にマッチしないため除外
            # .gitignore は *.py や *.txt にマッチしないため除外
            # tests/__pycache__/cached_file.pyc は除外されるべき
        ]
        self.assertEqual(sorted(files), sorted(expected))

    # 以下、新たに追加されたテストケース

    def test10_find_files_with_or_pattern_py_txt(self):
        """
        -P "*.py|*.txt" オプションを使用し、*.py または *.txt にマッチするファイルのみを含めることを確認します。
        """
        patterns = ["*.py|*.txt"]
        files = find_files(directory=self.test_dir, patterns=patterns, ignore_patterns=None, use_gitignore=False, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # .gitignore と tests/__pycache__/cached_file.pyc は除外されるべき
            # 隠しファイル/ディレクトリも除外される
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test11_find_files_with_character_class_pattern(self):
        """
        -P "*.[dwc]pp" オプションを使用し、*.dpp, *.wpp, *.cpp にマッチするファイルのみを含めることを確認します。
        """
        patterns = ["*.[dwc]pp"]
        files = find_files(directory=self.test_dir, patterns=patterns, ignore_patterns=None, use_gitignore=False, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file5.cpp'),
            os.path.join(self.test_dir, 'src', 'file6.dpp'),
            os.path.join(self.test_dir, 'src', 'file7.wpp'),
            # 他のファイルは除外されるべき
            # .gitignore と tests/__pycache__/cached_file.pyc は除外
            # 隠しファイル/ディレクトリも除外
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test12_find_files_with_combined_patterns(self):
        """
        -P "*.py|*.txt" "*.[dwc]pp" オプションを使用し、*.py または *.txt または *.dpp, *.wpp, *.cpp にマッチするファイルのみを含めることを確認します。
        """
        patterns = ["*.py|*.txt", "*.[dwc]pp"]
        files = find_files(directory=self.test_dir, patterns=patterns, ignore_patterns=None, use_gitignore=False, include_hidden=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            os.path.join(self.test_dir, 'src', 'file5.cpp'),
            os.path.join(self.test_dir, 'src', 'file6.dpp'),
            os.path.join(self.test_dir, 'src', 'file7.wpp'),
            # .gitignore と tests/__pycache__/cached_file.pyc は除外されるべき
            # 隠しファイル/ディレクトリも除外
        ]
        self.assertEqual(sorted(files), sorted(expected))

if __name__ == '__main__':
    unittest.main()
