from setuptools import setup, find_packages

setup(name='wifi_berry',
    version='0.1',
    description='Automate Raspberry Pi access point setup.',
    url='https://github.com/mellow-hype/wifi-berry',
    author='Enrique Castillo',
    license='GPL',
    packages=find_packages(),
    install_requires=[
        'menu3',
        'ipaddress'
    ],
    entry_points = {
        'console_scripts': ['wifi-berry=wifi_berry.menu.main_menu:main'],
    },
    include_package_data=True,
    zip_safe=False)