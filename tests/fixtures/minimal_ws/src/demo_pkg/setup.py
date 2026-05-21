from setuptools import setup

package_name = "demo_pkg"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Test",
    maintainer_email="test@example.com",
    description="Demo package",
    license="MIT",
    entry_points={
        "console_scripts": [
            "demo_node = demo_pkg.demo_node:main",
        ],
    },
)
