from weather_symphony.components.scene_parser import Scene
from weather_symphony.components.sections.harmony_section import HarmonySection
from weather_symphony.music import Track


class PercussionSection(HarmonySection):
    def __init__(self, *args):
        super().__init__(*args)

        self.track = Track(47, 10)
        self.base_octave = 1
        self.velocity_range_map = (0, 20, 30, 120)

        self.rhythm_settings_arpeggios = {
            Scene.OVERCAST_THUNDERSTORM: (16, 1.0, 0.7),
            Scene.OVERCAST_WINDY: (16, 0.8, 0.3),
            Scene.BROKEN_RAINY: (0, 0.0, 0.0),
            Scene.BROKEN_GUSTY: (8, 0.9, 0.2),
            Scene.SCATTERED_WINDY: (8, 0.9, 0.2),
            Scene.SCATTERED_SWELTRY: (1, 1.0, 0.3),
            Scene.CLEAR_BROILING: (0, 0.0, 0.0),
            Scene.CLEAR_NICE: (0, 0.0, 0.5),
            Scene.NIGHT_CHILLY: (0, 0.3, 0.5),
            Scene.NIGHT_WARM: (0, 0.8, 0.4),
        }
        self.arpeggio_probabilities = {
            Scene.OVERCAST_THUNDERSTORM: 1.0,
            Scene.OVERCAST_WINDY: 1.0,
            Scene.BROKEN_RAINY: 1.0,
            Scene.BROKEN_GUSTY: 1.0,
            Scene.SCATTERED_WINDY: 1.0,
            Scene.SCATTERED_SWELTRY: 1.0,
            Scene.CLEAR_BROILING: 1.0,
            Scene.CLEAR_NICE: 1.0,
            Scene.NIGHT_CHILLY: 1.0,
            Scene.NIGHT_WARM: 1.0,
        }
