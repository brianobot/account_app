# Account App 

Django custom app to handle account functionality in a Django Web Application such as creating users (for Authentication/Authorization) and user-profiles (to stored additional user data and configurations).

## Description 
This application solves the overhead of having to build a custom django application for account management which uses email/password as authentication factors from scratch, the codebase is constantly updated and improved to fixed known bugs and vulnerability and improve efficiency.

## Installation and Setup
- Clone the repo into a local machine 
- Rename the repo directory to `accounts` and move into your Django project base directory (same level as manage.py)
- Open the Folder (Containing your Django Project) in any IDE of your choice (you can optionally work from Your File Explorer view)
- Add the `accounts.apps.AccountAppConfig` to your installed application in your `settings.py` file 
- Add the following lines to your project's settings (`settings.py`)
    ```
    AUTH_USER_MODEL = 'accounts.User' 

    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = '/' # rethink this process 
    LOGIN_URL = 'accounts:login-account'

    SYSTEM_ACCOUNT_EMAIL = 'email_username@domain.com'
    ```
- Make sure this line is in your accounts `__init__.py` file 
    ```
    default_app_config = 'accounts.apps.AccountsConfig'
    ```
- Make sure this line is in your accounts `apps.py` file
    ```
    class AccountConfig(AppConfig):
        ...

        def ready(self):
            import signals
    ```
- Customize as it fits your needs


## Contribution
If you come across a piece of code that could benefit from an improvement, document process and reason for improvement,
and create a pull request to the original repository


## Maintainer
Brian Obot <brianobot9@gmail.com>