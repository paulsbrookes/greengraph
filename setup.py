from setuptools import setup, find_packages

setup(
    name = "Greengraph",
    version = "1.0 ",
    packages = find_packages(exclude=['*test']),
    license = "Apache",
    author_email = 'paul.s.brookes@gmail.com',
    install_requires = ['geopy','numpy','matplotlib','requests','nose'],
    scripts = ['scripts/greengraph']
)
