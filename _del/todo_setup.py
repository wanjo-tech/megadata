from setuptools import setup, find_packages

name = "megadata"
version = "0.0.66"
author = "Wanjo Chan"
author_email = "wanjochan@email.com"
description = "tools from/for megadata"
long_description_file = "README.md"
url = "https://github.com/wanjo-tech/megadata"
license = "MIT"

with open(long_description_file, "r", encoding="utf-8") as f:
    long_description = f.read()

install_requires = []

setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    license=license,
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'megadata = megadata:megadata_command',
        ],
    },
)

