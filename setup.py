#
#   setup.py
#       This file makes our project installable.
#       See also: https://packaging.python.org/en/latest/tutorials/packaging-projects/
#

#
#   The pros to making this an installable:
#       • Currently, Python and Flask understand how to use the flaskr package only because you’re running from your project’s directory.
#         Installing means you can import it no matter where you run from.
#       • You can manage the project’s dependencies just like other packages do, so pip install bobchat.whl installs them.
#       • Test tools can isolate your test environment from your development environment.
#

from setuptools import find_packages, setup

setup(
    name='bobchat',
    version='1.0.0',

    # packages tells Python what package directories (and the Python files they contain) to include.
    # find_packages() finds these directories automatically so you don’t have to type them out.
    packages=find_packages(),

    # To include other files, such as the static and templates directories, include_package_data is set.
    # Python needs another file named MANIFEST.in to tell what this other data is.
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'pandas',
        'gunicorn',
    ],
)

#
#   If you use pip to install this package (in a virtual environment) via:
#       pip install -e .
#
#   That tells pip to find setup.py in the current directory and install it in editable or development mode.
#

