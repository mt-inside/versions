import requests
import re

from itertools import groupby, islice
from distutils.version import LooseVersion


def get_ver_num(s):
    ver_num = re.compile("[0-9.]+.*")
    return ver_num.search(s).group()


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


def parse_gh_release(rs, depth, count):
    # TODO maybe fix the algorithmic complexity of this

    ret = []

    vers = map(lambda r: {
        "ver": LooseVersion(get_ver_num(r['tag_name'])),
        "name": r['name'],
        "date": r['published_at'],
        "pre": r['prerelease']
    }, rs)

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

    response = requests.get("https://www.kernel.org/releases.json")
    rs = response.json()['releases']

    vers = parse_kernel(rs)

    for m, v in vers:
        print("{}: {}".format(m, v['version']))

    print("")


def parse_kernel(rs):
    def latest(rs):
        s = sorted(rs, key=lambda r: LooseVersion(r['version']), reverse=True)
        return s[0]

    vers = sorted(rs, key=lambda r: r['moniker'])
    serieses = groupby(vers, lambda v: v['moniker'])
    # all the groups share the same underlying iterator, so have to reify
    # carefully
    d = {}
    for moniker, series in serieses:
        d[moniker] = list(series)

    return [(m, latest(d[m])) for m in ["mainline", "stable", "longterm"]]


def gke_masters():
    print("== GKE ==")

    rs = parse_gke()

    for r in rs:
        print("{}: {}".format(r['series'], r['ver']))

    print("")


# NB: needs application-default-credentials available
def parse_gke():
    from googleapiclient import discovery
    from oauth2client.client import GoogleCredentials

    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('container', 'v1', credentials=credentials)

    # Deprecated. The Google Developers Console [project ID or project
    # number](https://support.google.com/cloud/answer/6158840).
    # This field has been deprecated and replaced by the name field.
    project_id = 'esqimo-adm'  # TODO: Update placeholder value.

    # Deprecated. The name of the Google Compute Engine
    # [zone](/compute/docs/zones#available) to return operations for.
    # This field has been deprecated and replaced by the name field.
    zone = 'europe-west2-b'  # TODO: Update placeholder value.

    request = service \
        .projects() \
        .zones() \
        .getServerconfig(projectId=project_id, zone=zone)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    return [
        {"series": "latest", "ver": response['validMasterVersions'][0]},
        {"series": "default", "ver": response['defaultClusterVersion']}
    ]
