"""Setup for housler-crypto package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="housler-crypto",
    version="1.0.0",
    author="Housler Team",
    author_email="dev@housler.ru",
    description="Unified PII encryption for Housler ecosystem (152-FZ compliant)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/housler/housler-crypto",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.10",
    install_requires=[
        "cryptography>=41.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
)
