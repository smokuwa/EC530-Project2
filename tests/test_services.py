from unittest.mock import patch
import services.cli_service as cli_service


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