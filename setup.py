from setuptools import setup

setup(
    name="weightlifting_tracker",
    version="0.0.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-login",
        "flask-bcrypt",
        "flask-wtf",
        "email-validator",
        "gunicorn",
    ],
)