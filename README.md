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

## Load up some sample posts from Reddit

A great way to load up content into this Reddit clone is to copy some submissions from Reddit to your local sandbox. I've created a custom flask command (`sample_data load`), but in order to run it you'll need to configure the PRAW API with a praw.ini file. Create such a file in the root of your project, and add these entries:

``` ini
[DEFAULT]
client_id=<your client ID>
client_secret=<your secret>
user_agent=python:edu.wou.<your user ID at WOU>
```

You will get your ID and secret by [creating an app under your Reddit profile](https://www.reddit.com/prefs/apps).

Follow these steps:

1. Click the "create app" at the bottom of the [Reddit apps page](https://www.reddit.com/prefs/apps).
2. Give it a name you will recognize, such as "Load posts for Wolfit".
3. Select the script option.
4. Fill in this for the redirect API: `http://www.example.com/unused/redirect/uri`
5. Client the "create app" button.
6. Under your app name you will see a client ID that looks something like this: `R2jyWgoETNkBfQ`
7. You will also see your secret shown. Copy both the client ID and the secret into your praw.ini file.

Then you can load up some sample posts by running the following shell script:

``` sh
export WOLFIT_SETTINGS=$(pwd)/dev.settings
uv run flask sample_data load
```

You can optionally give the name of a subreddit as parameter to the `load` command. By default the script will load from [`/r/learnpython`](https://www.reddit.com/r/learnpython/). This example will load recent posts from the `computerscience` subreddit:

``` sh
export WOLFIT_SETTINGS=$(pwd)/dev.settings
uv run flask sample_data load -s computerscience
```
