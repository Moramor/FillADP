import re
from pathlib import Path
from setuptools import setup


def get_dependencies():
    requirements = Path(__file__).resolve().parent / "requirements.txt"
    with requirements.open() as fh:
        requirements = fh.readlines()
        return list(
            map(
                lambda x: re.search("([^>=<~]*)[>=<~]", x).group(1),
                map(str.strip, requirements),
            )
        )


setup(
    name="adprout",
    version="2.0.0",
    description="Automatically fill ADP day to day hours and projects with the same hours and the same project",
    url="https://github.com/Moramor/ADPROUT",
    entry_points={"console_scripts": ["adprout=adprout.filler:fill_adp"]},
    author="Ludovic Bondon",
    author_email="ludovicbondon@gmail.com",
    python_requires=">=3.6",
    packages=["adprout"],
    install_requires=get_dependencies(),
    zip_safe=False,
    include_package_data=True,
)
