from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='openvpn-status-parser',
    version='0.0.3',
    description='OpenVPN status parser',
    long_description=long_description,
    url='https://github.com/ojarva/openvpn-status-parser',
    author='Olli Jarva',
    author_email='olli@jarva.fi',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='openvpn',
    packages=["openvpn_status_parser"],
    install_requires=["docopt>=0.6.2"],
    test_suite="tests",
    scripts=["openvpn_status_parser/openvpn-status-parser"],
    extras_require={
        'dev': ['twine', 'wheel'],
    },
)
