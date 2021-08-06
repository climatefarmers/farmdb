# farmdb
FarmDB is Climate Farmers internal database system for connecting farms, consultants, practices, modelled scenarios and metrics

## For local development and testing

Prerequisites: 
- docker
- docker-compose

1) First you need to clone the git repo.
2) create a .env.dev file to manage environment variables. The following list contains defaults for local development. Chose your own secrets. The .env.dev file is ignored by git and should remain so. Next you find the needed environment variables listed:

    **Development settings**:
    - PGNAME=farmdb
    - PGUSER=your_postgres_user
    - PGPASS=your_postgres_password
    - PGHOST=db
    - PGPORT=5432
    - DEBUG=true
    - DJANGO_SECRET_KEY=your_django_secret
    - ADDRESS_SERVICE_ENDPOINT=http://address:8080/parse/
    - MONITORING_SVC_URL=http://monitoring:5000


    Optional, for the address widget in the django admin panel:
    - GOOGLE_API_KEY=your_google_api_key_with_maps_api_activated

3) Start all services using  
`docker-compose --env-file .env.dev up`
4) Perform initial migrations by running:  
`docker-compose exec web python manage.py makemigrations`  
`docker-compose exec web python manage.py migrate`

4) Configure a django admin user by running  
`docker-compose exec web python manage.py createsuperuser`

5) Navigate to `localhost:8000` in your browser and use your credentials to login  
Other routes:  
/admin - the django admin panel  
/api - the django rest framework documentation


For now your local dev environment will not contain any farms to work with. You can add some manually in the admin panel. 

The "real" farmdb is cloud hosted with protected access. 

## Contributing

Climate Farmers has a large community of Open Source contributors that are currently coordinating via slack: climatefarmer-djr8071.slack.com

### Get started:
Have a look at the open issues listed in this repository to get an idea of what tasks we might need help with. 
If you find typos or points that you believe could be clearer in this documentation you could also submit your updates. 
Lastly we're always grateful for people who bring to our attention issues and possible improvements that you found within our code. 