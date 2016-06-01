from setuptools import find_packages, setup



setup(
    name="jump-map-list",
    packages=find_packages() + ["twisted.plugins"],
    install_requires=[
        "twisted",
        "axiom",
        "txspinneret >= 0.1.2",
        "service_identity >= 14.0.0",
        "python-openid"
    ]
)
