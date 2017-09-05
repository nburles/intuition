#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name="intuition",
	packages=['intuition'],
	version="0.2",
	description="Library and applications to interact with OWL Intuition in Python.",
	author="Michael Farrell",
	author_email="micolous@gmail.com",
	url="https://github.com/shortbloke/intuition",
	license="LGPL3+",
	requires=[
		'Twisted (>=12.0.0)',
		'lxml (>=2.3)',
	],
	
	# entry_points={
	# 	'console_scripts': [
	# 	]
	# },
	
	classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' +
            'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'	
	]
)

