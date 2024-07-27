from setuptools import find_packages, setup


setup(
    name="mypathfinding",
    version="1.0.1",
    packages=find_packages(),
    install_requires=["setuptools", \
                      "pygame", \
                      "pygwrapper", \
                      "grid", \
                      "csv2d", \
                      ],
    include_package_data=True,
    description="Pathfinding package",
    author="Michael Naef",
    author_email="mister_naef@hotmail.com",
    url="https://github.com/forcodeinmymind/mypathfinding.git",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
