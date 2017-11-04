from setuptools import setup, find_packages

runtime = set([
    'ansible',
    'insights-core'
    'lxml'
])

if __name__ == "__main__":
    name = "ansible_insights"

    setup(
        name=name,
        version="0.0.1",
        author_email="csams@redhat.com",
        packages=find_packages(),
        install_requires=list(runtime),
        dependency_links=[
            "git+https://github.com/RedHatInsights/insights-core.git@master#egg=insights-core-0"
        ]
    )
