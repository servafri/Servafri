# Auth0 Setup Instructions

1. Sign up for an Auth0 account:
   - Go to https://auth0.com/ and click on the "Sign Up" button.
   - Fill in the required information and create your account.

2. Set up a new Auth0 application:
   - After logging in, go to the Auth0 dashboard.
   - Click on "Applications" in the left sidebar.
   - Click on "Create Application".
   - Give your application a name (e.g., "ServafriCloud").
   - Choose "Regular Web Applications" as the application type.
   - Click "Create".

3. Configure the application:
   - In the application settings, scroll down to "Application URIs".
   - Set the following URIs:
     - Allowed Callback URLs: http://localhost:5000/callback, https://your-cpanel-domain.com/callback
     - Allowed Logout URLs: http://localhost:5000, https://your-cpanel-domain.com
     - Allowed Web Origins: http://localhost:5000, https://your-cpanel-domain.com
   - Scroll down and click "Save Changes".

4. Note down the following information:
   - Domain
   - Client ID
   - Client Secret

5. Create an API:
   - In the Auth0 dashboard, go to "APIs" in the left sidebar.
   - Click "Create API".
   - Provide a name for your API (e.g., "ServafriCloud API").
   - Set an identifier (e.g., https://api.servafricloud.com).
   - Keep the signing algorithm as RS256.
   - Click "Create".

Please complete these steps and provide the Domain, Client ID, and Client Secret. We'll need this information to configure our application.
