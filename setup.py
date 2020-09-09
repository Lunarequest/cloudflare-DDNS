from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name="cloudflare-ddns",
    version="1.0.0",
    description="A battries included quick way to update dns records",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/advaithm/cloudflare-DDNS",
    author="nullrequest",
    author_email="advaith.madhukar@gmail.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GPL License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8.5",
    ],
    packages=["cloudflare-ddns"],
    include_package_data=True,
    install_requires=["requests", "pyyaml","sockets"],
    entry_points={
        "console_scripts": [
            "cloudflareddns=cloudflareddns.__main__:main",
        ]
    },
)