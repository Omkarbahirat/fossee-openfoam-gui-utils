from setuptools import setup, find_packages

setup(
    name='treelib',
    version='0.1.0',
    description='Binary/General Tree library with YAML integration',
    packages=find_packages(include=['treelib', 'treelib.*']),
    install_requires=['PyYAML>=5.4'],
    python_requires='>=3.8',
)
