"""
Rich details for each event: who discovered/led it, and the lineage graph
(related_ids = events this one directly enabled or was enabled by).
Keeps the main history_data.py compact and lets us layer detail without
churning the primary schema.

RELATED_WHY holds a one-sentence explanation for each (event -> related event)
edge, surfaced in the frontend as a hover tooltip on the Lineage & Trade Chain
panel and woven into the AI Deep Dive's Legacy section, so a connection is
never just a bare name -- it says *why* the two are linked.
"""

DETAILS = {
    # ------- Technology lineage: the great chain of human invention -------
    "tech-fire": {
        "discovered_by": "Early Homo (Homo erectus and later H. sapiens) across East and Southern Africa",
        "related_ids": ["tech-pottery", "tech-agri", "tech-bronze", "tech-neandermed"],
    },
    "tech-agri": {
        "discovered_by": "Neolithic farming communities of the Fertile Crescent (Levant, Anatolia, Zagros foothills)",
        "related_ids": ["tech-fire", "tech-pottery", "civ-jericho", "civ-catalhoyuk", "civ-sumer", "tech-wheel", "tech-dentistry"],
    },
    "tech-pottery": {
        "discovered_by": "Late Pleistocene hunter-gatherers of southern China (Xianrendong Cave)",
        "related_ids": ["tech-fire", "tech-agri", "civ-catalhoyuk"],
    },
    "tech-writing": {
        "discovered_by": "Sumerian temple accountants in Uruk",
        "related_ids": ["civ-sumer", "tech-alphabet", "tech-papermsk", "tech-print-china", "tech-gutenberg", "tech-egyptmed"],
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
    "tech-zoroaster": {
        "discovered_by": "Zoroaster (Zarathustra) in ancient Persia",
        "related_ids": ["tech-torah", "tech-islam", "civ-islam"],
    },
    "tech-upanishads": {
        "discovered_by": "Vedic sages and philosophers of ancient India",
        "related_ids": ["tech-buddhism", "tech-confucius", "civ-indus", "tech-ayurveda"],
    },
    "tech-torah": {
        "discovered_by": "Jewish scribes during and after the Babylonian exile",
        "related_ids": ["tech-zoroaster", "tech-christianity", "tech-islam"],
    },
    "tech-buddhism": {
        "discovered_by": "Siddhartha Gautama (the Buddha) in the Ganges plain",
        "related_ids": ["tech-upanishads", "tech-confucius", "civ-tang"],
    },
    "tech-confucius": {
        "discovered_by": "Confucius (Kong Qiu) and his disciples in the state of Lu",
        "related_ids": ["tech-buddhism", "tech-greekphil", "civ-han"],
    },
    "tech-greekphil": {
        "discovered_by": "Socrates, Plato, and Aristotle in Athens",
        "related_ids": ["tech-confucius", "civ-greece", "tech-enlightenment"],
    },
    "tech-christianity": {
        "discovered_by": "Jesus of Nazareth and his early apostles",
        "related_ids": ["tech-torah", "civ-rome", "tech-islam"],
    },
    "tech-islam": {
        "discovered_by": "The Prophet Muhammad and the early Muslim ummah",
        "related_ids": ["tech-torah", "tech-christianity", "civ-islam", "tech-zoroaster"],
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
        "related_ids": ["tech-writing", "tech-papermsk", "tech-print-china", "tech-steam", "tech-web", "tech-reformation"],
    },
    "tech-reformation": {
        "discovered_by": "Martin Luther and other Protestant reformers",
        "related_ids": ["tech-gutenberg", "tech-christianity", "tech-enlightenment"],
    },
    "tech-enlightenment": {
        "discovered_by": "Enlightenment philosophers including Locke, Voltaire, and Kant",
        "related_ids": ["tech-greekphil", "tech-reformation", "civ-usa"],
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
        "related_ids": ["tech-dna", "tech-crispr", "pan-flu-1918", "pan-hiv", "tech-germtheory", "tech-antiseptic"],
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

    # ------- History of medicine -------
    "tech-neandermed": {
        "discovered_by": "Neanderthals of El Sidrón, identified by Karen Hardy's research team",
        "related_ids": ["tech-fire", "tech-dentistry", "tech-egyptmed"],
    },
    "tech-dentistry": {
        "discovered_by": "An unnamed Late Upper Paleolithic individual and whoever treated him",
        "related_ids": ["tech-neandermed", "tech-agri", "tech-egyptmed"],
    },
    "tech-egyptmed": {
        "discovered_by": "The physician-priests of Sais, with Imhotep formalizing the tradition centuries later",
        "related_ids": ["tech-writing", "civ-egypt", "tech-hippocrates", "tech-dentistry"],
    },
    "tech-ayurveda": {
        "discovered_by": "Sushruta, physician of ancient India",
        "related_ids": ["civ-indus", "tech-upanishads", "tech-hippocrates"],
    },
    "tech-hippocrates": {
        "discovered_by": "Hippocrates of Kos and his school",
        "related_ids": ["tech-egyptmed", "civ-greece", "tech-galen"],
    },
    "tech-galen": {
        "discovered_by": "Galen of Pergamon",
        "related_ids": ["tech-hippocrates", "civ-rome", "tech-ibnsina"],
    },
    "tech-ibnsina": {
        "discovered_by": "Ibn Sina (Avicenna) in Persia",
        "related_ids": ["tech-galen", "civ-islam", "pan-blackdeath"],
    },
    "tech-quarantine": {
        "discovered_by": "The Republic of Ragusa's Great Council",
        "related_ids": ["pan-blackdeath", "tech-ibnsina", "tech-vaccine"],
    },
    "tech-vaccine": {
        "discovered_by": "Edward Jenner in Gloucestershire, England",
        "related_ids": ["pan-smallpox-am", "tech-germtheory", "tech-quarantine"],
    },
    "tech-anesthesia": {
        "discovered_by": "William T. G. Morton in Boston",
        "related_ids": ["tech-antiseptic", "tech-germtheory"],
    },
    "tech-germtheory": {
        "discovered_by": "Louis Pasteur, with Robert Koch's later formalization",
        "related_ids": ["tech-antibiotic", "tech-antiseptic", "tech-vaccine"],
    },
    "tech-antiseptic": {
        "discovered_by": "Joseph Lister in Glasgow",
        "related_ids": ["tech-germtheory", "tech-anesthesia", "tech-antibiotic"],
    },

    # ------- Civilizations -------
    "civ-jericho": {"discovered_by": "Natufian foragers turned farmers", "related_ids": ["tech-agri", "civ-catalhoyuk", "civ-sumer"]},
    "civ-catalhoyuk": {"discovered_by": "Neolithic Anatolian farmers", "related_ids": ["tech-agri", "tech-pottery", "civ-jericho"]},
    "civ-sumer": {"discovered_by": "Sumerian city-states of southern Mesopotamia", "related_ids": ["tech-writing", "tech-wheel", "tech-bronze", "civ-egypt", "civ-indus"]},
    "civ-egypt": {"discovered_by": "King Narmer, unifying Upper and Lower Egypt", "related_ids": ["tech-writing", "civ-sumer", "civ-greece", "civ-rome", "tech-egyptmed"]},
    "civ-indus": {"discovered_by": "Harappan urbanists of the Indus and Sarasvati valleys", "related_ids": ["tech-agri", "civ-sumer", "civ-xia", "tech-ayurveda"]},
    "civ-xia": {"discovered_by": "Erlitou culture along the Yellow River", "related_ids": ["tech-bronze", "civ-han", "civ-tang"]},
    "civ-olmec": {"discovered_by": "Olmec heartland peoples of the Gulf coast", "related_ids": ["civ-maya", "civ-aztec"]},
    "civ-greece": {"discovered_by": "Cleisthenes and the Athenian demos", "related_ids": ["tech-alphabet", "civ-rome", "civ-byzantium", "tech-greekphil", "tech-hippocrates"]},
    "civ-rome": {"discovered_by": "Augustus (Octavian), first princeps of Rome", "related_ids": ["civ-greece", "civ-byzantium", "pan-antonine", "land-vesuvius", "tech-christianity", "tech-galen"]},
    "civ-han": {"discovered_by": "Emperor Wu of Han and the Silk Road merchants", "related_ids": ["civ-xia", "tech-papermsk", "civ-tang", "tech-confucius", "tech-buddhism"]},
    "civ-maya": {"discovered_by": "Classic Maya city-states (Tikal, Palenque, Copán)", "related_ids": ["civ-olmec", "civ-aztec"]},
    "civ-byzantium": {"discovered_by": "Justinian I and the Eastern Roman court", "related_ids": ["civ-rome", "pan-justinian", "civ-ottoman"]},
    "civ-islam": {"discovered_by": "The Abbasid Caliphate and the House of Wisdom scholars", "related_ids": ["tech-papermsk", "civ-byzantium", "civ-mali", "civ-ottoman", "tech-islam", "tech-zoroaster", "tech-ibnsina"]},
    "civ-tang": {"discovered_by": "Tang emperors ruling from Chang'an", "related_ids": ["civ-han", "tech-gunpowder", "tech-print-china", "tech-buddhism"]},
    "civ-vikings": {"discovered_by": "Norse seafarers of Scandinavia", "related_ids": ["arc-viking-vinland", "civ-byzantium"]},
    "civ-mongol": {"discovered_by": "Genghis Khan (Temüjin) and the Mongol tribes", "related_ids": ["civ-tang", "pan-blackdeath", "civ-ottoman"]},
    "civ-mali": {"discovered_by": "Mansa Musa I and the Mandé peoples", "related_ids": ["civ-islam", "arc-slave-trade"]},
    "civ-inca": {"discovered_by": "Pachacuti and the Quechua-speaking Andean peoples", "related_ids": ["civ-aztec", "pan-smallpox-am", "arc-columbian-e"]},
    "civ-aztec": {"discovered_by": "Mexica of Tenochtitlán and the Triple Alliance", "related_ids": ["civ-maya", "civ-olmec", "pan-smallpox-am", "pan-cocoliztli"]},
    "civ-ottoman": {"discovered_by": "Mehmed II 'the Conqueror' and the Ottoman dynasty", "related_ids": ["civ-byzantium", "civ-islam", "tech-gunpowder"]},
    "civ-usa": {"discovered_by": "The Second Continental Congress in Philadelphia", "related_ids": ["tech-steam", "tech-flight", "tech-moon", "tech-internet", "tech-enlightenment"]},
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
    "pan-blackdeath": {"discovered_by": "Silk-Road caravans and Genoese ships from Kaffa", "related_ids": ["arc-silkroad-cn-rome", "civ-mongol", "pan-justinian", "tech-quarantine"]},
    "pan-smallpox-am": {"discovered_by": "Spanish conquistadors and Variola virus", "related_ids": ["arc-columbian-e", "civ-inca", "civ-aztec", "tech-vaccine"]},
    "pan-cocoliztli": {"discovered_by": "Post-conquest Salmonella outbreak in New Spain", "related_ids": ["pan-smallpox-am", "civ-aztec"]},
    "pan-cholera": {"discovered_by": "Vibrio cholerae from the Ganges delta", "related_ids": ["arc-columbian-e"]},
    "pan-flu-1918": {"discovered_by": "H1N1 influenza spread by WWI troop movements", "related_ids": ["tech-antibiotic"]},
    "pan-hiv": {"discovered_by": "HIV-1 group M zoonotic spillover in Central Africa", "related_ids": ["tech-antibiotic", "tech-dna"]},
    "pan-covid": {"discovered_by": "SARS-CoV-2 zoonotic spillover, first identified in Wuhan", "related_ids": ["tech-dna", "tech-crispr"]},
}


# One-sentence reason for every (event_id -> related_id) edge above.
# Missing pairs simply render without a tooltip, so this can be filled in
# gradually without breaking anything.
RELATED_WHY = {
    "tech-fire": {
        "tech-pottery": "Firing clay into durable ceramics required the sustained, controllable heat that mastering fire first made possible.",
        "tech-agri": "Cooking with fire unlocked nutrients in cereals and legumes, making a farming-based diet worthwhile.",
        "tech-bronze": "Smelting copper and tin into bronze demanded furnace temperatures only fire-based metallurgy could reach.",
        "tech-neandermed": "Neanderthals mastered fire themselves, and the same resourceful use of their environment shows up in their selection of medicinal plants.",
    },
    "tech-agri": {
        "tech-fire": "Fire-cooked grains made cultivated crops like wheat and barley nutritionally worthwhile to grow at scale.",
        "tech-pottery": "Storing surplus grain and dairy from farming created the need for sealed ceramic containers.",
        "tech-dentistry": "The rise of starchy, grain-based farming diets closely tracks the sharp increase in tooth decay visible in the skeletal record from this era onward.",
        "civ-jericho": "Jericho's Natufian foragers turned farmers, becoming one of the first year-round settlements founded on grain agriculture.",
        "civ-catalhoyuk": "Çatalhöyük's dense agricultural surplus supported one of the earliest large proto-urban communities.",
        "civ-sumer": "Reliable irrigation-based agriculture in Mesopotamia produced the food surplus that let Sumerian cities grow.",
        "tech-wheel": "Farming's need to move heavy loads of grain and building material drove early wheeled-cart innovation.",
    },
    "tech-pottery": {
        "tech-fire": "Kiln-firing pottery is only possible once controlled, high-temperature fire had already been mastered.",
        "tech-agri": "Ceramic storage jars let farming communities keep grain and seed stock safe between harvests.",
        "civ-catalhoyuk": "Çatalhöyük's households used pottery extensively for storage and cooking, a hallmark of its settled lifestyle.",
    },
    "tech-writing": {
        "civ-sumer": "Sumerian temple bureaucrats invented cuneiform specifically to track the city-state's growing trade and tax records.",
        "tech-alphabet": "The Phoenicians simplified cumbersome cuneiform- and hieroglyph-style writing into a compact 22-letter alphabet.",
        "tech-egyptmed": "Egyptian physicians relied on writing to record and pass down the case studies collected in texts like the Edwin Smith Papyrus.",
        "tech-papermsk": "Cheap paper gave writing a portable, mass-producible surface far beyond clay tablets or papyrus.",
        "tech-print-china": "Movable type mechanized the reproduction of written texts that scribes had previously copied by hand.",
        "tech-gutenberg": "Gutenberg's press automated the same core idea — reproducing written words — at industrial scale in Europe.",
    },
    "tech-wheel": {
        "tech-agri": "Wheeled carts let farmers haul harvests and irrigation materials far more efficiently than by hand or sled.",
        "civ-sumer": "Sumerians paired the wheel with draft animals to build the first wheeled transport and war chariots.",
        "tech-bronze": "Bronze fittings made wheels stronger and more durable than wood alone.",
    },
    "tech-bronze": {
        "tech-fire": "Alloying copper and tin into bronze required furnace heat well beyond a simple cooking fire.",
        "civ-sumer": "Sumerian metallurgists were among the first to mass-produce bronze tools, weapons, and trade goods.",
        "tech-iron": "Bronze's reliance on scarce tin trade routes made iron — smeltable from common ore — an eventual replacement.",
    },
    "tech-iron": {
        "tech-bronze": "Iron smelting was developed as a stronger, more available alternative once bronze's supply chains grew strained.",
        "civ-rome": "Iron weapons and tools underpinned Roman military and agricultural dominance across the empire.",
        "civ-han": "Han China's ironworking industry, among the era's most advanced, powered its agriculture and armies.",
    },
    "tech-alphabet": {
        "tech-writing": "The Phoenician alphabet descended directly from earlier writing systems, stripped down for speed and trade.",
        "civ-greece": "The Greeks adapted the Phoenician alphabet, adding vowels to create the first true alphabet.",
        "civ-rome": "Rome inherited its Latin alphabet from the Greek adaptation of Phoenician letters.",
    },
    "tech-zoroaster": {
        "tech-torah": "Zoroastrian ideas about a single supreme god and cosmic judgment likely influenced Jewish theology during the Babylonian exile.",
        "tech-islam": "Zoroastrian Persia was conquered by early Muslim armies, and some of its dualistic ideas echo in later Islamic thought.",
        "civ-islam": "The Abbasid Caliphate's heartland was built atop former Zoroastrian Persian territory and absorbed much of its scholarly tradition.",
    },
    "tech-upanishads": {
        "tech-buddhism": "The Buddha trained in and ultimately broke from the Vedic/Upanishadic tradition his philosophy was formed against.",
        "tech-confucius": "Both emerged in the same Axial Age wave of systematic philosophical thought spreading independently across Eurasia.",
        "tech-ayurveda": "Ayurvedic medicine developed within the same Vedic intellectual world that produced the Upanishads.",
        "civ-indus": "The Upanishads grew out of the same Indian subcontinent civilization the earlier Indus Valley culture had inhabited.",
    },
    "tech-torah": {
        "tech-zoroaster": "Jewish monotheism developed further during the Babylonian exile, likely absorbing some Zoroastrian theological influence.",
        "tech-christianity": "Christianity emerged from within Judaism, treating the Hebrew Bible as its own foundational scripture.",
        "tech-islam": "Islam reveres the Torah's prophets and treats it as an earlier revelation later completed by the Quran.",
    },
    "tech-buddhism": {
        "tech-upanishads": "Buddhism arose directly in dialogue with, and partly in reaction against, Upanishadic Vedic philosophy.",
        "tech-confucius": "Buddhism and Confucianism both took shape during Eurasia's Axial Age of new ethical and philosophical systems.",
        "civ-tang": "Buddhism spread from India into China along Silk Road trade routes and flourished under Tang dynasty patronage.",
    },
    "tech-confucius": {
        "tech-buddhism": "Confucianism and Buddhism later coexisted and blended in Chinese thought, especially from the Tang dynasty onward.",
        "tech-greekphil": "Confucius and the early Greek philosophers were near-exact contemporaries in history's Axial Age, developing ethics independently.",
        "civ-han": "Han dynasty emperors adopted Confucianism as the empire's official state philosophy.",
    },
    "tech-greekphil": {
        "tech-confucius": "Greek and Chinese philosophy emerged in the same Axial Age window, each systematizing ethics and reason independently.",
        "civ-greece": "Athenian democracy and Greek philosophy developed together, each shaping the other's ideas about reason and citizenship.",
        "tech-enlightenment": "Enlightenment thinkers explicitly revived Greek rationalist and Socratic methods after centuries of eclipse.",
    },
    "tech-christianity": {
        "tech-torah": "Christianity's earliest followers were Jews who treated the Hebrew Bible as scripture pointing toward Jesus.",
        "civ-rome": "Christianity spread through the Roman Empire's road and trade networks and later became its official religion.",
        "tech-islam": "Islam recognizes Jesus as a major prophet and shares much of Christianity's Abrahamic scriptural lineage.",
    },
    "tech-islam": {
        "tech-torah": "Islam considers the Torah an earlier scripture from the same prophetic lineage the Quran completes.",
        "tech-christianity": "Islam and Christianity both trace their roots to the same Abrahamic tradition and revere many of the same figures.",
        "civ-islam": "The Abbasid Caliphate's Golden Age of science and philosophy grew directly out of the faith Muhammad founded.",
        "tech-zoroaster": "Muslim armies conquered Zoroastrian Persia within decades of Islam's founding, absorbing its scholars and institutions.",
    },
    "tech-papermsk": {
        "tech-writing": "Paper gave the written word a cheap, lightweight surface to replace bulky bamboo strips and silk.",
        "tech-print-china": "Bi Sheng's movable type was only practical once cheap paper existed to print onto.",
        "tech-gutenberg": "Papermaking techniques eventually reached Europe, supplying the material Gutenberg's press needed to work at scale.",
        "civ-han": "Cai Lun refined papermaking as an official at the Han imperial court.",
    },
    "tech-gunpowder": {
        "civ-tang": "Tang-era Daoist alchemists stumbled onto gunpowder while experimenting with immortality elixirs.",
        "civ-mongol": "Mongol armies helped carry gunpowder weapons and knowledge westward across Eurasia.",
        "civ-ottoman": "Ottoman armies used massive gunpowder cannons to breach Constantinople's ancient walls in 1453.",
    },
    "tech-print-china": {
        "tech-papermsk": "Movable type needed cheap paper to print onto in volume.",
        "tech-gutenberg": "Bi Sheng's ceramic movable type anticipated Gutenberg's metal type by four centuries.",
    },
    "tech-gutenberg": {
        "tech-writing": "Gutenberg's press mass-produced the same written word that scribes once copied one letter at a time.",
        "tech-papermsk": "European papermaking, ultimately descended from Chinese techniques, gave Gutenberg's press an affordable material to print on.",
        "tech-print-china": "Gutenberg independently reinvented movable type in Europe, unaware Bi Sheng had done so in China centuries earlier.",
        "tech-steam": "The information explosion the printing press triggered helped fuel the scientific and engineering culture behind the steam engine.",
        "tech-web": "The printing press was the first technology to make information radically cheaper to copy and spread — the web did the same for the digital age.",
        "tech-reformation": "Luther's Ninety-Five Theses spread across Europe within weeks specifically because Gutenberg's press could print them by the thousands.",
    },
    "tech-reformation": {
        "tech-gutenberg": "Luther's Ninety-Five Theses spread across Europe within weeks only because Gutenberg's press could copy them by the thousands.",
        "tech-christianity": "The Reformation permanently split Western Christianity into Catholic and Protestant branches.",
        "tech-enlightenment": "The Reformation's challenge to religious authority helped open the door to Enlightenment questioning of authority more broadly.",
    },
    "tech-enlightenment": {
        "tech-greekphil": "Enlightenment philosophers consciously revived Greek ideals of reason and rational inquiry.",
        "tech-reformation": "The Reformation's precedent of questioning religious authority paved the way for Enlightenment political and scientific skepticism.",
        "civ-usa": "Enlightenment ideas about natural rights and government directly shaped the founding documents of the United States.",
    },
    "tech-steam": {
        "tech-iron": "Iron provided the strong, heat-tolerant material steam engines needed for boilers and pistons.",
        "tech-gutenberg": "Printed technical manuals and scientific journals helped spread steam-engine designs across Europe.",
        "tech-electric": "Steam-driven generators were the first practical way to produce electricity at scale.",
        "tech-flight": "Steam-era engineering culture laid the groundwork for the internal combustion engines that made flight possible.",
    },
    "tech-electric": {
        "tech-steam": "Early electrical grids were powered by steam turbines long before other generation methods existed.",
        "tech-transistor": "Reliable electricity was the prerequisite for the electronic circuits transistors are built from.",
        "tech-internet": "The internet's servers and cables run entirely on the electrical infrastructure this era established.",
    },
    "tech-flight": {
        "tech-steam": "Engine science pioneered in the steam era fed directly into the internal combustion engines that powered the Wrights' aircraft.",
        "tech-space": "Powered flight proved humans could master controlled flight, a direct conceptual precursor to spaceflight.",
        "tech-moon": "Apollo's rockets descended from six decades of aeronautical engineering that began at Kitty Hawk.",
    },
    "tech-antibiotic": {
        "tech-dna": "Understanding DNA later explained exactly how antibiotics disrupt bacterial cells at the molecular level.",
        "tech-crispr": "CRISPR now lets scientists directly edit the genes behind the antibiotic resistance that penicillin's overuse helped create.",
        "pan-flu-1918": "The 1918 flu killed millions partly through secondary bacterial pneumonia — exactly what antibiotics would later treat.",
        "pan-hiv": "Antibiotics treat the opportunistic infections that HIV/AIDS patients' weakened immune systems become vulnerable to.",
        "tech-germtheory": "Fleming's discovery only made sense once germ theory had already established that specific microbes, not bad air, cause disease.",
        "tech-antiseptic": "Antiseptic surgery proved that killing germs saved lives, setting the stage for antibiotics as an internal, systemic version of the same idea.",
    },
    "tech-nuclear": {
        "tech-electric": "The same fission reactions that power atomic weapons also generate electricity in nuclear power plants.",
        "tech-space": "Nuclear-capable rockets and Cold War rivalry directly accelerated the space race that followed.",
        "civ-ussr": "The USSR's own 1949 atomic bomb test turned nuclear weapons into a defining feature of the Cold War.",
        "civ-usa": "The Manhattan Project was a US-led wartime effort that reshaped America's global military position.",
    },
    "tech-transistor": {
        "tech-electric": "Transistors are fundamentally electrical switches, dependent on the same grids and circuits this era established.",
        "tech-internet": "Transistorized computers were the hardware that made networked computing, and eventually the internet, possible.",
        "tech-web": "Every web server and browser runs on chips built from transistors.",
        "tech-smart": "Smartphones pack billions of transistors onto a single chip to fit a computer in your pocket.",
        "tech-ai": "Modern AI models run on GPUs containing billions of transistors performing trillions of calculations.",
    },
    "tech-dna": {
        "tech-antibiotic": "DNA's structure revealed exactly how bacteria mutate to develop antibiotic resistance.",
        "tech-crispr": "CRISPR is a direct tool for editing the DNA whose structure Watson and Crick first described.",
        "pan-covid": "Genomic sequencing of SARS-CoV-2's RNA, based on techniques DNA research pioneered, let scientists design vaccines within weeks.",
    },
    "tech-space": {
        "tech-flight": "Rocket engineering built directly on decades of aerodynamic knowledge from powered flight.",
        "tech-nuclear": "Cold War nuclear rivalry between the US and USSR was the political engine behind the space race.",
        "tech-moon": "Sputnik's launch triggered the US response that culminated in the Apollo moon landings.",
        "civ-ussr": "The Soviet Union's state space program launched Sputnik, opening the space age.",
    },
    "tech-moon": {
        "tech-space": "Apollo was the direct continuation of the space program Sputnik had launched a decade earlier.",
        "tech-flight": "Apollo's flight control systems descended from decades of aviation engineering.",
        "civ-usa": "The Apollo program was a US government effort driven by Cold War competition with the Soviet Union.",
    },
    "tech-internet": {
        "tech-transistor": "ARPANET's early computers depended on transistorized electronics to process and route data.",
        "tech-web": "The World Wide Web was built as a layer of hypertext running on top of the internet's existing network.",
        "tech-smart": "Smartphones brought the internet into everyone's pocket, transforming it from a desktop technology into a constant presence.",
        "tech-ai": "Today's AI models are trained on vast troves of text and data harvested from the internet.",
    },
    "tech-web": {
        "tech-internet": "The Web is a system of linked documents that runs on top of the internet's existing infrastructure.",
        "tech-smart": "Mobile browsers brought the Web to smartphones, making it accessible anywhere.",
        "tech-ai": "Web-scraped text became the primary training data for large language models decades later.",
    },
    "tech-smart": {
        "tech-transistor": "Smartphones exist because transistor miniaturization eventually fit a full computer onto a pocket-sized chip.",
        "tech-web": "The iPhone's browser made the full Web usable on a handheld device for the first time.",
        "tech-ai": "Smartphones later became the primary way people access AI assistants and chatbots.",
    },
    "tech-crispr": {
        "tech-dna": "CRISPR gene editing directly manipulates the DNA molecule Watson and Crick first described.",
        "tech-antibiotic": "CRISPR-based diagnostics can now detect antibiotic-resistant bacteria far faster than traditional lab culturing.",
        "pan-covid": "CRISPR-based diagnostic tests were adapted to rapidly detect SARS-CoV-2 infections during the pandemic.",
    },
    "tech-ai": {
        "tech-transistor": "Modern AI training runs on GPU chips containing billions of transistors.",
        "tech-internet": "Large language models are trained largely on text harvested from the internet.",
        "tech-web": "Much of an AI model's training data comes from webpages crawled across the World Wide Web.",
        "tech-smart": "Smartphones are now the main way billions of people interact with AI assistants daily.",
    },

    # ------- History of medicine -------
    "tech-neandermed": {
        "tech-fire": "Both fire use and medicinal plant selection show hominins deliberately manipulating their environment for survival, tens of thousands of years before Homo sapiens dominate the record.",
        "tech-dentistry": "Tens of thousands of years later, Homo sapiens were still acting on the same basic impulse: using whatever was at hand to treat pain and disease.",
        "tech-egyptmed": "The instinct to treat illness with deliberately chosen remedies, documented here first in Neanderthals, is the same instinct that eventually grew into Egypt's organized medical institutions.",
    },
    "tech-dentistry": {
        "tech-neandermed": "This Late Paleolithic dental treatment continues an impulse to actively treat pain and disease that predates Homo sapiens entirely, first documented in Neanderthals tens of thousands of years earlier.",
        "tech-agri": "This treatment predates the Neolithic agricultural revolution, whose new starchy, grain-heavy diets would soon make cavities and tooth decay far more common.",
        "tech-egyptmed": "This flint-tool treatment shows people were already practicing deliberate dental care over 8,000 years before Egypt built its first known medical institutions.",
    },
    "tech-egyptmed": {
        "tech-writing": "Egyptian physicians relied on hieroglyphic writing to record and pass down detailed case studies like those in the Edwin Smith Papyrus.",
        "civ-egypt": "This systematic medical tradition developed within, and was preserved by, the scribal institutions of ancient Egyptian civilization.",
        "tech-hippocrates": "Greek physicians including Hippocrates studied Egyptian medical knowledge, one of several traditions his school built on and moved beyond.",
        "tech-dentistry": "Egypt's medical tradition inherited an impulse to treat disease and pain that already had a roughly 9,000-year history by the time Sais's physicians were practicing.",
    },
    "tech-ayurveda": {
        "civ-indus": "Ayurvedic medicine developed within the same Indian subcontinent civilization the Indus Valley culture had inhabited centuries earlier.",
        "tech-upanishads": "Ayurveda grew out of the same Vedic intellectual tradition that produced the Upanishads' philosophy.",
        "tech-hippocrates": "Sushruta's surgical tradition and Hippocratic medicine arose within a few centuries of each other as independent, parallel foundings of systematic medicine.",
    },
    "tech-hippocrates": {
        "tech-egyptmed": "Greek physicians drew on older Egyptian medical knowledge even as Hippocrates broke sharply from its more ritual elements.",
        "civ-greece": "Hippocrates and his school taught and practiced on the Greek island of Kos, within the wider world of classical Greek civilization.",
        "tech-galen": "Roman-era physicians, above all Galen, treated Hippocratic texts as the founding authority of Western medicine.",
    },
    "tech-galen": {
        "tech-hippocrates": "Galen explicitly built his own medical system as a systematic elaboration of Hippocratic principles.",
        "civ-rome": "Galen practiced in Rome itself, and his writings became the medical authority of the Roman Empire for centuries.",
        "tech-ibnsina": "Islamic physicians including Ibn Sina translated, preserved, and expanded on Galen's anatomical writings after Rome's fall.",
    },
    "tech-ibnsina": {
        "tech-galen": "Ibn Sina's Canon systematized and built directly on Galen's anatomical and physiological framework.",
        "civ-islam": "The Canon of Medicine was produced within the Islamic Golden Age's flourishing of translation and scientific scholarship.",
        "pan-blackdeath": "The Canon's early theory of person-to-person contagion anticipated the public-health thinking the Black Death would later force into practice.",
    },
    "tech-quarantine": {
        "pan-blackdeath": "Ragusa's quarantine law was a direct emergency response to the repeated waves of plague sweeping the Mediterranean.",
        "tech-ibnsina": "The idea that disease could pass person-to-person, which quarantine assumes, echoed contagion theories already circulating from Ibn Sina's Canon.",
        "tech-vaccine": "Quarantine and vaccination were the two great pre-germ-theory public-health tools, developed centuries apart to fight the same kinds of epidemics.",
    },
    "tech-vaccine": {
        "pan-smallpox-am": "Jenner's vaccine targeted the very disease, smallpox, that had devastated the Americas three centuries earlier.",
        "tech-germtheory": "Jenner's vaccine worked decades before germ theory explained why — Pasteur's later work finally revealed the mechanism behind it.",
        "tech-quarantine": "Vaccination gave doctors a tool that could prevent disease directly, succeeding centuries of quarantine's containment-only approach.",
    },
    "tech-anesthesia": {
        "tech-antiseptic": "Anesthesia and antiseptic technique together, within a generation of each other, turned surgery from a brutal last resort into a controlled science.",
        "tech-germtheory": "Pain-free surgery under anesthesia created longer, more invasive operations, which made Lister's germ-theory-based antiseptic methods urgently necessary.",
    },
    "tech-germtheory": {
        "tech-antibiotic": "Germ theory's proof that specific microbes cause disease was the conceptual foundation Fleming's antibiotic discovery depended on.",
        "tech-antiseptic": "Joseph Lister directly applied Pasteur's germ theory to surgery, using carbolic acid to kill the microbes germ theory identified.",
        "tech-vaccine": "Germ theory retroactively explained, decades later, exactly why Jenner's smallpox vaccine had worked.",
    },
    "tech-antiseptic": {
        "tech-germtheory": "Lister built antiseptic surgery directly on Pasteur's germ theory, translating a laboratory discovery into an operating-room practice.",
        "tech-anesthesia": "Anesthesia's longer, more complex surgeries made antiseptic technique urgently necessary to prevent fatal post-operative infections.",
        "tech-antibiotic": "Antiseptic surgery proved that targeting microbes saved lives, foreshadowing the internal, systemic microbe-killing that antibiotics would achieve.",
    },

    # ------- Civilizations -------
    "civ-jericho": {
        "tech-agri": "Jericho's Natufian inhabitants transitioned from foraging to farming, becoming one of history's first agricultural settlements.",
        "civ-catalhoyuk": "Jericho and Çatalhöyük were contemporaneous early Neolithic settlements built on the same new farming economy.",
        "civ-sumer": "The settled, walled-town model Jericho pioneered anticipated the larger city-states Sumer would later build.",
    },
    "civ-catalhoyuk": {
        "tech-agri": "Çatalhöyük's dense population was sustained entirely by surrounding cultivated fields.",
        "tech-pottery": "Çatalhöyük households relied heavily on pottery for storage and cooking.",
        "civ-jericho": "Çatalhöyük and Jericho were sister settlements of the same early farming revolution.",
    },
    "civ-sumer": {
        "tech-writing": "Sumerian scribes invented cuneiform to manage the city-states' growing trade and temple records.",
        "tech-wheel": "Sumerians were among the first to put the wheel to practical use in carts and war chariots.",
        "tech-bronze": "Sumerian metallurgists were pioneers in smelting and working bronze at scale.",
        "civ-egypt": "Sumer and Egypt developed writing and city-based governance around the same era, likely through indirect trade contact.",
        "civ-indus": "The Indus Valley civilization traded with Sumer via Persian Gulf sea routes, exchanging goods and ideas.",
    },
    "civ-egypt": {
        "tech-writing": "Egyptian hieroglyphs developed as one of the world's earliest independent writing systems.",
        "civ-sumer": "Egypt and Sumer developed writing and monumental architecture in parallel, likely influencing each other through trade.",
        "tech-egyptmed": "Egyptian physicians produced some of the ancient world's most systematic medical and surgical texts, like the Edwin Smith Papyrus.",
        "civ-greece": "Greek scholars and travelers studied Egyptian mathematics, astronomy, and religion extensively.",
        "civ-rome": "Egypt became a prized Roman province after Cleopatra's defeat, feeding the empire with grain.",
    },
    "civ-indus": {
        "tech-agri": "The Indus Valley's advanced irrigation systems supported one of the ancient world's largest farming populations.",
        "civ-sumer": "Harappan merchants traded seals, beads, and goods with Sumer via the Persian Gulf.",
        "tech-ayurveda": "Ayurvedic medicine grew out of the same Indian subcontinent civilization the Indus Valley culture had inhabited centuries earlier.",
        "civ-xia": "The Indus and early Chinese Xia civilizations both built early Bronze Age urban cultures independently.",
    },
    "civ-xia": {
        "tech-bronze": "Xia-era Erlitou culture produced some of China's earliest bronze ritual vessels and weapons.",
        "civ-han": "Xia is traditionally regarded as the first dynasty in the lineage that leads to Han China.",
        "civ-tang": "The dynastic model Xia began was carried forward, through many dynasties, into Tang China.",
    },
    "civ-olmec": {
        "civ-maya": "The Olmecs are considered Mesoamerica's 'mother culture,' whose calendar and religious ideas the Maya inherited.",
        "civ-aztec": "Olmec religious and artistic motifs echoed for millennia into later Aztec civilization.",
    },
    "civ-greece": {
        "tech-alphabet": "The Greeks adapted the Phoenician alphabet, adding vowels to create the first true alphabet.",
        "civ-rome": "Rome absorbed enormous amounts of Greek art, philosophy, religion, and political thought.",
        "civ-byzantium": "The Byzantine Empire preserved and continued Greek language, culture, and administration for another thousand years.",
        "tech-greekphil": "Classical Athens was the direct setting where Socrates, Plato, and Aristotle developed Western philosophy.",
        "tech-hippocrates": "Hippocrates and his school taught on the Greek island of Kos, founding the clinical, non-religious medicine of the classical Greek world.",
    },
    "civ-rome": {
        "civ-greece": "Rome absorbed Greek philosophy, religion, and art wholesale into its own culture.",
        "civ-byzantium": "The Byzantine Empire was the direct continuation of Rome's eastern half after the western half collapsed.",
        "pan-antonine": "The Antonine Plague struck the Roman Empire at the height of its power, killing millions of citizens.",
        "land-vesuvius": "Vesuvius's eruption buried Roman cities like Pompeii and Herculaneum within the empire's own territory.",
        "tech-christianity": "Christianity spread through Roman roads and trade networks and eventually became the empire's official religion.",
        "tech-galen": "Galen practiced and wrote in Rome, and his medical writings became the unchallenged authority across the empire for centuries.",
    },
    "civ-han": {
        "civ-xia": "Han dynasty rulers saw themselves as heirs to the same Chinese dynastic lineage beginning with Xia.",
        "tech-papermsk": "Cai Lun refined papermaking as an official serving the Han imperial court.",
        "civ-tang": "Han China set the administrative and cultural template that later Tang China would build upon.",
        "tech-confucius": "Han emperors adopted Confucianism as the empire's official state philosophy.",
        "tech-buddhism": "Buddhism first entered China from India during the Han dynasty via Silk Road trade routes.",
    },
    "civ-maya": {
        "civ-olmec": "Maya civilization inherited its calendar system and religious iconography from the earlier Olmec culture.",
        "civ-aztec": "Aztec cosmology and calendar systems drew heavily on the earlier Maya tradition.",
    },
    "civ-byzantium": {
        "civ-rome": "Byzantium was literally the Eastern Roman Empire, continuing Roman law and administration for centuries.",
        "pan-justinian": "The Plague of Justinian struck Constantinople at the height of Byzantine imperial power under Justinian I.",
        "civ-ottoman": "The Ottoman Empire conquered Constantinople in 1453, ending Byzantium and inheriting much of its territory.",
    },
    "civ-islam": {
        "tech-papermsk": "Papermaking technology reached the Islamic world from China, fueling the Abbasid Caliphate's House of Wisdom scholarship.",
        "civ-byzantium": "The Abbasid Caliphate and Byzantine Empire were long-standing rival powers along the eastern Mediterranean.",
        "civ-mali": "Islam spread into West Africa through trans-Saharan trade routes, reaching the Mali Empire.",
        "civ-ottoman": "The Ottoman Empire later became the dominant power of the Islamic world after the Abbasid Caliphate's decline.",
        "tech-islam": "The Abbasid Caliphate's Golden Age of science and philosophy grew directly out of the faith Muhammad founded.",
        "tech-ibnsina": "Ibn Sina wrote his Canon of Medicine under the intellectual patronage of the Islamic Golden Age the Abbasid Caliphate sponsored.",
        "tech-zoroaster": "The Caliphate absorbed the scholarly and administrative traditions of the Zoroastrian Persian empire it conquered.",
    },
    "civ-tang": {
        "civ-han": "Tang China inherited and expanded on the administrative and cultural foundations Han China had built centuries earlier.",
        "tech-gunpowder": "Tang-era Daoist alchemists first stumbled onto gunpowder while searching for immortality elixirs.",
        "tech-print-china": "Movable-type printing under the Song dynasty built directly on Tang-era woodblock printing traditions.",
        "tech-buddhism": "Buddhism flourished across Tang China, becoming deeply woven into its art, literature, and court life.",
    },
    "civ-vikings": {
        "arc-viking-vinland": "Norse voyagers who raided and traded across Europe eventually pushed as far west as Vinland in North America.",
        "civ-byzantium": "Norse traders and mercenaries — the Varangian Guard — served directly within the Byzantine imperial court.",
    },
    "civ-mongol": {
        "civ-tang": "Mongol conquests eventually swept through territory once held by Tang-successor Chinese dynasties.",
        "pan-blackdeath": "Mongol trade and military routes across Eurasia are widely believed to have helped carry the Black Death westward.",
        "civ-ottoman": "The Ottoman dynasty rose in Anatolia in the power vacuum the Mongol invasions left behind.",
    },
    "civ-mali": {
        "civ-islam": "Mansa Musa's Mali Empire was a devoutly Muslim state deeply connected to the wider Islamic world.",
        "arc-slave-trade": "West African kingdoms including Mali were later drawn into trans-Atlantic slave trade networks.",
    },
    "civ-inca": {
        "civ-aztec": "The Inca and Aztec empires were the two largest Indigenous American civilizations when Europeans arrived.",
        "pan-smallpox-am": "Smallpox, introduced by Europeans, devastated the Inca population even before Spanish conquistadors fully arrived.",
        "arc-columbian-e": "The Inca Empire was permanently transformed by the biological and material exchange the Columbian Exchange triggered.",
    },
    "civ-aztec": {
        "civ-maya": "The Aztecs inherited calendar systems and religious concepts from the earlier Maya civilization.",
        "civ-olmec": "Aztec cosmology traced its symbolic and religious roots back to the ancient Olmec 'mother culture.'",
        "pan-smallpox-am": "Smallpox devastated the Aztec population during the Spanish conquest of Tenochtitlán.",
        "pan-cocoliztli": "The Cocoliztli epidemics struck Aztec territory in the decades following the initial conquest and smallpox outbreak.",
    },
    "civ-ottoman": {
        "civ-byzantium": "The Ottomans conquered Constantinople in 1453, ending the Byzantine Empire and inheriting its capital.",
        "civ-islam": "The Ottoman Empire became the last great Islamic caliphate after Abbasid power faded.",
        "tech-gunpowder": "Ottoman gunpowder cannons were decisive in breaching Constantinople's ancient walls.",
    },
    "civ-usa": {
        "tech-steam": "American industrialization in the 19th century was built on steam-powered factories and railroads.",
        "tech-flight": "The Wright brothers achieved the first powered flight on American soil at Kitty Hawk.",
        "tech-moon": "NASA's Apollo program was a US government effort that put the first humans on the Moon.",
        "tech-internet": "ARPANET, the internet's direct ancestor, was built by US Department of Defense-funded researchers.",
        "tech-enlightenment": "The Declaration of Independence and US Constitution were built directly on Enlightenment political philosophy.",
    },
    "civ-ussr": {
        "tech-space": "The Soviet space program launched Sputnik, humanity's first artificial satellite.",
        "tech-nuclear": "The USSR's 1949 atomic bomb test made it the world's second nuclear power, defining the Cold War.",
    },

    # ------- Land transformations -------
    "land-bering": {
        "arc-beringia": "The Bering Land Bridge was the physical route early humans walked across during the exposure this event describes.",
        "civ-olmec": "The Olmec are believed to descend from populations who crossed into the Americas via the Bering Land Bridge.",
        "civ-maya": "Maya ancestors, like other Indigenous Americans, trace their deepest roots to Bering Land Bridge migrations.",
        "civ-inca": "Inca ancestors ultimately descend from the same founding populations who crossed via the Bering Land Bridge.",
        "civ-aztec": "Aztec ancestors trace their deepest lineage back to the same Bering Land Bridge migrations as other Indigenous Americans.",
    },
    "land-doggerland": {
        "tech-agri": "Rising seas that drowned Doggerland coincided with the same post-glacial period farming was beginning to spread across Europe.",
    },
    "land-sahara-green": {
        "civ-egypt": "As the Sahara dried out, displaced pastoralist populations are thought to have contributed to the rise of settled agriculture along the Nile.",
        "tech-agri": "The drying Sahara pushed African pastoralist communities toward the more reliable farming the Nile valley allowed.",
    },
    "land-thera": {
        "civ-greece": "The Thera eruption devastated Minoan civilization, a precursor culture whose decline helped clear the way for Mycenaean and later Greek dominance in the Aegean.",
    },
    "land-vesuvius": {
        "civ-rome": "Vesuvius buried the Roman cities of Pompeii and Herculaneum, preserving a vivid snapshot of everyday Roman life.",
    },
    "land-krakatoa": {
        "land-tambora": "Krakatoa and Tambora were the 19th century's two most catastrophic volcanic eruptions, both reshaping global climate for years afterward.",
    },
    "land-tambora": {
        "land-krakatoa": "Tambora and Krakatoa were the 19th century's two most catastrophic volcanic eruptions, both reshaping global climate for years afterward.",
    },
    "land-aral": {
        "civ-ussr": "Soviet planners diverted the rivers feeding the Aral Sea for cotton irrigation, causing it to shrink catastrophically.",
    },

    # ------- Pandemics -------
    "pan-antonine": {
        "civ-rome": "The Antonine Plague struck at the height of Roman imperial power, killing millions of citizens and soldiers.",
    },
    "pan-justinian": {
        "civ-byzantium": "The Plague of Justinian devastated Constantinople and weakened the Byzantine Empire's reconquest ambitions.",
        "pan-blackdeath": "The Plague of Justinian and the Black Death were both caused by the same bacterium, Yersinia pestis, centuries apart.",
    },
    "pan-blackdeath": {
        "arc-silkroad-cn-rome": "The Black Death traveled west along the same Silk Road trade routes that connected China to Europe for centuries.",
        "civ-mongol": "Mongol trade and military networks across Eurasia are widely thought to have helped spread the plague westward.",
        "pan-justinian": "The Black Death and the Plague of Justinian were both caused by the same bacterium, Yersinia pestis, centuries apart.",
        "tech-quarantine": "The Black Death's devastation directly drove Ragusa to invent mandatory quarantine, the first codified public-health response of its kind.",
    },
    "pan-smallpox-am": {
        "arc-columbian-e": "Smallpox was one of the deadliest diseases Europeans introduced to the Americas as part of the Columbian Exchange.",
        "civ-inca": "Smallpox devastated the Inca population, weakening the empire even before Spanish conquistadors fully arrived.",
        "civ-aztec": "Smallpox ravaged Tenochtitlán during the Spanish conquest of the Aztec Empire.",
        "tech-vaccine": "The same disease that devastated the Americas was, three centuries later, the first to be defeated by vaccination.",
    },
    "pan-cocoliztli": {
        "pan-smallpox-am": "The Cocoliztli epidemics struck in the decades following the initial smallpox outbreak, compounding the population collapse.",
        "civ-aztec": "Cocoliztli devastated the Indigenous population of former Aztec territory under early Spanish colonial rule.",
    },
    "pan-cholera": {
        "arc-columbian-e": "Cholera spread globally along the same expanding trade and shipping networks the Columbian Exchange had established.",
    },
    "pan-flu-1918": {
        "tech-antibiotic": "Many 1918 flu deaths came from secondary bacterial pneumonia — exactly the kind of infection antibiotics would later treat.",
    },
    "pan-hiv": {
        "tech-antibiotic": "Antibiotics treat the opportunistic infections that HIV/AIDS patients' weakened immune systems become vulnerable to.",
        "tech-dna": "Understanding HIV's genetic structure through DNA science was essential to developing antiretroviral treatments.",
    },
    "pan-covid": {
        "tech-dna": "Rapid genomic sequencing of SARS-CoV-2's RNA let scientists design mRNA vaccines within weeks of the outbreak.",
        "tech-crispr": "CRISPR-based diagnostic tools were adapted to rapidly detect COVID-19 infections.",
    },
}


def get_details(event_id: str):
    d = DETAILS.get(event_id, {"discovered_by": None, "related_ids": []})
    return {**d, "related_why": RELATED_WHY.get(event_id, {})}
