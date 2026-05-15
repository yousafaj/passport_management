from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="passport_management",
    version="1.0.0",
    description="Passport Movement Management for ERPNext",
    author="Your Organization",
    author_email="admin@yourorg.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
