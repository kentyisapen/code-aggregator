# ./tests/test_finder_hidden.py

import unittest
import os
from codeaggregator.finder import find_files

class TestFinderHidden(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = 'test_env_hidden'
        os.makedirs(self.test_dir, exist_ok=True)
        
        # テストファイルとディレクトリを作成
        os.makedirs(os.path.join(self.test_dir, 'src'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, '.hidden_dir'), exist_ok=True)
        
        with open(os.path.join(self.test_dir, 'src', 'file1.py'), 'w') as f:
            f.write('print("Hello, World!")')
        with open(os.path.join(self.test_dir, 'src', 'file2.js'), 'w') as f:
            f.write('console.log("Hello, World!");')
        with open(os.path.join(self.test_dir, 'src', 'file3.txt'), 'w') as f:
            f.write('This is a text file.')
        with open(os.path.join(self.test_dir, '.hidden_file'), 'w') as f:
            f.write('This is a hidden file.')
        with open(os.path.join(self.test_dir, '.hidden_dir', 'hidden_inside.py'), 'w') as f:
            f.write('print("Hidden inside directory")')
    
    def tearDown(self):
        # テスト用の一時ディレクトリを削除
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.test_dir)
    
    def test01_hidden_directories_excluded(self):
        """
        隠しディレクトリ（例: .hidden_dir）および隠しファイル（例: .hidden_file）が正しく除外されることを確認します。
        """
        files = find_files(
            directory=self.test_dir,
            patterns=None,
            ignore_patterns=None,
            use_gitignore=False,
            include_hidden=False
        )
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            # .hidden_file と .hidden_dir/hidden_inside.py は除外されるべき
        ]
        self.assertEqual(sorted(files), sorted(expected))
    
    def test02_include_hidden_with_a_option(self):
        """
        -a オプションを使用し、先頭に '.' が付くファイルやフォルダも含めることを確認します。
        """
        files = find_files(
            directory=self.test_dir,
            patterns=None,
            ignore_patterns=None,
            use_gitignore=False,
            include_hidden=True
        )
        expected = [
            os.path.join(self.test_dir, '.hidden_file'),
            os.path.join(self.test_dir, '.hidden_dir', 'hidden_inside.py'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
        ]
        self.assertEqual(sorted(files), sorted(expected))
    
    def test03_include_hidden_with_patterns(self):
        """
        -P "*.py", "*.txt" -a オプションを使用し、インクルードパターンと共に隠しファイル/ディレクトリも含めることを確認します。
        """
        files = find_files(
            directory=self.test_dir,
            patterns=["*.py", "*.txt"],
            ignore_patterns=None,
            use_gitignore=False,
            include_hidden=True
        )
        expected = [
            os.path.join(self.test_dir, '.hidden_dir', 'hidden_inside.py'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'src', 'file2.js'),  # *.js はパターンに含まれないため除外
        ]
        # *.js はパターンに含まれないため除外
        expected_filtered = [
            os.path.join(self.test_dir, '.hidden_dir', 'hidden_inside.py'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
        ]
        self.assertEqual(sorted(files), sorted(expected_filtered))

if __name__ == '__main__':
    unittest.main()
