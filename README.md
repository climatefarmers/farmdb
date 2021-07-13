# farmdb
FarmDB is Climate Farmers internal database system for connecting farms, consultants, practices, modelled scenarios and metrics

## How to run
1) First you need to clone the git repo.
1) You will need `python3` and `pipenv` which is normally supplied by your operating system
1) As we are using python 3.8 you might need to install pyenv if you are using
   a newer (or older) version.  https://github.com/pyenv/pyenv

1) If you are planing on developing for farmdb you need to install all the packages with:
   ```
   $ pipenv install --system --dev --ignore-pipfile
   ```

   Don't forget to enable the env with:
   ```
   $ pipenv shell
   ```

1) You will need to install postgis (https://wiki.openstreetmap.org/wiki/PostGIS/Installation) which is an extension of postgresql

1) Please edit the `bin/dev_setup.sh` file accordingly to your setup
   
   Then import it into your local shell

   ```
   $ source bin/dev_setup.sh
   ```

1) Then you need to create the `farmdb` database with
   ```
   createdb farmdb
   ```

1) Now that you have all the DB setup you can migrate with
   ```
   $ ./src/manage.py migrate
   ```

1) And you can finally run the server with 
   ```
   ./src/manage.py runserver
   ```

   You might want to create a user first with 
   ```
   ./src/manage.py createsuperuser
   ```


