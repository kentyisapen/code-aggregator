# tests/test_finder_fromfile.py

import unittest
import os
from codeaggregator.finder import find_files
from unittest import mock
import io

class TestFinderFromFile(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = 'test_env_from_file'
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'src'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'docs'), exist_ok=True)
        
        # テストファイルを作成
        with open(os.path.join(self.test_dir, 'src', 'file1.py'), 'w') as f:
            f.write('print("Hello, World!")')
        with open(os.path.join(self.test_dir, 'src', 'file2.js'), 'w') as f:
            f.write('console.log("Hello, World!");')
        with open(os.path.join(self.test_dir, 'docs', 'README.md'), 'w') as f:
            f.write('# Documentation')
        # 存在しないファイルは作成しません

    def tearDown(self):
        # テスト用の一時ディレクトリを削除
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    @mock.patch('sys.stdin', new_callable=io.StringIO)
    def test01_fromfile_reads_from_stdin(self, mock_stdin):
        """
        --fromfile オプションを使用し、標準入力からのファイルリストを正しく処理することを確認します。
        存在しないファイルはfind_files関数自体ではそのまま通過される。(output時点でファイルがない場合にwarn)
        """
        # モックされた標準入力にファイルリストを書き込む
        mock_stdin.write("src/file1.py\nsrc/file2.js\ndocs/README.md\nnonexistent/file3.txt\n")
        mock_stdin.seek(0)

        files = find_files(
            directory=self.test_dir,
            patterns=None,
            ignore_patterns=None,
            fromfile='.',
            include_hidden=False
        )
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'src', 'file2.js'),
            os.path.join(self.test_dir, 'docs', 'README.md'),
            os.path.join(self.test_dir, 'nonexistent', 'file3.txt')
        ]
        self.assertCountEqual(sorted(files), sorted(expected))
    
    def test02_fromfile_reads_from_file(self):
        """
        --fromfile オプションを使用し、指定されたファイルからのファイルリストを正しく処理することを確認します。
        """
        # ファイルリストを模擬
        file_list = [
            'src/file1.py',
            'src/file2.js',
            'docs/README.md'
        ]
        # 'paths.txt' ファイルを作成して内容を書き込む
        path_txt = os.path.join(self.test_dir, 'paths.txt')
        with open(path_txt, 'w') as f:
            f.write('\n'.join(file_list))
    
        files = find_files(
            directory=self.test_dir,
            patterns=["*.py"],
            ignore_patterns=None,
            fromfile=path_txt,
            include_hidden=False
        )
        expected = [
            os.path.join(self.test_dir, 'src', 'file1.py'),
            # 'src/file2.js' と 'docs/README.md' は *.py にマッチしないため除外
        ]
        self.assertCountEqual(sorted(files), sorted(expected))
    
    @mock.patch('sys.stdin', new_callable=io.StringIO)
    def test03_fromfile_include_hidden(self, mock_stdin):
        """
        --fromfile と -a オプションを使用し、隠しファイルも含めて処理することを確認します。
        """
        # モックされた標準入力に隠しファイルを含むファイルリストを書き込む
        mock_stdin.write(".hidden_file.py\nsrc/file1.py\ndocs/.hidden_dir/README.md\n")
        mock_stdin.seek(0)

        # 隠しファイルを含める設定
        files = find_files(
            directory=self.test_dir,
            patterns=None,
            ignore_patterns=None,
            fromfile='.',
            include_hidden=True
        )
        expected = [
            os.path.join(self.test_dir, '.hidden_file.py'),
            os.path.join(self.test_dir, 'src', 'file1.py'),
            os.path.join(self.test_dir, 'docs', '.hidden_dir', 'README.md'),
        ]
        self.assertCountEqual(sorted(files), sorted(expected))
