from setuptools import setup

package_name = 'rqt_bag_diagnostics_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=['rqt_bag_diagnostics_demo'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['plugins.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='David V. Lu!!',
    maintainer_email='davidvlu@gmail.com',
    description='Demo rqt_bag plugin for diagnostics_msgs',
    license='BSD',
)
