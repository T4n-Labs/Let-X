import pytest
from unittest.mock import patch, MagicMock
from letx.src.cmd import cmd_search

# Mock data untuk pengujian
MOCK_PACKAGES = [
    {"name": "dinit", "category": "core", "description": "Service manager"},
    {"name": "brave", "category": "extra", "description": "Web browser"}
]

@patch('letx.src.cmd.load_json')
@patch('letx.src.cmd.print')
def test_cmd_search_found(mock_print, mock_load_json):
    mock_load_json.return_value = MOCK_PACKAGES
    
    cmd_search("dinit")
    
    # Memastikan print dipanggil (artinya paket ditemukan)
    assert mock_print.called
    # Cek apakah output mengandung nama paket
    call_args = str(mock_print.call_args_list)
    assert "dinit" in call_args

@patch('letx.src.cmd.load_json')
@patch('letx.src.cmd.print')
def test_cmd_search_not_found(mock_print, mock_load_json):
    mock_load_json.return_value = MOCK_PACKAGES
    
    cmd_search("nonexistent-package")
    
    # Memastikan pesan "No packages match" dicetak
    mock_print.assert_any_call("🔍 No packages match 'nonexistent-package'.")