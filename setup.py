import os

from setuptools import setup

from pygram import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='pygram',
    version=__version__,
    packages=['pygram'],
    package_data={
        '.': [
            '*.pub',
        ]},
    include_package_data=True,
    url='https://github.com/RedXBeard/pygram',
    license='MIT',
    author='Barbaros Yildirim',
    author_email='barbarosaliyildirim@gmail.com',
    description='Telegram messaging from your terminal.',
    long_description=LONG_DESCRIPTION,
    entry_points={
        'console_scripts': [
            'pygram = pygram.command:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Chat'
    ],
    install_requires=[
        'npyscreen',
        'DictObject',
        'pytg'
    ]
)
