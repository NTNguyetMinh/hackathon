from setuptools import setup, find_packages

setup(
    name='hackathon',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'redis',
    ],
)