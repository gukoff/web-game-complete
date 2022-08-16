# web-game-complete

1. Run application

    ```sh
    cd app
    pip install -r requirements.txt
    FLASK_DEBUG=1 flask run
    ```

## Deploy

1. Login to Azure CLI

    ```sh
    az login
    ```

2. Create a webapp

    ```sh
    cd src/99_complete_app
    SITE_PREFIX=<your_inititals>
    az webapp up --runtime PYTHON:3.9 --sku FREE --logs --name ${SITE_PREFIX}-sjf-site --location westeurope --resource-group ${SITE_PREFIX}-sjf-rg --plan ${SITE_PREFIX}-sjf-plan
    ```

    > [!NOTE]
    > The `az webapp up` command does the following actions:
    >
    >- Create a default [resource group](/cli/azure/group#az-group-create). (randomly generated)
    >
    >- Create a default [App Service plan](/cli/azure/appservice/plan#az-appservice-plan-create).
    >
    >- [Create an app](/cli/azure/webapp#az-webapp-create) with the specified name.
    >
    >- [Zip deploy](../articles/app-service/deploy-zip.md#deploy-a-zip-package) all files from the current working directory, [with build automation enabled](../articles/app-service/deploy-zip.md#enable-build-automation-for-zip-deploy).
    >
    >- Cache the parameters locally in the *.azure/config* file so that you don't need to specify them again when deploying later with `az webapp up` or other `az webapp` commands from the project folder. The cached values are used automatically by default.
    >