from setuptools import setup
# https://packaging.python.org/guides/making-a-pypi-friendly-readme/

# TO CREATE SETUP:
# 1. cd to the directory where the setup.py script is
# 2. RUN THE COMMAND:
# python setup.py sdist bdist_wheel

# check distr: 
# twine check dist/*

# upload to PYPI: https://realpython.com/pypi-publish-python-package/#testing-your-package

# upload to PYPI:
# twine upload dist/*

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
	
setup(
   name='camex',
   version='0.0.1a1',
   author='Andrei Keino',
   author_email='andreikeino@gmail.com',
   packages=['camex'],
   entry_points={
         'console_scripts': ['camex=camex.cam_ex:main'],},
   url='http://pypi.python.org/pypi/camex/',
   license='LICENSE.txt',
   include_package_data=True,
   description='Computational Applied Mathematics EXamples',
   long_description_content_type="text/markdown",
   long_description=long_description,
   python_requires='>=3.7',
   install_requires=[
   
       "PyQtWebEngine",
       "qtconsole",
	   "matplotlib",
	   "cvxpy",
	   "cvxopt",
	   "pandas",
	   "pandas-datareader",
	  
   ],
)
