from setuptools import setup, find_packages

setup(
    name="autoagent-oss",
    version="0.1.0",
    description="Natural language task automation powered by OpenAI",
    author="guotongyu227-bot",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "openai>=1.0.0",
        "requests>=2.28.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
