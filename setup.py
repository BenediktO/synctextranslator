import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synctextranslator",
    version="0.0.1",
    author="Benedikt Otto",
    author_email="benedikt_o@web.de",
    description="translator of synctex linenumbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenediktO/synctextranslator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'synctextranslator=translator.translator:main'
        ],
	}
)