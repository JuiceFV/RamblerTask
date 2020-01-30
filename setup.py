from setuptools import setup, find_packages

setup(
    name="Kitty Getter",
    version="1.0",
    description="The Queue Management System which shows kitties images according queue order.",
    author="Aleksandr Kasian",
    author_email="aleksandr.juicefv@gmail.com",
    packages=find_packages(),
    zip_safe=True,
    entry_points={
        'console_scripts':
            ['start_app = entry.py']
    },
    install_requires=[
        'aiohttp==3.6.2',
        'aiohttp-jinja2==1.2.0',
        'aiohttp-session==2.9.0',
        'async-timeout==3.0.1',
        'asyncpg==0.20.1',
        'asyncpgsa==0.26.1',
        'attrs==19.3.0',
        'cchardet==2.1.5',
        'cffi==1.13.2',
        'chardet==3.0.4',
        'cryptography==2.8',
        'idna==2.8',
        'Jinja2==2.11.0',
        'MarkupSafe==1.1.1',
        'multidict==4.7.4',
        'pycparser==2.19',
        'PyYAML==5.3',
        'six==1.14.0',
        'SQLAlchemy==1.3.13',
        'yarl==1.4.2'
    ]
)
