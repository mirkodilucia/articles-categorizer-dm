from setuptools import find_packages, setup

setup(
    name='@datamining',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add other common dependencies
    ],
    entry_points={
        'console_scripts': [
            'run_dataflow=scripts.run_dataflow:app',
            'run_classifier=scripts.run_classifier:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
