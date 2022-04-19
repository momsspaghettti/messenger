from setuptools import setup, find_packages
from pkg_resources import parse_requirements
from typing import List


def load_requirements(file_name: str) -> List[str]:
    requirements = []
    with open(file_name, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements


setup(
    name='messenger',
    platforms='all',
    python_requires='>=3.9',
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'messenger-api = messenger.__main__:main',
            'messenger-db = messenger.db.__main__:main'
        ]
    },
    include_package_data=True
)
