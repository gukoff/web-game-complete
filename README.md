# web-game-complete


1. Run frontend
    ```sh
    cd app/frontend
    npm run dev
    ```

2. Run backend

    ```sh
    cd app/backend
    pip install -r requirements.txt
    cd ..
    FLASK_DEBUG=1 flask run
    ```


## Deploy

1. Compile frontend dist

    ```sh
    cd app/frontend
    npm run build
    ```

2. Login to Azure CLI

    ```sh
    az login
    ```

3. Create a webapp

    ```sh
    cd .. # into the /app folder
    az webapp up --runtime PYTHON:3.9 --sku B1 --logs
    ```

    > [!NOTE]
    > The `az webapp up` command does the following actions:
    >
    >- Create a default [resource group](/cli/azure/group#az-group-create). (randmoly generated)
    >
    >- Create a default [App Service plan](/cli/azure/appservice/plan#az-appservice-plan-create).
    >
    >- [Create an app](/cli/azure/webapp#az-webapp-create) with the specified name.
    >
    >- [Zip deploy](../articles/app-service/deploy-zip.md#deploy-a-zip-package) all files from the current working directory, [with build automation enabled](../articles/app-service/deploy-zip.md#enable-build-automation-for-zip-deploy).
    >
    >- Cache the parameters locally in the *.azure/config* file so that you don't need to specify them again when deploying later with `az webapp up` or other `az webapp` commands from the project folder. The cached values are used automatically by default.
    >