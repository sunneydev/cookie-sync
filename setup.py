from setuptools import setup


setup(
    name='cookie-sync',
    version='0.0.1',
    description='Sync cookies between Chrome',
    author='Sunney-X',
    author_email='sunneyxdev@gmail.com',
    url='https://github.com/Sunney-X/cookie-sync',
    packages=['cookie_sync'],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "aiohttp"
    ],
)
