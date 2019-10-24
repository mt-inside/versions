import requests
import os
import re

from itertools import groupby, islice
from distutils.version import LooseVersion


def github_releases_groupby_maj_min(owner, repo, depth, count):
    def format_release(r):
        if r is None:
            return ""
        else:
            return '{} ({})'.format(r['ver'], r['date'])

    response = requests.get(
            "https://api.github.com/repos/{}/{}/releases".format(owner, repo)
    )
    rs = response.json()

    arrs = parse_gh_release(rs, depth, count)

    print("== {} ==".format(repo))
    for s in arrs:
        print("{}: ".format(s['series']), end='')
        if s['pre']:
            print("PRE {}".format(format_release(s['pre'])), end='')
        if s['pre'] and s['ga']:
            print(" | ", end='')
        if s['ga']:
            print("GA {}".format(format_release(s['ga'])), end='')
        print("")
    print("")


def get_ver_num(s):
    ver_num = re.compile("[0-9.]+.*")
    return ver_num.search(s).group()


def parse_gh_release(rs, depth, count):
    # TODO chnage to list / dict comprehensions
    # TODO maybe fix the algorithmic complexity of this

    ret = []

    names = map(lambda r: {
        "tag": get_ver_num(r['tag_name']),
        "name": r['name'],
        "date": r['published_at'],
        "pre": r['prerelease']
    }, rs)
    # TODO: syntax for old dict + change
    vers = map(lambda o: {
        "ver": LooseVersion(o['tag']),
        "name": o['name'],
        "date": o['date'],
        "pre": o['pre']
    }, names)
    s_vers = sorted(vers, key=lambda o: o['ver'], reverse=True)
    for series, rels in islice(
        groupby(s_vers, lambda v: v['ver'].version[0:depth]),
        count
    ):
        rs = list(rels)  # Walk this iterator only once
        gas = filter(lambda r: not r['pre'], rs)
        pres = filter(lambda r: r['pre'], rs)

        try:
            ga = next(gas)
        except StopIteration:
            ga = None

        try:
            pre = next(pres)
            if ga and pre['ver'] < ga['ver']:
                pre = None
        except StopIteration:
            pre = None

        ret.append({
            "series": ".".join([str(i) for i in series]),
            "pre": pre,
            "ga": ga
        })

    return ret


def kernel_org_mainline_stable():
    print("== linux ==")

    def single(xs):
        assert(len(xs) == 1)
        return xs.pop()

    def latest(xs):
        assert(len(xs) >= 1)
        return sorted(xs, key=lambda x: x['version']).pop()

    response = requests.get("https://www.kernel.org/releases.json")
    data = response.json()
    releases = data['releases']

    # TODO groupby here

    # rc = single(filter(lambda r : r['moniker'] == "mainline", releases))
    rcs = filter(lambda r: r['moniker'] == "mainline", releases)
    for rc in rcs:
        print("Latest Mainline: {} ({})".format(rc['version'], rc['released']['isodate']))

    stable = latest([r for r in releases if r['moniker'] == "stable"])
    print("Latest Stable: {} ({})".format(stable['version'], stable['released']['isodate']))

    print("")


def gke_masters():
    print("== GKE ==")

    os.system("gcloud container get-server-config --zone=us-west1-b | head -n 10")
