# Account App 

Django custom app to handle account functionality such as creating users (for Authentication) and profiles (to stored additional user data)

## Description 
This application solves the problem of having to build a custom django application for account management which uses email/password as authentication factors from scratch, the codebase is constantly updated and improved to fixed known bugs and vulnerability and improve efficiency

## Usage
- Clone the repo into a local machine
- Open the Folder in any IDE of your choice (you can optionally work from the OS folder viewer)
- Add the `account_app.apps.AccountAppConfig` to your installed application in your `settings.py` file 
- Add the following lines to your project settings file `settings.py` by default
    ```
    AUTH_USER_MODEL = 'account.User' 

    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = '/' # rethink this process 
    LOGIN_URL = 'account:login-account'

    SYSTEM_ACCOUNT_EMAIL = 'email_username@domain.com'

    ```
- Make sure this line is in your account `__init__.py` file 
    ```
    default_app_config = 'account.apps.AccountConfig'

    ```
- Make sure this line is in your account `apps.py` file
    ```
    class AccountConfig(AppConfig):
        ...

        def ready(self):
            import signals

    ```
- Update the following files to match the application's version
  - `admin.py`
  - `test.py`
  - `models.py`
  - `managers.py`
  - `forms.py`
  - `signals.py`
  - `views.py`
- Customize as it fits your needs


## Maintainer
Brian Obot <brianobot9@gmail.com>