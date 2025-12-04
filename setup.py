from setuptools import setup, find_packages

setup(
    name="mylittleansible",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "paramiko==3.4.0",
        "jinja2==3.1.2",
        "click==8.1.7",
        "pyyaml==6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "mla = mylittleansible.cli:main",
        ],
    },
)
