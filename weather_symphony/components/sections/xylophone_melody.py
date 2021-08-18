from weather_symphony.components.scene_parser import Scene
from weather_symphony.components.sections.melody_section import MelodySection
from weather_symphony.music import Track


class XylophoneMelody(MelodySection):
    def __init__(self, *args):
        super().__init__(*args)

        self.track = Track(13, self.channel_num)
        self.base_octave = 5
        self.velocity_range_map = (0, 30, 40, 100)

        self.rhythm_settings = {
            Scene.BROKEN_RAINY: (0.6, 8, 0.3, 0.2),
            Scene.BROKEN_GUSTY: (0.6, 8, 0.3, 0.3),
            Scene.SCATTERED_WINDY: (0.3, 8, 0.4, 0.3),
            Scene.CLEAR_NICE: (0.2, 16, 0.05, 0.2),
        }
        self.scene_vel_add = {}
