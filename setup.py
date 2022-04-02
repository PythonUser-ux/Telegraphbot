from setuptools import setup, Extension

with open("README.md", "r") as fh:
      long_description=fh.read()

setup(
   name='telegraphbot', 
   version='0.0.3',
   # packages=[],
   license='MIT', 
   description='A tool for python Telegram bots',

   long_description=long_description,
   long_description_content_type="text/markdown",
   py_modules=["telegraphbot"],
   package_dir={'': 'src'},
   classifiers=["Programming Language :: Python :: 3"],
)