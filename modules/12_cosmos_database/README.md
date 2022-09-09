# Cosmos Database

## Goal

Store game data in the database in the cloud instead of the in-memory storage.

This will let us restart the server without losing all game data,
and will free the precious memory space on the server.

## Tutorial

> In this tutorial we will assume that you've completed the previous tutorials
and already save images to the blob storage.

### Part 1. Create a Cosmos DB

#### Intro

Cosmos DB is one of the database solutions Microsoft offers on Azure.

It's relatively simple and doesn't require preconfiguration, we can  
just create it and start inserting data to it right away.

However, users should be aware of one complex concept of Cosmos - [partitions](https://docs.microsoft.com/en-us/azure/cosmos-db/account-databases-containers-items#azure-cosmos-db-containers).
In this tutorial this can just assume that our partition key is "id",
but it's advisable to read about Cosmos data model to understand what this means.

#### 1. Create Cosmos DB account in your own subscription

Follow this [instruction](https://docs.microsoft.com/en-us/azure/cosmos-db/sql/create-cosmosdb-resources-portal).

You'll be asked to configure many options, but only 2 are important for our task:
- name of the account - we'll use it to connect to the storage;
- if possible, choose "Apply Free Tier Discount - Apply".

All other options you can leave on their default values.

#### 2. Find and save the connection data

On portal, navigate to the newly created storage account.
Click on the "keys" tab on the left.

Copy the values of "URI" and "PRIMARY KEY" on this page to your computer -
we'll use them later to connect to this Cosmos DB.

> More about these keys you can read [here](https://docs.microsoft.com/en-us/azure/cosmos-db/database-security?tabs=sql-api#primarysecondary-keys).

### Part 2. Crate the basic Cosmos DB storage in python

#### Intro

We will try to make the interface the new storage class
as close to the existing InMemoryStorage as possible. 

This will allow us to replace InMemoryStorage with CosmosStorage
in the server code with no (or very little) changes to the server
code itself.

#### 1. Install the SDK

Add `azure-cosmos` to the `requirements.txt` file.
Then either wait for your IDE to pick up the change, or proactively 
reinstall the dependencies with `pip install -r requirements.txt`.

#### 2. Move in-memory storage to a new module

Create a folder `src/database` with an empty file `__init__.py` in it.

> Python needs such a file to understand how to import modules
> from this folder. This file will stay empty.

Move `in_memory_storage.py` to this folder.
Also move the `StorageItem` class out to a separate file `src/database/storage_item.py`. 
Update the imports accordingly - now old import paths like
`from src.in_memory_storage import InMemoryStorage` should look like
`from src.database.in_memory_storage import InMemoryStorage`.

This refactoring should have no effect on the application. 
But it will make our code structure less complicated when we add 
the cosmos db storage.

#### 3. Create CosmosStorage skeleton

Create a new file `cosmos_storage.py` with a class `CosmosStorage`.

This class will encapsulate a connection to a CosmosDB container,
in which we will store data.

Feel free to base your implementation off this code:

```python
import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey, ContainerProxy


class CosmosStorage:
    """
    Cosmos DB database to store game items: secret words and hint images.
    """

    def __init__(self, container: ContainerProxy):
        self.container = container

    @classmethod
    def from_parameters(cls, account_endpoint, account_key, db_name, container_name):
        """ Create storage from account credentials and db/container names """
        client = CosmosClient(account_endpoint, account_key)

        try:
            database = client.create_database(id=db_name)
        except exceptions.CosmosResourceExistsError:  # db already exists
            database = client.get_database_client(database=db_name)

        try:
            container = database.create_container(
                id=container_name, partition_key=PartitionKey(path="/id")  # partition by ID
            )
        except exceptions.CosmosResourceExistsError:  # container already exists
            container = database.get_container_client(container_name)

        return cls(container)

    @classmethod
    def from_env(cls):
        """ Create storage from environment variables """
        return cls.from_parameters(
            account_endpoint=os.environ["COSMOS_ACCOUNT_ENDPOINT"],
            account_key=os.environ["COSMOS_ACCOUNT_KEY"],
            db_name=os.environ["COSMOS_DB_NAME"],
            container_name=os.environ["COSMOS_CONTAINER_NAME"],
        )
```

This code assumes you will create a new storage by calling `database = CosmosStorage.from_env()`,
and you'll have set 4 environment variables that describe how to connect to the cosmos account,
and what db/container names it should use.

In `COSMOS_ACCOUNT_ENDPOINT` you want to store the URI of the account, in `COSMOS_ACCOUNT_KEY` - 
the primary key, and db/container names are completely up to you, you can name them anything.

Set these environment variables in your IDE to always start the server with them.

### Part 3. Implement methods of CosmosStorage

### Intro

As mentioned before, we want to make the interface of `CosmosStorage`
as close to `InMemoryStorage` as possible, to make these storages
interchangeable.

In this part, you'll implement the methods yourself.

But before you do it, let us explain a few important concepts of working with Cosmos.

Before we can save our StorageItem to CosmosDB, we need to _serialize_ it to the 
format that CosmosDB can understand:
- it must be a Python dictionary;
- it must have a unique "id" column, that must be a string.

For example, we can save `StorageItem` to Cosmos like this:

```python
import dataclasses, uuid
from src.database.storage_item import StorageItem

...
    def add(self, item: StorageItem) -> str:
        """
        Store a secret word with the image.
        Return the id of the created item.
        """
        item_as_dict = dataclasses.asdict(item)  # convert to Python dict
        cosmos_item = {
            "id": str(uuid.uuid4()),  # create a random unique id
            "storage_item": item_as_dict,
        }
        self.container.upsert_item(cosmos_item)
        return cosmos_item['id']
```

Similarly, when we're reading from Cosmos, we need to _deserialize_
our StorageItem from the python dictionary that we get. We also need to 
specify a `partition_key` for every query. As we agreed in the beginning, 
the partition key is the id itself.

For example, we can read StorageItem from Cosmos like this:

```python
from src.database.storage_item import StorageItem

...
    def get_item_by_index(self, index: str) -> StorageItem:
        """
        Return the item by the index from the database.
        """
        # our container has PartitionKey(path="/id"), hence partition key == id: 
        cosmos_item = self.container.read_item(index, partition_key=index)
        return StorageItem(
            image_url=cosmos_item['storage_item']['image_url'],
            secret_word=cosmos_item['storage_item']['secret_word'],
        )
```

As you might have noticed, in these examples the item ID that used to be 
an auto-incrementing integer with InMemoryStorage (0,1,2,3,...) 
has now become a string (`str(UUID)`). This is something we can't easily 
workaround - Cosmos IDs must be strings. It'll likely be easier to make
InMemoryStorage indexes strings as well.

#### 1. Implement missing methods

Copy over all methods of `InMemoryStorage`, and implement them using
`self.container` as a storage.

A few useful methods in the SDK you can use are:

```python
# read the whole container (or the first N items)
container.read_all_items(max_item_count=None)

# add new item to the container 
# (or update, if item with the same ID already exists)
container.upsert_item({
    'id': 'item_one',
    'some_value': 123, 
    'some_other_value': ['a', 'b', 'c']
})

# read one item from DB by id
item_id = 'item_one'
container.read_item(item_id, partition_key=item_id)
```

#### 2. Verify the game works

Start the server, and verify the game works end-to-end: you still can upload
images, see them on the game, and guess the words.

Restart the server, and navigate directly to the game page. Notice everything 
you've uploaded will still be there, not lost after restart like before!

### Part 4. Testing

#### Intro

Let's add some unit tests, like we did with BlobStorage.

For BlobStorage, we used **mocks**. This time let's try a different 
[test double](https://martinfowler.com/bliki/TestDouble.html): a **fake**.

Notice how our CosmosDB client accepts its only dependency, the container,
in the constructor `def __init__(self, container)`. We can pass it a fake 
cosmos container that would imitate the behaviour of a real container,
but will not actually communicate with CosmosDB. 

Feel free to use this fake container in the tests, and modify it if needed: 

```python
from collections import defaultdict


# See the concept of test doubles at
# https://martinfowler.com/bliki/TestDouble.html
class FakeCosmosContainer:
    """
    Imitation of a real cosmos container, but it only implements a small 
    subset of the functionality, and stores everything in memory.
    """
    def __init__(self):
        self._partitions = defaultdict(dict)

    def read_item(self, item_id, partition_key):
        return self._partitions[partition_key][item_id]

    def read_all_items(self, max_item_count=None):
        all_items = [
            item
            for partition in self._partitions.values()
            for item in partition.values()
        ]
        if max_item_count is None:
            return all_items
        return all_items[:max_item_count]

    def upsert_item(self, item: dict):
        item_id = item['id']
        partition_key = item_id  # assuming our containers are always partitioned by id
        self._partitions[partition_key][item_id] = item
```

Example test:

```python
def test_is_empty():
    storage = CosmosStorage(FakeCosmosContainer())

    assert storage.is_empty()

    storage.add(StorageItem(
        image_url="image_url",
        secret_word="a cat 1",
    ))
    assert not storage.is_empty()
```

#### 1. Test all methods

Cover all methods with unit tests, like on the example above.

Very likely you'll be able to reuse some tests for the in-memory storage, 
since both storages share the same interface.

### Recap

We moved the storage of the game data to the cloud, and now
we can restart our server, or even start it on a different machine,
and no data will be lost.

We learned a bit about CosmosDB - a schemaless database where you can
store arbitrary JSONs, but that still has some requirements for the 
data stored: mandatory string IDs, mandatory explicit partition key.

We also learned about another flavour of test doubles: fakes.
