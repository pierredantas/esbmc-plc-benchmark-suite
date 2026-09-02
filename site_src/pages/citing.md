# Citing

Cite the archived release rather than this site. The pages are the readable face of the
artifact; the citable object is the versioned archive on Zenodo.

{{citation: CITATION.cff}}

The first DOI always resolves to the newest release. The other three pin a specific
version, v1.1.1, v1.1.0 and v1.0.1. Cite whichever pinned DOI matches the release you
actually measured against, not the version-independent one, because that one can start
resolving to a release that no longer contains the task you measured. The manuscript
under review reports the v1.0.1 figures, so a citation of that paper should pin
`10.5281/zenodo.21642386`.

Zenodo's own page for the v1.1.1 and v1.1.0 archives describes v1.0.1's content: its
metadata is generated from `.zenodo.json` at archival time, and that file lagged the
tree for those two releases. The archived tarball itself is the correct release; the
description on Zenodo's page is what is wrong, and only for those two entries.

An accompanying article is under review at *Scientific Reports*. `CITATION.cff` in the
repository carries its details and stays current; this page is generated from that file.
