import os
import platform

CHANGE_MAKEFILE = (
    """python -c "ff=open('Makefile').read();f=open('Makefile', 'w');f.write(ff.replace(' -Werror',''));f.close()" """)

PLATFORM = platform.system()


def getoutput(cmd):
    import subprocess
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    if p.returncode:
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

if result and PLATFORM == "Darwin":
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

os.chdir(home_folder)
