from setuptools import setup, find_packages

setup(
    name='flasksearchapp',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=["flask", "gunicorn", "redis", "nltk"],
    description='',
)

import nltk

nltk.download('punkt')
