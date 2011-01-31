"""
Based entirely on Django's own ``setup.py``.
"""
import os
from distutils.command.install import INSTALL_SCHEMES
from distutils.core import setup

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
faq_dir = os.path.join(root_dir, 'faq')
pieces = fullsplit(root_dir)
if pieces[-1] == '':
    len_root_dir = len(pieces) - 1
else:
    len_root_dir = len(pieces)

for dirpath, dirnames, filenames in os.walk(faq_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)[len_root_dir:]))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

# Dynamically calculate the version based on faq.VERSION
# this would be cool if I can figure out how to get it to work.
"""version_tuple = __import__('faq').VERSION
if version_tuple[2] is not None:
    version = "%d.%d_%s" % version_tuple
else:
    version = "%d.%d" % version_tuple[:2]"""

setup(
	name='django-faq',
	version='0.1.1',
	description='This is a simple FAQ application.',
	author='Kevin Fricovsky',
	author_email='kfricovsky@gmail.com',
	url='http://github.com/howiworkdaily/django-faq/tree/master',
	packages=packages,
	classifiers= ['Development Status :: 3 - Alpha',
					'Environment :: Web Environment',
					'Framework :: Django',
					'Intended Audience :: Developers',
					'License :: OSI Approved :: BSD License',
					'Operating System :: OS Independent',
					'Programming Language :: Python',
					'Topic :: Application'],
	include_package_data=True,
	zip_safe=False,
	install_requires=['setuptools', 'simplejson'],
	# also helpful: 'editdist' from http://www.mindrot.org/projects/py-editdist/
)
