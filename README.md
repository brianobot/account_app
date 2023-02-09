# Account App 

Django custom app to handle account functionality in a Django Web Application such as creating users (for Authentication/Authorization) and user-profiles (to stored additional user data and configurations).

## Description 
This application solves the overhead of having to build a custom django application for account management which uses email/password as authentication factors from scratch, the codebase is constantly updated and improved to fixed known bugs and vulnerability and improve efficiency.

## Features
- ✔ Uses Email for User Authentication
- ✔ Provides Profile Model which extends the User model to store non-authentication related data
- ✔ Provides Support Both Vanilla Django (Template system) and Django RestFramework (Rest API)

## Installation and Setup
1. Clone the repo into a local machine:
    ```git
    git clone https://github.com/brianobot/account_app.git
    ``` 
2. Rename the repo directory to `accounts` and move into your Django project base directory (same level as manage.py)
    ```git
    mv accounts_app accounts
    ```
3. Open the Folder (Containing your Django Project) in any IDE of your choice (you can optionally work from Your File Explorer view)
4. Add the `accounts.apps.AccountAppConfig` to your list of installed application in your `settings.py` file 
5. Add the following lines to your project's settings (`settings.py`)
    ```python
    AUTH_USER_MODEL = 'accounts.User' 

    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = '/' # rethink this process 
    LOGIN_URL = 'accounts:login-account'
    ```
6. Make sure this line is in your accounts `__init__.py` file 
    ```python
    default_app_config = 'accounts.apps.AccountsConfig'
    ```
7. Make sure this line is in your accounts `apps.py` file
    ```python
    class AccountConfig(AppConfig):
        ...

        def ready(self):
            import signals
    ```
8. All the following url paths to your project's main url file
    ```python
    urlpatterns = [
        ...
        path('account/', include('accounts.api.urls'))
        path('account/', include('accounts.page.urls'))
        ...
    ]
    ```
    
Customize as it fits your needs

## Api Endpoints
The API has the following endpoints for authentication
   - `accounts/api/v1/api-token-auth/`:  Endpoint for obtaining tokens
   - `accounts/api/v1/signup/` : Endpoint for Creating a user instance in the system
   - `accounts/api/v1/login/`  : Endpoint for Authenicating a user, returns auth token
   - `accounts/api/v1/users/`  : List all the user currently registered on the system


## Contribution
If you come across a piece of code that could benefit from an improvement, document process and reason for improvement,
and create a pull request to the original repository


## Maintainer
Brian Obot <brianobot9@gmail.com>