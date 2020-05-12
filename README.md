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

```python

from rayvision_api import RayvisionAPI
api_access_id = "xxxxxx"
api_access_key = "xxxxx"
ray = RayvisionAPI(access_id=api_access_id, access_key=api_access_key)
# Print current user profiles.
print(ray.user_operator)
# Access profile settings or info like a object.
print(ray.user_operator.user_name)
print(ray.user_operator.email)
print(ray.user_operator.user_id)

```

```python

from rayvision_api import RayvisionAPI

api_access_id = "xxxxxx"
api_access_key = "xxxxx"

with RayvisionAPI(access_id=api_access_id, 
                  access_key=api_access_key) as ray:
    # Print current user profiles.
    print(ray.user_operator)
    # Access profile settings or info like a object.
    print(ray.user_operator.user_name)
    print(ray.user_operator.email)
    print(ray.user_operator.user_id)

```

# Documentation

- [Official documents]( https://renderbus.readthedocs.io/en/latest/index.html)
