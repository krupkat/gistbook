[![Deploy Jekyll site to Pages](https://github.com/krupkat/gistbook/actions/workflows/jekyll.yml/badge.svg)](https://github.com/krupkat/gistbook/actions/workflows/jekyll.yml)

# gistbook

Use this repo to set up a personal Gist dashboard hosted on Github Pages. Check out this example [gistbook](https://krupkat.github.io/gistbook/).

## Setup

Getting started is easy, you can finish everything in a few minutes from your browser:

0. Fork this repository
1. User settings -> Developer settings -> Personal access tokens -> Generate new token -> Allow Gists permission -> Generate token -> Copy
2. Repository settings -> Secrets -> Actions -> New repository secret -> Name it `GIST_TOKEN` + paste the generated token
3. Repository settings -> Pages -> Source -> Github Actions
4. Actions -> Enable workflows
5. Trigger the workflow for the first time by pushing a commit, e.g.:
    - Edit `_config.yml` -> url: https://(your_username).github.io -> Commit
6. Wait for the action to finish -> Check https://(your_username).github.io/gistbook

## Workflow

The website will be rebuilt automatically every day, you can trigger a manual rebuild from the Actions tab.

## Gist metadata

Tags are parsed from the Gist description, the following formats are supported:

1. "A nice title #tag1 #tag2"
2. "[Another nice title] #tag1 #tag2"
3. "#tag1 #tag2"

In case there is no suitable title found in the description, name of the first file will be used.

## Customization

1. Edit `.github/workflows/jekyll.yml` to include secret Gists in your dashboard:
    - `python bootstrap.py ${{ secrets.GIST_TOKEN }} --include_private`
2. Edit `_data/menu.yml` to modify homepage layout ([docs](https://github.com/riggraz/no-style-please#customize-the-menu)).
3. Edit `README.md` to include workflow badges for your Gistbook:
    - replace `krupkat` with your Github username
4. Edit `_config.yml`
    - `title`, `author`, `description`, `url`
    - for details on `theme_config` options check the [config](https://github.com/riggraz/no-style-please/blob/9011f75e2e8af5eaaff96dc8f939357d1a417deb/_config.yml) from the original theme

## Local build

### Prerequisites
- Jekyll build environment, see [docs](https://jekyllrb.com/docs/) for setup instructions. (on Windows I recommend running on [WSL](https://docs.microsoft.com/en-us/windows/wsl/install))
- Python 3 + `Jinja2`, `PyGithub` and `sanitize-filename` pip packages
- The requirements specified in `Gemfile` work on Ubuntu 22.04, you can modify the versions needed to suit your distribution

### Build

One time:

```
git clone
cd repo
bundle install
```

This will generate the files in the `_site` directory:

```
./bootstrap.py GIST_TOKEN
bundle exec jekyll serve
```

## Credit

Inspiration: https://jpmens.net/2019/04/03/backup-all-my-gists/

Theme: https://github.com/riggraz/no-style-please
