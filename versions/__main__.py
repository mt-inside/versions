#!/usr/bin/env python3

import versions

versions.github_releases_groupby_maj_min("kubernetes", "kubernetes", 2, 3)
versions.github_releases_prerelease_ga("envoyproxy", "envoy")
versions.github_releases_prerelease_ga("istio", "istio")
versions.github_releases_prerelease_ga("linkerd", "linkerd")
versions.github_releases_prerelease_ga("runconduit", "conduit")
versions.kernel_org_mainline_stable()
versions.github_releases_prerelease_ga("zfsonlinux", "zfs")
