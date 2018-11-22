from setuptools import setup

setup(
    name='pybinaryedge',
    version='0.1',
    description='Python 3 Wrapper for the binary edge API https://www.binaryedge.io/',
    url='https://github.com/Te-k/pybinaryedge',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='osint',
    install_requires=['requests', 'configparser'],
    license='MIT',
    packages=['pybinaryedge'],
    entry_points= {
        'console_scripts': [ 'binaryedge=pybinaryedge.cli:main' ]
    }
)
