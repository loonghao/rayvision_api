"""Provides paths related functions."""

# Import built-in modules
import os


def package_root():
    return os.path.join(os.path.dirname(__file__))


def get_schema_file(name):
    root = package_root()
    return os.path.join(root, "schemas", "{}.yaml".format(name))
