from setuptools import find_packages, _install_setup_requires
import distutils.core
import os

requirements = ['telethon']
def setup(**attrs):
    _install_setup_requires(attrs)
    return distutils.core.setup(**attrs)

def main():
    setup(name='TL-Send',
          packages=find_packages(),
          license="MIT",
          author='Nitan Alexandru Marcel',
          author_email='nitan.marcel@gmail.com',
          install_requires=requirements,
          entry_points={'console_scripts': ['tl = tlsend.app:main']})

if __name__ == "__main__":
    main()