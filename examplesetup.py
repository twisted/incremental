from setuptools import setup

setup(
    name='exampleproj',
    package_dir={"": "src"},
    packages=["exampleproj"],
    use_incremental=True,
    setup_requires=['incremental'],
)
