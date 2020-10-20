from setuptools import setup


setup(
    name='Password Change Reporter',
    version='1.0',
    py_modules=['main'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        pwcr=main:main
    '''
)