# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='sphinx_recent_pages',
      version='0.1',
      author='Sho Shimauchi',
      author_email='sho.shimauchi@gmail.com',
      test_suite='nose.collector',
      tests_require='Nose',
      packages=find_packages(exclude=['test']),
      package_dir= {'' : 'src' }
      )
