import re

from itertools import groupby, islice
from distutils.version import LooseVersion


def get_ver_num(s):
    ver_num = re.compile("[0-9.]+.*")
    return ver_num.search(s).group()


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


# NB: needs application-default-credentials available
def parse_gke(rs):
    return [
        {"series": "latest", "ver": rs['validMasterVersions'][0]},
        {"series": "default", "ver": rs['defaultClusterVersion']}
    ]
