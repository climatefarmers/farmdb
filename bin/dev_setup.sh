# This will set a few shell variables we assume to be there
# You should overwrite this file locally with your own settings
# for the DB for example

export DJANGO_SECRET_KEY="SomethingReallySecret"
export TYPEFORM_SECRET="MoreSecrets"
export GOOGLE_API_KEY="YouNeedToFigureThisOut"

export PGNAME='farmdb'
export PGUSER=`whoami`
export PGPASS=''
export PGHOST='localhost'
export PGPORT=5432
