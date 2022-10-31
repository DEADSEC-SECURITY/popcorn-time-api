from setuptools import find_packages, setup
import pathlib

README = (pathlib.Path(__file__).parent / "README.md").read_text(encoding='utf8')

setup(
    name='popcorn-time',
    packages=find_packages(),
    version='1.0.2',
    description='Interact with the Popcorn Time API with python',
    long_description=README,
    long_description_content_type='text/markdown',
    author='DeadSec-Security',
    author_email='amng835@gmail.com',
    url='https://github.com/DEADSEC-SECURITY/popcorn-time-api',
    keywords=[
        'popcorn',
        'popcorntime',
        'popcorn-time',
        'popcorn api',
        'popcorntimeapi',
        'popcorntime-api',
        'popcorn-time-api'
    ],
    license='MIT',
    install_requires=[
        'requests==2.27.1'
    ],
    python_requires='>=3.7'
)
