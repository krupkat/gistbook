#!/usr/bin/python

import argparse
import collections
import datetime
import github
import jinja2
import re
import sanitize_filename

Gist = collections.namedtuple("Gist", ["id", "login", "title", "tags", "updated"])

TITLE_RE_1 = re.compile(r"^\[(.+)\]")
TITLE_RE_2 = re.compile(r"^(.*?)#")
TAG_RE = re.compile(r"#(\S+)")


def ParseTitle(gist):
    title_match = re.search(TITLE_RE_1, gist.description)
    if not title_match:
        title_match = re.search(TITLE_RE_2, gist.description)

    if title_match:
        title = title_match.group(1).strip()
    else:
        title = gist.description

    if not title:
        title = min(gist.files.keys())
    return title


def ParseTags(gist):
    return re.findall(TAG_RE, gist.description)


def FromUtc(date):
    utc = datetime.timezone.utc
    return date.replace(tzinfo=utc).astimezone()


def GetGists(git, include_private):
    git_user = git.get_user()
    for gist in git_user.get_gists():
        if gist.public or include_private:
            yield Gist(
                gist.id,
                git_user.login,
                ParseTitle(gist),
                ParseTags(gist),
                FromUtc(gist.updated_at),
            )


def WriteGist(gist, env):
    template = env.get_template("gist.txt")
    filename = "_posts/{}-{}.md".format(gist.updated.strftime("%Y-%m-%d"), gist.id)
    with open(filename, "w") as file:
        file.write(template.render(gist=gist))


def WriteTag(tag, env):
    template = env.get_template("tag.txt")
    filename = "_tags/{}.md".format(sanitize_filename.sanitize(tag))
    with open(filename, "w") as file:
        file.write(template.render(tag=tag))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gist bootstrap")
    parser.add_argument("secret", help="Github token with Gist permissions")
    parser.add_argument(
        "--include_private", action="store_true", help="Include private Gists"
    )
    args = parser.parse_args()
    env = jinja2.Environment(
        loader=jinja2.PackageLoader("bootstrap"), autoescape=jinja2.select_autoescape()
    )

    tags = set()
    git = github.Github(args.secret)
    for gist in GetGists(git, args.include_private):
        tags.update(gist.tags)
        WriteGist(gist, env)

    for tag in tags:
        WriteTag(tag, env)
