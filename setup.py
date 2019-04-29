from setuptools import find_packages, setup


setup(
    name='uas',
    version='1.0.0',
    url = 'https://uas-app.herokuapp.com/',
    author = 'Marco Hernandez',
    author_email = 'marcohdes94i@gmail.com',
    classifiers = [" Programming Language Python 3.6 "],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)