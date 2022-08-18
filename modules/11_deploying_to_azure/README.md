# Deploying to Azure

In this stage we'll be deploying our solution to the [Microsoft Azure Cloud](https://docs.microsoft.com/en-us/azure/developer/intro/azure-developer-overview) using [Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/overview). Azure App Service is an HTTP-based service for hosting web applications, REST APIs, and mobile back ends.

At the end of this stage you and everyone else will be able to access your website from the internet.

1. Login to Azure CLI

    ```sh
    az login
    ```

2. Create a webapp

    ```sh
    # Replace <your_initials> with your initials
    SITE_PREFIX=<your_initials>
    az webapp up --runtime PYTHON:3.9 --sku FREE --logs --name ${SITE_PREFIX}-sjf-site --location westeurope --resource-group ${SITE_PREFIX}-sjf-rg --plan ${SITE_PREFIX}-sjf-plan
    ```

3. After waiting for a few minutes, you should be able to access your website from the url: <https://<your_initial>-sjf-gamesite.azurewebsites.net>
4. You can also view the resources you've deployed on [Azure portal](https://portal.azure.com/) under `<your_initial>-sjf-rg` resource group
