from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in unem/__init__.py
from unem import __version__ as version

setup(
    name="unem",
    version=version,
    description="Union Nationale de l'Enseignement au Maroc Management System",
    author="UNEM",
    author_email="admin@unem.ma",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
