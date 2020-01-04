import os

import core.maps as maps


class TestMapController:
    def test__render(self):
        map_1_path = os.path.join("./maps", "world_1.map")
        map_1_controller = maps.MapController(map_1_path)

        assert map_1_controller.rect is not None

        map_2_path = os.path.join("./maps", "world_2.map")
        map_2_controller = maps.MapController(map_2_path)

        assert map_2_controller.rect is not None

    # def test_update(self):
    #     assert False
    #
    # def test__handle_input(self):
    #     assert False
    #
    # def test_draw(self):
    #     assert False
