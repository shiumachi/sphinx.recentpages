# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='sphinx.recentpages',
      version='0.1',
      author='Sho Shimauchi',
      author_email='sho.shimauchi@gmail.com',
      test_suite='nose.collector',
      tests_require='Nose',
      namespace_packages=['sphinx'],
      packages=find_packages('src', exclude=['test']),
      package_dir={'' : 'src' },
      entry_points={
        'console_scripts': [
            "recentpages = sphinx.recentpages.recentpages:main",
            ],
        }
      )
