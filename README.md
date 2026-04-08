# All About Wolfit

## First Things First: Python 3 and SQLite

Before you clone and try to get the sample app working, you'll need a valid Python 3 (3.8 or newer) installation ([Python downloads](https://www.python.org/downloads/)).

You will also need [uv](https://docs.astral.sh/uv/getting-started/installation/) installed for Python environment and dependency management.

Next, make sure you have a working [SQLite3](https://www.sqlite.org/) engine installed. On MacOS or Linux it is probably already installed. You should also install the [DB Browser for SQLite](https://sqlitebrowser.org/) as this will help you inspect schemas and data.

## Clone this repository to your local dev environment

Your command will look something like this:

``` sh
git clone https://github.com/wou-cs/wolfit.git
```

In addition, you probably want to connect this local repo to your own remote, detaching from the master repository.

``` sh
cd wolfit
git remote set-url origin https://new.url.here
```

## Configure your settings files

You will create two settings files, one for development and one for test. These files will provide a [Flask secret key](https://stackoverflow.com/questions/22463939/demystify-flask-app-secret-key) and a name for your development and test databases. The development database is a *sandbox* that you can use for interactive play and testing. It will retain data and allow you to interact with the app. The test database will get torn down and recreated **every time you run the test suite**.

* Create your own dev.settings and test.settings files (do not check these into Git). Start by copying the `example.settings` file.

``` sh
cp example.settings dev.settings
cp example.settings test.settings
```

* Each will contain two environment variables:

``` py
SECRET_KEY = "your generated secret key"
BLOG_DATABASE_NAME = 'wolfit_XYZ.db'
```

* [Generate your own secret key](https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask). Best practice is to *not* check secrets like this into Git, hence the reason `dev.settings` and `test.settings` are in the `.gitignore` file.
* Install the project dependencies using uv:

``` sh
uv sync
```

This will create a `.venv` virtual environment and install all required packages (including dev dependencies). You do not need to manually activate the virtual environment — the helper scripts use `uv run` to automatically run commands in the correct environment.

## Build / migrate the development database

### Automatically

We need to create the development database, which you will allow you to run the application and interact with Wolfit. The simplest way is to run the utility script:

``` sh
./create_dev_db.sh
```

### Manually

You can also do this manually. First, we need to tell the Wolfit app which one to use before we setup the database. This variable is set automatically when you run `rundev.sh`, `runtests.sh`, and `cov.sh`. We need to set it manually now for the following steps:

``` sh
export WOLFIT_SETTINGS=$(pwd)/dev.settings
```

Now run the database upgrade, which will create

``` sh
uv run flask db upgrade
```

You should see all of the migrations being applied to your development database. Ignore any "unsupported ALTER" warnings: we are using a non-production quality database (SQLite) that doesn't support the full SQL language.

## Run tests

The easiest way to run all the tests is with the helper script:

``` sh
./runtests.sh
```

Note that the script will pass parameters to `pytest`, allowing you to filter tests that you run while you work on test coverage improvement. For example, if you were working on testing pagination and links to more posts, you might run:

``` sh
./runtests.sh -k post_limit
```

The `-k` option will do a regular expression match on test case names.

## Run dev server (local web server)

``` sh
./rundev.sh
```

## Test Coverage

To look at test coverage, simply run:

``` sh
./cov.sh
```

### If you are on WSL...

The final line in the `cov.sh` scripts "opens" the generated web page. You can just browse to the generated `htmlcov/index.html` file in Explorer and open it from there in your browser. Or, with a little more work you can probably get it to work natively. Install the WSL utilities package:

``` sh
sudo apt install wslu
```

Then run `cov.sh`.

## Load up some sample posts

You can populate the app with randomly generated sample posts using the `sample_data load` command. No external API keys are needed.

``` sh
./load_sample_data.sh
```

You can optionally give the name of a subreddit (category) and a count. By default the script generates 100 posts under `learnpython`. This example generates 50 posts under `computerscience`:

``` sh
./load_sample_data.sh computerscience 50
```
