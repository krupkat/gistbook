#!/usr/bin/python

import argparse
import collections
import datetime
import github
import re
import sanitize_filename

Gist = collections.namedtuple("Gist", ["id", "title", "tags", "updated", "embed"])

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


def EmbedGist(username, id):
    return "{{% gist {}/{} %}}".format(username, id)


def FromUtc(date):
    utc = datetime.timezone.utc
    return date.replace(tzinfo=utc).astimezone()


def GetGists(git, include_private):
    git_user = git.get_user()
    for gist in git_user.get_gists():
        if gist.public or include_private:
            title = ParseTitle(gist)
            tags = ParseTags(gist)
            yield Gist(
                gist.id,
                title,
                tags,
                FromUtc(gist.updated_at),
                EmbedGist(git_user.login, gist.id),
            )


def WritePost(gist):
    with open(
        "_posts/{}-{}.md".format(gist.updated.strftime("%Y-%m-%d"), gist.id), "w"
    ) as file:
        file.write("---\n")
        file.write("layout: post\n")
        file.write("title: {}\n".format(gist.title))
        file.write("category: gist\n")
        file.write("permalink: /gist/{}\n".format(gist.id))
        file.write("date: {}\n".format(gist.updated.strftime("%Y-%m-%d %H:%M:%S %z")))
        if gist.tags:
            file.write("tags:\n")
            for tag in gist.tags:
                file.write("  - {}\n".format(tag))
        file.write("---\n")
        file.write("\n")
        file.write(gist.embed)
        file.write("\n")


def WriteTag(tag):
    filename = sanitize_filename.sanitize(tag)
    with open("_tags/{}.md".format(filename), "w") as file:
        file.write("---\n")
        file.write("layout: tags\n")
        file.write("tag-name: {}\n".format(tag))
        file.write("title: {}\n".format(tag))
        file.write("---\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gist bootstrap")
    parser.add_argument(
        "secret",
        help="Github token with Gist permissions"
    )
    parser.add_argument(
        "--include_private", action="store_true", help="Include private Gists"
    )
    args = parser.parse_args()

    tags = set()

    git = github.Github(args.secret)
    for gist in GetGists(git, args.include_private):
        tags.update(gist.tags)
        WritePost(gist)

    for tag in tags:
        WriteTag(tag)
