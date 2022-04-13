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


here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'atomic_operator', '__meta__.py'), 'r') as f:
    exec(f.read(), about)


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
    name=about['__title__'],
    version=about['__version__'],
    packages=find_packages(exclude=['tests*']),
    license=about['__license__'],
    description=about['__description__'],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    project_urls=PROJECT_URLS,
    install_requires=[
        'requests>=2.20.0; python_version >= "3.6"',
        'charset_normalizer~=2.0.0; python_version >= "3"',
        'chardet>=3.0.2,<5; python_version < "3"',
        'idna>=2.5,<3; python_version < "3"',
        'idna>=2.5,<4; python_version >= "3"',
        'urllib3>=1.21.1,<1.27',
        'certifi>=2017.4.17',
        'windows-curses>=2.2.0,<3.0.0; platform_system=="Windows" and python_version >= "3.6"',
        'attrs>=21.3.0; python_version >= "3.6"',
        'pyyaml>=6.0; python_version >= "3.6"',
        'fire>=0.4.0; python_version >= "3.6"',
        'pypsrp>=0.5.0; python_version >= "3.6"',
        'paramiko>=2.7.2; python_version >= "3.6"',
        'pick>=1.2.0; python_version >= "3.6"'
    ],
    keywords=['atomic-red-team', 'att&ck', 'test', 'mitre', 'executor'],
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],
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