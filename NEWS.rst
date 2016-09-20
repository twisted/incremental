Incremental 16.9.1 (2016-09-21)
===============================

Bugfixes
--------

- python -m incremental.update <package> --dev now starts a dev-less
  package at 0, not 1. (#15)


Incremental 16.9.0 (2016-09-18)
===============================

Features
--------

- Incremental now uses 'rcX' instead of 'pre' for prereleases/release
  candidates, to match PEP440. (#4)
- If you reference "<yourproject> NEXT" and use `python -m
  incremental.update`, it will automatically be updated to the next
  release version number. (#7)

Misc
----

- #1, #10
