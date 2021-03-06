rayvision-api
=============
[![](https://img.shields.io/badge/docs--English-latest-green)](https://renderbus.readthedocs.io/en/latest)
[![](https://img.shields.io/badge/license-Apache%202-blue)](http://www.apache.org/licenses/LICENSE-2.0.txt)
![](https://img.shields.io/badge/python-2.7.10+%20%7C%203.6%20%7C%203.7-blue)
![](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)
[![CodeFactor](https://www.codefactor.io/repository/github/loonghao/rayvision_api/badge)](https://www.codefactor.io/repository/github/loonghao/rayvision_api)

A Python-based API for Using Renderbus cloud rendering service.

-------------------------------------------------------------------------------
**This is a refactored branch based on the official version.**

**Request speed is three times faster than the official version.**

**Query speed is 40 times faster than the official version.**

Changes
--------
- Follow the [Semantic Versioning](https://semver.org/) standard.
- Support use session of request.
- API key and API access id can be overloaded using environment variables `RAYVISION_API_KEY` and `RAYVISION_API_ACCESS_ID`.
- Code decoupling.
- Remove unnecessary code.
- Improve namespace and function naming.
- Add scheme to verify data type for `POST`.

# Examples:
Ues the api in the context.
```python

from rayvision_api import RayvisionAPI

api_access_id = "xxxxxx"
api_access_key = "xxxxx"

with RayvisionAPI(access_id=api_access_id, 
                  access_key=api_access_key) as ray:
    # Print current user profiles.
    print(ray.user_profile)
    # Access profile settings or info like a object.
    print(ray.user_profile.user_name)
    print(ray.user_profile.email)
    print(ray.user_profile.user_id)

```
Add custom request hooks for the api.
```python


from rayvision_api import RayvisionAPI

def print_resp_url(resp, *args, **kwargs):
    print(resp.url)


def check_for_errors(resp, *args, **kwargs):
    resp.raise_for_status()

# https://alexwlchan.net/2017/10/requests-hooks/
hooks = {'response': [print_resp_url, check_for_errors]}
options = {
    "render_platform": "6",
    "access_id": "xxxx",
    "access_key": "xxxx",
    "hooks": hooks
}

ray = RayvisionAPI(**options)
# Print current user profiles.
print(ray.user_profile)
```
Old school.
```python

from rayvision_api import RayvisionAPI
api_access_id = "xxxxxx"
api_access_key = "xxxxx"
ray = RayvisionAPI(access_id=api_access_id, access_key=api_access_key)
# Print current user profiles.
print(ray.user_profile)
# Access profile settings or info like a object.
print(ray.user_profile.user_name)
print(ray.user_profile.email)
print(ray.user_profile.user_id)

```

# Documentation

- [Official documents]( https://renderbus.readthedocs.io/en/latest/index.html)
