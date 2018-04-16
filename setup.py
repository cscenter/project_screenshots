from setuptools import setup, find_packages

setup(
    name="screenqual",
    version="1.0.0",
    description="Quality of SERP Screenshots",
    packages=find_packages(exclude=("tests",)),
    install_requires=['numpy', 'opencv-python'],
    package_data={
        '': ['*']
    }
)
