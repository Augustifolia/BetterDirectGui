from setuptools import setup

setup(
    name="BetterDirectGui",
    version="0.1",
    description="An extended version of DirectGui for use in panda3d",
    author="Augustifolia",
    url="https://github.com/Augustifolia/BetterDirectGui",
    packages=["BetterDirectGui"],
    python_requires=">=3.8, <4",
    install_requires=["panda3d"]
)
