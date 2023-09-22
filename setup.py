from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.md', 'r').read()

REQUIREMENTS = [
    'cytoolz==0.12.1',
    'eth_keys',
    'eth-account>=0.4.0,<0.6.0',
    'mpmath==1.0.0',
    'web3>=5.0.0,<6.0.0',
]

setup(
    name='goldlink-client-python',
    version='0.0.1',
    packages=find_packages(),
    package_data={
        'goldlink': [
            'abi/*.json',
        ],
    },
    description='GoldLink client for borrowing, lending and active management',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/GoldLink-Protocol/goldlink-client-python',
    author='GoldLink Protocol Inc.',
    license='Apache 2.0',
    author_email='info@goldlink.io',
    install_requires=REQUIREMENTS,
    keywords='goldlink defi arb arbitrum ethereum eth',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
