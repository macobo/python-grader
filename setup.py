from setuptools import setup

setup(
    name = 'grader',
    packages=['grader'],
    version='0.0.1',
    description='Python grader',
    author='Karl-Aksel Puulmann',
    author_email='oxymaccy@gmail.com',
    install_requires= ["six"],
    dependency_links= [
        'http://github.com/macobo/macropy/tarball/master'
    ]
)