import re
import setuptools

with open("requirements.txt") as stream:
    install_requires = stream.read().splitlines()

with open("aioipc/__init__.py") as stream:
    version = re.search(r"^__version__\s*=\s*[\'\"]([^\'\"]*)[\'\"]", stream.read(), re.MULTILINE).group(1)

setuptools.setup(
    author="Riksou",
    url='https://github.com/Riksou/aioipc',
    version=version,
    packages=['aioipc'],
    description='An asynchronous python library for inter-process communication.',
    python_requires='>=3.7'
)
