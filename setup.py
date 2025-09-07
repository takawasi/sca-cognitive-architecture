#!/usr/bin/env python3
"""Setup script for SCA Tools package"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('-'):
            requirements.append(line)

setup(
    name="sca-tools",
    version="1.0.0",
    author="TAKAWASI Research Team",
    author_email="research@takawasi-social.com",
    description="Symbiotic Cognitive Architecture framework for AI collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takawasi/sca-cognitive-architecture",
    project_urls={
        "Bug Reports": "https://github.com/takawasi/sca-cognitive-architecture/issues",
        "Source": "https://github.com/takawasi/sca-cognitive-architecture",
        "Documentation": "https://takawasi-social.com/sca-system/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "ai": [
            "openai>=1.0.0",
            "anthropic>=0.3.0",
            "tiktoken>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sca=sca_tools.cli:main",
            "sca-context-mapper=sca_tools.context_mapper:main",
            "sca-decomposition=sca_tools.decomposition:main",
            "sca-synthesis=sca_tools.synthesis:main",
            "sca-memory=sca_tools.memory:main",
        ],
    },
    include_package_data=True,
    package_data={
        "sca_tools": [
            "config/*.json",
            "templates/*.txt",
        ],
    },
    keywords="ai artificial-intelligence cognitive-architecture symbiotic collaboration framework",
    zip_safe=False,
)