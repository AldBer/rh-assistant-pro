# setup.py - Coloque na raiz do projeto
from setuptools import setup, find_packages
import os

# Lê requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='rh-assistant-pro',
    version='1.0.0',
    author='AldBer',
    author_email='aldo.bernardi@gmail.com',
    description='Sistema inteligente de consulta de políticas com triagem automática',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AldBer/rh-assistant-pro',
    packages=find_packages(),
    package_data={
        '': ['*.json', '*.css', '*.js', '*.ico', '*.png']
    },
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'rh-assistant=src.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Enterprise',
    ],
    python_requires='>=3.8',
)