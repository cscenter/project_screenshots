from distutils.core import setup

setup(
    name="screenshot-quality",
    version="1.0.0",
    description="Quality of SERP Screenshots",
    packages=['src/screenshots', 'src/screenshots/core', 'src/screenshots/screenshot_filters'],
    install_requires=['numpy', 'opencv-python'],
    # requires=['numpy', 'opencv-python']
)
