from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="unem",
    version="0.0.1",
    description="Union Nationale de l'Enseignement au Maroc Management System",
    author="UNEM",
    author_email="admin@unem.ma",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
