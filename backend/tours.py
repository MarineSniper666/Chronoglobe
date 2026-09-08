"""
Curated guided tours for Story Mode.
Each tour is an ordered sequence of event ids from history_data.
"""

TOURS = [
    {
        "id": "wheel",
        "title": "How the Wheel Changed Everything",
        "subtitle": "One invention that reshaped civilization",
        "description": (
            "From potters spinning clay on the Eurasian steppe to airplanes lifting off "
            "at Kitty Hawk, follow the wheel across seven pivotal moments."
        ),
        "stops": ["tech-wheel", "civ-sumer", "civ-egypt", "tech-bronze",
                  "civ-han", "tech-steam", "tech-flight"],
    },
    {
        "id": "dyings",
        "title": "The Great Dyings",
        "subtitle": "Six pandemics that broke empires",
        "description": (
            "From the Antonine Plague that shook Rome to COVID-19, see how disease "
            "reshaped populations and toppled dynasties."
        ),
        "stops": ["pan-antonine", "pan-justinian", "pan-blackdeath",
                  "pan-smallpox-am", "pan-flu-1918", "pan-covid"],
    },
    {
        "id": "silk-road",
        "title": "The Silk Road Story",
        "subtitle": "1,500 years of Eurasian trade",
        "description": (
            "How Han China's diplomats, Tang cosmopolitans, and Mongol conquerors "
            "wove East and West — and how the Black Death rode the same road home."
        ),
        "stops": ["civ-han", "civ-tang", "civ-mongol", "pan-blackdeath"],
    },
    {
        "id": "moon",
        "title": "How We Reached the Moon",
        "subtitle": "From steam engines to Apollo 11",
        "description": (
            "Follow the technological chain from Watt's steam engine to Edison's "
            "electricity to the transistor to Sputnik — culminating in Armstrong's "
            "first step."
        ),
        "stops": ["tech-steam", "tech-electric", "tech-transistor",
                  "tech-space", "tech-moon"],
    },
    {
        "id": "discovery",
        "title": "The Age of Discovery",
        "subtitle": "Print, plague, and the remaking of the world",
        "description": (
            "How Gutenberg's press, Ottoman siege, and Columbian exchange "
            "collided to reshape every continent."
        ),
        "stops": ["tech-gutenberg", "civ-ottoman", "pan-smallpox-am",
                  "civ-aztec", "civ-inca"],
    },
]


def list_tours():
    return TOURS


def find_tour(tour_id: str):
    for t in TOURS:
        if t["id"] == tour_id:
            return t
    return None
