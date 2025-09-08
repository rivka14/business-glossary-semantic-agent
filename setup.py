"""Setup configuration for BigQuery Metrics AppsFlyer AI Agent."""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="bigquery-metrics-appsflyer-ai-agent",
    version="1.0.0",
    author="BigQuery Metrics AppsFlyer AI Agent Team",
    author_email="",
    description="AI-powered analytics agent for AppsFlyer marketing data in BigQuery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rivka14/bigquery-metrics-appsflyer-ai-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    keywords=[
        "bigquery",
        "appsflyer", 
        "ai-agent",
        "analytics",
        "mobile-marketing",
        "sql-generation",
        "natural-language",
        "data-analysis",
        "metrics",
        "roas",
        "retention",
        "mobile-attribution"
    ],
    project_urls={
        "Bug Reports": "https://github.com/rivka14/bigquery-metrics-appsflyer-ai-agent/issues",
        "Source": "https://github.com/rivka14/bigquery-metrics-appsflyer-ai-agent",
        "Documentation": "https://github.com/rivka14/bigquery-metrics-appsflyer-ai-agent/blob/main/README.md",
    },
)