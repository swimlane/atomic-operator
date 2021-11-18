import os

from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


PROJECT_URLS = {
    "Documentation": "https://swimlane.com",
    "Changelog": "https://github.com/swimlane/atomic-operator/blob/main/CHANGELOG.md",
    "Bug Tracker": "https://github.com/swimlane/atomic-operator/issues",
    "Source Code": "https://github.com/swimlane/atomic-operator",
    "Funding": "https://github.com/sponsors/msadministrator",
}

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Information Technology",
    "Intended Audience :: System Administrators",
    "Intended Audience :: End Users/Desktop",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Security"
]

setup(
    name='atomic-operator',
    version=get_version("atomic_operator/__init__.py"),
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A python package to execute Atomic tests',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    project_urls=PROJECT_URLS,
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['atomic-red-team', 'att&ck', 'test', 'mitre', 'executor'],
    url='https://github.com/swimlane/atomic-operator',
    author='MSAdministrator',
    author_email='rickardja@live.com',
    maintainer='MSAdministrator',
    maintainer_email='rickardja@live.com',
    python_requires='>=3.6, <4',
    classifiers=CLASSIFIERS,
    package_data={
        'atomic_operator':  ['data/logging.yml']
    },
    entry_points={
          'console_scripts': [
              'atomic-operator = atomic_operator.__main__:main'
          ]
    }
)