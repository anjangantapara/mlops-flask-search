from setuptools import setup, find_packages

setup(
    name='flasksearchapp',
    version="0.0.1",
    author="Anjan Gantapara",
    description="App to to post documents to a flask app. The app also facilitates search facility",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=["flask", "gunicorn", "redis", "nltk", "httpie", "pandas", "numpy", "textblob", "scikit-learn"]
)

import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('reuters')
