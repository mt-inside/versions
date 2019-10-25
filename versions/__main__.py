#!/usr/bin/env python3

import fetcher

# date parsing and printing
# read gh repos from cmdline "a/b" "b/c" args

fetcher.kernel_org_mainline_stable()
fetcher.github_releases_groupby_maj_min("zfsonlinux", "zfs", 2, 2)
fetcher.github_releases_groupby_maj_min("golang", "go", 2, 2)
fetcher.github_releases_groupby_maj_min("kubernetes", "kubernetes", 2, 5)
fetcher.gke_masters()
fetcher.github_releases_groupby_maj_min("helm", "helm", 2, 2)
fetcher.github_releases_groupby_maj_min("envoyproxy", "envoy", 2, 2)
fetcher.github_releases_groupby_maj_min("istio", "istio", 2, 2)
fetcher.github_releases_groupby_maj_min("linkerd", "linkerd2", 1, 2)
fetcher.github_releases_groupby_maj_min("hashicorp", "terraform", 2, 2)
