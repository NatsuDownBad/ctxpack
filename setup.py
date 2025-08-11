from setuptools import setup, find_packages

setup(
    name="ctxpack",
    version="0.1.0",
    description="Context window compression and management",
    author="chu2bard",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "tiktoken>=0.5",
        "openai>=1.0",
        "pydantic>=2.0",
    ],
)
