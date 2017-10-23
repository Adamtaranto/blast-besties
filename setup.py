from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

pypi_classifiers = [
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Operating System :: OS Independent",
    'Intended Audience :: Science/Research',
    'Natural Language :: English',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    "Topic :: Software Development :: Libraries :: Python Modules",
    'License :: OSI Approved :: MIT License',
]

desc = """Rapid discovery of reciprocal best blast pairs from BLAST output files."""

setup(name='blastbesties',
      version='1.1.1',
      description=desc,
      long_description=readme(),
      url='https://github.com/Adamtaranto/blast-besties',
      author='Adam Taranto',
      author_email='adam.taranto@anu.edu.au',
      license='MIT',
      packages=['blastbesties'],
      classifiers=pypi_classifiers,
      keywords=["Orthologues", "Reciprocal best BLAST"],
      include_package_data=True,
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'blastbesties=blastbesties.cmd_rbb:main',
        ],
    },
    )



