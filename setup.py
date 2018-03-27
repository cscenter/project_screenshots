from setuptools import setup, find_packages

setup(
    name="screenshot-quality",
    version="1.0.0",
    description="Quality of SERP Screenshots",
    packages=find_packages(),
    install_requires=['numpy', 'opencv-python'],
    # requires=['numpy', 'opencv-python']
)
