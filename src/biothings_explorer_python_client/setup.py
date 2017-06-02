import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="biothings_explorer",
    version="0.1.0",
    author="Jiwen Xin, Chunlei Wu",
    author_email="cwu@scripps.edu",
    description="Python Client for BioThings Explorer",
    license="BSD",
    keywords="link API interoperability biology explore",
    url="https://github.com/biothings/biothings_explorer",
    packages=['biothings_explorer'],
    package_data={'biothings_explorer': ['context']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    install_requires=[
        'requests>=2.3.0',
        "PyLD>=0.7.2",
        'biothings_client>=0.1.1'
    ],
)
