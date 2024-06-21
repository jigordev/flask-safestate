from setuptools import setup

def parse_requirements(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

setup(
    name = "flask-safestate",
    version = "0.1",
    packages = ["flask_safestate"],
    install_requires = parse_requirements("requirements.txt"),
    author = "jigordev",
    author_email = "jigordev@gmail.com",
    description = "Extension for Flask that uses the safestate library for thread-safe and async-safe state management.",
    url = "https://github.com/jigordev/flask-safestate",
)