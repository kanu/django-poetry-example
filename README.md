# Django setup with poetry and pytest

## Installing poetry

Install poetry with the install-poetry.py script or with pip. Read the [documentation](https://python-poetry.org/docs/#installation) about the pros/cons of each method.


## Creating a poetry project

You can create a new project by using the `poetry new` command.
```shell
poetry new django-poetry-example
```
The project will have the following structure.
```
django-poetry-example
├── README.rst
├── django_poetry_example
│   └── __init__.py
├── pyproject.toml
└── tests
    ├── __init__.py
    └── test_django_poetry_example.py
```
Poetry uses a `pyproject.toml` to configure the package.
It stores the meta data, dependencies and configurations of the package.


## Adding/changing dependencies
When you get into the project folder you can start using the poetry command for several tasks such as managing dependencies, running scripts or building the package.


```shell
cd django-poetry-example
```

I had to update poetry's pytest version from the default to avoid a TypeError with python 3.10.

```shell
poetry add pytest^7.1
```

## Creating a django project
Install django
```
poetry add django^4.0
```

After installing django you can use django-admin to create the project. 
Be aware that you have to either enter the projects shell or use the poetry run command to use
this instance of django.

```shell
poetry shell
cd django_poetry_example
django-admin startproject project .
```
or
```shell
poetry run django-admin startproject project ./django_poetry_example/
```

This will add the project named "project" inside the django_poetry_example directory.
```
django-poetry-example
├── README.rst
├── django_poetry_example
│   ├── __init__.py
│   ├── manage.py
│   └── project
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── poetry.lock
├── pyproject.toml
└── tests
    ├── __init__.py
    └── test_django_poetry_example.py
```
I prefer the generic name "project" because I find it easier to find when there are tons of django apps around.
I also prefer to have the django code in a subdirectory and not mixed with other stuff that is in the poetry root folder.

The downside of the extra directory is that manage.py is not in the root level. You also have to point pytest to the correct directory.
Finally editors like pycharm need a hint too for auto-importing modules.


### Creating a manage.py for the root folder
```
cp django_poetry_example/manage.py .
```
Alter the new manage.py to change the working directory before running any subcommand.
```python
root = os.path.join(os.getcwd(), "django_poetry_example")
sys.path.insert(0, root)
os.chdir(root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
```

### Configuring pytest to set the working directory

You can configure pytest in the `tool.pytest.ini_options` section of the pyproject.toml file.
```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "django_poetry_example.project.settings"
pythonpath = "django_poetry_example"
```

### Configuring PyCharm
If you are using pycharm you should mark the `django_poetry_example` directory as "Sources" in the  "Project Structure" configuration.
![Screenshot 2022-05-30 at 15 02 27](https://user-images.githubusercontent.com/738398/171011436-81aa4e02-302f-463b-8027-eb2e8a97f76c.png)

## Adding scripts as shortcut for management commands
You can assign python functions to commands which can be called in the shell directly or outside the shell with `poetry run`

```toml
[tool.poetry.scripts]
server = "scripts:run_server"
shell = "scripts:shell_plus"
manage = "scripts:manage"
```
After updating the local installation with `poetry install` the command `server` would call the run_server function from the scripts.py file.


# Settings up pytest 

To use pytest with django install the [pytest-django](https://pypi.org/project/pytest-django/) package as development dependency. 
It offers some usefull fixtures like `rf`, `client`, `db`
```
poetry add -D pytest-django
```

## Structuring tests

Although django creates a test.py file for every app I prefer to keep tests inside the test directory.
So a django project containing two apps `pizza` and `restaurant` would look like this.
```
django-poetry-example
├── README.rst
├── django_poetry_example
│   ├── __init__.py
│   ├── manage.py
│   ├── pizza
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   └── views.py
│   ├── project
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── restaurant
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       │   ├── 0001_initial.py
│       │   └── __init__.py
│       ├── models.py
│       └── views.py
├── manage.py
├── poetry.lock
├── pyproject.toml
├── scripts.py
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── pizza
    │   ├── fixtures.py
    │   └── test_pizza.py
    ├── restaurant
    │   ├── fixtures.py
    │   └── test_restaurants.py
    └── test_django_poetry_example.py
```
Usually you put fixtures in a conftest.py file next to the tests files. Those fixtures are only available in that folder and below. 
So to avoid declaring all fixtures that might be used in multiple apps in the roots conftest.py I define common fixtures like
model factories in a separate `fixtures.py` file. You have to add those files to the roots conftest.py to have them always accessible.

```python
pytest_plugins = ("tests.pizza.fixtures", "tests.restaurant.fixtures")
```
