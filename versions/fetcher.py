import requests
import datetime

import parser


def elapsed(d):
    return "{} days ago".format((datetime.datetime.now() - d).days)


def github_releases_groupby_maj_min(owner, repo, depth, count):
    def format_release(r):
        if r is None:
            return ""
        else:
            d = datetime.datetime.strptime(
                r['published_at'],
                "%Y-%m-%dT%H:%M:%SZ"
            )
            if r['name'] and r['name'] != r['tag_name']:
                n = '"{}", '.format(r['name'])
            else:
                n = ""
            return '{} ({}{})'.format(r['ver'], n, elapsed(d))

    response = requests.get(
        "https://api.github.com/repos/{}/{}/releases".format(owner, repo)
    )
    rs = response.json()

    arrs = parser.parse_gh_release(rs, depth, count)

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


def kernel_org_mainline_stable():
    print("== linux ==")

    response = requests.get("https://www.kernel.org/releases.json")
    rs = response.json()['releases']

    vers = parser.parse_kernel(rs)

    for m, v in vers:
        d = datetime.datetime.strptime(v['released']['isodate'], "%Y-%m-%d")
        print("{}: {} ({})".format(m, v['version'], elapsed(d)))

    print("")


def gke_masters():
    print("== GKE ==")

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

    rs = parser.parse_gke(response)

    for r in rs:
        print("{}: {}".format(r['series'], r['ver']))

    print("")
