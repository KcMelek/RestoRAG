# DialAgent Project: LLM & RAG Component Testing Suite

> ### 📋 Test Suite Overview
> * **Objective:** This file contains the complete collection of automated and manual QA test questions for evaluating the DialAgent conversational engineering pipeline.
> * **Target Sub-Components:** Component 2A (Advanced Multimodal/Form Ingestion) and Component 2B (Standard Text LLM Orchestration Loop).
> * **Ground-Truth References:** `complex_menu.md`, `kitchen_recipes.txt`, `shifts_may_2026.csv`, and `restaurant_policy.txt`.

---

## 🔠 Category 1: General FAQs & Standard Text RAG (Component 2B Verification)
*Focus: Verifying that the language layer extracts precise, literal information from clean, linear prose files without hallucinating.*

### Test Case 1.1: Physical Ingestion & Facilities
* **Input Query:** "Where exactly is your restaurant located, and do you have a private parking lot on-site?"
* **Expected System Logic:** Checks `restaurant_policy.txt` -> Section 1.1.
* **Expected Output:** "We are located at 14 Rue de Rivoli, 75001 Paris, France. Please note that we do not have a private parking lot on-site; however, public street parking is available at Parking Vinci, which is located just 150 meters away."

### Test Case 1.2: Hard Operating Constraints (Calendar Rules)
* **Input Query:** "Can I book a table for lunch this Sunday at 1:00 PM?"
* **Expected System Logic:** Evaluates operating availability boundaries inside `restaurant_policy.txt`.
* **Expected Output:** "I am sorry, but we cannot accept a booking for Sunday. The restaurant is completely closed on Sundays for building maintenance."

### Test Case 1.3: Complex Hour Intersections (Kitchen Shutdown Boundaries)
* **Input Query:** "Can I arrive at 10:45 PM on a Friday night to sit down and order a quick meal?"
* **Expected System Logic:** Cross-references closing time (11:00 PM) against order cutoff policies (10:30 PM).
* **Expected Output:** "While our doors remain open until 11:00 PM on Fridays, our kitchen completely halts all new orders at exactly 10:30 PM. Therefore, we will not be able to serve you a meal if you arrive at 10:45 PM."

---

## 🍔 Category 2: Nested Layouts & Complex Menu Extraction (Component 2A Verification)
*Focus: Stress-testing structural spatial parsing, non-linear pricing layouts, and parent-child parameter associations.*

### Test Case 2.1: Multi-Variable Horizontal Grid Mapping
* **Input Query:** "How much do you charge for a glass of the Bordeaux Reserve wine versus ordering a whole bottle?"
* **Expected System Logic:** Correctly parses separated pricing values across textual dashes inside `complex_menu.md`.
* **Expected Output:** "A single glass of our Bordeaux Reserve is €14.50, and a full bottle is €78.00."

### Test Case 2.2: Contextual Child Modification Matrix
* **Input Query:** "I want to order your Burger Gourmet, but it is critical that my beef patty is cooked completely well-done. Can you confirm that?"
* **Expected System Logic:** Recognizes specific customization exclusions linked underneath `Le Burger Gourmet`.
* **Expected Output:** "I can certainly add the Burger Gourmet to your order, but I must inform you that our kitchen explicitly rejects requests for well-done meat preparation parameters to preserve dish quality."

### Test Case 2.3: Structural Text Tag Isolation
* **Input Query:** "I am checking your classics list, what specific items are marked as safe for a vegetarian or gluten-free diet?"
* **Expected System Logic:** Sweeps the document arrays for specific tag identifiers matching the filter criteria.
* **Expected Output:** "Our *Risotto Aux Champignons Sauvages* (€19.00) perfectly matches your needs. It is explicitly flagged as both Vegetarian and Gluten-Free."

---

## 🍳 Category 3: Deep Recipe Parameterization & Allergen Control (Component 2A/2B Cross-Check)
*Focus: Evaluating hidden safety thresholds, cross-contamination warnings, and alternative conditional paths inside internal instructions.*

### Test Case 3.1: Conditional Path Logic Verification
* **Input Query:** "I am completely vegan. Can I order the wild mushroom risotto as-is, or does it contain dairy?"
* **Expected System Logic:** Scans the ingredient profile within `kitchen_recipes.txt`.
* **Expected Output:** "By default, the dish contains Grana Padano cheese, which means it is not vegan as-is. However, our kitchen can prepare this specifically for you using a vegan cheese substitute upon request."

### Test Case 3.2: Critical Allergen Trace Identification
* **Input Query:** "I have a highly volatile, life-threatening allergy to tree nuts. Can I eat your truffle risotto safely?"
* **Expected System Logic:** Identifies explicit structural cross-contamination vectors inside the internal kitchen instructions.
* **Expected Output:** "We advise caution: our internal kitchen records note that the truffle risotto sharing trays intersect with pine nut preparation zones. Due to your volatile allergy, we recommend choosing an alternative option to guarantee your safety."

---

## 📅 Category 4: Multi-Hop Tabular Reasoning (Component 2B Verification)
*Focus: Assessing cell coordinate navigation, intersecting dates/times, and role extraction.*

### Test Case 4.1: Row-Column Multi-Filter Resolution (Floor Staff)
* **Input Query:** "I left my jacket at the restaurant during dinner on Monday night. Who was managing the floor that I can speak with to retrieve it?"
* **Expected System Logic:** Reads `shifts_may_2026.csv` -> Filters where `Day = Monday` AND `Shift_Type = Dinner` -> Extracts `Floor_Manager`.
* **Expected Output:** "The floor manager on duty during the dinner shift this past Monday was Marc Dubois. I can patch you through or leave a note for him."

### Test Case 4.2: Row-Column Multi-Filter Resolution (Kitchen Staff)
* **Input Query:** "I need to coordinate a special ingredient delivery with your kitchen team on Tuesday evening. Who is leading the kitchen line during that shift?"
* **Expected System Logic:** Reads `shifts_may_2026.csv` -> Filters where `Date = 2026-05-26` AND `Shift_Type = Dinner` -> Extracts `Kitchen_Lead`.
* **Expected Output:** "Our kitchen operations for Tuesday evening will be under the direct supervision of Sous-Chef Pierre."

---

## 🚨 Category 5: Boundary Hardening & Automated Human Escalation (Guardrail Validation)
*Focus: Enforcement of domain parameters, structured intent classification, fallback boundaries, and automated transfer hooks.*

### Test Case 5.1: Maximum Capacity Safety Ceiling
* **Input Query:** "I want to book a large celebration dinner for a party of 14 people next Thursday evening at 7:30 PM."
* **Expected System Logic:** Evaluates variable request parameter `Party_Size = 14` against maximum system allowance limit `8`.
* **Expected Action Trigger:** **[ACTION: CALL_TRANSFER_BRIDGE]**
* **Expected Output:** "Our automated reservation system can only process table configurations for groups up to 8 guests. Because you have a larger group of 14, I am transferring this call right now to our events coordinator to handle your request manually."

### Test Case 5.2: Out-of-Inventory Semantic Rejection
* **Input Query:** "Do you guys have any special deals on spicy tuna rolls or pepperoni pizza options?"
* **Expected System Logic:** Runs vector space search, finds zero intersection with bistro inventory context.
* **Expected Output:** "We do not serve sushi or pizza at Le Château Bistro. Our menu specializes exclusively in classic French restaurant dishes, such as our Charolais beef gourmet burger or wild mushroom risotto."

### Test Case 5.3: Sentiment-Driven Conflict Resolution Bridge
* **Input Query:** "My delivery order from last night arrived freezing cold and ruined our dinner! I am furious and want a complete refund processed to my bank account immediately!"
* **Expected System Logic:** Identifies high-friction financial and emotional keywords requiring immediate human oversight.
* **Expected Action Trigger:** **[ACTION: IMMEDIATE_STAFF_SLACK_ALERT]** + **[ACTION: CALL_TRANSFER_BRIDGE]**
* **Expected Output:** "I am incredibly sorry to hear that your meal arrived cold and impacted your dinner. I completely understand your frustration. To ensure your refund is handled instantly, I am transferring your call directly to our on-duty manager right now."