from setuptools import setup, find_packages

setup(
    name='PyBH',                # Nom de votre package
    version='1.0.0',            # Version de votre package
    packages=find_packages(),   # Trouver tous les packages dans le répertoire
    install_requires=[          # Liste des dépendances
        'matplotlib',
        'pandas',
        'numpy',
    ],
    description='Votre module qui dépend de Matplotlib et Pandas',
    long_description=open('README.md').read(),  # Description longue provenant de README.md
    long_description_content_type='text/markdown',
    author='Achour Margoum',
    author_email='margoumachour@gmail.com',
    url='https://github.com/MrgAch',  # Lien vers mon compte GitHub
    classifiers=[                      # Classificateurs PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',            # Version minimale de Python requise
)