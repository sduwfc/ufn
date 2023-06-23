from setuptools import setup, find_packages

setup(
    name='ufn',
    version='0.1.1',
    packages=find_packages(),
    description='upload for nas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='kilmu',
    author_email='mail@wfc.im',
    url='https://github.com/sduwfc/ufn',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
