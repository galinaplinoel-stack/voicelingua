from setuptools import setup, find_packages

setup(
    name="voicelingua",
    version="1.0.0",
    description="AI-powered voice translator — translate and speak in 14+ languages",
    author="VoiceLingua Team",
    packages=find_packages(exclude=["tests", "api", "web", "data"]),
    python_requires=">=3.10",
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
