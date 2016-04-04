import os
import platform
# from distutils.core import setup
from setuptools import setup, find_packages
from pygram import __version__

PLATFORM = platform.system()

CHANGE_MAKEFILE = (
    """python -c "ff=open('Makefile').read();f=open('Makefile', 'w');f.write(ff.replace(' -Werror',''));f.close()" """)



with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    LONG_DESCRIPTION = readme.read()


def getoutput(cmd):
    import subprocess
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    if p.returncode:  # if not returncode == 0
        print('WARNING: A problem occurred while running {0} (code {1})\n'
              .format(cmd, p.returncode))
        stderr_content = p.stderr.read()
        if stderr_content:
            print('{0}\n'.format(stderr_content))
        return ""
    return True

# Cloning
home_folder = os.path.expanduser('~')
print("Cloning client library...")
getoutput("rm -rf {}".format(os.path.join(home_folder, ".tg")))
result = getoutput("git clone --recursive https://github.com/vysheng/tg.git ~/.tg")

os.chdir(os.path.join(home_folder, ".tg"))

if result:
    print("Required libraries installing...")
    result = getoutput("brew install libconfig readline lua libevent jansson")

if result and PLATFORM == "Darwin":
    print("New paths exporting...")
    result = getoutput(
        'export CFLAGS="-I/usr/local/include -I/usr/local/Cellar/readline/6.3.8/include";'
        'export CPPFLAGS="-I/usr/local/opt/openssl/include";'
        'export LDFLAGS="-L/usr/local/opt/openssl/lib '
        '-L/usr/local/Cellar/readline/6.3.8/lib -L/usr/local/opt/lua/lib";'
        './configure;{};make'.format(CHANGE_MAKEFILE))

elif result:
    print("New paths exporting...")
    result = getoutput(
        'sudo apt-get install libreadline-dev libconfig-dev libssl-dev lua5.2 '
        'liblua5.2-dev libevent-dev libjansson-dev libpython-dev make;./configure;make'
    )
# if result:
#     print("Installation complete.")
#     getoutput(
#         " python -c \""
#         "ff=open('config.py').read();"
#         "ff=ff.replace('TELEGRAM_CLI_PATH = \"\"', 'TELEGRAM_CLI_PATH = \"{}/bin/telegram-cli\"');"
#         "f=open('config.py', 'w');"
#         "f.write(ff);f.close()"
#         "\" ".format(os.path.join(home_folder, ".tg"))
#     )
#
#     result = getoutput("./bin/telegram-cli server.pub")

os.chdir(home_folder)

setup(
    name='pygram',
    version=__version__,
    packages=['pygram'],
    # package_dir={'': '.'},
    package_data={
        '.': [
            '*.pub',
        ]},
    include_package_data=True,
    url='https://github.com/RedXBeard/pygram',
    license='MIT',
    author='Barbaros Yildirim',
    author_email='barbarosaliyildirim@gmail.com',
    description='Telegram messaging from your terminal.',
    long_description=LONG_DESCRIPTION,
    entry_points={
        'console_scripts': [
            'pygram = pygram.command:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Chat'
    ],
    install_requires=[
        'npyscreen',
        'DictObject',
        'pytg'
    ]
)
