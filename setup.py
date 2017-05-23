from setuptools import setup, find_packages


install_requires = ['molotov', 'bottle', 'requests']
description = ''

for file_ in ('README', 'CHANGELOG'):
    with open('%s.rst' % file_) as f:
        description += f.read() + '\n\n'


classifiers = ["Programming Language :: Python",
               "License :: OSI Approved :: Apache Software License",
               "Development Status :: 1 - Planning"]


setup(name='dogdriver',
      version='0.1',
      url='https://github.com/tarekziade/dogdriver',
      packages=find_packages(),
      long_description=description.strip(),
      description=("Performance Trends"),
      author="Tarek Ziade",
      author_email="tarek@ziade.org",
      include_package_data=True,
      zip_safe=False,
      classifiers=classifiers,
      install_requires=install_requires,
      entry_points="""
      [console_scripts]
      dogdriver = dogdriver.main:main
      dogserver = dogdriver.server:main
      """)
