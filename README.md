Simple script that checks the versions of various software projects I care about. YMMV.

Run as:
```
docker build .
docker run <image id>
```

or:
```
pip3 install -r requirements.txt
python3 versions
```

TODO
* Read list of projects from a config file
* supply a username and API token to auth to github, then won't get rate-limited.

Warning: don't run too often of you'll get rate-limited by github.
