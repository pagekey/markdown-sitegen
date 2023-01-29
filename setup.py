from distutils.core import setup


setup(
    name='markdown-sitegen',
    version='1.0.0',
    description='Markdown site generator',
    author='Steve G',
    author_email='steve@pagekeytech.com',
    packages=['markdown_sitegen'],
    entry_points={
        'console_scripts': ['markdown-sitegen=markdown_sitegen.cli:cli_entry_point'],
    },
    install_requires=[
        'python-frontmatter',
        'markdown',
    ],
)
