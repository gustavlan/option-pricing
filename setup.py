import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="option_pricing",                           
    version="0.1.0",                                 
    author="Gustav Lantz",
    author_email="lantzgustav@gmail.com",                  
    description=(
        "A Python library for Monte Carlo, Asian & Lookback option pricing"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gustavlan/option-pricing",
    project_urls={
        "Bug Tracker": "https://github.com/gustavlan/option-pricing/issues",
        "Source Code": "https://github.com/gustavlan/option-pricing",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=[
        "numpy>=1.20",
        "scipy>=1.6",
        "pandas>=1.2",
        "matplotlib>=3.4",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="option pricing monte-carlo asian lookback finance quant",
)
