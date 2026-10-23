"""Sample code with intentional bugs, security vulnerabilities, and style issues for testing Local CodeReview AI."""

import os
import subprocess
from hashlib import md5

# Hardcoded secret (Security issue)
api_key = "sk-1234567890abcdef1234567890abcdef"
DEBUG = True


def calculate_total(price, tax):
    # Missing docstring and type hints
    total = price + (price * tax)
    print("Total price calculated:", total)  # Using print instead of logger
    return total


def run_user_command(user_input):
    # Command injection vulnerability (Critical)
    cmd = "echo " + user_input
    return subprocess.check_output(cmd, shell=True)


def execute_dynamic_code(code_str):
    # Code injection via eval (Critical)
    return eval(code_str)


def hash_password(password):
    # Weak cryptography (MD5)
    return md5(password.encode()).hexdigest()


def read_data(filepath):
    # Bare except clause (Style issue)
    try:
        with open(filepath, "r") as f:
            return f.read()
    except:
        return None
