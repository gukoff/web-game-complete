# Add persistent storage for images

## Goal

Modify the app to add persistent storage for images.

## Tutorial

> In this tutorial we will assume that you've completed the previous tutorial
and already have a game where you get an image and you have to guess a word that describes it.
Now, we'll need to change the image storing functionality and upload the images to the cloud.
Then images will be served from the cloud and won't take precious memory space on our server.

### Part 1. Create the storage account

#### Intro

[Azure Blob Storage](https://docs.microsoft.com/azure/storage/blobs/) is Microsoft's object storage solution
 for the cloud. We will use it to store our images and also to get them from there using a URL. It's advisable that
 you read about this service and familiarise yourself with the concepts of a storage account, container and blob.

#### 1. Create a storage account in your own subscription where you will save the images

In order to store the images, we recommend that you create your own storage account using the portal.
The required steps are provided [here](https://docs.microsoft.com/azure/storage/common/storage-account-create?tabs=azure-portal)

#### 2. Save and expose the storage account information

In order to connect to the storage account from our code, we will need the name of the storage account and a
 storage account key that can be found in the Access Keys of the storage account like shown
 [here](https://docs.microsoft.com/azure/storage/blobs/storage-quickstart-blobs-python#copy-your-credentials-from-the-azure-portal).
Don't copy the connection string, copy the key instead, as we will use this to build the connection string
 and also to get the URL for each uploaded file.
These should be added to two environment variables: AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY.
An example on how to add an environment variable is [here](https://docs.microsoft.com/azure/storage/blobs/storage-quickstart-blobs-python#configure-your-storage-connection-string).

#### Modify the application code to store data into the storage account

Information on how to manage blobs with a storage account using Python is found [here](https://docs.microsoft.com/azure/storage/blobs/storage-quickstart-blobs-python)
We first need to add azure-storage-blob to the requirements.txt file and install the new dependency by using pip:
`pip install -r requirements.txt`.

In the `in_memory_storage.py`, modify the StorageItem.
We can replace the image_bytes and the image_content_type with an image_url that will link to the image saved in the storage account.
Now the object will look like this:

```python
class StorageItem:
    image_url: str
    secret_word: str
```

Don't forget to modify the unit tests to use this new structure.

When we upload the image, in `def upload_image()` we will add the code that uploads the image in the storage account.
Create a new `BlobStorage` class in a new file blob_storage.py. This class we'll use to upload images to blob storage.

An example on how to upload blobs to a container can be found [here](https://docs.microsoft.com/azure/storage/blobs/storage-quickstart-blobs-python?#upload-blobs-to-a-container).
The container should also be created in the code.
Create the method to upload an image and save the url to our in memory storage:

`def upload_image(self, image_bytes, content_type) -> str:`

Now run the app, upload an image, and verify on [portal.azure.com](https://portal.azure.com) 
that a blob is created in the container.

### Part 2. Display images for the storage account

#### 1. Allow anonymous public read access

Go back to the Azure portal, and change the access level of the container to provide public read access for blobs.
Information on this can be found [here](https://docs.microsoft.com/en-us/azure/storage/blobs/anonymous-read-access-configure?tabs=portal#about-anonymous-public-read-access).

#### 2. Modify the image retrieval

Now in the api file we can modify the endpoint that returns the image on the game page 
to redirect to the blob storage url instead:
`return redirect(item.image_url, code=302)`.

### Part 3. Testing

#### Intro

To unit test the blob upload, we need to mock the behavior as we don't want to upload data to a real blob as this takes time and generates cost.
We recommend the [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) library for this.

#### Create a test to check the upload blob functionality

[Monkeypatch](https://docs.pytest.org/en/7.1.x/how-to/monkeypatch.html) allows to modify the behavior of a function to use a mock instead of the real functionality.
Then we can call the function we want to test and check that calls were made with the parameters that we expected.

```python
def test_blob_storage(monkeypatch):
    monkeypatch.setattr(
        "azure.storage.blob.BlobServiceClient.from_connection_string", 
        mock.MagicMock(
        ))
    monkeypatch.setattr(
        "azure.storage.blob.BlobServiceClient.get_container_client",
        mock.MagicMock())
    
    blob_storage = BlobStorage()
    blob = blob_storage.upload_image(b"image_bytes", "image/png")
    blob_storage.container_client.get_blob_client.assert_called()
    blob_storage.container_client.get_blob_client(blob).upload_blob.assert_called_with(
        b"image_bytes", blob_type="BlockBlob", 
        content_settings=azure.storage.blob.ContentSettings(content_type="image/png"))
```

### Part 5. Recap

We've created a storage account and added code that creates a container in it and then  stored the images in blob.
We learned how to:

- create an Azure service like a storage account. 
- access it in the code using Python

Now you can think how you can further improve this game! For example:

- Estimating the cost for the storage account based on usage prediction. This [tool](https://azure.microsoft.com/pricing/calculator/)
- Deleting blobs from the storage account if the corresponding word is not in the database or if they were uploaded more than X days ago.

### Part 6. Moving to a production system

In a production system, the creation of the Azure resources like the storage account is done using a language like
 [bicep](https://docs.microsoft.com/azure/azure-resource-manager/bicep) or [terraform](https://www.terraform.io/).

Also secrets like storage account access keys will be normally kept into a secret manager, for example
 [Azure Keyvault](https://azure.microsoft.com/services/key-vault/).
