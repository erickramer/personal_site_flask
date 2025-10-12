from setuptools import setup, find_packages

setup(
    name="personal_site_flask",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-flask",
            "pytest-cov",
            "beautifulsoup4",
            "bs4",
            "pyyaml",
        ],
    },
)
