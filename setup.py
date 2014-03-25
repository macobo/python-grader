from setuptools import setup

setup(
    name='grader',
    packages=['grader'],
    data_files=[('sandbox', [
        'sandbox/run_test',
        'sandbox/run_tests_docker_sandbox'
    ])],
    version='0.0.1',
    description='Python grader',
    author='Karl-Aksel Puulmann',
    author_email='oxymaccy@gmail.com'
)
