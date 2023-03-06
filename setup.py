from setuptools import setup, find_packages

setup(
    name='GPT-prompts',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[line for line in open('requirements.txt')],
    entry_points={
        'console_scripts': [
            'GPT = gpt_prompts:main',
        ],
    },
)

