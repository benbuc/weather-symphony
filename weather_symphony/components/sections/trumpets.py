from weather_symphony.components.scene_parser import Scene
from weather_symphony.components.sections.harmony_section import HarmonySection
from weather_symphony.music import Track


class TrumpetsSection(HarmonySection):
    def __init__(self, *args):
        super().__init__(*args)

        self.track = Track(56, self.channel_num)
        self.base_octave = 3
        self.velocity_range_map = (0, 35, 10, 127)

        self.rhythm_settings_arpeggios = {
            Scene.OVERCAST_THUNDERSTORM: (0, 0.9, 0.5),
            Scene.OVERCAST_WINDY: (0, 0.8, 0.4),
            Scene.BROKEN_RAINY: (0, 0.6, 0.4),
            Scene.BROKEN_GUSTY: (0, 0.9, 0.4),
            Scene.SCATTERED_WINDY: (0, 0.9, 0.4),
            Scene.SCATTERED_SWELTRY: (0, 0.0, 0.0),
            Scene.CLEAR_BROILING: (0, 0.0, 0.3),
            Scene.CLEAR_NICE: (0, 0.0, 0.5),
            Scene.NIGHT_CHILLY: (0, 0.7, 0.5),
            Scene.NIGHT_WARM: (0, 0.8, 0.4),
        }
        self.rhythm_settings_chords = {
            Scene.OVERCAST_THUNDERSTORM: (4, 0.0, 0.7),
            Scene.OVERCAST_WINDY: (4, 0.0, 0.5),
            Scene.BROKEN_RAINY: (0, 0.0, 0.5),
            Scene.BROKEN_GUSTY: (2, 0.0, 0.5),
            Scene.SCATTERED_WINDY: (4, 0.0, 0.2),
            Scene.SCATTERED_SWELTRY: (4, 0.0, 0.1),
            Scene.CLEAR_BROILING: (1, 0.0, 0.3),
            Scene.CLEAR_NICE: (0, 0.0, 0.5),
            Scene.NIGHT_CHILLY: (0, 0.0, 0.5),
            Scene.NIGHT_WARM: (2, 0.0, 0.5),
        }
        self.arpeggio_probabilities = {
            Scene.OVERCAST_THUNDERSTORM: 0.1,
            Scene.OVERCAST_WINDY: 0.2,
            Scene.BROKEN_RAINY: 0.3,
            Scene.BROKEN_GUSTY: 0.4,
            Scene.SCATTERED_WINDY: 0.4,
            Scene.SCATTERED_SWELTRY: 0.4,
            Scene.CLEAR_BROILING: 0.6,
            Scene.CLEAR_NICE: 0.15,
            Scene.NIGHT_CHILLY: 0.6,
            Scene.NIGHT_WARM: 0.6,
        }
