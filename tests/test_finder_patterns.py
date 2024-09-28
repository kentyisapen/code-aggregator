# ./tests/test_finder_patterns.py

import unittest
import os
from codeaggregator.finder import find_files

class TestFinderPatterns(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = 'test_env_patterns'
        os.makedirs(self.test_dir, exist_ok=True)
        
        # テストファイルとディレクトリを作成
        os.makedirs(os.path.join(self.test_dir, 'src'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'src', 'subdir'), exist_ok=True)
        
        with open(os.path.join(self.test_dir, 'src', 'file1.py'), 'w') as f:
            f.write('print("Hello, World!")')
        with open(os.path.join(self.test_dir, 'src', 'file2.js'), 'w') as f:
            f.write('console.log("Hello, World!");')
        with open(os.path.join(self.test_dir, 'src', 'file3.txt'), 'w') as f:
            f.write('This is a text file.')
        with open(os.path.join(self.test_dir, 'src', 'file4.dpp'), 'w') as f:
            f.write('// DPP file')
        with open(os.path.join(self.test_dir, 'src', 'file5.wpp'), 'w') as f:
            f.write('// WPP file')
        with open(os.path.join(self.test_dir, 'src', 'file6.cpp'), 'w') as f:
            f.write('// C++ file')
    
    def tearDown(self):
        # テスト用の一時ディレクトリを削除
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.test_dir)
    
    def test01_include_multiple_patterns(self):
        """
        -P "*.py", "*.txt" オプションを使用し、特定のパターンに一致するファイルのみを含めることを確認します。
        """
        files = find_files(
            directory=self.test_dir,
            patterns=["*.py", "*.txt"],
            ignore_patterns=None,
            use_gitignore=False,
            include_hidden=False
        )
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
        ]
        self.assertCountEqual(sorted(files), sorted(expected))
    
    def test02_include_or_pattern_py_txt(self):
        """
        -P "*.py|*.txt" オプションを使用し、*.py または *.txt にマッチするファイルのみを含めることを確認します。
        """
        patterns = ["*.py|*.txt"]
        files = find_files(
            directory=self.test_dir,
            patterns=patterns,
            ignore_patterns=None,
            use_gitignore=False,
            include_hidden=False
        )
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
        ]
        self.assertCountEqual(sorted(files), sorted(expected))
    
    def test03_include_character_class_pattern(self):
        """
        -P "*.[dwc]pp" オプションを使用し、*.dpp, *.wpp, *.cpp にマッチするファイルのみを含めることを確認します。
        """
        patterns = ["*.[dwc]pp"]
        files = find_files(
            directory=self.test_dir,
            patterns=patterns,
            ignore_patterns=None,
            use_gitignore=False,
            include_hidden=False
        )
        expected = [
            os.path.join(self.test_dir, 'src', 'file4.dpp'),
            os.path.join(self.test_dir, 'src', 'file5.wpp'),
            os.path.join(self.test_dir, 'src', 'file6.cpp'),
        ]
        self.assertCountEqual(sorted(files), sorted(expected))
    
    def test04_include_combined_patterns(self):
        """
        -P "*.py|*.txt", "*.[dwc]pp" オプションを使用し、*.py または *.txt または *.dpp, *.wpp, *.cpp にマッチするファイルのみを含めることを確認します。
        """
        patterns = ["*.py|*.txt", "*.[dwc]pp"]
        files = find_files(
            directory=self.test_dir,
            patterns=patterns,
            ignore_patterns=None,
            use_gitignore=False,
            include_hidden=False
        )
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'src', 'file4.dpp'),
            os.path.join(self.test_dir, 'src', 'file5.wpp'),
            os.path.join(self.test_dir, 'src', 'file6.cpp'),
        ]
        self.assertCountEqual(sorted(files), sorted(expected))

if __name__ == '__main__':
    unittest.main()
