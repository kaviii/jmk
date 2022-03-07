from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in jmkfood/__init__.py
from jmkfood import __version__ as version

setup(
	name="jmkfood",
	version=version,
	description="Customisation for JMK Foods",
	author="Kavitha Balakrishnan",
	author_email="kavitha1995@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
