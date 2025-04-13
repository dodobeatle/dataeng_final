from setuptools import find_packages, setup

setup(
    name="dataeng_final",
    packages=find_packages(exclude=["dataeng_final_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
