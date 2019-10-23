#!/usr/bin/env python3

import sys

import versions

# fix git
# upgrade deps
# driver.py to fetch over network and print
# pure functional extraction to map json-object to something printable
# proper test runner (to read k8s.json)
# put functinoal bit under test
# flake8 etc
# read gh repos from cmdline "a/b" "b/c" args

versions.kernel_org_mainline_stable()
versions.github_releases_groupby_maj_min("zfsonlinux", "zfs", 2, 2)
versions.github_releases_groupby_maj_min("golang", "go", 2, 2)
versions.github_releases_groupby_maj_min("kubernetes", "kubernetes", 2, 2)
versions.gke_masters()
versions.github_releases_groupby_maj_min("helm", "helm", 2, 2)
versions.github_releases_groupby_maj_min("envoyproxy", "envoy", 2, 2)
versions.github_releases_groupby_maj_min("istio", "istio", 2, 2)
versions.github_releases_groupby_maj_min("linkerd", "linkerd2", 2, 2)
versions.github_releases_groupby_maj_min("hashicorp", "terraform", 2, 2)
