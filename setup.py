from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='linkedin profile picture',  
    version='0.0.2',
    author="Emanuel-Ionut Otel, original by Shashank Deshpande",
    author_email="manuotel@gmail.com",
    description="Python package to crawl linkedin profile pictures using google custom search API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ManuOtel/linkedin-profile-picture",
    python_requires=">=3.6.0",
    packages=find_packages()
    )
