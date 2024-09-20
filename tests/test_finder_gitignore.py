# ./tests/test_finder_gitignore.py

import unittest
import os
from codeaggregator.finder import find_files

class TestFinderGitignore(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = 'test_env_gitignore'
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
    
    def test01_gitignore_excludes_patterns(self):
        """
        --gitignore オプションを使用し、.gitignore ファイルのパターンに基づいてファイルを除外することを確認します。
        .gitignore 自体は含まれることを確認します。
        """
        files = find_files(
            directory=self.test_dir,
            patterns=None,
            ignore_patterns=None,
            use_gitignore=True,
            include_hidden=False
        )
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # node_modules/file4.py と tests/__pycache__/cached_file.pyc は除外されるべき
            # .gitignore自体は隠しファイルなのでデフォルトでは非表示
        ]
        self.assertEqual(sorted(files), sorted(expected))
    
    def test02_gitignore_with_patterns(self):
        """
        -P "*.py", "*.txt" --gitignore オプションを使用し、インクルードパターンと .gitignore の除外パターンが正しく適用されることを確認します。
        """
        files = find_files(
            directory=self.test_dir,
            patterns=["*.py", "*.txt"],
            ignore_patterns=None,
            use_gitignore=True,
            include_hidden=False
        )
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file3.txt'),
            os.path.join(self.test_dir, 'tests', 'test1.py'),
            # node_modules/file4.py と tests/__pycache__/cached_file.pyc は .gitignore により除外されるため含まれません
            # .gitignore 自体は *.py や *.txt にマッチしないため除外
        ]
        self.assertEqual(sorted(files), sorted(expected))

if __name__ == '__main__':
    unittest.main()
