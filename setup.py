import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description += "\n------\n"

setuptools.setup(
    name="maildropview",
    version='1.0.0',
    description="Produto para visualizar emails do maildrop",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jcjuliocss/maildrop_view",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    namespace_packages=['Products'],
    maintainer='Soft-RH',
    maintainer_email='ti@nube.com.br',
    author='Julio Cesar Schlindwein da Silva',
    author_email="julio.silva@softrh.com.br"
)
