#
# This script will download web2py and virtual env
# It will create a virtual environment with the makages necessary to run web2py
# And will allow you to run web2py from your home folder on shared hosts
# even if they only support 2.4 (to be tested)
#
echo 'downloading web2py'
echo '=================='
wget http://web2py.com/examples/static/web2py_src.zip
unzip web2py_src.zip
cd web2py
echo 'downloading virtualenv'
echo '======================'
wget http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.5.1.tar.gz
unzip virtualenv-1.5.1.tar.gz
tar xvf virtualenv-1.5.1.tar.gz
python virtualenv-1.5.1/virtualenv.py --distribute virtualenv
echo 'installing compatibility modules'
echo '================================'
virtualenv/bin/easy_install -U pysqlite hashlib
echo 'starting web2py'
echo '==============='
virtualenv/bin/python web2py.py
