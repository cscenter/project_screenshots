from setuptools import setup, find_packages

setup(
    name="screenqual",
    version="1.0.0",
    description="Quality of SERP Screenshots",
    packages=find_packages(exclude=("tests",)),
    install_requires=['numpy', 'opencv-python'],
    package_data={
        '': [
            'models/general_detector/avg_spectre.npy',
            'models/general_detector/spectre_indices.npy',
            'models/general_detector/threshold.txt'
        ],
        'screenqual': [
            'models/general_detector/avg_spectre.npy',
            'models/general_detector/spectre_indices.npy',
            'models/general_detector/threshold.txt'
        ]
    },
)
