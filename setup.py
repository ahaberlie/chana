from setuptools import setup, find_namespace_packages

setup(name='chana',
      version='0.1',
      description='ChAna - Cheyenne dataset Analyses',
      author='Alex Haberlie and Chris Battisto',
      author_email='ahaberlie1@lsu.edu',
      package_dir={'':'src'},
      packages=find_namespace_packages(where="src"),
      url='atlas.niu.edu'
     )