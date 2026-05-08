from unittest.mock import patch, MagicMock
import json
import services.cli_service as cli_service
import services.document_db_service as document_db_service


@patch("services.cli_service.handle_upload")
@patch("builtins.input", return_value="data/dog.jpeg")
def test_handle_image_calls_upload_service(mock_input, mock_handle_upload, capsys):
    mock_handle_upload.return_value = {
        "payload": {
            "image_id": "img_1",
            "path": "data/dog.jpeg",
        },
    }
    event = cli_service.handle_image()
    mock_input.assert_called_once_with("Enter image path: ")
    mock_handle_upload.assert_called_once_with("data/dog.jpeg")
    assert event["payload"]["image_id"] == "img_1"
    assert "Upload accepted. Image ID: img_1" in capsys.readouterr().out

def test_handle_image_prints_file_not_found(capsys):
    with patch("builtins.input", return_value="missing.jpg"):
        with patch("services.cli_service.handle_upload", side_effect=FileNotFoundError("missing.jpg")):
            event = cli_service.handle_image()
    assert event is None
    assert "Upload failed: I could not find that file." in capsys.readouterr().out

def test_handle_image_prints_invalid_upload(capsys):
    with patch("builtins.input", return_value="notes.txt"):
        with patch("services.cli_service.handle_upload", side_effect=ValueError("bad extension")):
            event = cli_service.handle_image()
    assert event is None
    assert "Upload failed: please enter a valid image file path." in capsys.readouterr().out

def test_main_exits_when_user_enters_exit(capsys):
    with patch("builtins.input", return_value="exit"):
        cli_service.main()
    assert "GOODBYE" in capsys.readouterr().out
    
def test_main_handles_invalid_command(capsys):
    with patch("builtins.input", side_effect=["badcommand", "exit"]):
        cli_service.main()
    output = capsys.readouterr().out
    assert "Invalid entry" in output
    assert "GOODBYE" in output

@patch("services.cli_service.get_redis")
@patch("builtins.input", side_effect=["img_1", "dog"])
def test_handle_correction_publishes_annotation_corrected(mock_input, mock_get_redis):
    mock_redis = MagicMock()
    mock_get_redis.return_value = mock_redis
    event = cli_service.handle_correction()
    assert event["topic"] == "annotation.corrected"
    assert event["payload"]["image_id"] == "img_1"
    assert event["payload"]["annotation_id"] == "ann_img_1"
    assert event["payload"]["objects"][0]["label"] == "dog"
    mock_redis.publish.assert_called_once()

@patch("services.cli_service.get_redis")
@patch("builtins.input", side_effect=["img_2", "car"])
def test_handle_correction_prints_success_message(mock_input, mock_get_redis, capsys):
    mock_redis = MagicMock()
    mock_get_redis.return_value = mock_redis
    cli_service.handle_correction()
    output = capsys.readouterr().out
    assert "Published annotation.corrected for img_2" in output

@patch("services.document_db_service.get_redis")
def test_handle_annotation_correction_updates_redis(mock_get_redis):
    mock_redis = MagicMock()
    mock_get_redis.return_value = mock_redis
    event = {
        "type": "publish",
        "topic": "annotation.corrected",
        "event_id": "evt_1",
        "timestamp": "2026",
        "payload": {
            "image_id": "img_1",
            "annotation_id": "ann_img_1",
            "objects": [
                {"label": "cat", "bbox": [0, 0, 100, 100], "conf": 1.0}
            ],
        },
    }
    document_db_service.handle_annotation_correction(event)
    mock_redis.set.assert_called_once()
    key, value = mock_redis.set.call_args[0]
    assert key == "annotation:ann_img_1"
    stored_document = json.loads(value)
    assert stored_document["image_id"] == "img_1"
    assert stored_document["annotation_id"] == "ann_img_1"
    assert stored_document["objects"][0]["label"] == "cat"
    assert stored_document["status"] == "corrected"