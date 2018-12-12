from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pybinaryedge',
    version='0.2',
    description='Python 3 Wrapper for the binary edge API https://www.binaryedge.io/',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Te-k/pybinaryedge',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='osint',
    install_requires=['requests', 'configparser'],
    license='MIT',
    packages=['pybinaryedge'],
    entry_points= {
        'console_scripts': [ 'binaryedge=pybinaryedge.cli:main' ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
