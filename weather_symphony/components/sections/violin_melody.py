from weather_symphony.components.scene_parser import Scene
from weather_symphony.components.sections.melody_section import MelodySection
from weather_symphony.music import Track


class ViolinMelody(MelodySection):
    def __init__(self, *args):
        super().__init__(*args)

        self.track = Track(40, self.channel_num)
        self.base_octave = 5
        self.velocity_range_map = (0, 30, 40, 100)

        self.rhythm_settings = {
            Scene.OVERCAST_THUNDERSTORM: (0.8, 16, 0.8),
            Scene.BROKEN_RAINY: (0.6, 8, 0.5),
            Scene.SCATTERED_WINDY: (0.3, 8, 0.4),
            Scene.CLEAR_BROILING: (0.3, 2, 0.15),
            Scene.CLEAR_NICE: (0.8, 8, 0.4),
            Scene.NIGHT_CHILLY: (0.8, 8, 0.8),
            Scene.NIGHT_WARM: (0.3, 4, 0.5),
        }
        self.scene_vel_add = {
            Scene.OVERCAST_THUNDERSTORM: 100,
        }
