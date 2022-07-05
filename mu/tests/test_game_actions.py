from unittest import TestCase
import mock

from src.game_actions import get_my_lvl


class TestGameActions(TestCase):

    @mock.patch("mu.src.game_actions.send_string")
    @mock.patch("mu.src.game_actions.read_lvl")
    def test_get_my_lvl(self, mock_send_string, mock_read_lvl):
        mock_send_string.return_value = None
        mock_read_lvl.side_effect = [0, 200]
        assert get_my_lvl() == 5

