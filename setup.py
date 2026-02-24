from setuptools import setup, find_packages

setup(
    name="biblioteca-personal-sandark67",
    version="1.0.1",
    description="Una aplicacion para la gestion de tu biblioteca personal",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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