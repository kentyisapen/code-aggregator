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
        with open(os.path.join(self.test_dir, '.gitignore'), 'w') as f:
            f.write('*.js\nnode_modules/\n__pycache__/\n')

    def tearDown(self):
        # テスト用の一時ディレクトリを削除
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.test_dir)

    def test_find_files_include_all(self):
        """
        何も指定しなければ、すべてのファイルが含まれることを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=None, use_gitignore=False)
        expected = [
            os.path.join(self.test_dir, '.gitignore'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', '__pycache__', 'cached_file.pyc'),
            os.path.join(self.test_dir, 'tests', 'test1.py')
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test_find_files_with_ignore_pattern_top_level(self):
        """
        -I "node_modules/" オプションを使用し、node_modules ディレクトリを除外することを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=["node_modules/"], use_gitignore=False)
        expected = [
            os.path.join(self.test_dir, '.gitignore'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'tests', '__pycache__', 'cached_file.pyc'),
            os.path.join(self.test_dir, 'tests', 'test1.py')
            # node_modules/file4.py は除外されるべき
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test_find_files_with_ignore_pattern_nested(self):
        """
        -I "__pycache__/" オプションを使用し、任意の階層にある __pycache__ ディレクトリを除外することを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=["__pycache__/"], use_gitignore=False)
        expected = [
            os.path.join(self.test_dir, '.gitignore'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', 'test1.py')
            # tests/__pycache__/cached_file.pyc は除外されるべき
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test_find_files_include_multiple_patterns(self):
        """
        -P "*.py", "*.txt" オプションを使用し、特定のパターンに一致するファイルのみを含めることを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=["*.py", "*.txt"], ignore_patterns=None, use_gitignore=False)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', 'test1.py')
            # .gitignore と tests/__pycache__/cached_file.pyc は除外されるべき
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test_find_files_with_gitignore(self):
        """
        --gitignore オプションを使用し、.gitignore ファイルのパターンに基づいてファイルを除外することを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=None, use_gitignore=True)
        expected = [
            os.path.join(self.test_dir, '.gitignore'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'tests', 'test1.py')
            #  node_modules/file4.py, tests/__pycache__/cached_file.pyc は除外されるべき
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test_find_files_include_with_gitignore_and_patterns(self):
        """
        -P "*.py", "*.txt" --gitignore オプションを使用し、インクルードパターンと .gitignore の除外パターンが正しく適用されることを確認します。
        """
        files = find_files(directory=self.test_dir, patterns=["*.py", "*.txt"], ignore_patterns=None, use_gitignore=True)
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'tests', 'test1.py')
            # node_modules/file4.py と tests/__pycache__/cached_file.pyc は除外されるべき
        ]
        self.assertEqual(sorted(files), sorted(expected))

    def test_find_files_hidden_directories_included(self):
        """
        隠しディレクトリ（__pycache__ や .gitignore）が正しく除外されていることを確認します。
        """
        # -I "__pycache__/"
        files = find_files(directory=self.test_dir, patterns=None, ignore_patterns=["__pycache__/"], use_gitignore=False)
        expected = [
            os.path.join(self.test_dir, '.gitignore'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'node_modules', 'file4.py'),
            os.path.join(self.test_dir, 'tests', 'test1.py')
            # tests/__pycache__/cached_file.pyc は除外されるべき
        ]
        self.assertEqual(sorted(files), sorted(expected))

if __name__ == '__main__':
    unittest.main()
