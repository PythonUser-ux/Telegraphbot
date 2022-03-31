from setuptools import setup

with open("README.md", "r") as fh:
      long_description=fh.read()

setup(
   name='telegraph', 
   version='0.0.1',
   # packages=[],
   license='MIT', 
   description='tool for python Telegrom bots',

   long_description=long_description,
   long_description_content="text/markdown",
   py_modules=["telegraph"],
   package_dir={'': 'src'},
   classifiers=["Programming Language :: Python ::3"]
)