from weather_symphony.components.scene_parser import Scene
from weather_symphony.components.sections.melody_section import MelodySection
from weather_symphony.music import Track


class GlockenspielMelody(MelodySection):
    def __init__(self, *args):
        super().__init__(*args)

        self.track = Track(9, self.channel_num)
        self.base_octave = 6
        self.velocity_range_map = (0, 30, 40, 100)

        self.rhythm_settings = {
            Scene.SCATTERED_WINDY: (0.3, 8, 0.4),
            Scene.CLEAR_BROILING: (0.7, 2, 0.15),
            Scene.CLEAR_NICE: (0.4, 8, 0.4),
            Scene.NIGHT_CHILLY: (0.2, 16, 0.2),
            Scene.NIGHT_WARM: (0.2, 4, 0.2),
        }
        self.scene_vel_add = {}
