from setuptools import setup, find_packages

setup(
    name="biblioteca_personal",
    version="1.0.0",
    description="Una aplicacion para la gestion de tu biblioteca personal",
    author="Alexandre",
    packages=find_packages(),
    py_modules=["main", "conexionBD"],
    install_requires=[
        "PyGObject"
    ],
    entry_points={
        'console_scripts': [
            'abrir-biblioteca=main:main',
        ],
    },
)