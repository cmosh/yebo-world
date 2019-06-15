# Yebo World

Use MS SQL on aws lambda with pyodbc

## Steps to achieve this

- Deploy MS SQL with cloudformation template in the templates folder with the following command

```sh 
aws cloudformation create-stack --stack-name rancher-lb-stack --template-body file:///path/to/repo/templates/ms_sql_db.yml
```

- Then run the sql scripts in the sql folder, schema.sql then seed.sql on the newly created instance
- After installing zappa, `zappa deploy dev` -- or whichever environment you choose
- Set environment variables as shown in .env.example, they are as follows:
    ```env
    DB_SERVER=localhost
    DB_PORT=1433
    DB_NAME=yebo
    DB_USER=sa
    DB_PASS=secret
    ```
- Then upload layers/pyodbc-layer.zip as an aws lambder layer
- Because zappa doesn't support lambda layers as of yet, manually add the layer on the AWS lambda console 
- Perform a GET request and be greeted by hello world with different hellos'

## Contents of zip folder/lambda layer

- A lambda layer makes the most sense for the MS SQL binaries so that they may be reused. 
- pyodbc-layer.zip was generated with the following

```sh

# use https://github.com/lambci/docker-lambda is a validated lambda environment
docker run -it --rm --entrypoint bash -e ODBCINI=/opt/odbc.ini -e ODBCSYSINI=/opt/ -v $PWD:/src -w /src lambci/lambda:build-python3.7

# download and ompile unixODBC
curl ftp://ftp.unixodbc.org/pub/unixODBC/unixODBC-2.3.7.tar.gz -O
tar xzvf unixODBC-2.3.7.tar.gz
cd unixODBC-2.3.7
./configure --sysconfdir=/opt --disable-gui --disable-drivers --enable-iconv --with-iconv-char-enc=UTF8 --with-iconv-ucode-enc=UTF16LE --prefix=/opt
make
make install

# download and install ODBC driver for MSSQL 17 (https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017)
curl https://packages.microsoft.com/config/rhel/6/prod.repo > /etc/yum.repos.d/mssql-release.repo # RHEL 6 (AWS Lambda runs on RHEL 6)
yum install e2fsprogs.x86_64 0:1.43.5-2.43.amzn1 fuse-libs.x86_64 0:2.9.4-1.18.amzn1 libss.x86_64 0:1.43.5-2.43.amzn1
yum install msodbcsql17 --disablerepo=amzn* # Make sure to accept the eula
export CFLAGS="-I/opt/include"
export LDFLAGS="-L/opt/lib"

cd /opt
cp -r /opt/microsoft/msodbcsql17/ .
rm -rf /opt/microsoft/

# install pyodbc for use with python.
mkdir /opt/python/
cd /opt/python/
pip install pyodbc -t .

cd /opt
cat <<EOF > odbcinst.ini
[ODBC Driver 17 for SQL Server]
Description=Microsoft ODBC Driver 17 for SQL Server
Driver=/opt/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1
UsageCount=1
EOF

cat <<EOF > odbc.ini
[ODBC Driver 17 for SQL Server]
Driver = ODBC Driver 17 for SQL Server
Description = My ODBC Driver 17 for SQL Server
Trace = No
EOF

# package the content in a zip file to use as a lambda layer
zip -r9 /src/pyodbc-layer.zip .

# Voila lambda layer available in your working folder after exiting the image
# Refrence: https://medium.com/faun/aws-lambda-microsoft-sql-server-how-to-66c5f9d275ed 
# Used python 3.7 and MSSQL 17 driver instead and as a lambda layer
```
