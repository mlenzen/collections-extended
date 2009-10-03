#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Michael Lenzen <m.lenzen@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
"""
from distutils.core import setup

setup(
		name='datastructures',
		version = '0.1.0',
		description = 'Python Data Structures - bags/multisets and setlists',
		author = 'Michael Lenzen',
		author_email = 'm.lenzen@gmail.com',
		url = 'http://code.google.com/p/python-data-structures/',
		packages = ['datastructures'],
		keywords = ['collections', 'bag', 'multiset', 'setlist'],
		classifiers = [
			'Development Status :: 4 - Beta',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: Apache Software License',
			'Operating System :: OS Independent',
			'Programming Language :: Python',
			'Programming Language :: Python :: 3',
			'Topic :: Software Development',
			'Topic :: Software Development :: Libraries',
			'Topic :: Software Development :: Libraries :: Python Modules',
			],
		long_description = """\
Python Data Structures
----------------------

For now, this package includes one module - `collections_extended`.  This module
extends the built-in collections module to include a `bag` class, AKA multiset, and
a `setlist` class, which is a list of unique elements or an ordered set depending on
how you look at it.  There are also frozen (hashable) varieties of each included.
Finally, all collections are abstracted into one Collection abstract base class and
a Collection factory is provided where you can create a Collection by specifying
the properties unique, ordered and mutable.

See http://code.google.com/p/python-data-structures/wiki/CollectionsExtendedProposal
for more.
				""",
		)
