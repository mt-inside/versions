#!/usr/bin/env python3

import versions

versions.github_releases_groupby_maj_min("kubernetes", "kubernetes", 2, 3)
versions.github_releases_prerelease_ga("envoyproxy", "envoy")
versions.github_releases_prerelease_ga("istio", "istio")
versions.github_releases_prerelease_ga("linkerd", "linkerd2")
versions.github_releases_prerelease_ga("golang", "go")
versions.github_releases_prerelease_ga("helm", "helm")
versions.kernel_org_mainline_stable()
versions.gke_masters()
