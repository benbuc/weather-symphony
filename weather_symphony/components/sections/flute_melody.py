from weather_symphony.components.scene_parser import Scene
from weather_symphony.components.sections.melody_section import MelodySection
from weather_symphony.music import Track


class FluteMelody(MelodySection):
    def __init__(self, *args):
        super().__init__(*args)

        self.track = Track(73, self.channel_num)
        self.base_octave = 4
        self.velocity_range_map = (0, 20, 40, 110)

        self.rhythm_settings = {
            Scene.BROKEN_GUSTY: (0.3, 8, 0.4),
            Scene.SCATTERED_WINDY: (0.3, 8, 0.4),
            Scene.CLEAR_BROILING: (0.7, 4, 0.15),
            Scene.CLEAR_NICE: (0.8, 8, 0.4),
            Scene.NIGHT_CHILLY: (0.6, 16, 0.3),
            Scene.NIGHT_WARM: (0.3, 4, 0.5),
        }
        self.scene_vel_add = {}
