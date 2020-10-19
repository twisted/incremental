from setuptools import setup

setup(
    name="exampleproj",
    package_dir={"": "src"},
    packages=["exampleproj"],
    use_incremental=True,
    zip_safe=False,
    setup_requires=["incremental"],
)
