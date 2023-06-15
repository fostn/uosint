from setuptools import setup, find_packages

setup(
    name='uosint',
    version='1.0.0',
    packages=['src','config'],
    py_modules=["main"],
    include_package_data=True,
    package_data={'': ['*.ini']},
    entry_points={
        'console_scripts': [
            'uosint = main:main'
        ]
    },
    install_requires=[
        'requests',
        'tabulate==0.9.0',
        'pycryptodome==3.18.0'
    ],

)
