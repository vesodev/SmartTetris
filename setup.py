from setuptools import setup, find_packages

setup(
    name="SmartTetris",
    version="0.1",
    packages=find_packages(),
    install_requires=['PyQt5>=5.5'],
    author="Veselin Ivanov",
    author_email="veselin.ivanov.jr@gmail.com",
    description="A Tetris game with included AI",
    license="GPLv3",
    keywords="tetris AI",
    url="https://github.com/vesodev/SmartTetris"
)
