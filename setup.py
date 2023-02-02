import setuptools
from distutils.core import setup


setup(
    name='markdown-sitegen',
    version='0.0.1',
    description='Markdown site generator',
    author='Steve G',
    author_email='steve@pagekeytech.com',
    packages=['markdown_sitegen'],
    entry_points={
        'console_scripts': ['markdown-sitegen=markdown_sitegen.cli:cli_entry_point'],
    },
    install_requires=[
        'jinja2',
        'python-frontmatter',
        'markdown',
    ],
    package_data={'markdown_sitegen': ['web/*']},
    project_urls={
        'Source Code': 'https://github.com/pagekeytech/markdown-sitegen'
    },
)
