# data.py

# In-memory dictionaries to store chat history, user balances, research papers, and rules
chat_history = {}
user_balances = {}
notes = {}
rules = {
    "Computer Science": [
        "Operating systems manage hardware resources and provide a platform for running applications and services.",
        "Data structures organize and store data efficiently for quick access and modification.",
        "Algorithms are step-by-step procedures for solving problems and performing tasks.",
        "Networking involves connecting computers and devices to share data and resources.",
        "Databases store, retrieve, and manage data in a structured way.",
        "Cybersecurity protects systems, networks, and data from digital attacks.",
        "Software engineering applies engineering principles to software development.",
        "Artificial intelligence enables machines to perform tasks that typically require human intelligence.",
        "Machine learning is a subset of AI that allows systems to learn from data and improve over time.",
        "Web development involves creating websites and web applications using various technologies."
    ],
    "Science": [
        "The scientific method involves observation, hypothesis, experimentation, and conclusion.",
        "Matter is anything that has mass and takes up space.",
        "Energy is the ability to do work or cause change.",
        "The laws of thermodynamics govern the principles of energy transfer.",
        "Atoms are the basic units of matter.",
        "Chemical reactions involve the rearrangement of atoms to form new substances.",
        "Cells are the basic units of life.",
        "Evolution explains the diversity of life on Earth.",
        "The universe is expanding, as evidenced by the redshift of distant galaxies.",
        "The Earth's climate is influenced by both natural and human factors."
    ],
    "Physics": [
        "Newton's laws of motion describe the relationship between the motion of an object and the forces acting on it.",
        "The law of universal gravitation states that every mass attracts every other mass.",
        "Energy can neither be created nor destroyed, only transformed (conservation of energy).",
        "The speed of light in a vacuum is a universal constant.",
        "Quantum mechanics describes the behavior of particles on a very small scale.",
        "Relativity theory explains the relationship between space and time.",
        "Electromagnetism describes the interaction between electric charges and magnetic fields.",
        "Thermodynamics deals with heat, work, and temperature, and their relation to energy and physical properties.",
        "Wave-particle duality states that particles can exhibit both wave-like and particle-like properties.",
        "The standard model of particle physics describes the fundamental particles and their interactions."
    ],
    "Chemistry": [
        "The periodic table organizes elements by increasing atomic number and similar chemical properties.",
        "Chemical bonds form when atoms share or transfer electrons.",
        "Acids and bases react to form water and salts.",
        "The pH scale measures the acidity or basicity of a solution.",
        "Chemical kinetics studies the rates of chemical reactions.",
        "Thermochemistry involves the study of energy changes during chemical reactions.",
        "Organic chemistry focuses on compounds containing carbon.",
        "Inorganic chemistry deals with compounds that are not organic.",
        "Electrochemistry studies the relationship between electricity and chemical reactions.",
        "Stoichiometry involves the calculation of reactants and products in chemical reactions."
    ],
    "Biology": [
        "The cell theory states that all living organisms are composed of cells.",
        "DNA carries genetic information and is the blueprint for life.",
        "Photosynthesis converts light energy into chemical energy in plants.",
        "Cellular respiration converts glucose into usable energy (ATP) in cells.",
        "Genetics is the study of heredity and variation in organisms.",
        "Evolution by natural selection explains the adaptation of species over time.",
        "Ecosystems consist of interacting organisms and their physical environment.",
        "Homeostasis is the maintenance of a stable internal environment in an organism.",
        "Proteins are essential molecules that perform a variety of functions in cells.",
        "The immune system protects the body from pathogens and foreign substances."
    ]
}

functions = [
    "Art",
    "Computer Science",
    "Economics",
    "English",
    "Geography",
    "History",
    "Math",
    "Music",
    "Physical Education",
    "Science"
]

knowledge_areas = {
    "Art": [
        "Painting",
        "Sculpture",
        "Photography",
        "Drawing",
        "Printmaking",
        "Ceramics",
        "Textiles",
        "Digital Art",
        "Art History",
        "Graphic Design"
    ],
    "Computer Science": [
        "Algorithms",
        "Data Structures",
        "Operating Systems",
        "Databases",
        "Networking",
        "Artificial Intelligence",
        "Machine Learning",
        "Cybersecurity",
        "Software Engineering",
        "Web Development"
    ],
    "Economics": [
        "Microeconomics",
        "Macroeconomics",
        "International Economics",
        "Development Economics",
        "Labor Economics",
        "Public Economics",
        "Health Economics",
        "Environmental Economics",
        "Behavioral Economics",
        "Econometrics"
    ],
    "English": [
        "Literature",
        "Creative Writing",
        "Linguistics",
        "Grammar",
        "Composition",
        "Rhetoric",
        "Poetry",
        "Drama",
        "Prose",
        "Literary Theory"
    ],
    "Geography": [
        "Physical Geography",
        "Human Geography",
        "Cartography",
        "Geographic Information Systems",
        "Urban Geography",
        "Environmental Geography",
        "Economic Geography",
        "Political Geography",
        "Cultural Geography",
        "Historical Geography"
    ],
    "History": [
        "Ancient History",
        "Medieval History",
        "Modern History",
        "World History",
        "Military History",
        "Social History",
        "Economic History",
        "Cultural History",
        "Political History",
        "Historiography"
    ],
    "Math": [
        "Algebra",
        "Geometry",
        "Calculus",
        "Statistics",
        "Trigonometry",
        "Number Theory",
        "Combinatorics",
        "Probability",
        "Linear Algebra",
        "Differential Equations"
    ],
    "Music": [
        "Music Theory",
        "Composition",
        "Music History",
        "Performance",
        "Conducting",
        "Music Technology",
        "Ethnomusicology",
        "Jazz Studies",
        "Music Education",
        "Music Therapy"
    ],
    "Physical Education": [
        "Exercise Physiology",
        "Kinesiology",
        "Sports Psychology",
        "Motor Learning",
        "Biomechanics",
        "Sports Nutrition",
        "Adapted Physical Education",
        "Health Education",
        "Sports Management",
        "Coaching"
    ],
    "Science": [
        "Physics",
        "Chemistry",
        "Biology",
        "Earth Science",
        "Astronomy",
        "Environmental Science",
        "Materials Science",
        "Genetics",
        "Ecology",
        "Geology"
    ]
}