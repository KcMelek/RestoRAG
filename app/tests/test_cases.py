# tests/test_cases.py

TEST_CASES = [
    {
        "id": "1.1",
        "query": (
            "Where exactly is your restaurant located, "
            "and do you have a private parking lot on-site?"
        ),
        "expected_answer_keywords": [
            "14 Rue de Rivoli",
            "75001 Paris",
            "Parking Vinci",
            "150 meters",
        ],
        "expected_action": None,
    },
    {
        "id": "1.2",
        "query": "Can I book a table for lunch this Sunday at 1 PM?",
        "expected_answer_keywords": [
            "closed",
            "Sunday",
        ],
        "expected_action": None,
    },
        {
        "id": "1.3",
        "query": (
            "Can I arrive at 10:45 PM on a Friday night "
            "to sit down and order a quick meal?"
        ),
        "expected_answer_keywords": [
            "10:30 PM",
            "kitchen",
            "new orders",
            "10:45 PM",
        ],
        "expected_action": None,
    },
    {
        "id": "2.1",
        "query": "How much is a glass of Bordeaux Reserve wine versus a bottle?",
        "expected_answer_keywords": [
            "65.00",
            "380.00",
        ],
        "expected_action": None,
    },
    
    {
        "id": "2.2",
        "query": (
            "I want to order your Burger Gourmet, "
            "but my beef patty must be well-done."
        ),
        "expected_answer_keywords": [
            "Burger Gourmet",
            "well-done",
            "reject",
            "quality",
        ],
        "expected_action": None,
    },
    {
        "id": "2.3",
        "query": (
            "Which menu items are marked as vegetarian "
            "or gluten-free?"
        ),
        "expected_answer_keywords": [
            "Risotto",
            "Vegetarian",
            "Gluten-Free",
        ],
        "expected_action": None,
    },
    {
        "id": "3.1",
        "query": "I am completely vegan. Can I order the risotto?",
        "expected_answer_keywords": [
            "Comt",
            "dairy",
            "non-vegan",
        ],
        "expected_action": None,
    },
    {
        "id": "3.2",
        "query": (
            "I have a severe tree nut allergy. "
            "Can I safely eat the truffle risotto?"
        ),
        "expected_answer_keywords": [
            "pine nut",
            "cross-contamination",
            "caution",
            "alternative",
        ],
        "expected_action": None,
    },
    {
        "id": "4.1",
        "query": "Who managed the floor during Monday dinner?",
        "expected_answer_keywords": [
            "Marc Dubois",
        ],
        "expected_action": None,
    },
    
    {
        "id": "4.2",
        "query": (
            "Who is leading the kitchen on Tuesday evening?"
        ),
        "expected_answer_keywords": [
            "Pierre",
            "Sous-Chef",
        ],
        "expected_action": None,
    },
    {
        "id": "5.1",
        "query": "I want a reservation for 14 people.",
        "expected_answer_keywords": [
            "events coordinator",
        ],
        "expected_action": "CALL_TRANSFER_BRIDGE",
    },
    {
        "id": "5.2",
        "query": (
            "Do you have spicy tuna rolls or pepperoni pizza?"
        ),
        "expected_answer_keywords": [
            "do not serve",
            "sushi",
            "pizza",
            "French",
        ],
        "expected_action": None,
    },
    {
        "id": "5.3",
        "query": (
            "My delivery arrived freezing cold and I want "
            "an immediate refund."
        ),
        "expected_answer_keywords": [
            "sorry",
            "refund",
            "manager",
            "transfer",
        ],
        "expected_action": [
            "IMMEDIATE_STAFF_SLACK_ALERT",
            "CALL_TRANSFER_BRIDGE",
        ],
    },
]
