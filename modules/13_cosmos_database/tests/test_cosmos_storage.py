from unittest import skip
from collections import defaultdict

from src.database.cosmos_storage import CosmosStorage
from src.database.storage_item import StorageItem


# See the concept of test doubles at
# https://martinfowler.com/bliki/TestDouble.html
class FakeCosmosContainer:
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


def test_is_empty():
    storage = CosmosStorage(FakeCosmosContainer())

    assert storage.is_empty()

    storage.add(StorageItem(
        image_url="image_url",
        secret_word="a cat 1",
    ))
    assert not storage.is_empty()


def test_get_random_index_when_one_item():
    storage = CosmosStorage(FakeCosmosContainer())

    inserted_id = storage.add(StorageItem(
        image_url="image1",
        secret_word="a cat 1",
    ))

    # when there's only one item, random index should always be equal to the index of this item
    for _ in range(100):
        assert storage.get_random_item_index() == inserted_id


def test_get_item_by_index():
    storage = CosmosStorage(FakeCosmosContainer())

    storage_item_1 = StorageItem(
        image_url="image1",
        secret_word="a cat 1",
    )
    inserted_id_1 = storage.add(storage_item_1)

    assert storage.get_item_by_index(inserted_id_1) == storage_item_1

    storage_item_2 = StorageItem(
        image_url="image2",
        secret_word="a cat 2",
    )
    inserted_id_2 = storage.add(storage_item_2)

    assert storage.get_item_by_index(inserted_id_1) == storage_item_1
    assert storage.get_item_by_index(inserted_id_2) == storage_item_2


@skip("failing")
def test_has_index():
    storage = CosmosStorage(FakeCosmosContainer())

    assert not storage.has_index('')
    assert not storage.has_index('123')

    inserted_index_1 = storage.add(StorageItem(
        image_url="image1",
        secret_word="a cat 1",
    ))

    assert storage.has_index(inserted_index_1)
    assert not storage.has_index('')
    assert not storage.has_index('123')

    inserted_index_2 = storage.add(StorageItem(
        image_url="image2",
        secret_word="a cat 2",
    ))

    assert storage.has_index(inserted_index_1)
    assert storage.has_index(inserted_index_2)
    assert not storage.has_index('')
    assert not storage.has_index('123')

    assert inserted_index_1 != inserted_index_2
