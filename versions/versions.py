import requests
import os

from itertools import groupby, islice
from distutils.version import LooseVersion

def github_releases_prerelease_ga(owner, repo):
    print("== {} ==".format(repo))

    response = requests.get("https://api.github.com/repos/{}/{}/releases".format(owner,repo))
    rs = response.json()

    try:
        pres = filter(lambda r: r['prerelease'], rs)
        pre = next(pres)
        pre_render = "{} - \"{}\" - {}".format(pre['tag_name'], pre['name'], pre['published_at'])
    except StopIteration:
        pre_render = None
    print("Prerelease: {}".format(pre_render))

    try:
        gas = filter(lambda r: not r['prerelease'], rs)
        ga = next(gas)
        ga_render = "{} - \"{}\" - {}".format(ga['tag_name'], ga['name'], ga['published_at'])
    except StopIteration:
        ga_render = None
    print("GA: {}".format(ga_render))

    print("")


def github_releases_groupby_maj_min(owner, repo, depth, count):
    print("== {} ==".format(repo))

    response = requests.get("https://api.github.com/repos/{}/{}/releases".format(owner,repo))
    rs = response.json()

    names = map(lambda r: r['name'][1:], rs)
    vers = map(lambda name: LooseVersion(name), names)
    s_vers = sorted(vers, reverse=True)
    for majmin, rels in islice(groupby(s_vers, lambda v: v.version[0:depth]), count):
        print("Latest {}: {}".format(majmin, next(rels)))

    print("")


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

    #rc = single(filter(lambda r : r['moniker'] == "mainline", releases))
    rcs = filter(lambda r : r['moniker'] == "mainline", releases)
    for rc in rcs:
        print("Latest Mainline: {} ({})".format(rc['version'], rc['released']['isodate']))

    stable = latest([r for r in releases if r['moniker'] == "stable"])
    print("Latest Stable: {} ({})".format(stable['version'], stable['released']['isodate']))

    print("")

def gke_masters():
    print("== GKE ==")

    os.system("gcloud container get-server-config --zone=us-west1-b | head -n 10")
