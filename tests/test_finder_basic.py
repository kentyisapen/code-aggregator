# ./tests/test_finder_basic.py

import unittest
import os
from codeaggregator.finder import find_files

class TestFinderBasic(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = 'test_env_basic'
        os.makedirs(self.test_dir, exist_ok=True)
        
        # テストファイルとディレクトリを作成
        os.makedirs(os.path.join(self.test_dir, 'src'), exist_ok=True)
        
        with open(os.path.join(self.test_dir, 'src', 'file1.py'), 'w') as f:
            f.write('print("Hello, World!")')
        with open(os.path.join(self.test_dir, 'src', 'file2.js'), 'w') as f:
            f.write('console.log("Hello, World!");')
        with open(os.path.join(self.test_dir, 'src', 'file3.txt'), 'w') as f:
            f.write('This is a text file.')
    
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
        ]
        self.assertCountEqual(sorted(files), sorted(expected))

if __name__ == '__main__':
    unittest.main()
