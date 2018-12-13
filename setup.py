#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages


def load_requirements(path):
    with open(path) as fin:
        return [
            line
            for line in map(lambda l: l.strip(), fin.readlines())
            if line and not line.startswith('#')
        ]


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = load_requirements('requirements_prod.txt')
test_requirements = load_requirements('requirements_dev.txt')

setup(
    author="Hunt Zhan",
    author_email='huntzhan.dev@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="None",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cnt.rulebase',
    name='cnt.rulebase',
    packages=find_packages(),
    test_suite='tests',
    tests_require=test_requirements,
    extras_require={'test': test_requirements},
    url='https://github.com/cnt-dev/cnt.rulebase',
    version='0.11.1',
    zip_safe=False,
)
