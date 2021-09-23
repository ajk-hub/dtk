import setuptools

setuptools.setup(
    name="dtk",
    version="1.0.0",
    description="Development Tool Kit",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"}
)
