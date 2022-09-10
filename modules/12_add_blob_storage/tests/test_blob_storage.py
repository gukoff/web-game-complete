from unittest import mock
import azure.storage.blob
from src.blob_storage import BlobStorage


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
    blob_storage.container_client.get_blob_client.assert_called()  # pylint: disable=E1101
    blob_storage.container_client.get_blob_client(blob).upload_blob.assert_called_with(  # pylint: disable=E1101
        b"image_bytes", blob_type="BlockBlob",
        content_settings=azure.storage.blob.ContentSettings(content_type="image/png"))
