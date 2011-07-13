from setuptools import setup, find_packages
import sys
import os

# wd = os.path.dirname(os.path.abspath(__file__))
# os.chdir(wd)
# sys.path.insert(0, wd)

url = 'http://www.scsitaly.com/'

namespace_package = 'Products'
package_name = '%s.%s' % (namespace_package, 'Town')

package = __import__(package_name, {}, {}, [namespace_package])
version = package.__version__
description, long_description = package.__description__.split('\n',1)
classifiers = package.__classifiers__
author, email = package.__author__.strip('<>').rsplit(' ',1)

setup(
    name=package_name,
    version=version,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    url='%s/docs/%s' % (url, package_name),
    description=description,
    long_description=long_description,
    download_url='%s/eggs/%s' % (url, package_name),
    classifiers=classifiers,
    namespace_packages=[namespace_package],
    packages=find_packages(exclude=['ez_setup']),
    keywords='web zope plone content',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
#     entry_points="""
#     # -*- Entry points: -*-
# 
#     [distutils.setup_keywords]
#     paster_plugins = setuptools.dist:assert_string_list
# 
#     [egg_info.writers]
#     paster_plugins.txt = setuptools.command.egg_info:write_arg
#     """,
#     paster_plugins = ["ZopeSkel"],
    test_suite='%s.tests.suite' % package_name)

