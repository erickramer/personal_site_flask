from setuptools import setup, find_packages

setup(
    name="personal_site_flask",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "tensorflow>=2.12.0,<2.14.0",
        "numpy>=1.22.0,<1.25.0",
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