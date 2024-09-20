from setuptools import setup, find_packages

setup(
    name='CodeAggregator',
    version='0.1.0',
    author='kentyisapen',
    author_email='kenkenpoco@gmail.com',
    description='生成AI用にコードファイルをまとめて出力するツール',
    long_description=open('docs/README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kentyisapen/code-aggregator',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'code-aggregator=codeaggregator.cli:main',
        ],
    },
    install_requires=[
        # 必要な依存関係をここに記載
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
