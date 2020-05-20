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
