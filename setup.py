from setuptools import setup, find_packages
import codecs

with codecs.open('bladoxy/README.md', encoding='utf-8') as f:
    long_description = f.read()


def parse_requirements(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        return [line for line in lines if line.strip() and not line.strip().startswith('#')]

setup(
    name="bladoxy",
    version="1.4.3",
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description="Bladoxy is a linux network assistant.",
    author='Magicum Sidus',
    author_email='M.S@MS.com',
    url='https://github.com/magicum-sidus/Bladoxy',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'bladoxy': ['README.md', 'LICENSE', 'modules/dependeencies/**/*', 'modules/dependeencies_src/**/*','modules/privoxy/**/*'],  
    },
    # install_requires=[
    #     # Add any other dependencies your package requires
    # ],
    install_requires=parse_requirements('bladoxy/requirements.txt'),
    entry_points="""
    [console_scripts]
    bladoxy = bladoxy.cli.cli_app:main
    sslocal = bladoxy.modules.shadowsocks_module.shadowsocks.local:main
    ssserver = bladoxy.modules.shadowsocks_module.shadowsocks.server:main
    """,           # sslocal/ssserver我不希望暴露给用户
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Proxy Servers'
    ],
    python_requires='>=3.5, <3.10',
    long_description=long_description,
    long_description_content_type='text/markdown'
)

