### Basic install.

Assumes working in a virtualenv. If not, setup.py needs root access.

```bash
git clone https://github.com/macobo/python-grader.git
cd python-grader

python setup.py install

python run_tests.py
```

### Installing python from source and create virtualenv.

Not required.

```bash
hg clone http://hg.python.org/cpython
cd cpython
hg checkout 3.3
./configure  && make -j3
# so we don't overwrite python executable
sudo make altinstall

virtualenv -p /usr/local/bin/python3.3 ~/py33env
source ~/py33env/bin/activate
```