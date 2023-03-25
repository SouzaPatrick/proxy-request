from decouple import config

# CHECK_PROXY
# ----------------------------------------------------------------------------------
DESTINATION_HOST = config("DESTINATION_HOST")
TIMEOUT_CHECK_PROXY = config("TIMEOUT_CHECK_PROXY", default=10, cast=int)  # Seconds

TTL_PROXY = config("TTL_PROXY", default=30, cast=int)  # Minutes
