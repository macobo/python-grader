hg clone http://hg.python.org/cpython
cd cpython
hg checkout 3.3
./configure  && make -j3
# so we don't overwrite python executable
sudo make altinstall

cd ~
virtualenv -p /usr/local/bin/python3.3 py33env
source py33env/bin/activate

git clone https://github.com/macobo/macropy.git
cd macropy
pip install six
python setup.py install

cd ..
git clone https://github.com/macobo/python-grader.git
cd python-grader
python setup.py install

python run_tests.py