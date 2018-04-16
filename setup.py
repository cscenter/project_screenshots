from setuptools import setup, find_packages

setup(
    name="screenqual",
    version="1.0.0",
    description="Quality of SERP Screenshots",
    packages=find_packages(exclude=("tests",)),
    install_requires=['numpy', 'opencv-python', 'setuptools_git'],
    include_data_files=True,
    setup_requires=['setuptools_git >= 0.3', ],
    package_data={
        '': ['*'],
        'screenqual': ['*']
    }
)
