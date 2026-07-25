"""
Rich details for each event: who discovered/led it, and the lineage graph
(related_ids = events this one directly enabled or was enabled by).
Keeps the main history_data.py compact and lets us layer detail without
churning the primary schema.
"""

DETAILS = {
    # ------- Technology lineage: the great chain of human invention -------
    "tech-fire": {
        "discovered_by": "Early Homo (Homo erectus and later H. sapiens) across East and Southern Africa",
        "related_ids": ["tech-pottery", "tech-agri", "tech-bronze"],
    },
    "tech-agri": {
        "discovered_by": "Neolithic farming communities of the Fertile Crescent (Levant, Anatolia, Zagros foothills)",
        "related_ids": ["tech-fire", "tech-pottery", "civ-jericho", "civ-catalhoyuk", "civ-sumer", "tech-wheel"],
    },
    "tech-pottery": {
        "discovered_by": "Late Pleistocene hunter-gatherers of southern China (Xianrendong Cave)",
        "related_ids": ["tech-fire", "tech-agri", "civ-catalhoyuk"],
    },
    "tech-writing": {
        "discovered_by": "Sumerian temple accountants in Uruk",
        "related_ids": ["civ-sumer", "tech-alphabet", "tech-papermsk", "tech-print-china", "tech-gutenberg"],
    },
    "tech-wheel": {
        "discovered_by": "Late Neolithic Mesopotamian potters and steppe pastoralists",
        "related_ids": ["tech-agri", "civ-sumer", "tech-bronze"],
    },
    "tech-bronze": {
        "discovered_by": "Metallurgists of Sumer, Anatolia, and the Aegean",
        "related_ids": ["tech-fire", "civ-sumer", "tech-iron"],
    },
    "tech-iron": {
        "discovered_by": "Hittite smiths in Anatolia",
        "related_ids": ["tech-bronze", "civ-rome", "civ-han"],
    },
    "tech-alphabet": {
        "discovered_by": "Phoenician traders of the Levantine coast",
        "related_ids": ["tech-writing", "civ-greece", "civ-rome"],
    },
    "tech-papermsk": {
        "discovered_by": "Cai Lun, official at the Han imperial court",
        "related_ids": ["tech-writing", "tech-print-china", "tech-gutenberg", "civ-han"],
    },
    "tech-gunpowder": {
        "discovered_by": "Daoist alchemists of Tang-era China",
        "related_ids": ["civ-tang", "civ-mongol", "civ-ottoman"],
    },
    "tech-print-china": {
        "discovered_by": "Bi Sheng, Song dynasty artisan",
        "related_ids": ["tech-papermsk", "tech-gutenberg"],
    },
    "tech-gutenberg": {
        "discovered_by": "Johannes Gutenberg in Mainz, Holy Roman Empire",
        "related_ids": ["tech-writing", "tech-papermsk", "tech-print-china", "tech-steam", "tech-web"],
    },
    "tech-steam": {
        "discovered_by": "James Watt and Matthew Boulton, Scottish Enlightenment industrialists",
        "related_ids": ["tech-iron", "tech-gutenberg", "tech-electric", "tech-flight"],
    },
    "tech-electric": {
        "discovered_by": "Thomas Edison's Menlo Park lab (with Joseph Swan in Britain)",
        "related_ids": ["tech-steam", "tech-transistor", "tech-internet"],
    },
    "tech-flight": {
        "discovered_by": "Wilbur and Orville Wright of Dayton, Ohio",
        "related_ids": ["tech-steam", "tech-space", "tech-moon"],
    },
    "tech-antibiotic": {
        "discovered_by": "Alexander Fleming at St. Mary's Hospital, London",
        "related_ids": ["tech-dna", "tech-crispr", "pan-flu-1918", "pan-hiv"],
    },
    "tech-nuclear": {
        "discovered_by": "The Manhattan Project (Oppenheimer, Fermi, Szilard et al.) in the United States",
        "related_ids": ["tech-electric", "tech-space", "civ-ussr", "civ-usa"],
    },
    "tech-transistor": {
        "discovered_by": "John Bardeen, Walter Brattain, and William Shockley at Bell Labs",
        "related_ids": ["tech-electric", "tech-internet", "tech-web", "tech-smart", "tech-ai"],
    },
    "tech-dna": {
        "discovered_by": "James Watson, Francis Crick, Rosalind Franklin, and Maurice Wilkins in Cambridge & London",
        "related_ids": ["tech-antibiotic", "tech-crispr", "pan-covid"],
    },
    "tech-space": {
        "discovered_by": "Sergei Korolev's team at the Soviet space program",
        "related_ids": ["tech-flight", "tech-nuclear", "tech-moon", "civ-ussr"],
    },
    "tech-moon": {
        "discovered_by": "NASA's Apollo Program under Werner von Braun and thousands of engineers",
        "related_ids": ["tech-space", "tech-flight", "civ-usa"],
    },
    "tech-internet": {
        "discovered_by": "ARPA researchers led by Vint Cerf, Bob Kahn, and Leonard Kleinrock",
        "related_ids": ["tech-transistor", "tech-web", "tech-smart", "tech-ai"],
    },
    "tech-web": {
        "discovered_by": "Tim Berners-Lee at CERN",
        "related_ids": ["tech-internet", "tech-smart", "tech-ai"],
    },
    "tech-smart": {
        "discovered_by": "Apple Inc. under Steve Jobs, Cupertino, California",
        "related_ids": ["tech-transistor", "tech-web", "tech-ai"],
    },
    "tech-crispr": {
        "discovered_by": "Jennifer Doudna & Emmanuelle Charpentier (Berkeley / Umeå)",
        "related_ids": ["tech-dna", "tech-antibiotic", "pan-covid"],
    },
    "tech-ai": {
        "discovered_by": "OpenAI and the wider machine-learning research community",
        "related_ids": ["tech-transistor", "tech-internet", "tech-web", "tech-smart"],
    },

    # ------- Civilizations -------
    "civ-jericho": {"discovered_by": "Natufian foragers turned farmers", "related_ids": ["tech-agri", "civ-catalhoyuk", "civ-sumer"]},
    "civ-catalhoyuk": {"discovered_by": "Neolithic Anatolian farmers", "related_ids": ["tech-agri", "tech-pottery", "civ-jericho"]},
    "civ-sumer": {"discovered_by": "Sumerian city-states of southern Mesopotamia", "related_ids": ["tech-writing", "tech-wheel", "tech-bronze", "civ-egypt", "civ-indus"]},
    "civ-egypt": {"discovered_by": "King Narmer, unifying Upper and Lower Egypt", "related_ids": ["tech-writing", "civ-sumer", "civ-greece", "civ-rome"]},
    "civ-indus": {"discovered_by": "Harappan urbanists of the Indus and Sarasvati valleys", "related_ids": ["tech-agri", "civ-sumer", "civ-xia"]},
    "civ-xia": {"discovered_by": "Erlitou culture along the Yellow River", "related_ids": ["tech-bronze", "civ-han", "civ-tang"]},
    "civ-olmec": {"discovered_by": "Olmec heartland peoples of the Gulf coast", "related_ids": ["civ-maya", "civ-aztec"]},
    "civ-greece": {"discovered_by": "Cleisthenes and the Athenian demos", "related_ids": ["tech-alphabet", "civ-rome", "civ-byzantium"]},
    "civ-rome": {"discovered_by": "Augustus (Octavian), first princeps of Rome", "related_ids": ["civ-greece", "civ-byzantium", "pan-antonine", "land-vesuvius"]},
    "civ-han": {"discovered_by": "Emperor Wu of Han and the Silk Road merchants", "related_ids": ["civ-xia", "tech-papermsk", "civ-tang"]},
    "civ-maya": {"discovered_by": "Classic Maya city-states (Tikal, Palenque, Copán)", "related_ids": ["civ-olmec", "civ-aztec"]},
    "civ-byzantium": {"discovered_by": "Justinian I and the Eastern Roman court", "related_ids": ["civ-rome", "pan-justinian", "civ-ottoman"]},
    "civ-islam": {"discovered_by": "The Abbasid Caliphate and the House of Wisdom scholars", "related_ids": ["tech-papermsk", "civ-byzantium", "civ-mali", "civ-ottoman"]},
    "civ-tang": {"discovered_by": "Tang emperors ruling from Chang'an", "related_ids": ["civ-han", "tech-gunpowder", "tech-print-china"]},
    "civ-vikings": {"discovered_by": "Norse seafarers of Scandinavia", "related_ids": ["arc-viking-vinland", "civ-byzantium"]},
    "civ-mongol": {"discovered_by": "Genghis Khan (Temüjin) and the Mongol tribes", "related_ids": ["civ-tang", "pan-blackdeath", "civ-ottoman"]},
    "civ-mali": {"discovered_by": "Mansa Musa I and the Mandé peoples", "related_ids": ["civ-islam", "arc-slave-trade"]},
    "civ-inca": {"discovered_by": "Pachacuti and the Quechua-speaking Andean peoples", "related_ids": ["civ-aztec", "pan-smallpox-am", "arc-columbian-e"]},
    "civ-aztec": {"discovered_by": "Mexica of Tenochtitlán and the Triple Alliance", "related_ids": ["civ-maya", "civ-olmec", "pan-smallpox-am", "pan-cocoliztli"]},
    "civ-ottoman": {"discovered_by": "Mehmed II 'the Conqueror' and the Ottoman dynasty", "related_ids": ["civ-byzantium", "civ-islam", "tech-gunpowder"]},
    "civ-usa": {"discovered_by": "The Second Continental Congress in Philadelphia", "related_ids": ["tech-steam", "tech-flight", "tech-moon", "tech-internet"]},
    "civ-ussr": {"discovered_by": "The Bolsheviks led by Vladimir Lenin", "related_ids": ["tech-space", "tech-nuclear"]},

    # ------- Land transformations -------
    "land-bering": {"discovered_by": "Ancient Beringians / Paleo-Indian founder populations", "related_ids": ["arc-beringia", "civ-olmec", "civ-maya", "civ-inca", "civ-aztec"]},
    "land-doggerland": {"discovered_by": "Mesolithic North Sea communities", "related_ids": ["tech-agri"]},
    "land-sahara-green": {"discovered_by": "African Humid Period pastoralists", "related_ids": ["civ-egypt", "tech-agri"]},
    "land-thera": {"discovered_by": "Minoans of Akrotiri", "related_ids": ["civ-greece"]},
    "land-vesuvius": {"discovered_by": "Rome's Bay of Naples cities (Pompeii, Herculaneum)", "related_ids": ["civ-rome"]},
    "land-krakatoa": {"discovered_by": "Colonial Dutch East Indies observers", "related_ids": ["land-tambora"]},
    "land-tambora": {"discovered_by": "Sumbawa islanders and global observers", "related_ids": ["land-krakatoa"]},
    "land-dustbowl": {"discovered_by": "American Great Plains farmers", "related_ids": []},
    "land-aral": {"discovered_by": "Soviet agricultural planners", "related_ids": ["civ-ussr"]},

    # ------- Pandemics -------
    "pan-antonine": {"discovered_by": "Legionaries returning from the Parthian frontier", "related_ids": ["civ-rome"]},
    "pan-justinian": {"discovered_by": "Yersinia pestis on Egyptian grain ships", "related_ids": ["civ-byzantium", "pan-blackdeath"]},
    "pan-blackdeath": {"discovered_by": "Silk-Road caravans and Genoese ships from Kaffa", "related_ids": ["arc-silkroad-cn-rome", "civ-mongol", "pan-justinian"]},
    "pan-smallpox-am": {"discovered_by": "Spanish conquistadors and Variola virus", "related_ids": ["arc-columbian-e", "civ-inca", "civ-aztec"]},
    "pan-cocoliztli": {"discovered_by": "Post-conquest Salmonella outbreak in New Spain", "related_ids": ["pan-smallpox-am", "civ-aztec"]},
    "pan-cholera": {"discovered_by": "Vibrio cholerae from the Ganges delta", "related_ids": ["arc-columbian-e"]},
    "pan-flu-1918": {"discovered_by": "H1N1 influenza spread by WWI troop movements", "related_ids": ["tech-antibiotic"]},
    "pan-hiv": {"discovered_by": "HIV-1 group M zoonotic spillover in Central Africa", "related_ids": ["tech-antibiotic", "tech-dna"]},
    "pan-covid": {"discovered_by": "SARS-CoV-2 zoonotic spillover, first identified in Wuhan", "related_ids": ["tech-dna", "tech-crispr"]},
}


def get_details(event_id: str):
    return DETAILS.get(event_id, {"discovered_by": None, "related_ids": []})
