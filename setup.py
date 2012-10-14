# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='sphinx.recentpages',
      version='0.3',
      author='Sho Shimauchi',
      author_email='sho.shimauchi@gmail.com',
      test_suite='nose.collector',
      tests_require='Nose',
      packages=find_packages('sphinx.recentpages'),
      package_dir={'' : 'sphinx.recentpages' },
      )
