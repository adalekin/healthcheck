import ast
import codecs
import os
import re

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description
with codecs.open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


# Get version
_VERSION_RE = re.compile(r"VERSION\s+=\s+(.*)")

with open("healthcheck/__init__.py", "rb") as f:
    VERSION = str(ast.literal_eval(_VERSION_RE.search(f.read().decode("utf-8")).group(1)))

# Get requirements
_EGG_RE = re.compile(r"#egg=(?P<egg>[-\w]+)")

def get_requirements(env=None):
    requirements = []
    requirements_filename = "requirements.txt"

    if env:
        requirements_filename = "requirements-{}.txt".format(env)

    with open(requirements_filename) as fp:
        for requirement in fp:
            if requirement.startswith("#"):
                continue

            if "#egg=" in requirement:
                egg_name = _EGG_RE.search(requirement).group("egg")
                requirements.append("{} @ {}".format(egg_name, requirement))
            else:
                requirements.append(requirement)

    return requirements


INSTALL_REQUIREMENTS = get_requirements()
TEST_REQUIREMENTS = get_requirements("test")

setup(
    name="healthcheck",
    version=VERSION,
    description="",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://gitlab.everynet.io/platform/libs/healthcheck",
    author="Alexey Dalekin",
    author_email="alexey.dalekin@everynet.com",
    platforms=["any"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Distributed Computing",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
    ],
    keywords="healthcheck",
    packages=find_packages(exclude=("tests",)),
    setup_requires=["pytest-runner"],
    install_requires=INSTALL_REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    extra_require={"gunicorn": ["gunicorn>=19.10.0"]},
    include_package_data=True,
)
