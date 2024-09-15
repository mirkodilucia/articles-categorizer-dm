from setuptools import find_packages, setup

setup(
    name='@datamining/crawler',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'html5lib==1.1',
        'selenium==4.11.2',
        'beautifulsoup4==4.11.1',
        'webdriver-manager==3.7.0',
        'asyncio==3.4.3',
        'setuptools~=65.5.1',
        'python-dotenv~=0.20.0',
    ],
    entry_points={
        'console_scripts': [
            'run_api=scripts.run_dataflow:app',
            'run_classifier=scripts.run_classifier:main',
        ],
    },
)
