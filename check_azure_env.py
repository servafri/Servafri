import os

required_vars = [
    'AZURE_SUBSCRIPTION_ID',
    'AZURE_RESOURCE_GROUP',
    'AZURE_LOCATION',
    'AZURE_TENANT_ID',
    'AZURE_CLIENT_ID',
    'AZURE_CLIENT_SECRET'
]

missing_vars = [var for var in required_vars if not os.environ.get(var)]

if missing_vars:
    print(f"The following environment variables are missing: {', '.join(missing_vars)}")
else:
    print("All required Azure environment variables are set.")

# Print the values of the set variables (without revealing secrets)
for var in required_vars:
    value = os.environ.get(var)
    if value:
        print(f"{var}: {'*' * len(value)}")
    else:
        print(f"{var}: Not set")
