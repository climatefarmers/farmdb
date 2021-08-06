# FarmDB
FarmDB is Climate Farmers internal database system for connecting farms, consultants, practices, modelled scenarios and metrics


## Join our Open Source Community on Slack

We currently have more than 60 members on slack helping with a range of tasks from soil science research and prototyping remote sensing applications to marketing and finance.   
Please fill out this [survey](https://bitqcerk9h5.typeform.com/to/v3xC63oT) and tell us a bit about your motivation and skills to be invited. 

## Contributing to this repository

Please start by having a look at our [CONTRIBUTING.md](https://github.com/climatefarmers/farmdb/blob/main/CONTRIBUTING.md), especially the conventions around Git Branching that we aim to adhere to. 

### What you can do here:

- **Fixing open issues:**  Have a look at the open issues listed in this repository to get an idea of what tasks we might need help with.  
- **Help with documentation:** You don't necessarily need to be a programmer to contribute to open source software: documentations like this one might need to be corrected for typos and clarity. If you spot something, follow the steps below to introduce an update.  
- **Spot vulnerabilities and improvements:** Lastly we're always grateful for people who bring to our attention issues and possible improvements that people find within our code. Please have a look at our Issues and create a new one if warranted. And if you can, maybe even submit a fix!


**If you're new to git and github, have a look at the following resources:**  
- [Towards Data Science: Getting started with git and github](https://towardsdatascience.com/getting-started-with-git-and-github-6fcd0f2d4ac6)
- [YouTube: Git & GitHub Crash Course (32mins)](https://www.youtube.com/watch?v=SWYqp7iY_Tc)

**How to contribute?**  
- Create a personal fork of this repository.
- Clone the fork on your local machine. Your remote repo on Github is called `origin`.
- Add the original repository as a remote called `upstream`.
- If you created your fork a while ago be sure to pull upstream changes into your local repository.
- Create a new branch to work on! Branch from `develop` if it exists, else from `main`.
- Implement/fix your feature, comment your code.
- Follow the code style of the project, including indentation.
- If the project has tests run them!
- Write or adapt tests as needed.
- Add or change the documentation as needed.
- Squash your commits into a single commit with git's [interactive rebase](https://help.github.com/articles/interactive-rebase). Create a new branch if necessary.
- Push your branch to your fork on Github, the remote `origin`.
- From your fork open a pull request in the correct branch. Target the project's `develop` branch if there is one, else go for `main`!
- If the maintainer requests further changes just push them to your branch. The PR will be updated automatically.
- Once the pull request is approved and merged you can pull the changes from `upstream` to your local repo and delete
your extra branch(es).

This list is adapted from the following [guide](https://github.com/MarcDiethelm/contributing)

## Quickstart for local development and testing

The following steps should set up a functional local version of all current FarmDB components where you can easily develop and test new features before submitting them as PRs.

Prerequisites: 
- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)

1) First you need to clone this git repo.
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