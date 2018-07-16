from setuptools import setup

setup(
    name='ictv-plugin-sncb',
    version='0.1',
    packages=['ictv.plugins.sncb', 'ictv.renderer'],
    package_dir={'ictv': 'ictv'},
    url='https://github.com/OpenWeek/ictv-plugin-sncb',
    license='AGPL-3.0',
    author='OpenWeek members',
    author_email='',
    description='A plugin that brings the real-time information provided by SNCB/NMBS to ICTV',
    install_requires=['requests'],
    include_package_data=True,
)
