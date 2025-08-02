# Used to create data read by manual-forced-cluster2.py
import requests
import os
import time
# Get non zon
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import plotly.express as px
import json
import os
from jinja2 import Template
from collections import Counter, defaultdict
import pprint
pp = pprint.PrettyPrinter(indent=4)
from datetime import datetime
import subprocess
from datetime import datetime
import items_list
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import statistics
import html

def fetch_1kladder_characters(base_ladder_url, start_page=1, end_page=5):
    """Fetch all characters from a range of ladder pages, skipping page 0 by default."""
    all_characters = []
    for page in range(start_page, end_page + 1):  # Inclusive range
        ladder_url = f"{base_ladder_url}{page}"
        print(f"Fetching {ladder_url}")
        response = requests.get(ladder_url)
        if response.status_code == 200:
            ladder_data = response.json()
            all_characters.extend(ladder_data.get("ladder", []))
        else:
            print(f"⚠️ Failed to fetch page {page}: {response.status_code}")
    return all_characters

def fetch_ladder_characters(base_ladder_url, pages):
    """Fetch all characters from multiple pages of the ladder."""
    all_characters = []
    for page in range(0, pages + 1):
        ladder_url = f"{base_ladder_url}{page}"
        print(f"Fetching {ladder_url}")
        response = requests.get(ladder_url)
        if response.status_code == 200:
            ladder_data = response.json()
            all_characters.extend(ladder_data.get("ladder", []))
        else:
            print(f"⚠️ Failed to fetch page {page}: {response.status_code}")
    return all_characters

def MakeHome():
    # Define the consolidated JSON file path
    consolidated_file = "ladder_sc.json"  # Replace with your actual file path
    
    try:
        # Load the consolidated JSON file
        with open(consolidated_file, "r") as file:
            all_characters = json.load(file)
            all_characters = [json.loads(char) if isinstance(char, str) else char for char in all_characters]

        
        # Add this print statement to inspect the structure of the data
#        print("First 5 entries in all_characters:", all_characters[:5])  # Debugging output
#        print("Type of all_characters:", type(all_characters))  # Check if it's a list
        if isinstance(all_characters[0], str):  # Check if elements are strings
            print("First entry as string:", all_characters[0])  # Print one raw string entry
        
        # Convert strings to dictionaries if needed
        if isinstance(all_characters[0], str):  # If first element is a string
            all_characters = [json.loads(char_data) for char_data in all_characters]
            print("Converted all_characters to dictionaries.")  # Confirmation message
        
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading consolidated JSON file: {e}")
        return

    # Now you can safely process the characters
    try:
        class_counts, runeword_counter, unique_counter, set_counter, synth_counter = process_all_characters(all_characters)
        # Continue with the rest of your MakeHome logic...
    except Exception as e:
        print(f"Error during character processing: {e}")

#    data_folder = "sc/ladder-all"
    html_output = """"""
    output_file = "all_mercenary_report.html"
    synth_item = "Synth"


    dt = datetime.now()
    # format it to a string
    timeStamp = dt.strftime('%Y-%m-%d %H:%M')

    # Counters for classes, runewords, uniques, and set items
    class_counts = {}
    runeword_counter = Counter()
    unique_counter = Counter()
    set_counter = Counter()
    synth_counter = Counter()
    crafted_counters = {
        "Rings": Counter(),
        "Weapons and Shields": Counter(),
        "Arrows": Counter(),
        "Bolts": Counter(),
        "Body Armor": Counter(),
        "Gloves": Counter(),
        "Belts": Counter(),
        "Helmets": Counter(),
        "Boots": Counter(),
        "Amulets": Counter(),
    }
    magic_counters = {
        "Rings": Counter(),
        "Weapons and Shields": Counter(),
        "Arrows": Counter(),
        "Bolts": Counter(),
        "Body Armor": Counter(),
        "Gloves": Counter(),
        "Belts": Counter(),
        "Helmets": Counter(),
        "Boots": Counter(),
        "Amulets": Counter(),
    }
    rare_counters = {
        "Rings": Counter(),
        "Weapons and Shields": Counter(),
        "Arrows": Counter(),
        "Bolts": Counter(),
        "Body Armor": Counter(),
        "Gloves": Counter(),
        "Belts": Counter(),
        "Helmets": Counter(),
        "Boots": Counter(),
        "Amulets": Counter(),
    }
    
    synth_sources = {}  # Maps item names to all synth items that used them

    runeword_users = {}
    unique_users = {}
    set_users = {}
    synth_users = {}
    crafted_users = {category: {} for category in crafted_counters}  # Ensure all categories exist
    rare_users = {category: {} for category in rare_counters}  # Ensure all categories exist
    magic_users = {category: {} for category in magic_counters}  # Ensure all categories exist

    all_characters = []
    sorted_just_socketed_runes = {}
    sorted_just_socketed_excluding_runewords_runes = {}
    all_other_items = {}

    all_equipped_items = []
    two_handed_counter = Counter()
    bow_counter = Counter()

    def analyze_top_accounts():
        def get_top_accounts_with_class(account_class_counts, class_code, min_count=2, top_n=5):
            return [
                (acct, counts)
                for acct, counts in sorted(account_class_counts.items(), key=lambda x: x[1].get(class_code, 0), reverse=True)
                if counts.get(class_code, 0) >= min_count
            ][:top_n]

        base_ladder_url = "https://beta.pathofdiablo.com/api/ladder/13/0/0/"
        all_characters = fetch_1kladder_characters(base_ladder_url, start_page=1, end_page=5)
        all_characters = [char for char in all_characters if char.get('account')]

        level_counter = Counter(char['level'] for char in all_characters)

        print("\n🎯 High-Level Character Counts:")
        for level in [99, 98, 97, 96, 95]:
            print(f"Level {level}: {level_counter.get(level, 0)} characters")

        level99_accounts = defaultdict(int)

        for char in all_characters:
            if char['level'] == 99:
                level99_accounts[char['account']] += 1

        top_99s = sorted(level99_accounts.items(), key=lambda x: x[1], reverse=True)[:3]

        print("\n🥇 Top Accounts by Number of Level 99 Characters:")
        for acct, count in top_99s:
            print(f'<li><a href="https://beta.pathofdiablo.com/account/{acct}">{acct}</a>: {count} characters at level 99</li>')

        account_class_counts = defaultdict(lambda: defaultdict(int))

        for char in all_characters:
            acct = char['account']
            class_code = char['charClass']  # e.g., "sor"
            account_class_counts[acct][class_code] += 1

        #Who has the most amazons?
        most_zons = get_top_accounts_with_class(account_class_counts, "ama")
#        most_zons = sorted(account_class_counts.items(), key=lambda x: x[1].get("ama", 0), reverse=True)[:5]
        print("\n🧙 Accounts with Most Amazons:")
        for acct, class_count in most_zons:
            print(f"{acct}: {class_count.get('ama', 0)} Amazons")
        #Who has the most assassins?
        most_sins = get_top_accounts_with_class(account_class_counts, "asn")
#        most_sins = sorted(account_class_counts.items(), key=lambda x: x[1].get("asn", 0), reverse=True)[:5]
        print("\n🧙 Accounts with Most Assassins:")
        for acct, class_count in most_sins:
            print(f"{acct}: {class_count.get('asn', 0)} Assassins")
        #Who has the most barbs?
        most_barbs = get_top_accounts_with_class(account_class_counts, "bar")
#        most_barbs = sorted(account_class_counts.items(), key=lambda x: x[1].get("bar", 0), reverse=True)[:3]
        print("\n🧙 Accounts with Most Barbarians:")
        for acct, class_count in most_barbs:
            print(f"{acct}: {class_count.get('bar', 0)} Barbarians")
        #Who has the most druids?
        most_druids = get_top_accounts_with_class(account_class_counts, "dru")
#        most_druids = sorted(account_class_counts.items(), key=lambda x: x[1].get("dru", 0), reverse=True)[:3]
        print("\n🧙 Accounts with Most Druids:")
        for acct, class_count in most_druids:
            print(f"{acct}: {class_count.get('dru', 0)} Druids")
        #Who has the most necros?
        most_necros = get_top_accounts_with_class(account_class_counts, "nec")
#        most_necros = sorted(account_class_counts.items(), key=lambda x: x[1].get("nec", 0), reverse=True)[:5]
        print("\n🧙 Accounts with Most Necromancers:")
        for acct, class_count in most_necros:
            print(f"{acct}: {class_count.get('nec', 0)} Necromancers")
        #Who has the most paladins?
        most_pallys = get_top_accounts_with_class(account_class_counts, "pal")
#        most_pallys = sorted(account_class_counts.items(), key=lambda x: x[1].get("pal", 0), reverse=True)[:4]
        print("\n🧙 Accounts with Most Paladins:")
        for acct, class_count in most_pallys:
            print(f"{acct}: {class_count.get('pal', 0)} Paladins")
        #Who has the most sorceresses?
        most_sorcs = get_top_accounts_with_class(account_class_counts, "sor")
#        most_sorcs = sorted(account_class_counts.items(), key=lambda x: x[1].get("sor", 0), reverse=True)[:5]
        print("\n🧙 Accounts with Most Sorceresses:")
        for acct, class_count in most_sorcs:
            print(f"{acct}: {class_count.get('sor', 0)} sorceresses")

    ## Who has all the classes?
        # Map short class codes used by the API to full names (or use your preferred naming)
        CLASS_CODES = {"ama", "asn", "bar", "dru", "nec", "pal", "sor"}

        # Track each account's set of classes
        account_class_sets = defaultdict(set)

        for char in all_characters:
            acct = char['account']
            char_class = char['charClass']
            account_class_sets[acct].add(char_class)

        # Count accounts that have all 7 classes
        complete_class_accounts = [acct for acct, classes in account_class_sets.items() if CLASS_CODES.issubset(classes)]

        print(f"\n📈 Accounts with all 7 classes: {len(complete_class_accounts)}")
        print("Examples:", ", ".join(complete_class_accounts[:5]))

        account_stats = defaultdict(lambda: {'count': 0, 'levels': 0, 'xp': 0})

        for char in all_characters:
            acct = char.get('account')
            if not acct:
                continue
            account_stats[acct]['count'] += 1
            account_stats[acct]['levels'] += char.get('level', 0)
            account_stats[acct]['xp'] += char.get('exp', 0)

        # Convert to list of (account, stats) and sort
        sorted_by_xp = sorted(account_stats.items(), key=lambda x: x[1]['xp'], reverse=True)[:5]
        sorted_by_levels = sorted(account_stats.items(), key=lambda x: x[1]['levels'], reverse=True)[:5]
        sorted_by_count = sorted(account_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:10]

        print("\n📊 Top Accounts from Top 1,000 Characters:")

        print("\n🔸 Top 5 by Total XP:")
        for acct, stats in sorted_by_xp:
            avg_lvl = stats['levels'] / stats['count']
            print(f"{acct}: {stats['xp']:,} XP, {stats['count']} chars, avg level {avg_lvl:.2f}")

        print("\n🔸 Top 5 by Total Levels:")
        for acct, stats in sorted_by_levels:
            avg_lvl = stats['levels'] / stats['count']
            print(f"{acct}: {stats['levels']} levels, {stats['count']} chars, avg level {avg_lvl:.2f}")

        print("\n🔸 Top 5 by Character Count:")
        for acct, stats in sorted_by_count:
            avg_lvl = stats['levels'] / stats['count']
            print(f"{acct}: {stats['count']} characters, total level {stats['levels']}, avg level {avg_lvl:.2f}")



        kfun_facts_html = f"""
        <h3 id="top-account-stats">Top Account Statistics <a href="#top-account-stats" class="anchor-link">
            <img src="icons/anchor.png" alt="🔗" class="anchor-icon"></a></h3>

        <!-- Level 95+ Summary -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
            <h4>High-Level Character Counts</h4>
            <ul>
                {"".join(f"<li>Level {lvl}: {count} characters</li>" for lvl, count in level_counter.items() if lvl in [99, 98, 97, 96, 95])}
            </ul>
        </div>
        <!-- Level 99 Accounts -->
            <div class="fun-facts-column">
        <h4>Top Accounts by Number of Level 99 Characters</h4>
        <ul>
            {"".join(
                f"<li><a href='https://beta.pathofdiablo.com/ladder?account/{acct}'>{acct}</a>: {count} characters at level 99</li>"
                for acct, count in top_99s
            )}
        </ul> 
       </div></div>

        <!-- Per-Class Top 5 Lists -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with multiple Amazons in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('ama', 0)} Amazons</li>" for acct, count in most_zons)}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Accounts with multiple Assassins in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('asn', 0)} Assassins</li>" for acct, count in most_sins)}</ul>
            </div>
        </div>
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with multiple Barbarians in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('bar', 0)} Barbarians</li>" for acct, count in most_barbs)}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Accounts with multiple Druids in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('dru', 0)} Druids</li>" for acct, count in most_druids)}</ul>
            </div>
        </div>
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with multiple Necromancers in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('nec', 0)} Necromancers</li>" for acct, count in most_necros)}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Accounts with multiple Paladins in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('pal', 0)} Paladins</li>" for acct, count in most_pallys)}</ul>
            </div>
        </div>
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with multiple Sorceresses in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('sor', 0)} Sorceresses</li>" for acct, count in most_sorcs)}</ul>
            </div>
        </div>

        <!-- All 7 Classes -->
        <h3>Accounts with all 7 classes in the top 1K: {len(complete_class_accounts)}</h3>
        <p>{", ".join(f"<a href='https://beta.pathofdiablo.com/ladder?account={acct}'>{acct}</a>" for acct in complete_class_accounts[:5])}</p>

        <!-- XP / Level / Count -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with the most experience</h3>
                    <ul>
                        {"".join(
                            f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {stats['xp']:,} XP, {stats['count']} chars, avg level {stats['levels']/stats['count']:.2f}</li>"
                            for acct, stats in sorted_by_xp
                        )}
                    </ul>
           </div>
            <div class="fun-facts-column">
                <h3>Accounts with the most Levels</h3>
                    <ul>
                        {"".join(
                            f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {stats['levels']} levels, {stats['count']} chars, avg level {stats['levels']/stats['count']:.2f}</li>"
                            for acct, stats in sorted_by_levels
                        )}
                    </ul>
            </div>
        </div>
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with the most characters in the top 1K</h3>
                    <ul>
                        {"".join(
                            f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {stats['count']} characters, total level {stats['levels']}, avg level {stats['levels']/stats['count']:.2f}</li>"
                            for acct, stats in sorted_by_count
                        )}
                    </ul>
            </div>
        </div>
        """

        return kfun_facts_html

    # Generate fun facts
    kfun_facts_html = analyze_top_accounts()
    
    # Function to process each JSON file
    def process_all_characters():
        with open("ladder_sc.json", "r") as file:
            all_characters = json.load(file)  # Ensure it's a list of dictionaries

        for char_data in all_characters:
            if isinstance(char_data, str):  # If somehow it's still a string, convert it
                char_data = json.loads(char_data)

            char_name = char_data.get("Name", "Unknown")  # This should now work
#            print(f"Processing {char_name}")
            char_class = char_data.get("Class", "Unknown")
            char_level = char_data.get("Stats", {}).get("Level", "Unknown")

            # Debugging: Print details of the character being processed
#            print(f"Processing character: {char_name}, Class: {char_class}, Level: {char_level}")

            # Continue with processing logic (e.g., class counts, equipped items, etc.)

        # Dictionary to store class counts
        class_counts = {}

        # Counters for runewords, uniques, and set items
        runeword_counter = Counter()
        unique_counter = Counter()
        set_counter = Counter()
        synth_counter = Counter()

        # Categorize worn slots
        def categorize_worn_slot(worn_category, text_tag):
            if worn_category in ["sweapon1", "weapon1", "sweapon2", "weapon2"]:
                if text_tag == "Arrows":
                    return "Arrows"
                elif text_tag == "Bolts":
                    return "Bolts"
                else:
                    return "Weapons and Shields"

            worn_category_map = {
                "ring1": "Rings", "ring2": "Rings",
                "body": "Armor",
                "gloves": "Gloves",
                "belt": "Belts",
                "helmet": "Helmets",
                "boots": "Boots",
                "amulet": "Amulets",
            }

            return worn_category_map.get(worn_category, "Other")  # Default to "Other"

        # Process each character in the consolidated JSON
        for char_data in all_characters:
            try:
                char_name = char_data.get("Name", "Unknown")
                char_class = char_data.get("Class", "Unknown")
                char_level = char_data.get("Stats", {}).get("Level", "Unknown")

                # Process class data
                if char_class:
                    class_counts[char_class] = class_counts.get(char_class, 0) + 1

                # Process equipped items
                for item in char_data.get("Equipped", []):
                    all_equipped_items.append(item)
                    worn_category = categorize_worn_slot(item.get("Worn", ""), item.get("TextTag", ""))  # ✅ Call once

                    character_info = {
                        "name": char_name,
                        "class": char_class,
                        "level": char_level,
                    }

                    if "synth" in item.get("Tag", "").lower() or "synth" in item.get("TextTag", "").lower():
                        item_title = item["Title"]
                        synth_counter[item_title] += 1
                        synth_users.setdefault(item_title, []).append(character_info)

                        # Process SynthesisedFrom property
                        synthesized_from = item.get("SynthesisedFrom", [])
                        all_related_items = [item_title] + synthesized_from
                        for source_item in all_related_items:
                            synth_sources.setdefault(source_item, []).append({
                                "name": char_name,
                                "class": char_class,
                                "level": char_level,
                                "synthesized_item": item_title
                            })

                    if item.get("QualityCode") == "q_runeword":
                        title = item["Title"]
                        if title == "2693":
                            title = "Delirium"
                        elif title == "-26":
                            title = "Pattern2"

                        runeword_counter[title] += 1

                        base = item.get("Tag", "Unknown")
                        if title not in runeword_users:
                            runeword_users[title] = {}
                        if base not in runeword_users[title]:
                            runeword_users[title][base] = []
                        runeword_users[title][base].append(character_info)

                    if item.get("QualityCode") == "q_unique":
                        unique_counter[item["Title"]] += 1
                        unique_users.setdefault(item["Title"], []).append(character_info)

                    if item.get("QualityCode") == "q_set":
                        set_counter[item["Title"]] += 1
                        set_users.setdefault(item["Title"], []).append(character_info)

                    if item.get("QualityCode") == "q_crafted":
                        crafted_counters[worn_category][item["Title"]] += 1
                        crafted_users.setdefault(worn_category, {}).setdefault(item["Title"], []).append(character_info)

            except (KeyError, TypeError) as e:
                print(f"Error processing character: {char_name}, Error: {e}")
                continue

#        return class_counts, runeword_counter, unique_counter, set_counter, synth_counter
        return class_counts, runeword_counter, unique_counter, set_counter, synth_counter, runeword_users, unique_users, set_users, synth_users, crafted_counters, crafted_users, all_equipped_items

    def count_two_handed_weapons(equipped_items, two_handed_bases):
        counter = Counter()
        runeword_base_breakdown = defaultdict(Counter)

        for item in equipped_items:
            worn = item.get("Worn")
            if worn not in {"weapon1", "weapon2", "sweapon1", "sweapon2"}:
                continue

            tag = item.get("Tag", "")
            title = item.get("Title", "")
            quality = item.get("QualityCode", "")
            base_name = tag.strip()

            if base_name not in two_handed_bases:
                continue  # Skip non-two-handed items

            if quality == "q_runeword":
                label = f"{title} ({base_name})"
            else:
                label = title

            counter[label] += 1

        return counter, runeword_base_breakdown

    def count_two_handed_weapons(equipped_items, bow_bases):
        counter = Counter()
        runeword_base_breakdown = defaultdict(Counter)

        for item in equipped_items:
            worn = item.get("Worn")
            if worn not in {"weapon1", "weapon2", "sweapon1", "sweapon2"}:
                continue

            tag = item.get("Tag", "")
            title = item.get("Title", "")
            quality = item.get("QualityCode", "")
            base_name = tag.strip()

            if base_name not in bow_bases:
                continue  # Skip non-two-handed items

            if quality == "q_runeword":
                label = f"{title} ({base_name})"
            else:
                label = title

            counter[label] += 1

        return counter, runeword_base_breakdown

    def generate_two_handed_weapon_html(two_handed_counter):
        # First, aggregate base breakdowns for runewords
        aggregated_data = defaultdict(lambda: {"total": 0, "bases": Counter()})
        
        for label, count in two_handed_counter.items():
            if " (" in label and label.endswith(")"):
                # Runeword with base, e.g., "Memory (Cedar Staff)"
                name, base = label[:-1].split(" (", 1)
                aggregated_data[name]["total"] += count
                aggregated_data[name]["bases"][base] += count
            else:
                # Normal item
                aggregated_data[label]["total"] += count

        # Sort aggregated data by total count, descending
        sorted_items = sorted(aggregated_data.items(), key=lambda x: x[1]["total"], reverse=True)

        # Generate HTML
        html_output = [
            "<h2>Most Common Melee Weapons That Require two Hands</h2>",
            "<div style='column-count: 2; column-gap: 2em;'>",
            "<ul style='margin: 0; padding: 0;'>"
        ]

        for name, data in sorted_items:
            total = data["total"]
            bases = data["bases"]

            if bases:
                html_output.append(f"<li><strong>{name}: {total}</strong><ul>")
                for base_name, base_count in bases.most_common():
                    html_output.append(f"<li class='base-item'>{base_name}: {base_count}</li>")
                html_output.append("</ul></li>")
            else:
                html_output.append(f"<li>{name}: {total}</li>")

        html_output.append("</ul></div>")
        return "\n".join(html_output)

    def generate_two_handed_weapon_htmlbow(bow_counter):
        # First, aggregate base breakdowns for runewords
        aggregated_data = defaultdict(lambda: {"total": 0, "bases": Counter()})
        
        for label, count in bow_counter.items():
            if " (" in label and label.endswith(")"):
                # Runeword with base, e.g., "Memory (Cedar Staff)"
                name, base = label[:-1].split(" (", 1)
                aggregated_data[name]["total"] += count
                aggregated_data[name]["bases"][base] += count
            else:
                # Normal item
                aggregated_data[label]["total"] += count

        # Sort aggregated data by total count, descending
        sorted_items = sorted(aggregated_data.items(), key=lambda x: x[1]["total"], reverse=True)

        # Generate HTML
        html_output = [
            "<h2>Most Commonly Seen Bows and Crossbows</h2>",
            "<div style='column-count: 2; column-gap: 2em;'>",
            "<ul style='margin: 0; padding: 0;'>"
        ]

        for name, data in sorted_items:
            total = data["total"]
            bases = data["bases"]

            if bases:
                html_output.append(f"<li><strong>{name}: {total}</strong><ul>")
                for base_name, base_count in bases.most_common():
                    html_output.append(f"<li class='base-item'>{base_name}: {base_count}</li>")
                html_output.append("</ul></li>")
            else:
                html_output.append(f"<li>{name}: {total}</li>")

        html_output.append("</ul></div>")
        return "\n".join(html_output)

    def analyze_one_or_two_handed_usage(characters, one_or_two_hand_list):
        item_counts = defaultdict(lambda: {"total": 0, "bases": Counter()})

        for char in characters:
            equipped = {item["Worn"]: item for item in char.get("Equipped", [])}

            for slot_pair in [("weapon1", "weapon2"), ("sweapon1", "sweapon2")]:
                primary, secondary = slot_pair
                item = equipped.get(primary)
                other_item = equipped.get(secondary)

                if not item or other_item:
                    continue  # Skip if no item or dual-wielding

                base = item.get("Tag", "")
                if base not in one_or_two_hand_list:
                    continue  # Not a one/two-hand weapon

                title = item.get("Title", "Unknown")
                quality = item.get("QualityCode", "")
                
                if quality == "q_runeword":
                    item_counts[title]["total"] += 1
                    item_counts[title]["bases"][base] += 1
                else:
                    # Normal item
                    item_counts[f"{title}"] = item_counts.get(f"{title}", {"total": 0, "bases": Counter()})
                    item_counts[title]["total"] += 1

        # Sort by count descending
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1]["total"], reverse=True)

        # Output to HTML in two columns
        html_output = [
            "<h2>One or Two-Handed Items (Used Two-Handed)</h2>",
            "<div style='column-count: 2; column-gap: 2em;'>",
            "<ul style='margin: 0; padding: 0;'>"
        ]

        for name, data in sorted_items:
            total = data["total"]
            bases = data["bases"]

            if bases:
                html_output.append(f"<li><strong>{name}: {total}</strong><ul style='margin: 0;'>")
                for base_name, base_count in bases.most_common():
                    html_output.append(f"<li style='padding-left: 1.5em'>{base_name}: {base_count}</li>")
                html_output.append("</ul></li>")
            else:
                html_output.append(f"<li>{name}: {total}</li>")

        html_output.append("</ul></div>")
        return "\n".join(html_output)

    def analyze_one_or_two_handed_usage_with_characters(characters, one_or_two_hand_list):
        item_data = defaultdict(lambda: {"total": 0, "bases": defaultdict(list)})

        for char in characters:
            equipped = {item["Worn"]: item for item in char.get("Equipped", [])}

            for slot1, slot2 in [("weapon1", "weapon2"), ("sweapon1", "sweapon2")]:
                weapon = equipped.get(slot1)
                offhand = equipped.get(slot2)

                if not weapon or offhand:
                    continue  # Either missing weapon or dual wielding

                base = weapon.get("Tag", "")
                if base not in one_or_two_hand_list:
                    continue

                title = weapon.get("Title", "Unknown")
                quality = weapon.get("QualityCode", "")
#                pprint.pprint(characters[0])
                char_info = {
                    "name": char.get("Name", "Unknown"),
#                    "level": char.get("Stats.Level", "?"),
                    "class": char.get("Class", "Unknown"),
                }

                item_data[title]["total"] += 1
                item_data[title]["bases"][base].append(char_info)

        # Sort by total descending
        sorted_items = sorted(item_data.items(), key=lambda x: -x[1]["total"])

        html_output = [
            "<h2>One or Two-Handed Items (Used Two-Handed)</h2>",
            "<div style='column-count: 2; column-gap: 2em;'>",
            "<ul style='margin: 0; padding: 0;'>"
        ]

        for title, data in sorted_items:
            html_output.append(f"<li><strong>{title}: {data['total']}</strong>")

            for base, chars in sorted(data["bases"].items(), key=lambda x: (-len(x[1]), x[0])):
                base_name = base or "(unknown base)"

                base_id = slugify(f"{title}-{base_name}")

                html_output.append(f"""
                    <ul style="margin: 0;">
                        <li style="padding-left: 1.5em">
                            <button class="collapsible">
                                <img src="icons/open-grey.png" alt="Expand" class="icon-small open-icon hidden">
                                <img src="icons/closed-grey.png" alt="Collapse" class="icon-small close-icon">
                                <strong>
                                    <a href="#item-{base_id}" class="anchor-link">
                                        {base_name}: {len(chars)}
                                    </a>
                                </strong>
                            </button>
                            <div class="content" id="item-{base_id}">
                                {''.join(f'''
                                    <div class="character-info">
                                        <div class="character-link">
                                            <a href="https://beta.pathofdiablo.com/armory?name={c["name"]}" target="_blank">
                                                {c["name"]}
                                            </a>
                                        </div>
                                        <div>{c["class"]}</div>
                                        <div class="hover-trigger" data-character-name="{c["name"]}"></div>
                                    </div>
                                    <div class="character">
                                        <div class="popup hidden"></div>
                                    </div>
                                ''' for c in chars)}
                            </div>
                        </li>
                    </ul>
                """)

            html_output.append("</li>")

        html_output.append("</ul></div>")
        return "\n".join(html_output)

#    loadout_counts = defaultdict(int)
#    total_loadouts = 0
    def categorize_weapon_loadouts(characters):
        BOW_BASES = {b.lower() for b in all_the_items["zon_bows"] + all_the_items["bow_bows"]}
        XBOW_BASES = {x.lower() for x in all_the_items["cross_bows"]}

        loadout_counts = defaultdict(int)
        total_loadouts = 0

        def is_weapon(item):
            return isinstance(item, dict) and "DamageMinimum" in item and "DamageMaximum" in item

        def is_shield(item):
            return isinstance(item, dict) and "Block" in item and "Defense" in item

        def is_missile(item):
            tag = item.get("Tag", "").lower()
            return "arrow" in tag or "bolt" in tag

        other_examples = []

        def classify_loadout(w1, w2):
            if not w1 and not w2:
                return None  # Skip

            tag1 = w1.get("Tag", "").lower() if w1 else ""
            tag2 = w2.get("Tag", "").lower() if w2 else ""

            tags = {tag1, tag2}

            # Bow + Arrows
            if (tag1 in BOW_BASES or tag2 in BOW_BASES) and any("arrow" in t for t in tags):
                return "Bow + Arrows"
            if tag1 in BOW_BASES or tag2 in BOW_BASES:
                return "Bow Only (Missing Arrows)"
            if any("arrow" in t for t in tags):
                return "Arrows Only (Missing Bow)"

            # Crossbow + Bolts
            if (tag1 in XBOW_BASES or tag2 in XBOW_BASES) and any("bolt" in t for t in tags):
                return "Crossbow + Bolts"
            if tag1 in XBOW_BASES or tag2 in XBOW_BASES:
                return "Crossbow Only (Missing Bolts)"
            if any("bolt" in t for t in tags):
                return "Bolts Only (Missing Crossbow)"

            # Two-handed melee weapon (solo)
            if w1 and not w2 and is_weapon(w1):
                base = w1.get("Tag", "")
                if base in all_the_items["one_or_two_hand"] or base in all_the_items["two_handed_bases"]:
                    return "A Single Two-Handed Weapon"

            if w2 and not w1 and is_weapon(w2):
                base = w2.get("Tag", "")
                if base in all_the_items["one_or_two_hand"] or base in all_the_items["two_handed_bases"]:
                    return "A Single Two-Handed Weapon"

            # Weapon + Shield
            if (is_weapon(w1) and is_shield(w2)) or (is_shield(w1) and is_weapon(w2)):
                return "Weapon + Shield"

            # Dual wield
            if is_weapon(w1) and is_weapon(w2):
                return "Dual Wield"

            # Single One-Handed Weapon
            if (w1 and not w2 and is_weapon(w1)) or (w2 and not w1 and is_weapon(w2)):
                base = (w1 or w2).get("Tag", "")
                if base not in all_the_items["one_or_two_hand"] and base not in all_the_items["two_handed_bases"]:
                    return "Single One-Handed Weapon (Missing Shield or Second Weapon)"

            # Shield only
            if is_shield(w1) and not w2:
                return "Shield Only (Missing Weapon)"
            if is_shield(w2) and not w1:
                return "Shield Only (Missing Weapon)"

            # Two-handed
            tag = tag1 or tag2
            if tag in all_the_items["two_handed_bases"]:
                return "A Single Two-Handed Weapon"

            return "Other"

        empty_loadout_count = 0
        partially_empty_set_count = 0
        for char in characters:
            equipped = {item["Worn"]: item for item in char.get("Equipped", []) if isinstance(item, dict)}
            # Check if weapon1/weapon2 or sweapon1/sweapon2 are both missing
            has_set1 = equipped.get("weapon1") or equipped.get("weapon2")
            has_set2 = equipped.get("sweapon1") or equipped.get("sweapon2")

            if not has_set1 and not has_set2:
                empty_loadout_count += 1
            elif not has_set1 or not has_set2:
                partially_empty_set_count += 1

            sets_categorized = 0

            for set1, set2 in [("weapon1", "weapon2"), ("sweapon1", "sweapon2")]:
                w1 = equipped.get(set1)
                w2 = equipped.get(set2)

                category = classify_loadout(w1, w2)
                if category:
                    loadout_counts[category] += 1
                    total_loadouts += 1
                    sets_categorized += 1

            if sets_categorized == 0:
                empty_loadout_count += 1

        # Prepare output
        results = []
        print("Sample 'Other' loadouts:")
        for ex in other_examples[:20]:  # show first 20
            print(ex)

        for category, count in sorted(loadout_counts.items(), key=lambda x: -x[1]):
            pct = (count / total_loadouts) * 100 if total_loadouts else 0
            results.append(f"{category}: {count} ({pct:.1f}%)")

        print(f"Total non-empty loadouts: {total_loadouts}")
#        return results
        return loadout_counts, total_loadouts, empty_loadout_count, partially_empty_set_count

    complete_categories = {
        "Weapon + Shield",
        "Dual Wield",
        "Bow + Arrows",
        "Crossbow + Bolts",
        "A Single Two-Handed Weapon",
    }


    incomplete_categories = {
        "Single One-Handed Weapon (Missing Shield or Second Weapon)",
        "Shield Only (Missing Weapon)",
        "Bow Only (Missing Arrows)",
        "Arrows Only (Missing Bow)",
        "Crossbow Only (Missing Bolts)",
        "Bolts Only (Missing Crossbow)",
    }

    def generate_loadout_summary_html(loadout_counts, total, empty_loadout_count, partially_empty_set_count):
        # Complete section
        complete_html = "<h2>Overall Weapon Usage Stats, Characters Equipped with:</h2><ul>"
        for category, count in sorted(loadout_counts.items(), key=lambda x: -x[1]):
            if category in complete_categories:
                percentage = f"{(count / total * 100):.1f}%"
                complete_html += f"<li><strong>{category}:</strong> {count} ({percentage})</li>"
        complete_html += "</ul>"

        # Incomplete section inside collapsible
        collapsible_html = '''
    <button type="button" class="collapsible small-collapsible">
        <img src="icons/open.png" alt="Incomplete Loadouts Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Incomplete Loadouts Close" class="icon-small close-icon">
        <strong>Incomplete Loadouts</strong>
    </button>
    <div class="content">
        <div id="incompletes">
            <p>These character builds are incomplete and missing items:</p>
            <ul>
    '''

        for category, count in sorted(loadout_counts.items(), key=lambda x: -x[1]):
            if category in incomplete_categories:
                percentage = f"{(count / total * 100):.1f}%"
                collapsible_html += f"<li><strong>{category}:</strong> {count} ({percentage})</li>"

        collapsible_html += "</ul></div></div>"
        summary_html = f"""
            <p><strong>Characters with no weapons in either weapon slot:</strong> {empty_loadout_count}</p>
            <p><strong>Characters with no weapons on swap:</strong> {partially_empty_set_count}</p><br>
        """

        return complete_html + "<br>" + collapsible_html + "<br>" + summary_html


    def process_magic_and_rare_items(all_characters, magic_counters, rare_counters, magic_users, rare_users):
        with open("ladder_sc.json", "r") as file:
            all_characters = json.load(file)  # Ensure it's a list of dictionaries
        print(f"Total characters loaded by process_magic_and_rare_items: {len(all_characters)}")
#        equipped_items = char_data.get("Equipped", [])
#        print(f"Equipped: {equipped_items}")  # Prints raw data
        magic_counters = {category: Counter() for category in magic_counters}
        rare_counters = {category: Counter() for category in rare_counters}
        magic_users = {category: {} for category in magic_counters}
        rare_users = {category: {} for category in rare_counters}

        def categorize_worn_slot(worn_category, text_tag):
            if worn_category in ["sweapon1", "weapon1", "sweapon2", "weapon2"]:
                if text_tag == "Arrows":
                    return "Arrows"
                elif text_tag == "Bolts":
                    return "Bolts"
                else:
                    return "Weapons and Shields"

            worn_category_map = {
                "ring1": "Rings", "ring2": "Rings",
                "body": "Armor",
                "gloves": "Gloves",
                "belt": "Belts",
                "helmet": "Helmets",
                "boots": "Boots",
                "amulet": "Amulets",
            }

            return worn_category_map.get(worn_category, "Other")  # Default to "Other"

        # Process each character in the consolidated JSON
        for char_data in all_characters:
#            print(f"Checking {char_data.get('Name', 'Unknown')} - Equipped items: {len(char_data.get('Equipped', []))}")
            try:
                char_name = char_data.get("Name", "Unknown")
                char_class = char_data.get("Class", "Unknown")
                char_level = char_data.get("Stats", {}).get("Level", "Unknown")
                character_info = {"name": char_name, "class": char_class, "level": char_level}

                seen_magic_items = {category: set() for category in magic_counters}
                seen_rare_items = {category: set() for category in rare_counters}

                for item in char_data.get("Equipped", []):
                    worn_category = categorize_worn_slot(item.get("Worn", ""), item.get("TextTag", ""))
                    character_info = {"name": char_name, "class": char_class, "level": char_level}

                    if item.get("QualityCode") == "q_magic":
                        magic_counters[worn_category][item["Title"]] += 1
                        magic_users.setdefault(worn_category, {}).setdefault(item["Title"], []).append(character_info)

                    if item.get("QualityCode") == "q_rare":
                        rare_counters[worn_category][item["Title"]] += 1
                        rare_users.setdefault(worn_category, {}).setdefault(item["Title"], []).append(character_info)

            except (KeyError, TypeError) as e:
                print(f"Error processing character: {char_name}, Error: {e}")
                continue

        return magic_counters, magic_users, rare_counters, rare_users

    def GetSCFunFacts():
        # Path to the consolidated JSON file
        consolidated_file = "ladder_sc.json"

        # Load character data from the consolidated JSON file
        try:
            with open(consolidated_file, "r") as file:
                characters = json.load(file)  # Load all characters into a list
#            print(all_characters[:5])  # Display the first 5 elements

        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading consolidated JSON file: {e}")
            return ""

        # Extract alive characters
        alive_characters = [char for char in characters if not char.get("IsDead", True)]
        undead_count = len(alive_characters)

        # Function to format the alive characters list
        def GetTheLiving():
            return "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char.get("Name", "Unknown")}" target="_blank">
                            {char.get("Name", "Unknown")}
                        </a>
                    </div>
                    <div>Level {char.get("Stats", {}).get("Level", "N/A")} {char.get("Class", "Unknown")}</div>
                    <div class="hover-trigger" data-character-name="{char.get("Name", "Unknown")}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """
                for char in alive_characters
            )

        alive_list_html = GetTheLiving()

        # Function to get top 5 characters for a given stat
        def get_top_characters(stat_name):
            ranked = sorted(
                characters,
                key=lambda c: c.get("Stats", {}).get(stat_name, 0) + c.get("Bonus", {}).get(stat_name, 0),
                reverse=True,
            )[:5]

            return "".join(
                f"""<li>&nbsp;&nbsp;&nbsp;&nbsp;
                    <a href="https://beta.pathofdiablo.com/armory?name={char.get('Name', 'Unknown')}" target="_blank">
                        {char.get('Name', 'Unknown')} ({char.get('Stats', {}).get(stat_name, 0) + char.get('Bonus', {}).get(stat_name, 0)})
                    </a>
                </li>"""
                for char in ranked
            )
        # lists for median calculations
        mf_values = []
        gf_values = []
        life_values = []
        mana_values = []

        # Get the top 5 for each stat
        top_strength = get_top_characters("Strength")
        top_dexterity = get_top_characters("Dexterity")
        top_vitality = get_top_characters("Vitality")
        top_energy = get_top_characters("Energy")
        top_life = get_top_characters("Life")
        top_mana = get_top_characters("Mana")

        # Compute Magic Find (MF) and Gold Find (GF)
        total_mf = 0
        total_gf = 0
        total_life = 0
        total_mana = 0
        character_count = len(characters)

        for char in characters:
            mf = char.get("Bonus", {}).get("MagicFind", 0) + \
                char.get("Bonus", {}).get("WeaponSetMain", {}).get("MagicFind", 0) + \
                char.get("Bonus", {}).get("WeaponSetOffhand", {}).get("MagicFind", 0)
            gf = char.get("Bonus", {}).get("GoldFind", 0) + \
                char.get("Bonus", {}).get("WeaponSetMain", {}).get("GoldFind", 0) + \
                char.get("Bonus", {}).get("WeaponSetOffhand", {}).get("GoldFind", 0)
            life = char.get("Stats", {}).get("Life", 0)
            mana = char.get("Stats", {}).get("Mana", 0)

            total_mf += mf
            total_gf += gf
            total_life += life
            total_mana += mana

            mf_values.append(mf)
            gf_values.append(gf)
            life_values.append(life)
            mana_values.append(mana)

        top_magic_find = get_top_characters("MagicFind")
        top_gold_find = get_top_characters("GoldFind")

        # Calculate averages
        average_mf = total_mf / character_count if character_count > 0 else 0
        average_gf = total_gf / character_count if character_count > 0 else 0
        average_life = total_life / character_count if character_count > 0 else 0
        average_mana = total_mana / character_count if character_count > 0 else 0

        #calculate medians
        median_mf = statistics.median(mf_values) if mf_values else 0
        median_gf = statistics.median(gf_values) if gf_values else 0
        median_life = statistics.median(life_values) if life_values else 0
        median_mana = statistics.median(mana_values) if mana_values else 0

        def count_half_freeze_and_cbf(json_path="ladder_sc.json"):
            with open(json_path, "r") as file:
                all_characters = json.load(file)

            character_counts = Counter()
            source_counts = Counter()
            cbf_absent_count = 0
            cbf_absent_characters = []  # 🔥 Track characters who lack CBF

            for char_data in all_characters:
                if isinstance(char_data, str):
                    char_data = json.loads(char_data)

                half_freeze_sources = 0
                has_cbf = False

                for item in char_data.get("Equipped", []):
                    title = item.get("Title", "Unknown")
                    item_tagged = False

                    for prop in item.get("PropertyList", []):
                        prop_lower = prop.lower()
                        if "half freeze duration" in prop_lower:
                            half_freeze_sources += 1
                            source_counts[title] += 1
                            item_tagged = True
                            break
                        if "cannot be frozen" in prop_lower:
                            has_cbf = True

                    if not item_tagged:
                        for socket in item.get("Sockets", []):
                            socket_title = socket.get("Title", "Unknown")
                            for prop in socket.get("PropertyList", []):
                                prop_lower = prop.lower()
                                if "half freeze duration" in prop_lower:
                                    half_freeze_sources += 1
                                    source_counts[socket_title] += 1
                                    item_tagged = True
                                    break
                                if "cannot be frozen" in prop_lower:
                                    has_cbf = True
                            if item_tagged:
                                break

                if half_freeze_sources == 1:
                    character_counts["1_source"] += 1
                elif half_freeze_sources >= 2:
                    character_counts["2_or_more_sources"] += 1
                    if not has_cbf:
                        cbf_absent_count += 1
                        name = char_data.get("Name", "Unknown")
                        account = char_data.get("Account", char_data.get("account", ""))
                        link = f"https://beta.pathofdiablo.com/character/{name}" if name else "javascript:void(0);"
                        name = char_data.get("Name", "Unknown")
                        account = char_data.get("Account", char_data.get("account", ""))
                        level = char_data.get("Stats", {}).get("Level", "N/A")
                        char_class = char_data.get("Class", "Unknown")
                        cbf_absent_characters.append((name, account, level, char_class))

            return character_counts, source_counts, cbf_absent_count, cbf_absent_characters
        char_counts, item_sources, cbf_absent, cbf_absent_characters = count_half_freeze_and_cbf()

        cbf_absent_html = "".join(
            f"""
            <div class="character-info">
                <div class="character-link">
                    <a href="https://beta.pathofdiablo.com/armory?name={name}" target="_blank">{name}</a>
                </div>
                <div>Level {level} {char_class}</div>
                <div class="hover-trigger" data-character-name="{name}"></div>
            </div>
            <div class="character">
                <div class="popup hidden"></div>
            </div>
            """
            for name, account, level, char_class in cbf_absent_characters
        )

        
        # Generate fun facts HTML
        fun_facts_html = f"""
        <h3 id="fun-facts">Softcore Fun Facts <a href="#fun-facts" class="anchor-link"><img src="icons/anchor.png" alt="🔗" class="anchor-icon"></a></h3>
            <h3>{undead_count} Characters in the Softcore top {character_count} have not died</h3>
                <button type="button" class="collapsible sets-button">
                    <img src="icons/Special_click.png" alt="Undead Open" class="icon open-icon hidden">
                    <img src="icons/Special.png" alt="Undead Close" class="icon close-icon">
                </button>
                <div class="content">  
                    <div id="special">{alive_list_html}</div>
                </div>
        <br>

            <h3>{cbf_absent} Characters acheive Cannot Be Frozen through 2 or more sources of Half Freeze Duration</h3>
            <button type="button" class="collapsible sets-button">
                <img src="icons/Special_click.png" alt="CBF Missing Open" class="icon open-icon hidden">
                <img src="icons/Special.png" alt="CBF Missing Close" class="icon close-icon">
            </button>
            <div class="content">
                <div id="cbf-missing">{cbf_absent_html}</div>
            </div>
        <br>

        <!-- Strength & Dexterity Row -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Top 5 Characters with the most Strength:</h3>
                <ul>{top_strength}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Top 5 Characters with the most Dexterity:</h3>
                <ul>{top_dexterity}</ul>
            </div>
        </div>

        <!-- Vitality & Energy Row -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Top 5 Characters with the most Vitality:</h3>
                <ul>{top_vitality}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Top 5 Characters with the most Energy:</h3>
                <ul>{top_energy}</ul>
            </div>
        </div>

        <!-- Life & Mana Row -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>The 5 Characters with the Most Life*:</h3>
                <ul>{top_life}</ul>
                <p><strong>Average Life:</strong> {average_life:.2f} | <strong>Median Life:</strong> {median_life:.2f}</p>
            </div>
            <div class="fun-facts-column">
                <h3>The 5 Characters with the Most Mana*:</h3>
                <ul>{top_mana}</ul>
                <p><strong>Average Mana:</strong> {average_mana:.2f} | <strong>Median Mana:</strong> {median_mana:.2f}</p>
            </div>
        </div>
        <em>*"Most" Life and Mana values are from a snapshot in time and may or may not be affected by bonuses from BO, Oak, etc.</em>
        <!-- Magic Find & Gold Find Row -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>The 5 Characters with the Most Magic Find:</h3>
                <ul>{top_magic_find}</ul>
                <p><strong>Average Magic Find:</strong> {average_mf:.2f} | <strong>Median:</strong> {median_mf:.2f}</p>
            </div>
            <div class="fun-facts-column">
                <h3>The 5 Characters with the Most Gold Find:</h3>
                <ul>{top_gold_find}</ul>
                <p><strong>Average Gold Find:</strong> {average_gf:.2f} | <strong>Median:</strong> {median_gf:.2f}</p>
            </div>
        </div>
        """

        return fun_facts_html

    # Generate fun facts
    fun_facts_html = GetSCFunFacts()

    # Process the files in the data folder
    class_counts, runeword_counter, unique_counter, set_counter, synth_counter, runeword_users, unique_users, set_users, synth_users, crafted_counters, crafted_users, all_equipped_items = process_all_characters()
    magic_counters, magic_users, rare_counters, rare_users = process_magic_and_rare_items(all_characters, magic_counters, rare_counters, magic_users, rare_users)

    from items_list import all_the_items
    two_handed_counts, two_handed_users = count_two_handed_weapons(
        all_equipped_items,
        all_the_items["two_handed_bases"]
    )

    # Example: print top 10 most common
    for title, count in two_handed_counts.most_common(20):
        print(f"{title}: {count}")

    # Print the class counts
    print("Class Counts:")
    for char_class, count in class_counts.items():
        print(f"{char_class}: {count} characters")

    # Print the most and least common items
    def print_item_counts(title, counter):
        print(f"\n{title}:")
        most_common = counter.most_common(10)
        least_common = counter.most_common()[:-11:-1]
        for item, count in most_common:
            print(f"Most common - {item}: {count}")
        for item, count in least_common:
            print(f"Least common - {item}: {count}")

    #print_item_counts("Runewords", runeword_counter)
    #print_item_counts("Uniques", unique_counter)
    #print_item_counts("Set Items", set_counter)

    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    from matplotlib.font_manager import FontProperties

    # Generate pie chart data
    classes = list(class_counts.keys())
    counts = list(class_counts.values())
    total = sum(counts)


    # Load custom font
     # Load custom font
    armory = FontProperties(fname='armory/font/avqest.ttf')  # Update path if needed

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return f'{pct:.1f}% ({val})'
        return my_autopct

    # Timestamp for title
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Set figure size
    plt.figure(figsize=(22, 22))
    plt.subplots_adjust(top=0.5, bottom=0.15)

    # Create the pie chart
    wedges, texts, autotexts = plt.pie(
        counts, labels=classes, autopct=make_autopct(counts), startangle=250, 
        colors=plt.cm.Paired.colors, radius=1.4, textprops={'fontsize': 30, 'color': 'white', 'fontproperties': armory}
    )


    title = plt.title(
        f"Class Distribution of all {total} characters with a ladder ranking\n\nAs of {timestamp}", 
        pad=50, fontsize=40, fontproperties=armory, loc='left', color="white"
    )
    title.set_fontsize(45)  # 🔹 Force title size after creation

    for text in texts:
        text.set_fontsize(35)  # Class labels
    for autotext in autotexts:
        autotext.set_fontsize(25)  # Percentages on slices
        autotext.set_color('black')

    plt.axis('equal')  # Ensures the pie chart is circular

    # Save the plot with transparent background
    plt.savefig("charts/class_distribution.png", dpi=300, bbox_inches='tight', transparent=True)

    print("Plot saved as class_distribution.png")

    # Display the plot
    plt.show()


    # Get the most common items
    most_common_runewords = runeword_counter.most_common(10)
    most_common_uniques = unique_counter.most_common(10)
    most_common_set_items = set_counter.most_common(10)

    # Get all the items
    all_uniques = unique_counter.most_common(150)
    all_runewords = runeword_counter.most_common(150)
    all_uniques_all = unique_counter.most_common(450)
    all_set = set_counter.most_common(150)
    all_synth = synth_counter.most_common(150)

    # Get the least common items
    least_common_runewords = runeword_counter.most_common()[:-11:-1]
    least_common_uniques = unique_counter.most_common()[:-11:-1]
    least_common_set_items = set_counter.most_common()[:-11:-1]

    def slugify(name):
        return name.lower().replace(" ", "-").replace("'", "").replace('"', "")

    # Generate list items
    def generate_list_items(items):
        return ''.join(
            f'<li><a href="#{slug}">{name}</a>: {count}</li>'
            for item, count in items
            for name in [  # map item IDs to readable names
                "Delirium" if item == "2693" else 
                "Pattern2" if item == "-26" else 
                item
            ]
            for slug in [slugify(name)]
        )

    def generate_all_list_items(counter, character_data):
        if not isinstance(character_data, dict):
            print("Error: character_data is not a dict! Type:", type(character_data))
            return ""

        items_html = ""

        for item, count in counter:
            display_item = "Delirium" if item == "2693" else "Pattern2" if item == "-26" else item
            anchor_id = slugify(display_item)

            character_info = character_data.get(item)

            # 🧠 If this item has nested dicts (base → [characters]), it's a runeword
            if isinstance(character_info, dict):
                base_html = ""
                for base, characters in sorted(character_info.items(), key=lambda kv: len(kv[1]), reverse=True):
                    characters_html = "".join(
                        f""" 
                        <div class="character-info">
                            <div class="character-link">
                                <a href="https://beta.pathofdiablo.com/armory?name={char['name']}" target="_blank">
                                    {char['name']}
                                </a>
                            </div>
                            <div>Level {char['level']} {char['class']}</div>
                            <div class="hover-trigger" data-character-name="{char['name']}"></div>
                        </div>
                        <div class="character"><div class="popup hidden"></div></div>
                        """ for char in characters
                    )

                    base_html += f"""
                    <button class="collapsible">
                        <img src="icons/open-grey.png" class="icon-small open-icon hidden">
                        <img src="icons/closed-grey.png" class="icon-small close-icon">
                        <strong>{base} ({len(characters)} users)</strong>
                    </button>
                    <div class="content" id="{slugify(f"{display_item}-{base}")}">
                        {characters_html or "<p>No characters using this base.</p>"}
                    </div>
                    """

                items_html += f"""
                <button class="collapsible">
                    <img src="icons/open-grey.png" class="icon-small open-icon hidden">
                    <img src="icons/closed-grey.png" class="icon-small close-icon">
                    <strong>
                        <a href="#{anchor_id}" class="anchor-link">
                            {display_item} ({count} users)
                        </a>
                    </strong>
                </button>
                <div class="content" id="{anchor_id}">
                    {base_html or "<p>No characters using this item.</p>"}
                </div>
                """

            else:
                # 🧠 Flat list: uniques, sets, synths
                character_list = character_info or []

                character_list_html = "".join(
                    f""" 
                    <div class="character-info">
                        <div class="character-link">
                            <a href="https://beta.pathofdiablo.com/armory?name={char['name']}" target="_blank">
                                {char['name']}
                            </a>
                        </div>
                        <div>Level {char['level']} {char['class']}</div>
                        <div class="hover-trigger" data-character-name="{char['name']}"></div>
                    </div>
                    <div class="character"><div class="popup hidden"></div></div>
                    """ for char in character_list
                )

                items_html += f"""
                <button class="collapsible">
                    <img src="icons/open-grey.png" class="icon-small open-icon hidden">
                    <img src="icons/closed-grey.png" class="icon-small close-icon">
                    <strong>
                        <a href="#{anchor_id}" class="anchor-link">
                            {display_item} ({count} users)
                        </a>
                    </strong>
                </button>
                <div class="content" id="{anchor_id}">
                    {character_list_html or "<p>No characters using this item.</p>"}
                </div>
                """

        return items_html

    def generate_synth_list_items(counter: Counter, synth_users: dict):
        items_html = ""
#        for item, count in counter.items():
        for item, count in sorted(counter.items(), key=lambda x: (-x[1], x[0])):

            character_list = synth_users.get(item, [])  # Directly fetch correct list

            character_list_html = "".join(
                f""" 
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in character_list
            )

            anchor_id = slugify(item)
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>
                <a href="#synth-{anchor_id}" class="anchor-link">
                    {item} ({count} users)
                </a>
                </strong>
            </button>
            <div class="content" id="synth-{anchor_id}">
                {character_list_html if character_list else "<p>No characters using this item.</p>"}
            </div>
            """
        
        return items_html

    synth_user_count = sum(len(users) for users in synth_users.values())

    def generate_synth_source_list(synth_sources):
        items_html = ""

#        for source_item, characters in synth_sources.items():
        for source_item, characters in sorted(synth_sources.items(), key=lambda x: (-len(x[1]), x[0])):
    
            character_list_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div>Used in: <strong>{char["synthesized_item"]}</strong></div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in characters
            )

            anchor_id = slugify(source_item)
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>
                <a href="#synthsource-{anchor_id}" class="anchor-link">
                    {source_item} (Found in {len(characters)} Items)
                </a>
                </strong>
            </button>
            <div class="content" id="synthsource-{anchor_id}">
                {character_list_html if characters else "<p>No characters using this item.</p>"}
            </div>
            """

        return items_html
    synth_source_user_count = sum(len(users) for users in synth_sources.values())


    def generate_crafted_list_items(crafted_counters, crafted_users):
        items_html = ""

        for worn_category, counter in crafted_counters.items():
            if not counter:  # Skip empty categories
                continue
            
            unique_users = {char["name"]: char for item in counter for char in crafted_users.get(worn_category, {}).get(item, [])}
            # Skip categories with no users
            if not unique_users:
                continue

            # Collect all characters in this category
            category_users = []
            for item, count in counter.items():
                category_users.extend(crafted_users.get(worn_category, {}).get(item, []))

            # Skip categories with no users
            if not category_users:
                continue

            # Create the list of all users in this category
            character_list_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in category_users
            )

            # Create a collapsible button for each category
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>Crafted {worn_category} ({len(category_users)} users)</strong>
            </button>
            <div class="content">
                {character_list_html if category_users else "<p>No characters using crafted items in this category.</p>"}
            </div>
            """

        return items_html
    craft_user_count = len({char["name"] for users in crafted_users.values() for item_users in users.values() for char in item_users})
    craft_user_count = sum(len(users) for users in crafted_users.values())


    def generate_magic_list_items(magic_counters, magic_users):
        items_html = ""

        for worn_category, counter in magic_counters.items():
            if not counter:  # Skip empty categories
                continue

            # Collect unique characters in this category
            unique_users = {char["name"]: char for item in counter for char in magic_users.get(worn_category, {}).get(item, [])}

            # Skip categories with no users
            if not unique_users:
                continue

            # Create the list of all unique users in this category
            character_list_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in unique_users.values()
            )

            # Create a collapsible button for each category
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>Magic {worn_category} ({len(unique_users)} users)</strong>
            </button>
            <div class="content">
                {character_list_html if unique_users else "<p>No characters using magic items in this category.</p>"}
            </div>
            """

        return items_html

    # ✅ Count total **unique** magic item users across all categories
    magic_user_count = len({char["name"] for users in magic_users.values() for item_users in users.values() for char in item_users})
    magic_user_count = sum(len(users) for users in magic_users.values())


    def generate_rare_list_items(rare_counter, rare_users):
        items_html = ""

        for worn_category, counter in rare_counter.items():
            if not counter:  # Skip empty categories
                continue

            # Collect unique characters in this category
            unique_users = {char["name"]: char for item in counter for char in rare_users.get(worn_category, {}).get(item, [])}

            # Skip categories with no users
            if not unique_users:
                continue

            # Create the list of all unique users in this category
            character_list_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in unique_users.values()
            )

            # Create a collapsible button for each category
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>Rare {worn_category} ({len(unique_users)} users)</strong>
            </button>
            <div class="content">
                {character_list_html if unique_users else "<p>No characters using Rare items in this category.</p>"}
            </div>
            """

        return items_html

    # ✅ Count total **unique** rare item users across all categories
    rare_user_count = len({char["name"] for users in rare_users.values() for item_users in users.values() for char in item_users})
    rare_user_count = sum(len(users) for users in rare_users.values())

    def socket_html(sorted_runes, sorted_excluding_runes, all_other_items):
        just_socketed = []  # ✅ Holds ALL socketed items  
        just_socketed_excluding_runewords = []  # ✅ Should hold socketed items EXCEPT those inside runewords  

        def extract_element(item):
            if item.get('Title') == 'Rainbow Facet':
                element_types = ["fire", "cold", "lightning", "poison", "physical", "magic"]
                for element in element_types:
                    for prop in item.get('PropertyList', []):
                        if element in prop.lower():
                            return element.capitalize()
            return item.get('Title', 'Unknown')  # Use title if not "Rainbow Facet"


        # Define runes separately
        rune_names = {
            "El Rune", "Eld Rune", "Tir Rune", "Nef Rune", "Eth Rune", "Ith Rune", "Tal Rune", "Ral Rune", "Ort Rune", "Thul Rune", "Amn Rune", "Sol Rune",
            "Shael Rune", "Dol Rune", "Hel Rune", "Io Rune", "Lum Rune", "Ko Rune", "Fal Rune", "Lem Rune", "Pul Rune", "Um Rune", "Mal Rune", "Ist Rune",
            "Gul Rune", "Vex Rune", "Ohm Rune", "Lo Rune", "Sur Rune", "Ber Rune", "Jah Rune", "Cham Rune", "Zod Rune"
        }

        # Categorize worn slots
        def categorize_worn_slot(worn_category, text_tag):
            if worn_category in ["sweapon1", "weapon1", "sweapon2", "weapon2"]:
                if text_tag == "Arrows":
                    return "Arrows"
                elif text_tag == "Bolts":
                    return "Bolts"
                else:
                    return "Weapons and Shields"

            worn_category_map = {
                "ring1": "Rings", "ring2": "Rings",
                "body": "Armor",
                "gloves": "Gloves",
                "belt": "Belts",
                "helmet": "Helmets",
                "boots": "Boots",
                "amulet": "Amulets",
            }
            return worn_category_map.get(worn_category, "Other")  # Default to "Other"

        # Extract element type from Rainbow Facets
        def extract_element(item):
            if item.get('Title') == 'Rainbow Facet':
                element_types = ["fire", "cold", "lightning", "poison", "physical", "magic"]
                for element in element_types:
                    for prop in item.get('PropertyList', []):
                        if element in prop.lower():
                            return element.capitalize()
            return item.get('Title', 'Unknown')  # Use title if not "Rainbow Facet"

        # Function to process all characters from the single JSON file
        def process_all_items(json_file):
            with open(json_file, "r") as file:
                all_characters = json.load(file)  # ✅ Read all characters at once

            # Initialize counters
            all_items = []  
            socketed_items = []  
            items_excluding_runewords = []  
            facet_elements = defaultdict(list)
            
            shields_for_skulls = []
            weapons_for_skulls = []
            helmets_for_skulls = []
            armor_for_skulls = []
            
            jewel_counts = Counter()
            jewel_groupings = {"magic": [], "rare": []}

            # Process each character
            for char_data in all_characters:
                for item in char_data.get('Equipped', []):
                    
                    # Process Skull socketing locations
                    if item.get('Worn') == 'helmet':
                        if any(s.get('Title') == "Perfect Skull" for s in item.get('Sockets', [])):
                            helmets_for_skulls.append(item)
                    elif item.get('Worn') == 'body':
                        if any(s.get('Title') == "Perfect Skull" for s in item.get('Sockets', [])):
                            armor_for_skulls.append(item)
                    elif item.get('Worn') in ['weapon1', 'weapon2', 'sweapon1', 'sweapon2']:
                        is_shield = any("Block" in prop for prop in item.get('PropertyList', []))
                        for socketed_item in item.get('Sockets', []):
                            if socketed_item.get('Title') == "Perfect Skull":
                                if is_shield:
                                    shields_for_skulls.append(socketed_item)
                                else:
                                    weapons_for_skulls.append(socketed_item)

                    # Process Socketed Items
                    if item.get('SocketCount', '0') > '0':  # Check if item has sockets
                        all_items.append(item)
                        if item.get('QualityCode') != 'q_runeword':  # Exclude runewords
                            items_excluding_runewords.append(item)

                        for socketed_item in item.get('Sockets', []):
                            element = extract_element(socketed_item)
                            socketed_items.append(socketed_item)
                            facet_elements[element].append(socketed_item)

                            just_socketed.append(socketed_item)

                            # ✅ Extract QualityCode for categorization
                            quality_code = socketed_item.get('QualityCode', '')

                            # ✅ Separate Magic and Rare Jewels
                            if quality_code == "q_magic":
                                socketed_item["GroupedTitle"] = "Misc. Magic Jewels"
                            elif quality_code == "q_rare":
                                socketed_item["GroupedTitle"] = "Misc. Rare Jewels"
                            else:
                                socketed_item["GroupedTitle"] = socketed_item.get("Title", "Unknown")  # Default title

                            if item.get('QualityCode') != 'q_runeword':
                                items_excluding_runewords.append(socketed_item)
                                just_socketed_excluding_runewords.append(socketed_item)

                            if socketed_item.get('Title') == 'Rainbow Facet':
                                facet_elements[element].append(socketed_item)

            return (
                all_items, socketed_items, items_excluding_runewords,
                just_socketed, just_socketed_excluding_runewords, facet_elements,
                shields_for_skulls, weapons_for_skulls, helmets_for_skulls, armor_for_skulls
            )

        # Function to count item types
        def count_items_by_type(items):
            rune_counter = Counter()
            non_rune_counter = Counter()
            magic_jewel_counter = Counter()
            rare_jewel_counter = Counter()
            facet_counter = defaultdict(lambda: {"count": 0, "perfect": 0})

            for item in items:
                title = item.get('Title', 'Unknown')
                quality = item.get('QualityCode', '')

                if title in rune_names:  # ✅ Sort runes separately
                    rune_counter[title] += 1
                elif "Rainbow Facet" in title:  # ✅ Sort Rainbow Facets separately
                    element = extract_element(item)
                    facet_counter[element]["count"] += 1

                    # ✅ Check for perfect (both +5% and -5% properties)
                    properties = item.get('PropertyList', [])
                    if any("+5" in prop for prop in properties) and any("-5" in prop for prop in properties):
                        facet_counter[element]["perfect"] += 1
                elif quality == "q_magic":  # ✅ Track Magic Jewels with splash
                    has_splash = any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ias = any("attack speed" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ed = any("enhanced damage" in prop.lower() for prop in item.get("PropertyList", []))
                    
                    magic_jewel_counter["Misc. Magic Jewels"] += 1
                    if has_splash:
                        magic_jewel_counter["splash"] += 1
                    if has_ias:
                        magic_jewel_counter["attack speed"] += 1
                    if has_ed:
                        magic_jewel_counter["enhanced damage"] += 1
                elif quality == "q_rare":  # ✅ Track Rare Jewels with splash
                    has_splash = any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    rare_jewel_counter["Misc. Rare Jewels"] += 1
                    if has_splash:
                        rare_jewel_counter["splash"] += 1
                else:  # ✅ All other non-rune items
                    non_rune_counter[title] += 1

            return rune_counter, non_rune_counter, magic_jewel_counter, rare_jewel_counter, facet_counter

        # Example Usage
        json_file = "ladder_sc.json"
        all_items, socketed_items, *_ = process_all_items(json_file)
        just_socketed_runes, just_socketed_non_runes, *_ = count_items_by_type(socketed_items)


        def count_items_by_type(items):
            rune_counter = Counter()
            non_rune_counter = Counter()
            magic_jewel_counter = Counter()
            rare_jewel_counter = Counter()
            facet_counter = defaultdict(lambda: {"count": 0, "perfect": 0})
            skull_counter = Counter()

            for item in items:
                title = item.get('Title', 'Unknown')
                quality = item.get('QualityCode', '')

                if title in rune_names:  # ✅ Sort runes separately
                    rune_counter[title] += 1
                elif "Rainbow Facet" in title:  # ✅ Sort Rainbow Facets separately
                    element = extract_element(item)
                    facet_counter[element]["count"] += 1

                    # ✅ Check for perfect (both +5% and -5% properties)
                    properties = item.get('PropertyList', [])
                    if any("+5" in prop for prop in properties) and any("-5" in prop for prop in properties):
                        facet_counter[element]["perfect"] += 1
                elif quality == "q_magic":  # ✅ Track Magic Jewels with splash
                    has_splash = any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ias = any("attack speed" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ed = any("enhanced damage" in prop.lower() for prop in item.get("PropertyList", []))
                    has_iassplash = any("attack speed" in prop.lower() for prop in item.get("PropertyList", [])) & any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    has_iased = any("attack speed" in prop.lower() for prop in item.get("PropertyList", [])) & any("enhanced damage" in prop.lower() for prop in item.get("PropertyList", []))
                    magic_jewel_counter["Misc. Magic Jewels"] += 1
                    if has_splash:
                        magic_jewel_counter["splash"] += 1
                    if has_ias:
                        magic_jewel_counter["attack speed"] += 1
                    if has_ed:
                        magic_jewel_counter["enhanced damage"] += 1
                    if has_iassplash:
                        magic_jewel_counter["iassplash"] += 1
                    if has_iased:
                        magic_jewel_counter["iased"] += 1
#                    if has_splash & has_ias:
#                        magic_jewel_counter["splash"] += 1
                elif quality == "q_rare":  # ✅ Track Rare Jewels with splash
                    has_splash = any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ed = any("enhanced damage" in prop.lower() for prop in item.get("PropertyList", []))
                    rare_jewel_counter["Misc. Rare Jewels"] += 1
                    if has_splash:
                        rare_jewel_counter["splash"] += 1
                    if has_ed:
                        rare_jewel_counter["enhanced damage"] += 1
#                elif "Perfect Skull" in title:  # ✅ Sort Rainbow Facets separately
#                    skull_counter[title] += 1
                else:  # ✅ All other non-rune items
                    non_rune_counter[title] += 1

            return rune_counter, non_rune_counter, magic_jewel_counter, rare_jewel_counter, facet_counter #, skull_counter

        just_socketed_runes, just_socketed_non_runes, just_socketed_magic, just_socketed_rare, just_socketed_facets = count_items_by_type(socketed_items)
        just_socketed_excluding_runewords_runes, just_socketed_excluding_runewords_non_runes, just_socketed_excluding_runewords_magic, just_socketed_excluding_runewords_rare, just_socketed_excluding_runewords_facets = count_items_by_type(just_socketed_excluding_runewords)

        # Use .most_common() to sort data in descending order
        sorted_just_socketed_runes = just_socketed_runes.most_common()
        sorted_just_socketed_excluding_runewords_runes = just_socketed_excluding_runewords_runes.most_common()

        # Combine non-runes, magic, rare, and facets into a single list
        all_other_items = [
            *(f"{item}: {count}" for item, count in just_socketed_excluding_runewords_non_runes.items()),
            f"Misc. Magic Jewels: {just_socketed_excluding_runewords_magic['Misc. Magic Jewels']} ({just_socketed_excluding_runewords_magic['splash']} include melee splash, {just_socketed_excluding_runewords_magic['attack speed']} include IAS, {just_socketed_excluding_runewords_magic['enhanced damage']} include ED; of those, there are {just_socketed_excluding_runewords_magic['iassplash']} IAS/Splash and {just_socketed_excluding_runewords_magic['iased']} IAS/ED)",
            f"Misc. Rare Jewels: {just_socketed_excluding_runewords_rare['Misc. Rare Jewels']} ({just_socketed_excluding_runewords_rare['splash']} include melee splash, {just_socketed_excluding_runewords_rare['enhanced damage']} include ED)",
            *(f"Rainbow Facet ({element}): {counts['count']} ({counts['perfect']} are perfect)" for element, counts in just_socketed_excluding_runewords_facets.items()),
#            f"Perfect Skull:  (tacos)"

        ]
#        return sorted_just_socketed_runes, sorted_just_socketed_excluding_runewords_runes, all_other_items
        return (
            format_socket_html_runes(sorted_just_socketed_runes), 
            format_socket_html_runes(sorted_just_socketed_excluding_runewords_runes), 
            format_socket_html(all_other_items)
        )

    def format_socket_html(counter_data):
        """Formats socketed items as an HTML table or list."""
        if isinstance(counter_data, list):  # If it's a list, format as an unordered list
            items = "".join(f"<li>{item}</li>" for item in counter_data)
            return f"<ul>{items}</ul>"

        elif isinstance(counter_data, Counter):  # If it's a Counter, format as a table
            rows = "".join(f"<tr><td>{item}</td><td>{count}</td></tr>" for item, count in counter_data.items())
            return f"<table><tr><th>Item</th><th>Count</th></tr>{rows}</table>"

        elif isinstance(counter_data, dict):  # If it's a dict (e.g., facet counts), format as a list
            items = "".join(f"<li>{item}: {count['count']} ({count['perfect']} perfect)</li>" for item, count in counter_data.items())
            return f"<ul>{items}</ul>"

        return ""  # Return empty string if there's no data

    def format_socket_html_runes(counter_data):
        """Formats socketed items as an HTML table or list."""
        if isinstance(counter_data, list):  # If it's a list of tuples (like runes), format properly
            items = "".join(f"<li>{item}: {count}</li>" for item, count in counter_data)
            return f"<ul>{items}</ul>"

        elif isinstance(counter_data, Counter):  # If it's a Counter, format as a table
            rows = "".join(f"<tr><td>{item}</td><td>{count}</td></tr>" for item, count in counter_data.items())
            return f"<table><tr><th>Item</th><th>Count</th></tr>{rows}</table>"

        elif isinstance(counter_data, dict):  # If it's a dict (e.g., facet counts), format as a list
            items = "".join(f"<li>{item}: {count['count']} ({count['perfect']} perfect)</li>" for item, count in counter_data.items())
            return f"<ul>{items}</ul>"

        return ""  # Return empty string if there's no data


    # Merc things
    def map_readable_names(mercenary_type, worn_category):
        mercenary_mapping = {
            "Desert Mercenary": "Act 2 Desert Mercenary",
            "Rogue Scout": "Act 1 Rogue Scout",
            "Eastern Sorceror": "Act 3 Eastern Sorceror",
            "Barbarian": "Act 5 Barbarian"
        }
        worn_mapping = {
            "body": "Armor",
            "helmet": "Helmet",
            "weapon1": "Weapon",
            "weapon2": "Offhand"
        }
        readable_mercenary = mercenary_mapping.get(mercenary_type, mercenary_type)
        readable_worn = worn_mapping.get(worn_category, worn_category)
        return readable_mercenary, readable_worn
    # Function to analyze mercenaries from a single JSON fileu
    def analyze_mercenaries(all_characters, runeword_counter, unique_counter, set_counter):
        """Analyzes mercenary equipment, updates global item counters, and tracks which mercs use which items."""
        mercenary_counts = Counter()
        mercenary_equipment = defaultdict(lambda: defaultdict(Counter))
        mercenary_names = Counter()
        merc_users = defaultdict(list)  # ✅ Track mercenary users for each item

        for char_data in all_characters:
            if not isinstance(char_data, dict):
                print(f"Skipping unexpected data format: {char_data}")
                continue  # Skip invalid entries

            mercenary = char_data.get("MercenaryType")
            if mercenary:
                readable_mercenary, _ = map_readable_names(mercenary, "")
                mercenary_counts[readable_mercenary] += 1

                merc_name = char_data.get("MercenaryName", "Unknown")
                mercenary_names[merc_name] += 1

                for item in char_data.get("MercenaryEquipped", []):
                    worn_category = item.get("Worn", "Unknown")
                    readable_mercenary, readable_worn = map_readable_names(mercenary, worn_category)
                    title = item.get("Title", "Unknown")
                    quality = item.get("QualityCode", "default")

                    # ✅ Add mercenary items to global counters
                    if quality == "q_runeword":
                        runeword_counter[title] += 1
                    elif quality == "q_unique":
                        unique_counter[title] += 1
                    elif quality == "q_set":
                        set_counter[title] += 1

                    mercenary_equipment[readable_mercenary][readable_worn][title] += 1

                    # ✅ Track which characters' mercenaries are using each item
                    # ✅ Track which characters' mercenaries are using each item
                    merc_users[title.strip().lower()].append({
                        "Name": char_data.get("Name", "Unknown"),
                        "Class": char_data.get("Class", "Unknown"),
                        "Level": char_data.get("Stats", {}).get("Level", "N/A")
                    })

        return mercenary_counts, mercenary_equipment, mercenary_names, merc_users  # ✅ Return merc_users

           
    def generate_mercenary_report(all_characters, runeword_counter, unique_counter, set_counter):
        """Generates HTML report for mercenaries while ensuring their items are included in the item lists."""
        html_output = "<p><h2>Mercenary Analysis and Popular Equipment</h2></p>"

        # Mercenary type counts
        html_output += "<p><h3>Mercenary Type Counts</h3></p><ul>"
        for mercenary, count in mercenary_counts.items():
            html_output += f"<li>{mercenary}: {count}</li>"
        html_output += "</ul>"

        # Most Common Mercenary Names
        html_output += "<h3>Most Common Mercenary Names</h3><ul>"
        for name, count in mercenary_names.most_common(15):
            html_output += f"<li>{name}: {count}</li>"
        html_output += "</ul>"

        # Popular Equipment by Mercenary Type
        html_output += "<p><h3>Popular Equipment by Mercenary Type</h3></p>"
        for mercenary, categories in mercenary_equipment.items():
            html_output += f"<div class='row'><p><strong>{mercenary}</strong></p>"
            for worn_category, items in categories.items():
                html_output += f"<div class='merccolumn'><strong>Most Common {worn_category}s:</strong>"
                html_output += "<ul>"
                top_items = items.most_common(15)
                for title, count in top_items:
                    html_output += f"<li>{title}: {count}</li>"
                html_output += "</ul></div>"
            html_output += "</div>"

        return html_output

    # ✅ Load the consolidated JSON file
    with open("ladder_sc.json", "r") as file:
        all_characters = json.load(file)


    # ✅ Call analyze_mercenaries and store its results
    mercenary_counts, mercenary_equipment, mercenary_names, merc_users = analyze_mercenaries(
        all_characters, runeword_counter, unique_counter, set_counter
    )

    # ✅ Extract all items used by mercenaries (after calling analyze_mercenaries)
    merc_used_items = set()
    for categories in mercenary_equipment.values():  # Iterate over mercenary types
        for worn_category, items in categories.items():
            merc_used_items.update(items.keys())  # Add all item names to the set

    # Analyze mercenaries while updating item counts
    html_output = generate_mercenary_report(all_characters, runeword_counter, unique_counter, set_counter)

    # Now, the used item lists include mercenary items!

    # Generate the report
#    html_output = generate_mercenary_report(all_characters)

    used_runewords = {item[0] for item in all_runewords}
    used_uniques = {item[0] for item in all_uniques_all}
    used_set_items = {item[0] for item in all_set}
    all_the_items = items_list.all_the_items
    # Ensure `items_list.all_the_items` exists
    try:
        all_the_items = items_list.all_the_items  # ✅ Ensure this is defined
        unused_runewords = {rw.strip().lower() for rw in all_the_items["all_the_runewords"]} - {rw.strip().lower() for rw in used_runewords}
        unused_uniques = {rw.strip().lower() for rw in all_the_items["all_the_uniques"]} - {rw.strip().lower() for rw in used_uniques}
        unused_set_items = {rw.strip().lower() for rw in all_the_items["all_the_sets"]} - {rw.strip().lower() for rw in used_set_items}
    except AttributeError as e:
        print("Error: items_list is not defined or missing required keys.", e)
        unused_runewords = unused_uniques = unused_set_items = set()  # ✅ Prevent crashes

#    print("Unused Runewords:", unused_runewords)
#    print("Unused Unique Items:", unused_uniques)
#    print("Unused Set Items:", unused_set_items)

    # ✅ Ensure merc_used_items is case-insensitive
    merc_used_items = {item.strip().lower() for item in merc_used_items}

    def format_unused_items(items, merc_used_items, merc_users):
        """Converts a set of unused items into an HTML list, with expandy sections for mercs using them."""
        if not items:
            return "<p>No unused items found.</p>"

        html_output = "<ul>"
        
        for item in sorted(items):
            formatted_item = item.strip().lower()
            is_merc_only = formatted_item in merc_used_items
            merc_list = merc_users.get(formatted_item, [])

            # ✅ Generate character list HTML for merc users
            merc_character_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["Name"]}" target="_blank">
                            {char["Name"]}
                        </a>
                    </div>
                    <div>Level {char["Level"]} {char["Class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["Name"]}"><!-- Armory Quickview--></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div>
                </div>
                """
                for char in merc_list
            )

            # ✅ Add collapsible button for mercs
            merc_html_section = ""
            if merc_list:
                merc_html_section = f"""
                <button class="collapsible">
                    <img src="icons/open-grey.png" alt="Expand Mercenaries" class="icon-small open-icon hidden">
                    <img src="icons/closed-grey.png" alt="Collapse Mercenaries" class="icon-small close-icon">
                    <p>Characters whose mercs use {item}</p>
                </button>
                <div class="content">
                    {merc_character_html if merc_character_html else "<p>No mercenaries using this item.</p>"}
                </div>
                """

            # ✅ Add item to list with (only used on mercenaries) if applicable
            html_output += f"""
            <li>
                <strong>{item} </strong>
                <span style='color:gray;'>{'(only used on mercenaries)' if is_merc_only else ''}</span>
                {merc_html_section}
            </li>
            """

        html_output += "</ul>"
        return html_output
    
    merc_used_items = set(merc_users.keys())  # ✅ All lowercase and stripped
    # ✅ Generate updated HTML
    unused_runewords_html = format_unused_items(unused_runewords, merc_used_items, merc_users)
    unused_uniques_html = format_unused_items(unused_uniques, merc_used_items, merc_users)
    unused_set_items_html = format_unused_items(unused_set_items, merc_used_items, merc_users)

    # Generating the HTML for the results
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Ever wonder how many Shako's are in use? Or what the most popular Sorc skills are? This site provides information about class build trends and item details from characters on the current Path of Diablo (PoD) ladder.">
        <meta name="keywords" content="path of diablo, builds, stats, statistics, data, analysis, analytics">
        <meta name="robots" content="index, follow">
        <title>PoD Softcore Stats</title>
        <link rel="stylesheet" type="text/css" href="./css/test-css.css">
        
        
    </head>
    <body class="special-background">
        <div class="is-clipped">
        <nav class="navbar is-fixed-top is-dark" style="height: 50px;">

            <div class="navbar-brand">
                <a class="is-48x48" href="https://beta.pathofdiablo.com/"><img src="icons/pod.ico" alt="Path of Diablo: Web Portal" width="48" height="48" class="is-48x48" style="height: 48px; width: 48px; margin-left:0;"></a>
    <button class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="podNavbar">
        <br>
        <span></span>
        <span></span>
        <span></span>
    </button>            </div>
            <div id="podNavbar" class="navbar-menu">
                <div class="navbar-start">
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/trade-search">Trade</a>
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/servers">Servers</a>
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/ladder">Ladder</a>
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/public-games">Public Games</a>
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/runewizard">Runewizard</a>
                    <a class="navbar-item" href="https://pathofdiablo.com/p/armory">Armory</a>
                    <a class="navbar-item" href="https://build.pathofdiablo.com">Build Planner</a>
                    <!--<a class="navbar-item" href="https://pathofdiablo.com/p/?live" style="width: 90px;"><span><img src="https://beta.pathofdiablo.com/images/twitchico.png"></span></a>-->
                </div>
                <div class="navbar-end">

                    <div class="navbar-start">	
                        <a class="navbar-item-right" href="https://beta.pathofdiablo.com/my-toons">Character Storage</a>
                        <div class="navbar-item dropdown2">
                            <button class="dropdown2-button">Trends History</button>
                            <div class="dropdown2-content">
                                <a href="https://trends.pathofdiablo.com/Home.html">Current</a>
                                <!--  <a href="https://trends.pathofdiablo.com/Season/14/April/Home">S14</a> -->
                                <div class="dropdown2-item dropdown-sub">
                                    <a class="dropdown-sub-button">S13</a>
                                    <div class="dropdown-sub-content">
                                        <a href="https://trends.pathofdiablo.com/Season/13/July/Home">July</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/June/Home">June</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/May/Home">May</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/April/Home">April</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/March/Home.html">March</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/February/Home.html">February</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        </nav>  

        
        <div class="hamburger" onclick="toggleMenu()">
            <div class="line"></div>
            <div class="line"></div>
            <div class="line"></div>
        </div>
        <div class="top-buttons">
            <a href="Home" class="top-button home-button" onclick="setActive('Home')"></a>
            <a href="#" id="SC_HC" class="top-button"> </a>
            <a href="Amazon" id="Amazon" class="top-button amazon-button"></a>
            <a href="Assassin" id="Assassin" class="top-button assassin-button"></a>
            <a href="Barbarian" id="Barbarian" class="top-button barbarian-button"></a>
            <a href="Druid" id="Druid" class="top-button druid-button"></a>
            <a href="Necromancer" id="Necromancer" class="top-button necromancer-button"></a>
            <a href="Paladin" id="Paladin" class="top-button paladin-button"></a>
            <a href="Sorceress" id="Sorceress" class="top-button sorceress-button"></a>
            <a href="https://github.com/qordwasalreadytaken/pod-stats/blob/main/README.md" class="top-button about-button" target="_blank"></a>
        </div>
<!--    <div class="dropdown">
        <button>When</button>
        <div class="dropdown-content">
            <a href="https://trends.pathofdiablo.com/Home">Current</a>
            <a href="https://trends.pathofdiablo.com/Season/13/February/Home.html">S13-February</a>
            <a href="https://trends.pathofdiablo.com/Season/13/March/Home.html">S13-March</a>
        </div>
    </div>        -->
<div class="main page-intro">
        <h1>PoD SOFTCORE LADDER TOP 1,000 CLASS DISTRIBUTION </h1>
        <h2>Looking at the class distribution for the ladders top 1,000 characters shows which classes are played for longer, a measure of which classes are more popular in the endgame</h2>
        <!-- Embed the Plotly pie chart -->
    <!--     <h2>Pick a class below for more detail</h2>-->
    <!--     <iframe src="cluster_analysis_report.html"></iframe>  -->
        <div>
            <img src="charts/1kclass_distribution.png">
        </div>
        <h2>
            Ladder top 1K Fun Facts
        </h2>
        {kfun_facts_html}
        <br>
        <hr>
        <br>
        <h1>PoD SOFTCORE STATS, ALL RANKED LADDER CHARACTERS</h1>
       <h3>Since there are class ladders in addition to the top 1,000, and many ranked characters do not appear in the top 1k, they are included below and in the rest of the Trends reporting to get as large a data set as possible when looking at item & equipment usage and skill distribution within classes</h3>
        <!-- Embed the Plotly pie chart -->
    <!--     <h2>Pick a class below for more detail</h2>-->
    <!--     <iframe src="cluster_analysis_report.html"></iframe>  -->
        <div>
            <img src="charts/class_distribution.png">
        </div>
        <h3>THESE PAGES INCLUDE DATA FROM ALL AVAILABLE RANKED LADDER CHARACTERS (THE TOP 1,000 AS WELL AS THE TOP 200 FROM EACH CLASS)</h3>
<!--        <h3>UNLESS STATED OTHERWISE, OTHER PAGE STATS AND DATA ARE FROM THE TOP 200 CHARACTERS OF THE RELEVANT CLASS OR CLASSES</h3> -->
    <hr>
        <h3>Class and special pages have taken character data and separated it into probable builds. As such, the groupings and associated data
            will change over time to reflect what is currently accurate.
            <br><br>
            Looking at class and build pages, what you see and what it means:</h3>
        <div>
            <img src="charts/build-pages-legend.png">
        </div>
        <h3>Looking at skills you can assume that:</h3>
        <ul style="padding-left:20px">
         <li>If the first number is 50%, then half of the characters fall into that "build"</li>
         <li>If the percent bar following a skill is 100% then every character in that group has points in that skill</li>
         <li>If the percent is 100% and the total points is high that skill is likely a main skill or synergy </li>
         <li>If the percent is 100% but the total is low that skill is likely one-point-wonder like Hydra and Whirlwind or just a prerequisite </li>
         </ul>
         </h3>
       <!-- Moved the Plotly scatter plot to the bottom -->
        <button onclick="topFunction()" id="backToTopBtn" class="back-to-top"></button>
        <hr> 

<h1>Mercenary reporting</h1>
<h3 id="merc-equipment">
    Mercenary counts and Most Used Runewords, Uniques, and Set items equipped
    <a href="#merc-equipment" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h3>

<button type="button" class="collapsible">
    <img src="icons/Merc_click.png" alt="Merc Details Open" class="icon open-icon hidden">
    <img src="icons/Merc.png" alt="Merc Details Close" class="icon close-icon">
</button>

<div class="content">
    <div id="mercequips">
        {html_output}
    </div>
</div>
<br>
<hr>
<h1>Item And Equipment Stats And Data</h1>
{loadouthtml} 
<hr>
<h2 id="runeword-usage">
    Most and Least Used Runewords, Uniques, and Set items currently equipped by characters
    <a href="#runeword-usage" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
<button type="button" class="collapsible runewords-button">
    <img src="icons/Runewords_click.png" alt="Runewords Open" class="icon open-icon hidden">
    <img src="icons/Runewords.png" alt="Runewords Close" class="icon close-icon">
<!--    <strong>Runewords</strong> -->
</button>
<div class="content">
    <div id="runewords" class="container">
        <div class="column">
            <h3>Most Used Runewords:</h3>
            <ul id="most-popular-runewords">
                {most_popular_runewords}
            </ul>
        </div>
        <div class="column">
            <h3>Least Used Runewords:</h3>
            <ul id="least-popular-runewords">
                {least_popular_runewords}
            </ul>
        </div>
    </div>


    <button type="button" class="collapsible small-collapsible">
        <img src="icons/open.png" alt="All Runewords Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Runewords Close" class="icon-small close-icon">
        <strong>ALL Runewords</strong>
    </button>

    <div class="content">
        <div id="allrunewords">
            {all_runewords}
        </div>
    </div>
</div>

<br>
<button type="button" class="collapsible uniques-button">
    <img src="icons/Uniques_click.png" alt="Uniques Open" class="icon open-icon hidden">
    <img src="icons/Uniques.png" alt="Uniques Close" class="icon close-icon">
<!--    <strong>Uniques</strong>-->
</button>    
<div class="content">   
    <div id="uniques" class="container">
        <div class="column">
            <h3>Most Used Uniques:</h3>
            <ul id="most-popular-uniques">
                {most_popular_uniques}
            </ul>
        </div>
        <div class="column">
            <h3>Least Used Uniques:</h3>
            <ul id="least_popular_uniques">
                {least_popular_uniques}
            </ul>
        </div>
    </div>
    <button type="button" class="collapsible small-collapsible">
        <img src="icons/open.png" alt="All Uniques Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Uniques Close" class="icon-small close-icon">
        <strong>ALL Uniques</strong>
    </button>

    <div class="content">
        <div id="alluniques">
            {all_uniques_all}
        </div>
    </div>

</div>

<br>
<button type="button" class="collapsible sets-button">
    <img src="icons/Sets_click.png" alt="Sets Open" class="icon open-icon hidden">
    <img src="icons/Sets.png" alt="Sets Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
    <div id="sets" class="container">
        <div class="column">
            <h3>Most Used Set Items:</h3>
            <ul id="most-popular-set-items">
                {most_popular_set_items}
            </ul>
        </div>
        <div class="column">
            <h3>Least Used Set Items:</h3>
            <ul id="least_popular_set_items">
                {least_popular_set_items}
            </ul>
        </div>
    </div>
    <button type="button" class="collapsible small-collapsible">
        <img src="icons/open.png" alt="All Set Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Set Close" class="icon-small close-icon">
        <strong>ALL Set</strong>
    </button>

    <div class="content">
        <div id="allset">
            {all_set}
        </div>
    </div>
</div>
<br>
        <hr>
        <h2>Synth reporting</h2>
<h2 id="synth-items">
    {synth_user_count} Characters with Synthesized items equipped
    <a href="#synth-items" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>

<h3>This is base synthesized items</h3>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
</button>  
<div class="content">  
    <div id="special">
        {all_synth}
    </div>
</div>

<h2 id="synth-from">
    {synth_source_user_count} Synthesized FROM listings
    <a href="#synth-from" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
        <h3>This shows where propertied an item are showing up in other items. If you wanted to see where the slow from Kelpie or the Ball light from Ondal's had popped up, this is where to look </h3>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <div id="special">
            {synth_source_data}
        </div>
    </div>


        <br>

<h2 id="craft-reporting">Craft reporting
    <a href="#craft-reporting" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>        
<h3>{craft_user_count} Characters with crafted items equipped</h3>

<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <div id="special">
            {all_crafted}
        </div>
    </div>


<br>
<h2 id="magic-reporting">Magic reporting
    <a href="#magic-reporting" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
        <h3>{magic_user_count} Characters with Magic items equipped</h3>

<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <div id="special">
            {all_magic}
        </div>
    </div>

<br>

<h2 id="rare-reporting">Rare reporting
    <a href="#rare-reporting" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
        <h3>{rare_user_count} Characters with rare items equipped</h3>

<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <div id="special">
            {all_rare}
        </div>
    </div>

<br>

<h2 id="socketable-reporting">Socketable reporting
    <a href="#socketable-reporting" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
        <h3>What are people puting in sockets</h3>

<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <h2>Socketed Runes Count</h2>
        <h3>Includes Only Character Data, No Mercs</h3>
    <div id="special"  class="container">
<br>
        <div class="column">
            <!-- Left Column -->
                <h2>Most Common Runes <br>(Including Runewords)</h2>
            <ul id="sorted_just_socketed_runes"
                {sorted_just_socketed_runes}
            </ul>
            </div>

            <!-- Right Column -->
            <div class="column">
                <h2>Most Common Runes <br>(Excluding Runewords)</h2>
            <ul id="sorted_just_socketed_excluding_runewords_runes">
                {sorted_just_socketed_excluding_runewords_runes}
            </ul>
            </div>
        </div>

        <div>
            <h2>Other Items Found in Sockets</h2>
        <h3>Includes Only Character Data, No Mercs</h3>
            {all_other_items}
        </div>
    </div>
<br>
<h2 id="unused-items">Unused Items
    <a href="#unused-items" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
            <h3>Some items get no love at the top of the ladder *</h3>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">
    <!-- Runewords -->
    <button class="collapsible"> 
        <img src="icons/open.png" alt="Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Close" class="icon-small close-icon">
        <strong>Unused Runewords</strong>
    </button>
    <div class="content">{unused_runewords}</div>

    <!-- Uniques -->
    <button class="collapsible"> 
        <img src="icons/open.png" alt="Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Close" class="icon-small close-icon">
        <strong>Unused Unique Items</strong>
    </button>
    <div class="content">{unused_uniques}</div>

    <!-- Set Items -->
    <button class="collapsible"> 
        <img src="icons/open.png" alt="Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Close" class="icon-small close-icon">
        <strong>Unused Set Items</strong>
    </button>
    <div class="content">{unused_set_items}</div>
</div>
<br>
<em>*Reference list used for <a href="https://github.com/GreenDude120/builds_data/blob/main/items_list.py">all runewords, uniques, and set items</a> can be found here</em>
<br>
<br>
<h2 id="one-two-handed">Characters Weilding 2-Handed Swords
    <a href="#one-two-handed" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
</button>  
<div class="content">
{one_or_two_html}
</div>

<br>
<h2 id="two-handed">Melee Weapons That Require Two Hands
    <a href="#two-handed" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
</button>  
<div class="content">
{runewordbasehtml_output}
</div>
<br>
<h2 id="all-bows">Bows and Crossbows
    <a href="#all-bows" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
</button>  
<div class="content">
{bowbasehtml_output}
</div>


<br>




<hr>

<br>

        <h1>Specialty Searches, Character Builds</h1>
        <h2>Special builds and custom querries that don't fit in class specific pages</h2>
<!--        <h2>Iron Jang Bong & Warpspear</h2>
        <a href="Bong_and_Warpspear"> <img src="icons/Special.png" alt="Iron Jang Bong & Warpspear" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br>
-->
        <h2>Unique Arrows & Bolts</h2>
        <a href="Unique_Bolts_and_Arrows"> <img src="icons/Special.png" alt="Unique Arrows & Bolts" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br>
        <h2>Non-Amazon Bow Users</h2>
        <a href="Notazons"> <img src="icons/Special.png" alt="Non-Amazon Bow Users" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br>
        <h2>Dual Offensive Aura Items Equipped</h2>
        <a href="2AuraItems"> <img src="icons/Special.png" alt="Dual Offensive Aura Items Equipped" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br>
<!--        <h2>Dashing Strikers</h2>
        <a href="Dashadin"> <img src="icons/Special.png" alt="Dashing Strikers" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br> -->
<!--        <h2>Possibly Chargers</h2>
        <a href="Charge"> <img src="icons/Special.png" alt="Possibly Chargers" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br> -->
        <br>
        <hr>
        <h1>Specialty Searches, Misc. Data</h1>
{fun_facts_html}
<br>
<br>        
<br>
<br>


        </div>
        <div class="footer">
        <p>PoD data current as of {timeStamp}</p>
        </div>





<script>
// Collapsible elemets
var coll = document.getElementsByClassName("collapsible");
for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        var openIcon = this.querySelector("img.icon[alt='Open']");
        var closeIcon = this.querySelector("img.icon[alt='Close']");

        if (content.style.display === "block") {
            content.style.display = "none";
            openIcon.classList.remove("hidden");
            closeIcon.classList.add("hidden");
        } else {
            content.style.display = "block";
            openIcon.classList.add("hidden");
            closeIcon.classList.remove("hidden");
        }
    });
}


//Back to top button
var backToTopBtn = document.getElementById("backToTopBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
backToTopBtn.style.display = "block";
} else {
backToTopBtn.style.display = "none";
}
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
document.body.scrollTop = 0; // For Safari
document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

//Trends toolbar
// Trends toolbar
function toggleMenu() {
    const navMenu = document.querySelector('.top-buttons');
    navMenu.classList.toggle('show');
}

document.addEventListener("DOMContentLoaded", function () {
    const scHcButton = document.getElementById("SC_HC");
    const currentUrl = window.location.href;
    const filename = currentUrl.split("/").pop(); // Get the last part of the URL

    // Check if the current page is Hardcore or Softcore
    const isHardcore = filename.startsWith("hc");

    // Update button appearance based on current mode
    if (isHardcore) {
        scHcButton.classList.add("hardcore");
        scHcButton.classList.remove("softcore");
    } else {
        scHcButton.classList.add("softcore");
        scHcButton.classList.remove("hardcore");
    }

    // Update background image based on mode
    updateButtonImage(isHardcore);

    // Add click event to toggle between SC and HC pages
    scHcButton.addEventListener("click", function () {
        let newUrl;

        if (isHardcore) {
            // Convert HC -> SC (remove "hc" from filename)
            newUrl = currentUrl.replace(/hc(\w+)$/, "$1"); // Remove "hc"
        } else {
            // Convert SC -> HC (prepend "hc" to the filename)
            newUrl = currentUrl.replace(/\/(\w+)$/, "/hc$1"); // Prepend "hc"
        }

        // Redirect to the new page
        if (newUrl !== currentUrl) {
            window.location.href = newUrl;
        }
    });

    // Function to update button background image
    function updateButtonImage(isHardcore) {
        if (isHardcore) {
            scHcButton.style.backgroundImage = "url('icons/Hardcore_click.png')";
        } else {
            scHcButton.style.backgroundImage = "url('icons/Softcore_click.png')";
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const currentPage = window.location.pathname.split("/").pop(); // Get current page filename
    const menuItems = document.querySelectorAll(".top-button");

    menuItems.forEach(item => {
        const itemPage = item.getAttribute("href");
        if (itemPage && currentPage === itemPage) {
            item.classList.add("active");
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
const currentPage = window.location.pathname.split("/").pop(); // Get current page filename
const menuItems = document.querySelectorAll(".top-button");

menuItems.forEach(item => {
const itemPage = item.getAttribute("href");
if (itemPage && currentPage === itemPage) {
item.classList.add("active");
}
});
});

//Armory pop up
document.addEventListener("DOMContentLoaded", function () {
let activePopup = null;

document.querySelectorAll(".hover-trigger").forEach(trigger => {
trigger.addEventListener("click", function (event) {
event.stopPropagation();
const characterName = this.getAttribute("data-character-name");

// Close any open popup first
if (activePopup) {
activePopup.classList.remove("active");
activePopup.innerHTML = ""; // Remove iframe for memory efficiency
activePopup = null;
}

// Find the associated popup container
const popup = this.closest(".character-info").nextElementSibling.querySelector(".popup");

// If this popup was already active, just close it
if (popup === activePopup) {
return;
}

// Create an iframe and set its src
const iframe = document.createElement("iframe");
iframe.src = `./armory/video_component.html?charName=${encodeURIComponent(characterName)}`;
iframe.setAttribute("id", "popupFrame");

// Add iframe to the popup
popup.appendChild(iframe);
popup.classList.add("active");

// Set this popup as the active one
activePopup = popup;
});
});

// Close the popup when clicking anywhere outside
document.addEventListener("click", function (event) {
if (activePopup && !activePopup.contains(event.target)) {
activePopup.classList.remove("active");
activePopup.innerHTML = ""; // Remove iframe to free memory
activePopup = null;
}
});
});


//PoD nav buttons
document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.navbar-burger');
    const menu = document.querySelector('.navbar-menu');

    burger.addEventListener('click', () => {
        menu.classList.toggle('is-active');
        burger.classList.toggle('is-active');
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const dropdownButton = document.querySelector('.dropdown2-button');
    const dropdownContent = document.querySelector('.dropdown2-content');

    dropdownButton.addEventListener('click', (event) => {
        event.stopPropagation(); // Prevents clicks from propagating to other elements
        dropdownContent.classList.toggle('is-active'); // Toggles the dropdown visibility
    });

    // Close the dropdown if you click anywhere outside it
    document.addEventListener('click', () => {
        if (dropdownContent.classList.contains('is-active')) {
            dropdownContent.classList.remove('is-active');
        }
    });
});


//Anchor in place fix
// Expand collapsibles and scroll to anchor
function scrollWithOffset(el, offset = -50) {
    const y = el.getBoundingClientRect().top + window.pageYOffset + offset;
    window.scrollTo({ top: y, behavior: 'smooth' });
}

function expandToAnchor(anchorId) {
    console.log("expandToAnchor called with:", anchorId);
    const target = document.getElementById(anchorId);
    if (!target) return;

    // Step 1: Collect all parent .content elements that need expanding
    const stack = [];
    let el = target;
    while (el) {
        if (el.classList?.contains('content')) {
            stack.unshift(el); // add to beginning to expand outermost first
        }
        el = el.parentElement;
    }

    // Step 2: Expand each .content section in order
    for (const content of stack) {
        const button = content.previousElementSibling;
        if (button?.classList.contains('collapsible')) {
            button.classList.add('active');
            content.style.display = "block";

            const openIcon = button.querySelector("img.open-icon");
            const closeIcon = button.querySelector("img.close-icon");
            if (openIcon) openIcon.classList.add("hidden");
            if (closeIcon) closeIcon.classList.remove("hidden");
        }
    }

    // Step 3: Delay scroll until DOM has reflowed
    setTimeout(() => {
        console.log("scrolling to:", target.id);
        scrollWithOffset(target);
    }, 250); // Adjust if necessary
}

// Handle clicks on .anchor-link elements
document.addEventListener('DOMContentLoaded', () => {
    // Handle clicks on .anchor-link elements
    document.querySelectorAll('.anchor-link, a[href^="#"]').forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default anchor behavior
            const anchorId = this.getAttribute('href').substring(1);
            const fullUrl = `${window.location.origin}${window.location.pathname}#${anchorId}`;

            navigator.clipboard.writeText(fullUrl); // Copy full link to clipboard
            history.pushState(null, '', `#${anchorId}`); // Update URL without page reload
            expandToAnchor(anchorId); // Expand and scroll
        });
    });

    // On initial load with hash
    if (window.location.hash) {
        const anchorId = window.location.hash.substring(1);
        // Wait a bit for collapsibles/content to render
        setTimeout(() => {
            expandToAnchor(anchorId);
        }, 200);
    }
});



</script>


    </body>
    </html>
    """

    socketed_runes_html, socketed_excluding_runes_html, other_items_html = socket_html(
        sorted_just_socketed_runes, 
        sorted_just_socketed_excluding_runewords_runes, 
        all_other_items
    )

    two_handed_counter, _ = count_two_handed_weapons(all_equipped_items, all_the_items["two_handed_bases"])
    html_result = generate_two_handed_weapon_html(two_handed_counter)

    bow_bases = all_the_items["bow_bows"] + all_the_items["zon_bows"] + all_the_items["cross_bows"]
    bow_counter, _ = count_two_handed_weapons(all_equipped_items, bow_bases)
    html_result += generate_two_handed_weapon_htmlbow(bow_counter)

#    all_characters = process_all_characters()[0]  # or however you access the list of characters
    one_or_two_html = analyze_one_or_two_handed_usage(all_characters, items_list.all_the_items["one_or_two_hand"])

#    all_characters = process_all_characters()[0]
    html = analyze_one_or_two_handed_usage_with_characters(
        all_characters,
        items_list.all_the_items["one_or_two_hand"]
    )

#    loadouts = categorize_weapon_loadouts(all_characters)
    loadout_counts, total_loadouts, empty_loadout_count, partially_empty_set_count = categorize_weapon_loadouts(all_characters)

#    for line in loadout_counts:
#        print(line)

    loadouthtml = generate_loadout_summary_html(loadout_counts, total_loadouts, empty_loadout_count, partially_empty_set_count)
#    with open("loadout_summary.html", "w") as f:
#        f.write(loadouthtml)

    filled_html_content = f"""{html_content}""".replace(
        "{most_popular_runewords}", generate_list_items(most_common_runewords)
    ).replace(
        "{most_popular_uniques}", generate_list_items(most_common_uniques)
    ).replace(
        "{most_popular_set_items}", generate_list_items(most_common_set_items)
    ).replace(
        "{least_popular_runewords}", generate_list_items(least_common_runewords)
    ).replace(
        "{least_popular_uniques}", generate_list_items(least_common_uniques)
    ).replace(
        "{least_popular_set_items}", generate_list_items(least_common_set_items)
    ).replace( 
        "{all_runewords}", generate_all_list_items(all_runewords, runeword_users)
    ).replace(
        "{all_uniques}", generate_all_list_items(all_uniques, unique_users)
    ).replace(
        "{all_uniques_all}", generate_all_list_items(all_uniques_all, unique_users)
    ).replace(
        "{all_set}", generate_all_list_items(all_set, set_users)
    ).replace(
        "{all_synth}", generate_synth_list_items(synth_counter, synth_users)
    ).replace(
        "{timeStamp}", timeStamp
    ).replace(
        "{synth_user_count}", str(synth_user_count)
    ).replace(
        "{all_crafted}", generate_crafted_list_items(crafted_counters, crafted_users)
    ).replace(
        "{craft_user_count}", str(craft_user_count)
    ).replace(
        "{synth_source_data}", generate_synth_source_list(synth_sources)
    ).replace(
        "{synth_source_user_count}", str(synth_source_user_count)
    ).replace(
        "{all_magic}", generate_magic_list_items(magic_counters, magic_users)
    ).replace(
        "{magic_user_count}", str(magic_user_count)
    ).replace(
        "{all_rare}", generate_rare_list_items(rare_counters, rare_users)
    ).replace(
        "{rare_user_count}", str(rare_user_count)
    ).replace(
        "{sorted_just_socketed_runes}", socketed_runes_html  # ✅ Correctly insert formatted HTML
    ).replace(
        "{sorted_just_socketed_excluding_runewords_runes}", socketed_excluding_runes_html
    ).replace(
        "{all_other_items}", other_items_html
    ).replace(
        "{fun_facts_html}", fun_facts_html
    ).replace(
        "{unused_runewords}", unused_runewords_html
    ).replace(
        "{unused_uniques}", unused_uniques_html
    ).replace(
        "{unused_set_items}", unused_set_items_html
    ).replace(
        "{kfun_facts_html}", kfun_facts_html
    ).replace(
        "{runewordbasehtml_output}", generate_two_handed_weapon_html(two_handed_counter)
    ).replace(
        "{bowbasehtml_output}", generate_two_handed_weapon_htmlbow(bow_counter)
    ).replace(
         "{one_or_two_html}", analyze_one_or_two_handed_usage_with_characters(all_characters, items_list.all_the_items["one_or_two_hand"])
    ).replace(
         "{loadouthtml}", generate_loadout_summary_html(loadout_counts, total_loadouts, empty_loadout_count, partially_empty_set_count)
    ).replace(
        "{html_output}", html_output
    )


    print("Runewords:", sum(runeword_counter.values()))
    print("Uniques:", sum(unique_counter.values()))
#    print(f"Uniques:", (unique_counter.most_common(400)))
    print("Set items:", sum(set_counter.values()))
#    print("Synth:", sum(synth_counter[worn_category][title] for worn_category in synth_counter for title in synth_counter[worn_category]))
 #   print("Crafted:", sum(crafted_counters[worn_category][title] for worn_category in crafted_counters for title in crafted_counters[worn_category]))
 #   print("Magic:", sum(magic_counters[worn_category][title] for worn_category in magic_counters for title in magic_counters[worn_category]))
 #   print("Rare:", sum(rare_counters[worn_category][title] for worn_category in rare_counters for title in rare_counters[worn_category]))

#    template = Template(html_content)
#    html_content = template.render(html_output=html_output)  # Pass sorted clusters to the template

    # Write the filled HTML content to a file
    with open('Home.html', 'w') as file:
        file.write(filled_html_content)
    with open('index.html', 'w') as file:
        file.write(filled_html_content)

    print("HTML file generated successfully.")

def fetch_ladder_characters(base_ladder_url, start_page=1, end_page=5):
    """Fetch all characters from a range of ladder pages, skipping page 0 by default."""
    all_characters = []
    for page in range(start_page, end_page + 1):  # Inclusive range
        ladder_url = f"{base_ladder_url}{page}"
        print(f"Fetching {ladder_url}")
        response = requests.get(ladder_url)
        if response.status_code == 200:
            ladder_data = response.json()
            all_characters.extend(ladder_data.get("ladder", []))
        else:
            print(f"⚠️ Failed to fetch page {page}: {response.status_code}")
    return all_characters

def MakehcHome():
    # Define the consolidated JSON file path
    consolidated_file = "ladder_hc.json"  # Replace with your actual file path
    
    try:
        # Load the consolidated JSON file
        with open(consolidated_file, "r") as file:
            all_characters = json.load(file)
            all_characters = [
                json.loads(char) if isinstance(char, str) else char 
                for char in all_characters 
                if isinstance(char, dict) and char.get("Stats", {}).get("Level", 0) >= 60
            ]

        
        # Add this print statement to inspect the structure of the data
#        print("First 5 entries in all_characters:", all_characters[:5])  # Debugging output
#        print("Type of all_characters:", type(all_characters))  # Check if it's a list
#        if isinstance(all_characters[0], str):  # Check if elements are strings
#            print("First entry as string:", all_characters[0])  # Print one raw string entry
        
        # Convert strings to dictionaries if needed
        if isinstance(all_characters[0], str):  # If first element is a string
            all_characters = [json.loads(char_data) for char_data in all_characters]
#            print("Converted all_characters to dictionaries.")  # Confirmation message
        
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading consolidated JSON file: {e}")
        return

    # Now you can safely process the characters
    try:
        class_counts, runeword_counter, unique_counter, set_counter, synth_counter = process_all_characters(all_characters)
        # Continue with the rest of your MakeHome logic...
    except Exception as e:
        print(f"Error during character processing: {e}")

#    data_folder = "sc/ladder-all"
    html_output = """"""
    output_file = "all_mercenary_report.html"
    synth_item = "Synth"


    dt = datetime.now()
    # format it to a string
    timeStamp = dt.strftime('%Y-%m-%d %H:%M')

    # Counters for classes, runewords, uniques, and set items
    class_counts = {}
    runeword_counter = Counter()
    unique_counter = Counter()
    set_counter = Counter()
    synth_counter = Counter()
    crafted_counters = {
        "Rings": Counter(),
        "Weapons and Shields": Counter(),
        "Arrows": Counter(),
        "Bolts": Counter(),
        "Body Armor": Counter(),
        "Gloves": Counter(),
        "Belts": Counter(),
        "Helmets": Counter(),
        "Boots": Counter(),
        "Amulets": Counter(),
    }
    magic_counters = {
        "Rings": Counter(),
        "Weapons and Shields": Counter(),
        "Arrows": Counter(),
        "Bolts": Counter(),
        "Body Armor": Counter(),
        "Gloves": Counter(),
        "Belts": Counter(),
        "Helmets": Counter(),
        "Boots": Counter(),
        "Amulets": Counter(),
    }
    rare_counters = {
        "Rings": Counter(),
        "Weapons and Shields": Counter(),
        "Arrows": Counter(),
        "Bolts": Counter(),
        "Body Armor": Counter(),
        "Gloves": Counter(),
        "Belts": Counter(),
        "Helmets": Counter(),
        "Boots": Counter(),
        "Amulets": Counter(),
    }
    
    synth_sources = {}  # Maps item names to all synth items that used them

    runeword_users = {}
    unique_users = {}
    set_users = {}
    synth_users = {}
    crafted_users = {category: {} for category in crafted_counters}  # Ensure all categories exist
    rare_users = {category: {} for category in rare_counters}  # Ensure all categories exist
    magic_users = {category: {} for category in magic_counters}  # Ensure all categories exist

    all_characters = []
    sorted_just_socketed_runes = {}
    sorted_just_socketed_excluding_runewords_runes = {}
    all_other_items = {}

    all_equipped_items = []
    two_handed_counter = Counter()
    bow_counter = Counter()

    def analyze_top_accounts():
        def get_top_accounts_with_class(account_class_counts, class_code, min_count=2, top_n=5):
            return [
                (acct, counts)
                for acct, counts in sorted(account_class_counts.items(), key=lambda x: x[1].get(class_code, 0), reverse=True)
                if counts.get(class_code, 0) >= min_count
            ][:top_n]
        base_ladder_url = "https://beta.pathofdiablo.com/api/ladder/13/1/0/"
        all_characters = fetch_ladder_characters(base_ladder_url, start_page=1, end_page=5)
        all_characters = [char for char in all_characters if char.get('account')]

        level_counter = Counter(char['level'] for char in all_characters)

        print("\n🎯 High-Level Character Counts:")
        for level in [99, 98, 97, 96, 95]:
            print(f"Level {level}: {level_counter.get(level, 0)} characters")

        level99_accounts = defaultdict(int)

        for char in all_characters:
            if char['level'] == 99:
                level99_accounts[char['account']] += 1

        top_99s = sorted(level99_accounts.items(), key=lambda x: x[1], reverse=True)[:3]

        print("\n🥇 Top Accounts by Number of Level 99 Characters:")
        for acct, count in top_99s:
            print(f'<li><a href="https://beta.pathofdiablo.com/account/{acct}">{acct}</a>: {count} characters at level 99</li>')

        account_class_counts = defaultdict(lambda: defaultdict(int))

        for char in all_characters:
            acct = char['account']
            class_code = char['charClass']  # e.g., "sor"
            account_class_counts[acct][class_code] += 1

        #Who has the most amazons?
        most_zons = get_top_accounts_with_class(account_class_counts, "ama")
#        most_zons = sorted(account_class_counts.items(), key=lambda x: x[1].get("ama", 0), reverse=True)[:5]
        print("\n🧙 Accounts with Most Amazons:")
        for acct, class_count in most_zons:
            print(f"{acct}: {class_count.get('ama', 0)} Amazons")
        #Who has the most assassins?
        most_sins = get_top_accounts_with_class(account_class_counts, "asn")
#        most_sins = sorted(account_class_counts.items(), key=lambda x: x[1].get("asn", 0), reverse=True)[:5]
        print("\n🧙 Accounts with Most Assassins:")
        for acct, class_count in most_sins:
            print(f"{acct}: {class_count.get('asn', 0)} Assassins")
        #Who has the most barbs?
        most_barbs = get_top_accounts_with_class(account_class_counts, "bar")
#        most_barbs = sorted(account_class_counts.items(), key=lambda x: x[1].get("bar", 0), reverse=True)[:2]
        print("\n🧙 Accounts with Most Barbarians:")
        for acct, class_count in most_barbs:
            print(f"{acct}: {class_count.get('bar', 0)} Barbarians")
        #Who has the most druids?
        most_druids = get_top_accounts_with_class(account_class_counts, "dru")
#        most_druids = sorted(account_class_counts.items(), key=lambda x: x[1].get("dru", 0), reverse=True)[:3]
        print("\n🧙 Accounts with Most Druids:")
        for acct, class_count in most_druids:
            print(f"{acct}: {class_count.get('dru', 0)} Druids")
        #Who has the most necros?
        most_necros = get_top_accounts_with_class(account_class_counts, "nec")
#        most_necros = sorted(account_class_counts.items(), key=lambda x: x[1].get("nec", 0), reverse=True)[:5]
        print("\n🧙 Accounts with Most Necromancers:")
        for acct, class_count in most_necros:
            print(f"{acct}: {class_count.get('nec', 0)} Necromancers")
        #Who has the most paladins?
        most_pallys = get_top_accounts_with_class(account_class_counts, "pal")
#        most_pallys = sorted(account_class_counts.items(), key=lambda x: x[1].get("pal", 0), reverse=True)[:4]
        print("\n🧙 Accounts with Most Paladins:")
        for acct, class_count in most_pallys:
            print(f"{acct}: {class_count.get('pal', 0)} Paladins")
        #Who has the most sorceresses?
        most_sorcs = get_top_accounts_with_class(account_class_counts, "sor")
#        most_sorcs = sorted(account_class_counts.items(), key=lambda x: x[1].get("sor", 0), reverse=True)[:5]
        print("\n🧙 Accounts with Most Sorceresses:")
        for acct, class_count in most_sorcs:
            print(f"{acct}: {class_count.get('sor', 0)} sorceresses")

    ## Who has all the classes?
        # Map short class codes used by the API to full names (or use your preferred naming)
        CLASS_CODES = {"ama", "asn", "bar", "dru", "nec", "pal", "sor"}

        # Track each account's set of classes
        account_class_sets = defaultdict(set)

        for char in all_characters:
            acct = char['account']
            char_class = char['charClass']
            account_class_sets[acct].add(char_class)

        # Count accounts that have all 7 classes
        complete_class_accounts = [acct for acct, classes in account_class_sets.items() if CLASS_CODES.issubset(classes)]

        print(f"\n📈 Accounts with all 7 classes: {len(complete_class_accounts)}")
        print("Examples:", ", ".join(complete_class_accounts[:5]))

        account_stats = defaultdict(lambda: {'count': 0, 'levels': 0, 'xp': 0})

        for char in all_characters:
            acct = char.get('account')
            if not acct:
                continue
            account_stats[acct]['count'] += 1
            account_stats[acct]['levels'] += char.get('level', 0)
            account_stats[acct]['xp'] += char.get('exp', 0)

        # Convert to list of (account, stats) and sort
        sorted_by_xp = sorted(account_stats.items(), key=lambda x: x[1]['xp'], reverse=True)[:5]
        sorted_by_levels = sorted(account_stats.items(), key=lambda x: x[1]['levels'], reverse=True)[:5]
        sorted_by_count = sorted(account_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:10]

        print("\n📊 Top Accounts from Top 1,000 Characters:")

        print("\n🔸 Top 5 by Total XP:")
        for acct, stats in sorted_by_xp:
            avg_lvl = stats['levels'] / stats['count']
            print(f"{acct}: {stats['xp']:,} XP, {stats['count']} chars, avg level {avg_lvl:.2f}")

        print("\n🔸 Top 5 by Total Levels:")
        for acct, stats in sorted_by_levels:
            avg_lvl = stats['levels'] / stats['count']
            print(f"{acct}: {stats['levels']} levels, {stats['count']} chars, avg level {avg_lvl:.2f}")

        print("\n🔸 Top 5 by Character Count:")
        for acct, stats in sorted_by_count:
            avg_lvl = stats['levels'] / stats['count']
            print(f"{acct}: {stats['count']} characters, total level {stats['levels']}, avg level {avg_lvl:.2f}")



        kfun_facts_html = f"""
        <h3 id="top-account-stats">Top Account Statistics <a href="#top-account-stats" class="anchor-link">
            <img src="icons/anchor.png" alt="🔗" class="anchor-icon"></a></h3>

        <!-- Level 95+ Summary -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
            <h4>High-Level Character Counts</h4>
            <ul>
                {"".join(f"<li>Level {lvl}: {count} characters</li>" for lvl, count in level_counter.items() if lvl in [99, 98, 97, 96, 95])}
            </ul>
        </div>
        <!-- Level 99 Accounts -->
            <div class="fun-facts-column">
        <h4>Top Accounts by Number of Level 99 Characters</h4>
        <ul>
            {"".join(
                f"<li><a href='https://beta.pathofdiablo.com/ladder?account/{acct}'>{acct}</a>: {count} characters at level 99</li>"
                for acct, count in top_99s
            )}
        </ul> 
       </div></div>

        <!-- Per-Class Top 5 Lists -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with multiple Amazons in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('ama', 0)} Amazons</li>" for acct, count in most_zons)}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Accounts with multiple Assassins in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('asn', 0)} Assassins</li>" for acct, count in most_sins)}</ul>
            </div>
        </div>
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with multiple Barbarians in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('bar', 0)} Barbarians</li>" for acct, count in most_barbs)}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Accounts with multiple Druids in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('dru', 0)} Druids</li>" for acct, count in most_druids)}</ul>
            </div>
        </div>
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with multiple Necromancers in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('nec', 0)} Necromancers</li>" for acct, count in most_necros)}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Accounts with multiple Paladins in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('pal', 0)} Paladins</li>" for acct, count in most_pallys)}</ul>
            </div>
        </div>
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with multiple Sorceresses in the top 1K</h3>
                <ul>{"".join(f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {count.get('sor', 0)} Sorceresses</li>" for acct, count in most_sorcs)}</ul>
            </div>
        </div>

        <!-- All 7 Classes -->
        <h3>Accounts with all 7 classes in the top 1K: {len(complete_class_accounts)}</h3>
        <p>{", ".join(f"<a href='https://beta.pathofdiablo.com/ladder?account={acct}'>{acct}</a>" for acct in complete_class_accounts[:5])}</p>

        <!-- XP / Level / Count -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with the most experience</h3>
                    <ul>
                        {"".join(
                            f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {stats['xp']:,} XP, {stats['count']} chars, avg level {stats['levels']/stats['count']:.2f}</li>"
                            for acct, stats in sorted_by_xp
                        )}
                    </ul>
           </div>
            <div class="fun-facts-column">
                <h3>Accounts with the most Levels</h3>
                    <ul>
                        {"".join(
                            f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {stats['levels']} levels, {stats['count']} chars, avg level {stats['levels']/stats['count']:.2f}</li>"
                            for acct, stats in sorted_by_levels
                        )}
                    </ul>
            </div>
        </div>
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Accounts with the most characters in the top 1K</h3>
                    <ul>
                        {"".join(
                            f"<li><a href='https://beta.pathofdiablo.com/account/{acct}'>{acct}</a>: {stats['count']} characters, total level {stats['levels']}, avg level {stats['levels']/stats['count']:.2f}</li>"
                            for acct, stats in sorted_by_count
                        )}
                    </ul>
            </div>
        </div>
        """

        return kfun_facts_html

    # Generate fun facts
    kfun_facts_html = analyze_top_accounts()

    
    # Function to process each JSON file
    def process_all_characters():
        with open(consolidated_file, "r") as file:
            all_characters = json.load(file)
            all_characters = [
                json.loads(char) if isinstance(char, str) else char 
                for char in all_characters 
                if isinstance(char, dict) and char.get("Stats", {}).get("Level", 0) >= 60
            ]

        for char_data in all_characters:
            if isinstance(char_data, str):  # If somehow it's still a string, convert it
                char_data = json.loads(char_data)

            char_name = char_data.get("Name", "Unknown")  # This should now work
#            print(f"Processing {char_name}")
            char_class = char_data.get("Class", "Unknown")
            char_level = char_data.get("Stats", {}).get("Level", "Unknown")

            # Debugging: Print details of the character being processed
#            print(f"Processing character: {char_name}, Class: {char_class}, Level: {char_level}")

            # Continue with processing logic (e.g., class counts, equipped items, etc.)

        # Dictionary to store class counts
        class_counts = {}

        # Counters for runewords, uniques, and set items
        runeword_counter = Counter()
        unique_counter = Counter()
        set_counter = Counter()
        synth_counter = Counter()

        # Categorize worn slots
        def categorize_worn_slot(worn_category, text_tag):
            if worn_category in ["sweapon1", "weapon1", "sweapon2", "weapon2"]:
                if text_tag == "Arrows":
                    return "Arrows"
                elif text_tag == "Bolts":
                    return "Bolts"
                else:
                    return "Weapons and Shields"

            worn_category_map = {
                "ring1": "Rings", "ring2": "Rings",
                "body": "Armor",
                "gloves": "Gloves",
                "belt": "Belts",
                "helmet": "Helmets",
                "boots": "Boots",
                "amulet": "Amulets",
            }

            return worn_category_map.get(worn_category, "Other")  # Default to "Other"

        # Process each character in the consolidated JSON
        for char_data in all_characters:
            try:
                char_name = char_data.get("Name", "Unknown")
                char_class = char_data.get("Class", "Unknown")
                char_level = char_data.get("Stats", {}).get("Level", "Unknown")

                # Process class data
                if char_class:
                    class_counts[char_class] = class_counts.get(char_class, 0) + 1

                # Process equipped items
                for item in char_data.get("Equipped", []):
                    all_equipped_items.append(item)
                    worn_category = categorize_worn_slot(item.get("Worn", ""), item.get("TextTag", ""))  # ✅ Call once

                    character_info = {
                        "name": char_name,
                        "class": char_class,
                        "level": char_level,
                    }

                    if "synth" in item.get("Tag", "").lower() or "synth" in item.get("TextTag", "").lower():
                        item_title = item["Title"]
                        synth_counter[item_title] += 1
                        synth_users.setdefault(item_title, []).append(character_info)

                        # Process SynthesisedFrom property
                        synthesized_from = item.get("SynthesisedFrom", [])
                        all_related_items = [item_title] + synthesized_from
                        for source_item in all_related_items:
                            synth_sources.setdefault(source_item, []).append({
                                "name": char_name,
                                "class": char_class,
                                "level": char_level,
                                "synthesized_item": item_title
                            })

                    if item.get("QualityCode") == "q_runeword":
                        title = item["Title"]
                        if title == "2693":
                            title = "Delirium"
                        elif title == "-26":
                            title = "Pattern2"

                        runeword_counter[title] += 1

                        base = item.get("Tag", "Unknown")
                        if title not in runeword_users:
                            runeword_users[title] = {}
                        if base not in runeword_users[title]:
                            runeword_users[title][base] = []
                        runeword_users[title][base].append(character_info)

                    if item.get("QualityCode") == "q_unique":
                        unique_counter[item["Title"]] += 1
                        unique_users.setdefault(item["Title"], []).append(character_info)

                    if item.get("QualityCode") == "q_set":
                        set_counter[item["Title"]] += 1
                        set_users.setdefault(item["Title"], []).append(character_info)

                    if item.get("QualityCode") == "q_crafted":
                        crafted_counters[worn_category][item["Title"]] += 1
                        crafted_users.setdefault(worn_category, {}).setdefault(item["Title"], []).append(character_info)

            except (KeyError, TypeError) as e:
                print(f"Error processing character: {char_name}, Error: {e}")
                continue

#        return class_counts, runeword_counter, unique_counter, set_counter, synth_counter
        return class_counts, runeword_counter, unique_counter, set_counter, synth_counter, runeword_users, unique_users, set_users, synth_users, crafted_counters, crafted_users, all_equipped_items

    def count_two_handed_weapons(equipped_items, two_handed_bases):
        counter = Counter()
        runeword_base_breakdown = defaultdict(Counter)

        for item in equipped_items:
            worn = item.get("Worn")
            if worn not in {"weapon1", "weapon2", "sweapon1", "sweapon2"}:
                continue

            tag = item.get("Tag", "")
            title = item.get("Title", "")
            quality = item.get("QualityCode", "")
            base_name = tag.strip()

            if base_name not in two_handed_bases:
                continue  # Skip non-two-handed items

            if quality == "q_runeword":
                label = f"{title} ({base_name})"
            else:
                label = title

            counter[label] += 1

        return counter, runeword_base_breakdown

    def generate_two_handed_weapon_html(two_handed_counter):
        # First, aggregate base breakdowns for runewords
        aggregated_data = defaultdict(lambda: {"total": 0, "bases": Counter()})
        
        for label, count in two_handed_counter.items():
            if " (" in label and label.endswith(")"):
                # Runeword with base, e.g., "Memory (Cedar Staff)"
                name, base = label[:-1].split(" (", 1)
                aggregated_data[name]["total"] += count
                aggregated_data[name]["bases"][base] += count
            else:
                # Normal item
                aggregated_data[label]["total"] += count

        # Sort aggregated data by total count, descending
        sorted_items = sorted(aggregated_data.items(), key=lambda x: x[1]["total"], reverse=True)

        # Generate HTML
        html_output = [
            "<h2>Most Common Melee Weapons That Require two Hands</h2>",
            "<div style='column-count: 2; column-gap: 2em;'>",
            "<ul style='margin: 0; padding: 0;'>"
        ]

        for name, data in sorted_items:
            total = data["total"]
            bases = data["bases"]

            if bases:
                html_output.append(f"<li><strong>{name}: {total}</strong><ul>")
                for base_name, base_count in bases.most_common():
                    html_output.append(f"<li class='base-item'>{base_name}: {base_count}</li>")
                html_output.append("</ul></li>")
            else:
                html_output.append(f"<li>{name}: {total}</li>")

        html_output.append("</ul></div>")
        return "\n".join(html_output)

    def generate_two_handed_weapon_htmlbow(bow_counter):
        # First, aggregate base breakdowns for runewords
        aggregated_data = defaultdict(lambda: {"total": 0, "bases": Counter()})
        
        for label, count in bow_counter.items():
            if " (" in label and label.endswith(")"):
                # Runeword with base, e.g., "Memory (Cedar Staff)"
                name, base = label[:-1].split(" (", 1)
                aggregated_data[name]["total"] += count
                aggregated_data[name]["bases"][base] += count
            else:
                # Normal item
                aggregated_data[label]["total"] += count

        # Sort aggregated data by total count, descending
        sorted_items = sorted(aggregated_data.items(), key=lambda x: x[1]["total"], reverse=True)

        # Generate HTML
        html_output = [
            "<h2>Most Commonly Seen Bows and Crossbows</h2>",
            "<div style='column-count: 2; column-gap: 2em;'>",
            "<ul style='margin: 0; padding: 0;'>"
        ]

        for name, data in sorted_items:
            total = data["total"]
            bases = data["bases"]

            if bases:
                html_output.append(f"<li><strong>{name}: {total}</strong><ul>")
                for base_name, base_count in bases.most_common():
                    html_output.append(f"<li class='base-item'>{base_name}: {base_count}</li>")
                html_output.append("</ul></li>")
            else:
                html_output.append(f"<li>{name}: {total}</li>")

        html_output.append("</ul></div>")
        return "\n".join(html_output)

    def analyze_one_or_two_handed_usage(characters, one_or_two_hand_list):
        item_counts = defaultdict(lambda: {"total": 0, "bases": Counter()})

        for char in characters:
            equipped = {item["Worn"]: item for item in char.get("Equipped", [])}

            for slot_pair in [("weapon1", "weapon2"), ("sweapon1", "sweapon2")]:
                primary, secondary = slot_pair
                item = equipped.get(primary)
                other_item = equipped.get(secondary)

                if not item or other_item:
                    continue  # Skip if no item or dual-wielding

                base = item.get("Tag", "")
                if base not in one_or_two_hand_list:
                    continue  # Not a one/two-hand weapon

                title = item.get("Title", "Unknown")
                quality = item.get("QualityCode", "")
                
                if quality == "q_runeword":
                    item_counts[title]["total"] += 1
                    item_counts[title]["bases"][base] += 1
                else:
                    # Normal item
                    item_counts[f"{title}"] = item_counts.get(f"{title}", {"total": 0, "bases": Counter()})
                    item_counts[title]["total"] += 1

        # Sort by count descending
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1]["total"], reverse=True)

        # Output to HTML in two columns
        html_output = [
            "<h2>One or Two-Handed Items (Used Two-Handed)</h2>",
            "<div style='column-count: 2; column-gap: 2em;'>",
            "<ul style='margin: 0; padding: 0;'>"
        ]

        for name, data in sorted_items:
            total = data["total"]
            bases = data["bases"]

            if bases:
                html_output.append(f"<li><strong>{name}: {total}</strong><ul style='margin: 0;'>")
                for base_name, base_count in bases.most_common():
                    html_output.append(f"<li style='padding-left: 1.5em'>{base_name}: {base_count}</li>")
                html_output.append("</ul></li>")
            else:
                html_output.append(f"<li>{name}: {total}</li>")

        html_output.append("</ul></div>")
        return "\n".join(html_output)

    def analyze_one_or_two_handed_usage_with_characters(characters, one_or_two_hand_list):
        item_data = defaultdict(lambda: {"total": 0, "bases": defaultdict(list)})

        for char in characters:
            equipped = {item["Worn"]: item for item in char.get("Equipped", [])}

            for slot1, slot2 in [("weapon1", "weapon2"), ("sweapon1", "sweapon2")]:
                weapon = equipped.get(slot1)
                offhand = equipped.get(slot2)

                if not weapon or offhand:
                    continue  # Either missing weapon or dual wielding

                base = weapon.get("Tag", "")
                if base not in one_or_two_hand_list:
                    continue

                title = weapon.get("Title", "Unknown")
                quality = weapon.get("QualityCode", "")
#                pprint.pprint(characters[0])
                char_info = {
                    "name": char.get("Name", "Unknown"),
#                    "level": char.get("Stats.Level", "?"),
                    "class": char.get("Class", "Unknown"),
                }

                item_data[title]["total"] += 1
                item_data[title]["bases"][base].append(char_info)

        # Sort by total descending
        sorted_items = sorted(item_data.items(), key=lambda x: -x[1]["total"])

        html_output = [
            "<h2>One or Two-Handed Items (Used Two-Handed)</h2>",
            "<div style='column-count: 2; column-gap: 2em;'>",
            "<ul style='margin: 0; padding: 0;'>"
        ]

        for title, data in sorted_items:
            html_output.append(f"<li><strong>{title}: {data['total']}</strong>")

            for base, chars in sorted(data["bases"].items(), key=lambda x: (-len(x[1]), x[0])):
                base_name = base or "(unknown base)"

                base_id = slugify(f"{title}-{base_name}")

                html_output.append(f"""
                    <ul style="margin: 0;">
                        <li style="padding-left: 1.5em">
                            <button class="collapsible">
                                <img src="icons/open-grey.png" alt="Expand" class="icon-small open-icon hidden">
                                <img src="icons/closed-grey.png" alt="Collapse" class="icon-small close-icon">
                                <strong>
                                    <a href="#item-{base_id}" class="anchor-link">
                                        {base_name}: {len(chars)}
                                    </a>
                                </strong>
                            </button>
                            <div class="content" id="item-{base_id}">
                                {''.join(f'''
                                    <div class="character-info">
                                        <div class="character-link">
                                            <a href="https://beta.pathofdiablo.com/armory?name={c["name"]}" target="_blank">
                                                {c["name"]}
                                            </a>
                                        </div>
                                        <div>{c["class"]}</div>
                                        <div class="hover-trigger" data-character-name="{c["name"]}"></div>
                                    </div>
                                    <div class="character">
                                        <div class="popup hidden"></div>
                                    </div>
                                ''' for c in chars)}
                            </div>
                        </li>
                    </ul>
                """)

            html_output.append("</li>")

        html_output.append("</ul></div>")
        return "\n".join(html_output)

#    loadout_counts = defaultdict(int)
#    total_loadouts = 0
    def categorize_weapon_loadouts(characters):
        BOW_BASES = {b.lower() for b in all_the_items["zon_bows"] + all_the_items["bow_bows"]}
        XBOW_BASES = {x.lower() for x in all_the_items["cross_bows"]}

        loadout_counts = defaultdict(int)
        total_loadouts = 0

        def is_weapon(item):
            return isinstance(item, dict) and "DamageMinimum" in item and "DamageMaximum" in item

        def is_shield(item):
            return isinstance(item, dict) and "Block" in item and "Defense" in item

        def is_missile(item):
            tag = item.get("Tag", "").lower()
            return "arrow" in tag or "bolt" in tag

        other_examples = []

        def classify_loadout(w1, w2):
            if not w1 and not w2:
                return None  # Skip

            tag1 = w1.get("Tag", "").lower() if w1 else ""
            tag2 = w2.get("Tag", "").lower() if w2 else ""

            tags = {tag1, tag2}

            # Bow + Arrows
            if (tag1 in BOW_BASES or tag2 in BOW_BASES) and any("arrow" in t for t in tags):
                return "Bow + Arrows"
            if tag1 in BOW_BASES or tag2 in BOW_BASES:
                return "Bow Only (Missing Arrows)"
            if any("arrow" in t for t in tags):
                return "Arrows Only (Missing Bow)"

            # Crossbow + Bolts
            if (tag1 in XBOW_BASES or tag2 in XBOW_BASES) and any("bolt" in t for t in tags):
                return "Crossbow + Bolts"
            if tag1 in XBOW_BASES or tag2 in XBOW_BASES:
                return "Crossbow Only (Missing Bolts)"
            if any("bolt" in t for t in tags):
                return "Bolts Only (Missing Crossbow)"

            # Two-handed melee weapon (solo)
            if w1 and not w2 and is_weapon(w1):
                base = w1.get("Tag", "")
                if base in all_the_items["one_or_two_hand"] or base in all_the_items["two_handed_bases"]:
                    return "A Single Two-Handed Weapon"

            if w2 and not w1 and is_weapon(w2):
                base = w2.get("Tag", "")
                if base in all_the_items["one_or_two_hand"] or base in all_the_items["two_handed_bases"]:
                    return "A Single Two-Handed Weapon"

            # Weapon + Shield
            if (is_weapon(w1) and is_shield(w2)) or (is_shield(w1) and is_weapon(w2)):
                return "Weapon + Shield"

            # Dual wield
            if is_weapon(w1) and is_weapon(w2):
                return "Dual Wield"

            # Single One-Handed Weapon
            if (w1 and not w2 and is_weapon(w1)) or (w2 and not w1 and is_weapon(w2)):
                base = (w1 or w2).get("Tag", "")
                if base not in all_the_items["one_or_two_hand"] and base not in all_the_items["two_handed_bases"]:
                    return "Single One-Handed Weapon (Missing Shield or Second Weapon)"

            # Shield only
            if is_shield(w1) and not w2:
                return "Shield Only (Missing Weapon)"
            if is_shield(w2) and not w1:
                return "Shield Only (Missing Weapon)"

            # Two-handed
            tag = tag1 or tag2
            if tag in all_the_items["two_handed_bases"]:
                return "A Single Two-Handed Weapon"

            return "Other"

        empty_loadout_count = 0
        partially_empty_set_count = 0
        for char in characters:
            equipped = {item["Worn"]: item for item in char.get("Equipped", []) if isinstance(item, dict)}
            # Check if weapon1/weapon2 or sweapon1/sweapon2 are both missing
            has_set1 = equipped.get("weapon1") or equipped.get("weapon2")
            has_set2 = equipped.get("sweapon1") or equipped.get("sweapon2")

            if not has_set1 and not has_set2:
                empty_loadout_count += 1
            elif not has_set1 or not has_set2:
                partially_empty_set_count += 1

            sets_categorized = 0

            for set1, set2 in [("weapon1", "weapon2"), ("sweapon1", "sweapon2")]:
                w1 = equipped.get(set1)
                w2 = equipped.get(set2)

                category = classify_loadout(w1, w2)
                if category:
                    loadout_counts[category] += 1
                    total_loadouts += 1
                    sets_categorized += 1

            if sets_categorized == 0:
                empty_loadout_count += 1

        # Prepare output
        results = []
        print("Sample 'Other' loadouts:")
        for ex in other_examples[:20]:  # show first 20
            print(ex)

        for category, count in sorted(loadout_counts.items(), key=lambda x: -x[1]):
            pct = (count / total_loadouts) * 100 if total_loadouts else 0
            results.append(f"{category}: {count} ({pct:.1f}%)")

        print(f"Total non-empty loadouts: {total_loadouts}")
#        return results
        return loadout_counts, total_loadouts, empty_loadout_count, partially_empty_set_count

    complete_categories = {
        "Weapon + Shield",
        "Dual Wield",
        "Bow + Arrows",
        "Crossbow + Bolts",
        "A Single Two-Handed Weapon",
    }


    incomplete_categories = {
        "Single One-Handed Weapon (Missing Shield or Second Weapon)",
        "Shield Only (Missing Weapon)",
        "Bow Only (Missing Arrows)",
        "Arrows Only (Missing Bow)",
        "Crossbow Only (Missing Bolts)",
        "Bolts Only (Missing Crossbow)",
    }

    def generate_loadout_summary_html(loadout_counts, total, empty_loadout_count, partially_empty_set_count):
        # Complete section
        complete_html = "<h2>Overall Weapon Usage Stats, Characters Equipped with:</h2><ul>"
        for category, count in sorted(loadout_counts.items(), key=lambda x: -x[1]):
            if category in complete_categories:
                percentage = f"{(count / total * 100):.1f}%"
                complete_html += f"<li><strong>{category}:</strong> {count} ({percentage})</li>"
        complete_html += "</ul>"

        # Incomplete section inside collapsible
        collapsible_html = '''
    <button type="button" class="collapsible small-collapsible">
        <img src="icons/open.png" alt="Incomplete Loadouts Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Incomplete Loadouts Close" class="icon-small close-icon">
        <strong>Incomplete Loadouts</strong>
    </button>
    <div class="content">
        <div id="incompletes">
            <p>These character builds are incomplete and missing items:</p>
            <ul>
    '''

        for category, count in sorted(loadout_counts.items(), key=lambda x: -x[1]):
            if category in incomplete_categories:
                percentage = f"{(count / total * 100):.1f}%"
                collapsible_html += f"<li><strong>{category}:</strong> {count} ({percentage})</li>"

        collapsible_html += "</ul></div></div>"
        summary_html = f"""
            <p><strong>Characters with no weapons in either weapon slot:</strong> {empty_loadout_count}</p>
            <p><strong>Characters with no weapons on swap:</strong> {partially_empty_set_count}</p><br>
        """

        return complete_html + "<br>" + collapsible_html + "<br>" + summary_html

    def process_magic_and_rare_items(all_characters, magic_counters, rare_counters, magic_users, rare_users):
        with open(consolidated_file, "r") as file:
            all_characters = json.load(file)
            all_characters = [
                json.loads(char) if isinstance(char, str) else char 
                for char in all_characters 
                if isinstance(char, dict) and char.get("Stats", {}).get("Level", 0) >= 60
            ]
        print(f"Total characters loaded by process_magic_and_rare_items: {len(all_characters)}")
#        equipped_items = char_data.get("Equipped", [])
#        print(f"Equipped: {equipped_items}")  # Prints raw data
        magic_counters = {category: Counter() for category in magic_counters}
        rare_counters = {category: Counter() for category in rare_counters}
        magic_users = {category: {} for category in magic_counters}
        rare_users = {category: {} for category in rare_counters}

        def categorize_worn_slot(worn_category, text_tag):
            if worn_category in ["sweapon1", "weapon1", "sweapon2", "weapon2"]:
                if text_tag == "Arrows":
                    return "Arrows"
                elif text_tag == "Bolts":
                    return "Bolts"
                else:
                    return "Weapons and Shields"

            worn_category_map = {
                "ring1": "Rings", "ring2": "Rings",
                "body": "Armor",
                "gloves": "Gloves",
                "belt": "Belts",
                "helmet": "Helmets",
                "boots": "Boots",
                "amulet": "Amulets",
            }

            return worn_category_map.get(worn_category, "Other")  # Default to "Other"

        # Process each character in the consolidated JSON
        for char_data in all_characters:
#            print(f"Checking {char_data.get('Name', 'Unknown')} - Equipped items: {len(char_data.get('Equipped', []))}")
            try:
                char_name = char_data.get("Name", "Unknown")
                char_class = char_data.get("Class", "Unknown")
                char_level = char_data.get("Stats", {}).get("Level", "Unknown")
                character_info = {"name": char_name, "class": char_class, "level": char_level}

                seen_magic_items = {category: set() for category in magic_counters}
                seen_rare_items = {category: set() for category in rare_counters}

                for item in char_data.get("Equipped", []):
                    worn_category = categorize_worn_slot(item.get("Worn", ""), item.get("TextTag", ""))
                    character_info = {"name": char_name, "class": char_class, "level": char_level}

                    if item.get("QualityCode") == "q_magic":
                        magic_counters[worn_category][item["Title"]] += 1
                        magic_users.setdefault(worn_category, {}).setdefault(item["Title"], []).append(character_info)

                    if item.get("QualityCode") == "q_rare":
                        rare_counters[worn_category][item["Title"]] += 1
                        rare_users.setdefault(worn_category, {}).setdefault(item["Title"], []).append(character_info)

            except (KeyError, TypeError) as e:
                print(f"Error processing character: {char_name}, Error: {e}")
                continue

        return magic_counters, magic_users, rare_counters, rare_users

    def GetSCFunFacts():
        # Path to the consolidated JSON file
        consolidated_file = "ladder_hc.json"

        # Load character data from the consolidated JSON file
        try:
            with open(consolidated_file, "r") as file:
                characters = json.load(file)
                characters = [
                    json.loads(char) if isinstance(char, str) else char 
                    for char in characters 
                    if isinstance(char, dict) and char.get("Stats", {}).get("Level", 0) >= 60
                ]
            print(all_characters[:5])  # Display the first 5 elements

        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading consolidated JSON file: {e}")
            return ""

        # Extract alive characters
        alive_characters = [char for char in characters if not char.get("IsDead", True)]
        undead_count = len(alive_characters)

        # Function to format the alive characters list
        def GetTheLiving():
            return "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char.get("Name", "Unknown")}" target="_blank">
                            {char.get("Name", "Unknown")}
                        </a>
                    </div>
                    <div>Level {char.get("Stats", {}).get("Level", "N/A")} {char.get("Class", "Unknown")}</div>
                    <div class="hover-trigger" data-character-name="{char.get("Name", "Unknown")}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """
                for char in alive_characters
            )

        alive_list_html = GetTheLiving()

        # Function to get top 5 characters for a given stat
        def get_top_characters(stat_name):
            ranked = sorted(
                characters,
                key=lambda c: c.get("Stats", {}).get(stat_name, 0) + c.get("Bonus", {}).get(stat_name, 0),
                reverse=True,
            )[:5]

            return "".join(
                f"""<li>&nbsp;&nbsp;&nbsp;&nbsp;
                    <a href="https://beta.pathofdiablo.com/armory?name={char.get('Name', 'Unknown')}" target="_blank">
                        {char.get('Name', 'Unknown')} ({char.get('Stats', {}).get(stat_name, 0) + char.get('Bonus', {}).get(stat_name, 0)})
                    </a>
                </li>"""
                for char in ranked
            )

        # lists for median calculations
        mf_values = []
        gf_values = []
        life_values = []
        mana_values = []

        # Get the top 5 for each stat
        top_strength = get_top_characters("Strength")
        top_dexterity = get_top_characters("Dexterity")
        top_vitality = get_top_characters("Vitality")
        top_energy = get_top_characters("Energy")
        top_life = get_top_characters("Life")
        top_mana = get_top_characters("Mana")

        # Compute Magic Find (MF) and Gold Find (GF)
        total_mf = 0
        total_gf = 0
        total_life = 0
        total_mana = 0
        character_count = len(characters)

        for char in characters:
            mf = char.get("Bonus", {}).get("MagicFind", 0) + \
                char.get("Bonus", {}).get("WeaponSetMain", {}).get("MagicFind", 0) + \
                char.get("Bonus", {}).get("WeaponSetOffhand", {}).get("MagicFind", 0)
            gf = char.get("Bonus", {}).get("GoldFind", 0) + \
                char.get("Bonus", {}).get("WeaponSetMain", {}).get("GoldFind", 0) + \
                char.get("Bonus", {}).get("WeaponSetOffhand", {}).get("GoldFind", 0)
            life = char.get("Stats", {}).get("Life", 0)
            mana = char.get("Stats", {}).get("Mana", 0)

            total_mf += mf
            total_gf += gf
            total_life += life
            total_mana += mana

            mf_values.append(mf)
            gf_values.append(gf)
            life_values.append(life)
            mana_values.append(mana)

        top_magic_find = get_top_characters("MagicFind")
        top_gold_find = get_top_characters("GoldFind")

        # Calculate averages
        average_mf = total_mf / character_count if character_count > 0 else 0
        average_gf = total_gf / character_count if character_count > 0 else 0
        average_life = total_life / character_count if character_count > 0 else 0
        average_mana = total_mana / character_count if character_count > 0 else 0

        #calculate medians
        median_mf = statistics.median(mf_values) if mf_values else 0
        median_gf = statistics.median(gf_values) if gf_values else 0
        median_life = statistics.median(life_values) if life_values else 0
        median_mana = statistics.median(mana_values) if mana_values else 0

        # Generate fun facts HTML
        fun_facts_html = f"""
        <h3 id="fun-facts">Hardcore Fun Facts <a href="#fun-facts" class="anchor-link"><img src="icons/anchor.png" alt="🔗" class="anchor-icon"></a></h3>
            <h3>{undead_count} Characters in the Hardcore top {character_count} have not died</h3>
                <button type="button" class="collapsible sets-button">
                    <img src="icons/Special_click.png" alt="Undead Open" class="icon open-icon hidden">
                    <img src="icons/Special.png" alt="Undead Close" class="icon close-icon">
                </button>
                <div class="content">  
                    <div id="special">{alive_list_html}</div>
                </div>
        <br>

        <!-- Strength & Dexterity Row -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Top 5 Characters with the most Strength:</h3>
                <ul>{top_strength}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Top 5 Characters with the most Dexterity:</h3>
                <ul>{top_dexterity}</ul>
            </div>
        </div>

        <!-- Vitality & Energy Row -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>Top 5 Characters with the most Vitality:</h3>
                <ul>{top_vitality}</ul>
            </div>
            <div class="fun-facts-column">
                <h3>Top 5 Characters with the most Energy:</h3>
                <ul>{top_energy}</ul>
            </div>
        </div>

        <!-- Life & Mana Row -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>The 5 Characters with the Most Life*:</h3>
                <ul>{top_life}</ul>
                <p><strong>Average Life:</strong> {average_life:.2f} | <strong>Median Life:</strong> {median_life:.2f}</p>
            </div>
            <div class="fun-facts-column">
                <h3>The 5 Characters with the Most Mana*:</h3>
                <ul>{top_mana}</ul>
                <p><strong>Average Mana:</strong> {average_mana:.2f} | <strong>Median Mana:</strong> {median_mana:.2f}</p>
            </div>
        </div>
        <em>*"Most" Life and Mana values are from a snapshot in time and may or may not be affected by bonuses from BO, Oak, etc.</em>
        <!-- Magic Find & Gold Find Row -->
        <div class="fun-facts-row">
            <div class="fun-facts-column">
                <h3>The 5 Characters with the Most Magic Find:</h3>
                <ul>{top_magic_find}</ul>
                <p><strong>Average Magic Find:</strong> {average_mf:.2f} | <strong>Median:</strong> {median_mf:.2f}</p>
            </div>
            <div class="fun-facts-column">
                <h3>The 5 Characters with the Most Gold Find:</h3>
                <ul>{top_gold_find}</ul>
                <p><strong>Average Gold Find:</strong> {average_gf:.2f} | <strong>Median:</strong> {median_gf:.2f}</p>
            </div>
        </div>
        """

        return fun_facts_html

    # Generate fun facts
    fun_facts_html = GetSCFunFacts()

    # Process the files in the data folder
    class_counts, runeword_counter, unique_counter, set_counter, synth_counter, runeword_users, unique_users, set_users, synth_users, crafted_counters, crafted_users, all_equipped_items = process_all_characters()
    magic_counters, magic_users, rare_counters, rare_users = process_magic_and_rare_items(all_characters, magic_counters, rare_counters, magic_users, rare_users)

    from items_list import all_the_items
    two_handed_counts, two_handed_users = count_two_handed_weapons(
        all_equipped_items,
        all_the_items["two_handed_bases"]
    )

    # Example: print top 10 most common
    for title, count in two_handed_counts.most_common(20):
        print(f"{title}: {count}")

    # Print the class counts
    print("Class Counts:")
    for char_class, count in class_counts.items():
        print(f"{char_class}: {count} characters")

    # Print the most and least common items
    def print_item_counts(title, counter):
        print(f"\n{title}:")
        most_common = counter.most_common(10)
        least_common = counter.most_common()[:-11:-1]
        for item, count in most_common:
            print(f"Most common - {item}: {count}")
        for item, count in least_common:
            print(f"Least common - {item}: {count}")

    #print_item_counts("Runewords", runeword_counter)
    #print_item_counts("Uniques", unique_counter)
    #print_item_counts("Set Items", set_counter)

    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    from matplotlib.font_manager import FontProperties

    # Generate pie chart data
    classes = list(class_counts.keys())
    counts = list(class_counts.values())
    total = sum(counts)


    # Load custom font
     # Load custom font
    armory = FontProperties(fname='armory/font/avqest.ttf')  # Update path if needed

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return f'{pct:.1f}% ({val})'
        return my_autopct

    # Timestamp for title
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Set figure size
    plt.figure(figsize=(22, 22))
    plt.subplots_adjust(top=0.5, bottom=0.15)

    # Create the pie chart
    wedges, texts, autotexts = plt.pie(
        counts, labels=classes, autopct=make_autopct(counts), startangle=250, 
        colors=plt.cm.Paired.colors, radius=1.4, textprops={'fontsize': 30, 'color': 'white', 'fontproperties': armory}
    )


    title = plt.title(
        f"Class Distribution, ALL characters on ladder ranking\n\nAs of {timestamp}", 
        pad=50, fontsize=40, fontproperties=armory, loc='left', color="white"
    )
    title.set_fontsize(45)  # 🔹 Force title size after creation

    for text in texts:
        text.set_fontsize(35)  # Class labels
    for autotext in autotexts:
        autotext.set_fontsize(25)  # Percentages on slices
        autotext.set_color('black')

    plt.axis('equal')  # Ensures the pie chart is circular

    # Save the plot with transparent background
    plt.savefig("charts/hcclass_distribution.png", dpi=300, bbox_inches='tight', transparent=True)

    print("Plot saved as class_distribution.png")

    # Display the plot
    plt.show()


    # Get the most common items
    most_common_runewords = runeword_counter.most_common(10)
    most_common_uniques = unique_counter.most_common(10)
    most_common_set_items = set_counter.most_common(10)

    # Get all the items
    all_uniques = unique_counter.most_common(150)
    all_runewords = runeword_counter.most_common(150)
    all_uniques_all = unique_counter.most_common(400)
    all_set = set_counter.most_common(150)
    all_synth = synth_counter.most_common(150)

    # Get the least common items
    least_common_runewords = runeword_counter.most_common()[:-11:-1]
    least_common_uniques = unique_counter.most_common()[:-11:-1]
    least_common_set_items = set_counter.most_common()[:-11:-1]


    def slugify(name):
        return name.lower().replace(" ", "-").replace("'", "").replace('"', "")

    # Generate list items
    def generate_list_items(items):
        return ''.join(
            f'<li><a href="#{slug}">{name}</a>: {count}</li>'
            for item, count in items
            for name in [  # map item IDs to readable names
                "Delirium" if item == "2693" else 
                "Pattern2" if item == "-26" else 
                item
            ]
            for slug in [slugify(name)]
        )

    def generate_all_list_items(counter, character_data):
        if not isinstance(character_data, dict):
            print("Error: character_data is not a dict! Type:", type(character_data))
            return ""

        items_html = ""

        for item, count in counter:
            display_item = "Delirium" if item == "2693" else "Pattern2" if item == "-26" else item
            anchor_id = slugify(display_item)

            character_info = character_data.get(item)

            # 🧠 If this item has nested dicts (base → [characters]), it's a runeword
            if isinstance(character_info, dict):
                base_html = ""
                for base, characters in sorted(character_info.items(), key=lambda kv: len(kv[1]), reverse=True):
                    characters_html = "".join(
                        f""" 
                        <div class="character-info">
                            <div class="character-link">
                                <a href="https://beta.pathofdiablo.com/armory?name={char['name']}" target="_blank">
                                    {char['name']}
                                </a>
                            </div>
                            <div>Level {char['level']} {char['class']}</div>
                            <div class="hover-trigger" data-character-name="{char['name']}"></div>
                        </div>
                        <div class="character"><div class="popup hidden"></div></div>
                        """ for char in characters
                    )

                    base_html += f"""
                    <button class="collapsible">
                        <img src="icons/open-grey.png" class="icon-small open-icon hidden">
                        <img src="icons/closed-grey.png" class="icon-small close-icon">
                        <strong>{base} ({len(characters)} users)</strong>
                    </button>
                    <div class="content" id="{slugify(f"{display_item}-{base}")}">
                        {characters_html or "<p>No characters using this base.</p>"}
                    </div>
                    """

                items_html += f"""
                <button class="collapsible">
                    <img src="icons/open-grey.png" class="icon-small open-icon hidden">
                    <img src="icons/closed-grey.png" class="icon-small close-icon">
                    <strong>
                        <a href="#{anchor_id}" class="anchor-link">
                            {display_item} ({count} users)
                        </a>
                    </strong>
                </button>
                <div class="content" id="{anchor_id}">
                    {base_html or "<p>No characters using this item.</p>"}
                </div>
                """

            else:
                # 🧠 Flat list: uniques, sets, synths
                character_list = character_info or []

                character_list_html = "".join(
                    f""" 
                    <div class="character-info">
                        <div class="character-link">
                            <a href="https://beta.pathofdiablo.com/armory?name={char['name']}" target="_blank">
                                {char['name']}
                            </a>
                        </div>
                        <div>Level {char['level']} {char['class']}</div>
                        <div class="hover-trigger" data-character-name="{char['name']}"></div>
                    </div>
                    <div class="character"><div class="popup hidden"></div></div>
                    """ for char in character_list
                )

                items_html += f"""
                <button class="collapsible">
                    <img src="icons/open-grey.png" class="icon-small open-icon hidden">
                    <img src="icons/closed-grey.png" class="icon-small close-icon">
                    <strong>
                        <a href="#{anchor_id}" class="anchor-link">
                            {display_item} ({count} users)
                        </a>
                    </strong>
                </button>
                <div class="content" id="{anchor_id}">
                    {character_list_html or "<p>No characters using this item.</p>"}
                </div>
                """

        return items_html

    def generate_synth_list_items(counter: Counter, synth_users: dict):
        items_html = ""
#        for item, count in counter.items():
        for item, count in sorted(counter.items(), key=lambda x: (-x[1], x[0])):

            character_list = synth_users.get(item, [])  # Directly fetch correct list

            character_list_html = "".join(
                f""" 
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in character_list
            )

            anchor_id = slugify(item)
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>
                <a href="#synth-{anchor_id}" class="anchor-link">
                    {item} ({count} users)
                </a>
                </strong>
            </button>
            <div class="content" id="synth-{anchor_id}">
                {character_list_html if character_list else "<p>No characters using this item.</p>"}
            </div>
            """
        
        return items_html

    synth_user_count = sum(len(users) for users in synth_users.values())

    def generate_synth_source_list(synth_sources):
        items_html = ""

#        for source_item, characters in synth_sources.items():
        for source_item, characters in sorted(synth_sources.items(), key=lambda x: (-len(x[1]), x[0])):
    
            character_list_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div>Used in: <strong>{char["synthesized_item"]}</strong></div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in characters
            )

            anchor_id = slugify(source_item)
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>
                <a href="#synthsource-{anchor_id}" class="anchor-link">
                    {source_item} (Found in {len(characters)} Items)
                </a>
                </strong>
            </button>
            <div class="content" id="synthsource-{anchor_id}">
                {character_list_html if characters else "<p>No characters using this item.</p>"}
            </div>
            """

        return items_html
    synth_source_user_count = sum(len(users) for users in synth_sources.values())


    def generate_crafted_list_items(crafted_counters, crafted_users):
        items_html = ""

        for worn_category, counter in crafted_counters.items():
            if not counter:  # Skip empty categories
                continue
            
            unique_users = {char["name"]: char for item in counter for char in crafted_users.get(worn_category, {}).get(item, [])}
            # Skip categories with no users
            if not unique_users:
                continue

            # Collect all characters in this category
            category_users = []
            for item, count in counter.items():
                category_users.extend(crafted_users.get(worn_category, {}).get(item, []))

            # Skip categories with no users
            if not category_users:
                continue

            # Create the list of all users in this category
            character_list_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in category_users
            )

            # Create a collapsible button for each category
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>Crafted {worn_category} ({len(category_users)} users)</strong>
            </button>
            <div class="content">
                {character_list_html if category_users else "<p>No characters using crafted items in this category.</p>"}
            </div>
            """

        return items_html
    craft_user_count = len({char["name"] for users in crafted_users.values() for item_users in users.values() for char in item_users})
    craft_user_count = sum(len(users) for users in crafted_users.values())


    def generate_magic_list_items(magic_counters, magic_users):
        items_html = ""

        for worn_category, counter in magic_counters.items():
            if not counter:  # Skip empty categories
                continue

            # Collect unique characters in this category
            unique_users = {char["name"]: char for item in counter for char in magic_users.get(worn_category, {}).get(item, [])}

            # Skip categories with no users
            if not unique_users:
                continue

            # Create the list of all unique users in this category
            character_list_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in unique_users.values()
            )

            # Create a collapsible button for each category
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>Magic {worn_category} ({len(unique_users)} users)</strong>
            </button>
            <div class="content">
                {character_list_html if unique_users else "<p>No characters using magic items in this category.</p>"}
            </div>
            """

        return items_html

    # ✅ Count total **unique** magic item users across all categories
    magic_user_count = len({char["name"] for users in magic_users.values() for item_users in users.values() for char in item_users})
    magic_user_count = sum(len(users) for users in magic_users.values())


    def generate_rare_list_items(rare_counter, rare_users):
        items_html = ""

        for worn_category, counter in rare_counter.items():
            if not counter:  # Skip empty categories
                continue

            # Collect unique characters in this category
            unique_users = {char["name"]: char for item in counter for char in rare_users.get(worn_category, {}).get(item, [])}

            # Skip categories with no users
            if not unique_users:
                continue

            # Create the list of all unique users in this category
            character_list_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["name"]}" target="_blank">
                            {char["name"]}
                        </a>
                    </div>
                    <div>Level {char["level"]} {char["class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["name"]}"></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div> <!-- No iframe inside initially -->
                </div>
                """ for char in unique_users.values()
            )

            # Create a collapsible button for each category
            items_html += f"""
            <button class="collapsible">
                <img src="icons/open-grey.png" alt="All Runewords Open" class="icon-small open-icon hidden">
                <img src="icons/closed-grey.png" alt="Runewords Close" class="icon-small close-icon">
                <strong>Rare {worn_category} ({len(unique_users)} users)</strong>
            </button>
            <div class="content">
                {character_list_html if unique_users else "<p>No characters using Rare items in this category.</p>"}
            </div>
            """

        return items_html

    # ✅ Count total **unique** rare item users across all categories
    rare_user_count = len({char["name"] for users in rare_users.values() for item_users in users.values() for char in item_users})
    rare_user_count = sum(len(users) for users in rare_users.values())

    def socket_html(sorted_runes, sorted_excluding_runes, all_other_items):
        just_socketed = []  # ✅ Holds ALL socketed items  
        just_socketed_excluding_runewords = []  # ✅ Should hold socketed items EXCEPT those inside runewords  

        def extract_element(item):
            if item.get('Title') == 'Rainbow Facet':
                element_types = ["fire", "cold", "lightning", "poison", "physical", "magic"]
                for element in element_types:
                    for prop in item.get('PropertyList', []):
                        if element in prop.lower():
                            return element.capitalize()
            return item.get('Title', 'Unknown')  # Use title if not "Rainbow Facet"


        # Define runes separately
        rune_names = {
            "El Rune", "Eld Rune", "Tir Rune", "Nef Rune", "Eth Rune", "Ith Rune", "Tal Rune", "Ral Rune", "Ort Rune", "Thul Rune", "Amn Rune", "Sol Rune",
            "Shael Rune", "Dol Rune", "Hel Rune", "Io Rune", "Lum Rune", "Ko Rune", "Fal Rune", "Lem Rune", "Pul Rune", "Um Rune", "Mal Rune", "Ist Rune",
            "Gul Rune", "Vex Rune", "Ohm Rune", "Lo Rune", "Sur Rune", "Ber Rune", "Jah Rune", "Cham Rune", "Zod Rune"
        }

        # Categorize worn slots
        def categorize_worn_slot(worn_category, text_tag):
            if worn_category in ["sweapon1", "weapon1", "sweapon2", "weapon2"]:
                if text_tag == "Arrows":
                    return "Arrows"
                elif text_tag == "Bolts":
                    return "Bolts"
                else:
                    return "Weapons and Shields"

            worn_category_map = {
                "ring1": "Rings", "ring2": "Rings",
                "body": "Armor",
                "gloves": "Gloves",
                "belt": "Belts",
                "helmet": "Helmets",
                "boots": "Boots",
                "amulet": "Amulets",
            }
            return worn_category_map.get(worn_category, "Other")  # Default to "Other"

        # Extract element type from Rainbow Facets
        def extract_element(item):
            if item.get('Title') == 'Rainbow Facet':
                element_types = ["fire", "cold", "lightning", "poison", "physical", "magic"]
                for element in element_types:
                    for prop in item.get('PropertyList', []):
                        if element in prop.lower():
                            return element.capitalize()
            return item.get('Title', 'Unknown')  # Use title if not "Rainbow Facet"

        # Function to process all characters from the single JSON file
        def process_all_items(json_file):
            with open(consolidated_file, "r") as file:
                all_characters = json.load(file)
                all_characters = [
                    json.loads(char) if isinstance(char, str) else char 
                    for char in all_characters 
                    if isinstance(char, dict) and char.get("Stats", {}).get("Level", 0) >= 60
                ]

            # Initialize counters
            all_items = []  
            socketed_items = []  
            items_excluding_runewords = []  
            facet_elements = defaultdict(list)
            
            shields_for_skulls = []
            weapons_for_skulls = []
            helmets_for_skulls = []
            armor_for_skulls = []
            
            jewel_counts = Counter()
            jewel_groupings = {"magic": [], "rare": []}

            # Process each character
            for char_data in all_characters:
                for item in char_data.get('Equipped', []):
                    
                    # Process Skull socketing locations
                    if item.get('Worn') == 'helmet':
                        if any(s.get('Title') == "Perfect Skull" for s in item.get('Sockets', [])):
                            helmets_for_skulls.append(item)
                    elif item.get('Worn') == 'body':
                        if any(s.get('Title') == "Perfect Skull" for s in item.get('Sockets', [])):
                            armor_for_skulls.append(item)
                    elif item.get('Worn') in ['weapon1', 'weapon2', 'sweapon1', 'sweapon2']:
                        is_shield = any("Block" in prop for prop in item.get('PropertyList', []))
                        for socketed_item in item.get('Sockets', []):
                            if socketed_item.get('Title') == "Perfect Skull":
                                if is_shield:
                                    shields_for_skulls.append(socketed_item)
                                else:
                                    weapons_for_skulls.append(socketed_item)

                    # Process Socketed Items
                    if item.get('SocketCount', '0') > '0':  # Check if item has sockets
                        all_items.append(item)
                        if item.get('QualityCode') != 'q_runeword':  # Exclude runewords
                            items_excluding_runewords.append(item)

                        for socketed_item in item.get('Sockets', []):
                            element = extract_element(socketed_item)
                            socketed_items.append(socketed_item)
                            facet_elements[element].append(socketed_item)

                            just_socketed.append(socketed_item)

                            # ✅ Extract QualityCode for categorization
                            quality_code = socketed_item.get('QualityCode', '')

                            # ✅ Separate Magic and Rare Jewels
                            if quality_code == "q_magic":
                                socketed_item["GroupedTitle"] = "Misc. Magic Jewels"
                            elif quality_code == "q_rare":
                                socketed_item["GroupedTitle"] = "Misc. Rare Jewels"
                            else:
                                socketed_item["GroupedTitle"] = socketed_item.get("Title", "Unknown")  # Default title

                            if item.get('QualityCode') != 'q_runeword':
                                items_excluding_runewords.append(socketed_item)
                                just_socketed_excluding_runewords.append(socketed_item)

                            if socketed_item.get('Title') == 'Rainbow Facet':
                                facet_elements[element].append(socketed_item)

            return (
                all_items, socketed_items, items_excluding_runewords,
                just_socketed, just_socketed_excluding_runewords, facet_elements,
                shields_for_skulls, weapons_for_skulls, helmets_for_skulls, armor_for_skulls
            )

        # Function to count item types
        def count_items_by_type(items):
            rune_counter = Counter()
            non_rune_counter = Counter()
            magic_jewel_counter = Counter()
            rare_jewel_counter = Counter()
            facet_counter = defaultdict(lambda: {"count": 0, "perfect": 0})

            for item in items:
                title = item.get('Title', 'Unknown')
                quality = item.get('QualityCode', '')

                if title in rune_names:  # ✅ Sort runes separately
                    rune_counter[title] += 1
                elif "Rainbow Facet" in title:  # ✅ Sort Rainbow Facets separately
                    element = extract_element(item)
                    facet_counter[element]["count"] += 1

                    # ✅ Check for perfect (both +5% and -5% properties)
                    properties = item.get('PropertyList', [])
                    if any("+5" in prop for prop in properties) and any("-5" in prop for prop in properties):
                        facet_counter[element]["perfect"] += 1
                elif quality == "q_magic":  # ✅ Track Magic Jewels with splash
                    has_splash = any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ias = any("attack speed" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ed = any("enhanced damage" in prop.lower() for prop in item.get("PropertyList", []))
                    
                    magic_jewel_counter["Misc. Magic Jewels"] += 1
                    if has_splash:
                        magic_jewel_counter["splash"] += 1
                    if has_ias:
                        magic_jewel_counter["attack speed"] += 1
                    if has_ed:
                        magic_jewel_counter["enhanced damage"] += 1
                elif quality == "q_rare":  # ✅ Track Rare Jewels with splash
                    has_splash = any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    rare_jewel_counter["Misc. Rare Jewels"] += 1
                    if has_splash:
                        rare_jewel_counter["splash"] += 1
                else:  # ✅ All other non-rune items
                    non_rune_counter[title] += 1

            return rune_counter, non_rune_counter, magic_jewel_counter, rare_jewel_counter, facet_counter

        # Example Usage
        json_file = "ladder_hc.json"
        all_items, socketed_items, *_ = process_all_items(json_file)
        just_socketed_runes, just_socketed_non_runes, *_ = count_items_by_type(socketed_items)


        def count_items_by_type(items):
            rune_counter = Counter()
            non_rune_counter = Counter()
            magic_jewel_counter = Counter()
            rare_jewel_counter = Counter()
            facet_counter = defaultdict(lambda: {"count": 0, "perfect": 0})
            skull_counter = Counter()

            for item in items:
                title = item.get('Title', 'Unknown')
                quality = item.get('QualityCode', '')

                if title in rune_names:  # ✅ Sort runes separately
                    rune_counter[title] += 1
                elif "Rainbow Facet" in title:  # ✅ Sort Rainbow Facets separately
                    element = extract_element(item)
                    facet_counter[element]["count"] += 1

                    # ✅ Check for perfect (both +5% and -5% properties)
                    properties = item.get('PropertyList', [])
                    if any("+5" in prop for prop in properties) and any("-5" in prop for prop in properties):
                        facet_counter[element]["perfect"] += 1
                elif quality == "q_magic":  # ✅ Track Magic Jewels with splash
                    has_splash = any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ias = any("attack speed" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ed = any("enhanced damage" in prop.lower() for prop in item.get("PropertyList", []))
                    has_iassplash = any("attack speed" in prop.lower() for prop in item.get("PropertyList", [])) & any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    has_iased = any("attack speed" in prop.lower() for prop in item.get("PropertyList", [])) & any("enhanced damage" in prop.lower() for prop in item.get("PropertyList", []))
                    magic_jewel_counter["Misc. Magic Jewels"] += 1
                    if has_splash:
                        magic_jewel_counter["splash"] += 1
                    if has_ias:
                        magic_jewel_counter["attack speed"] += 1
                    if has_ed:
                        magic_jewel_counter["enhanced damage"] += 1
                    if has_iassplash:
                        magic_jewel_counter["iassplash"] += 1
                    if has_iased:
                        magic_jewel_counter["iased"] += 1
#                    if has_splash & has_ias:
#                        magic_jewel_counter["splash"] += 1
                elif quality == "q_rare":  # ✅ Track Rare Jewels with splash
                    has_splash = any("splash" in prop.lower() for prop in item.get("PropertyList", []))
                    has_ed = any("enhanced damage" in prop.lower() for prop in item.get("PropertyList", []))
                    rare_jewel_counter["Misc. Rare Jewels"] += 1
                    if has_splash:
                        rare_jewel_counter["splash"] += 1
                    if has_ed:
                        rare_jewel_counter["enhanced damage"] += 1
#                elif "Perfect Skull" in title:  # ✅ Sort Rainbow Facets separately
#                    skull_counter[title] += 1
                else:  # ✅ All other non-rune items
                    non_rune_counter[title] += 1

            return rune_counter, non_rune_counter, magic_jewel_counter, rare_jewel_counter, facet_counter #, skull_counter

        just_socketed_runes, just_socketed_non_runes, just_socketed_magic, just_socketed_rare, just_socketed_facets = count_items_by_type(socketed_items)
        just_socketed_excluding_runewords_runes, just_socketed_excluding_runewords_non_runes, just_socketed_excluding_runewords_magic, just_socketed_excluding_runewords_rare, just_socketed_excluding_runewords_facets = count_items_by_type(just_socketed_excluding_runewords)

        # Use .most_common() to sort data in descending order
        sorted_just_socketed_runes = just_socketed_runes.most_common()
        sorted_just_socketed_excluding_runewords_runes = just_socketed_excluding_runewords_runes.most_common()

        # Combine non-runes, magic, rare, and facets into a single list
        all_other_items = [
            *(f"{item}: {count}" for item, count in just_socketed_excluding_runewords_non_runes.items()),
            f"Misc. Magic Jewels: {just_socketed_excluding_runewords_magic['Misc. Magic Jewels']} ({just_socketed_excluding_runewords_magic['splash']} include melee splash, {just_socketed_excluding_runewords_magic['attack speed']} include IAS, {just_socketed_excluding_runewords_magic['enhanced damage']} include ED; of those, there are {just_socketed_excluding_runewords_magic['iassplash']} IAS/Splash and {just_socketed_excluding_runewords_magic['iased']} IAS/ED)",
            f"Misc. Rare Jewels: {just_socketed_excluding_runewords_rare['Misc. Rare Jewels']} ({just_socketed_excluding_runewords_rare['splash']} include melee splash, {just_socketed_excluding_runewords_rare['enhanced damage']} include ED)",
            *(f"Rainbow Facet ({element}): {counts['count']} ({counts['perfect']} are perfect)" for element, counts in just_socketed_excluding_runewords_facets.items()),
#            f"Perfect Skull:  (tacos)"

        ]
#        return sorted_just_socketed_runes, sorted_just_socketed_excluding_runewords_runes, all_other_items
        return (
            format_socket_html_runes(sorted_just_socketed_runes), 
            format_socket_html_runes(sorted_just_socketed_excluding_runewords_runes), 
            format_socket_html(all_other_items)
        )

    def format_socket_html(counter_data):
        """Formats socketed items as an HTML table or list."""
        if isinstance(counter_data, list):  # If it's a list, format as an unordered list
            items = "".join(f"<li>{item}</li>" for item in counter_data)
            return f"<ul>{items}</ul>"

        elif isinstance(counter_data, Counter):  # If it's a Counter, format as a table
            rows = "".join(f"<tr><td>{item}</td><td>{count}</td></tr>" for item, count in counter_data.items())
            return f"<table><tr><th>Item</th><th>Count</th></tr>{rows}</table>"

        elif isinstance(counter_data, dict):  # If it's a dict (e.g., facet counts), format as a list
            items = "".join(f"<li>{item}: {count['count']} ({count['perfect']} perfect)</li>" for item, count in counter_data.items())
            return f"<ul>{items}</ul>"

        return ""  # Return empty string if there's no data

    def format_socket_html_runes(counter_data):
        """Formats socketed items as an HTML table or list."""
        if isinstance(counter_data, list):  # If it's a list of tuples (like runes), format properly
            items = "".join(f"<li>{item}: {count}</li>" for item, count in counter_data)
            return f"<ul>{items}</ul>"

        elif isinstance(counter_data, Counter):  # If it's a Counter, format as a table
            rows = "".join(f"<tr><td>{item}</td><td>{count}</td></tr>" for item, count in counter_data.items())
            return f"<table><tr><th>Item</th><th>Count</th></tr>{rows}</table>"

        elif isinstance(counter_data, dict):  # If it's a dict (e.g., facet counts), format as a list
            items = "".join(f"<li>{item}: {count['count']} ({count['perfect']} perfect)</li>" for item, count in counter_data.items())
            return f"<ul>{items}</ul>"

        return ""  # Return empty string if there's no data


    # Merc things
    def map_readable_names(mercenary_type, worn_category):
        mercenary_mapping = {
            "Desert Mercenary": "Act 2 Desert Mercenary",
            "Rogue Scout": "Act 1 Rogue Scout",
            "Eastern Sorceror": "Act 3 Eastern Sorceror",
            "Barbarian": "Act 5 Barbarian"
        }
        worn_mapping = {
            "body": "Armor",
            "helmet": "Helmet",
            "weapon1": "Weapon",
            "weapon2": "Offhand"
        }
        readable_mercenary = mercenary_mapping.get(mercenary_type, mercenary_type)
        readable_worn = worn_mapping.get(worn_category, worn_category)
        return readable_mercenary, readable_worn
    # Function to analyze mercenaries from a single JSON fileu
    def analyze_mercenaries(all_characters, runeword_counter, unique_counter, set_counter):
        """Analyzes mercenary equipment, updates global item counters, and tracks which mercs use which items."""
        mercenary_counts = Counter()
        mercenary_equipment = defaultdict(lambda: defaultdict(Counter))
        mercenary_names = Counter()
        merc_users = defaultdict(list)  # ✅ Track mercenary users for each item

        for char_data in all_characters:
            if not isinstance(char_data, dict):
                print(f"Skipping unexpected data format: {char_data}")
                continue  # Skip invalid entries

            mercenary = char_data.get("MercenaryType")
            if mercenary:
                readable_mercenary, _ = map_readable_names(mercenary, "")
                mercenary_counts[readable_mercenary] += 1

                merc_name = char_data.get("MercenaryName", "Unknown")
                mercenary_names[merc_name] += 1

                for item in char_data.get("MercenaryEquipped", []):
                    worn_category = item.get("Worn", "Unknown")
                    readable_mercenary, readable_worn = map_readable_names(mercenary, worn_category)
                    title = item.get("Title", "Unknown")
                    quality = item.get("QualityCode", "default")

                    # ✅ Add mercenary items to global counters
                    if quality == "q_runeword":
                        runeword_counter[title] += 1
                    elif quality == "q_unique":
                        unique_counter[title] += 1
                    elif quality == "q_set":
                        set_counter[title] += 1

                    mercenary_equipment[readable_mercenary][readable_worn][title] += 1

                    # ✅ Track which characters' mercenaries are using each item
                    # ✅ Track which characters' mercenaries are using each item
                    merc_users[title.strip().lower()].append({
                        "Name": char_data.get("Name", "Unknown"),
                        "Class": char_data.get("Class", "Unknown"),
                        "Level": char_data.get("Stats", {}).get("Level", "N/A")
                    })

        return mercenary_counts, mercenary_equipment, mercenary_names, merc_users  # ✅ Return merc_users

           
    def generate_mercenary_report(all_characters, runeword_counter, unique_counter, set_counter):
        """Generates HTML report for mercenaries while ensuring their items are included in the item lists."""
        html_output = "<p><h2>Mercenary Analysis and Popular Equipment</h2></p>"

        # Mercenary type counts
        html_output += "<p><h3>Mercenary Type Counts</h3></p><ul>"
        for mercenary, count in mercenary_counts.items():
            html_output += f"<li>{mercenary}: {count}</li>"
        html_output += "</ul>"

        # Most Common Mercenary Names
        html_output += "<h3>Most Common Mercenary Names</h3><ul>"
        for name, count in mercenary_names.most_common(15):
            html_output += f"<li>{name}: {count}</li>"
        html_output += "</ul>"

        # Popular Equipment by Mercenary Type
        html_output += "<p><h3>Popular Equipment by Mercenary Type</h3></p>"
        for mercenary, categories in mercenary_equipment.items():
            html_output += f"<div class='row'><p><strong>{mercenary}</strong></p>"
            for worn_category, items in categories.items():
                html_output += f"<div class='merccolumn'><strong>Most Common {worn_category}s:</strong>"
                html_output += "<ul>"
                top_items = items.most_common(15)
                for title, count in top_items:
                    html_output += f"<li>{title}: {count}</li>"
                html_output += "</ul></div>"
            html_output += "</div>"

        return html_output

    # ✅ Load the consolidated JSON file
    with open(consolidated_file, "r") as file:
        all_characters = json.load(file)
        all_characters = [
            json.loads(char) if isinstance(char, str) else char 
            for char in all_characters 
            if isinstance(char, dict) and char.get("Stats", {}).get("Level", 0) >= 60
        ]


    # ✅ Call analyze_mercenaries and store its results
    mercenary_counts, mercenary_equipment, mercenary_names, merc_users = analyze_mercenaries(
        all_characters, runeword_counter, unique_counter, set_counter
    )

    # ✅ Extract all items used by mercenaries (after calling analyze_mercenaries)
    merc_used_items = set()
    for categories in mercenary_equipment.values():  # Iterate over mercenary types
        for worn_category, items in categories.items():
            merc_used_items.update(items.keys())  # Add all item names to the set

    # Analyze mercenaries while updating item counts
    html_output = generate_mercenary_report(all_characters, runeword_counter, unique_counter, set_counter)

    # Now, the used item lists include mercenary items!

    # Generate the report
#    html_output = generate_mercenary_report(all_characters)

    used_runewords = {item[0] for item in all_runewords}
    used_uniques = {item[0] for item in all_uniques_all}
    used_set_items = {item[0] for item in all_set}
    all_the_items = items_list.all_the_items
    # Ensure `items_list.all_the_items` exists
    try:
        all_the_items = items_list.all_the_items  # ✅ Ensure this is defined
        unused_runewords = {rw.strip().lower() for rw in all_the_items["all_the_runewords"]} - {rw.strip().lower() for rw in used_runewords}
        unused_uniques = {rw.strip().lower() for rw in all_the_items["all_the_uniques"]} - {rw.strip().lower() for rw in used_uniques}
        unused_set_items = {rw.strip().lower() for rw in all_the_items["all_the_sets"]} - {rw.strip().lower() for rw in used_set_items}
    except AttributeError as e:
        print("Error: items_list is not defined or missing required keys.", e)
        unused_runewords = unused_uniques = unused_set_items = set()  # ✅ Prevent crashes

#    print("Unused Runewords:", unused_runewords)
#    print("Unused Unique Items:", unused_uniques)
#    print("Unused Set Items:", unused_set_items)

    # ✅ Ensure merc_used_items is case-insensitive
    merc_used_items = {item.strip().lower() for item in merc_used_items}

    def format_unused_items(items, merc_used_items, merc_users):
        """Converts a set of unused items into an HTML list, with expandy sections for mercs using them."""
        if not items:
            return "<p>No unused items found.</p>"

        html_output = "<ul>"
        
        for item in sorted(items):
            formatted_item = item.strip().lower()
            is_merc_only = formatted_item in merc_used_items
            merc_list = merc_users.get(formatted_item, [])

            # ✅ Generate character list HTML for merc users
            merc_character_html = "".join(
                f"""
                <div class="character-info">
                    <div class="character-link">
                        <a href="https://beta.pathofdiablo.com/armory?name={char["Name"]}" target="_blank">
                            {char["Name"]}
                        </a>
                    </div>
                    <div>Level {char["Level"]} {char["Class"]}</div>
                    <div class="hover-trigger" data-character-name="{char["Name"]}"><!-- Armory Quickview--></div>
                </div>
                <div class="character">
                    <div class="popup hidden"></div>
                </div>
                """
                for char in merc_list
            )

            # ✅ Add collapsible button for mercs
            merc_html_section = ""
            if merc_list:
                merc_html_section = f"""
                <button class="collapsible">
                    <img src="icons/open-grey.png" alt="Expand Mercenaries" class="icon-small open-icon hidden">
                    <img src="icons/closed-grey.png" alt="Collapse Mercenaries" class="icon-small close-icon">
                    <p>Characters whose mercs use {item}</p>
                </button>
                <div class="content">
                    {merc_character_html if merc_character_html else "<p>No mercenaries using this item.</p>"}
                </div>
                """

            # ✅ Add item to list with (only used on mercenaries) if applicable
            html_output += f"""
            <li>
                <strong>{item} </strong>
                <span style='color:gray;'>{'(only used on mercenaries)' if is_merc_only else ''}</span>
                {merc_html_section}
            </li>
            """

        html_output += "</ul>"
        return html_output
    
    merc_used_items = set(merc_users.keys())  # ✅ All lowercase and stripped
    # ✅ Generate updated HTML
    unused_runewords_html = format_unused_items(unused_runewords, merc_used_items, merc_users)
    unused_uniques_html = format_unused_items(unused_uniques, merc_used_items, merc_users)
    unused_set_items_html = format_unused_items(unused_set_items, merc_used_items, merc_users)

    # Generating the HTML for the results
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Ever wonder how many Shako's are in use? Or what the most popular Sorc skills are? This site provides information about class build trends and item details from characters on the current Path of Diablo (PoD) ladder. An alternative to the old analytics site we all know and love.">
        <meta name="keywords" content="path of diablo, builds, stats, statistics, data, analysis, analytics">
        <title>PoD Hardcore Stats</title>
        <link rel="stylesheet" type="text/css" href="./css/test-css.css">
        
        
    </head>
    <body class="special-background">
        <div class="is-clipped">
        <nav class="navbar is-fixed-top is-dark" style="height: 50px;">

            <div class="navbar-brand">
                <a class="is-48x48" href="https://beta.pathofdiablo.com/"><img src="icons/pod.ico" alt="Path of Diablo: Web Portal" width="48" height="48" class="is-48x48" style="height: 48px; width: 48px; margin-left:0;"></a>
    <button class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="podNavbar">
        <br>
        <span></span>
        <span></span>
        <span></span>
    </button>            </div>
            <div id="podNavbar" class="navbar-menu">
                <div class="navbar-start">
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/trade-search">Trade</a>
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/servers">Servers</a>
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/ladder">Ladder</a>
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/public-games">Public Games</a>
                    <a class="navbar-item" href="https://beta.pathofdiablo.com/runewizard">Runewizard</a>
                    <a class="navbar-item" href="https://pathofdiablo.com/p/armory">Armory</a>
                    <a class="navbar-item" href="https://build.pathofdiablo.com">Build Planner</a>
                    <!--<a class="navbar-item" href="https://pathofdiablo.com/p/?live" style="width: 90px;"><span><img src="https://beta.pathofdiablo.com/images/twitchico.png"></span></a>-->
                </div>
                <div class="navbar-end">

                    <div class="navbar-start">	
                        <a class="navbar-item-right" href="https://beta.pathofdiablo.com/my-toons">Character Storage</a>
                        <div class="navbar-item dropdown2">
                            <button class="dropdown2-button">Trends History</button>
                            <div class="dropdown2-content">
                                <a href="https://trends.pathofdiablo.com/Home.html">Current</a>
                                <!--  <a href="https://trends.pathofdiablo.com/Season/14/April/Home">S14</a> -->
                                <div class="dropdown2-item dropdown-sub">
                                    <a class="dropdown-sub-button">S13</a>
                                    <div class="dropdown-sub-content">
                                        <a href="https://trends.pathofdiablo.com/Season/13/July/Home">July</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/June/Home">June</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/May/Home">May</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/April/Home">April</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/March/Home.html">March</a>
                                        <a href="https://trends.pathofdiablo.com/Season/13/February/Home.html">February</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        </nav>  


        <!--<div class="top-buttons">
            <a href="Home" class="top-button" onclick="setActive('Home')">Home</a>
            <div class="split-button">
                <button id="SC" class="split-button-option" onclick="setActive('SC')">SC</button>
                <button id="HC" class="split-button-option" onclick="setActive('HC')">HC</button>
            </div>
            <a href="hcAmazon" class="top-button">Amazon</a>
            <a href="hcAssassin" class="top-button">Assassin</a>
            <a href="hcBarbarian" class="top-button">Barbarian</a>
            <a href="hcDruid" class="top-button">Druid</a>
            <a href="hcNecromancer" class="top-button">Necromancer</a>
            <a href="hcPaladin" class="top-button">Paladin</a>
            <a href="hcSorceress" class="top-button">Sorceress</a>
            <a href="https://github.com/qordwasalreadytaken/pod-stats/blob/main/README.md" class="top-button" target="_blank">About</a>
        </div> -->
        <div class="hamburger" onclick="toggleMenu()">
            <div class="line"></div>
            <div class="line"></div>
            <div class="line"></div>
        </div>

        <div class="top-buttons">
            <a href="Home" class="top-button home-button" onclick="setActive('Home')"></a>
            <a href="#" id="SC_HC" class="top-button"> </a>
            <a href="hcAmazon" id="Amazon" class="top-button amazon-button"></a>
            <a href="hcAssassin" id="Assassin" class="top-button assassin-button"></a>
            <a href="hcBarbarian" id="Barbarian" class="top-button barbarian-button"></a>
            <a href="hcDruid" id="Druid" class="top-button druid-button"></a>
            <a href="hcNecromancer" id="Necromancer" class="top-button necromancer-button"></a>
            <a href="hcPaladin" id="Paladin" class="top-button paladin-button"></a>
            <a href="hcSorceress" id="Sorceress" class="top-button sorceress-button"></a>
            <a href="https://github.com/qordwasalreadytaken/pod-stats/blob/main/README.md" class="top-button about-button" target="_blank"></a>
        </div>
        
<div class="main page-intro">
        <h1>PoD HARDCORE STATS </h1>
        <!-- Embed the Plotly pie chart -->
    <!--     <h2>Pick a class below for more detail</h2>-->
    <!--     <iframe src="hccluster_analysis_report.html"></iframe>  -->
        <div>
            <img src="charts/hcclass_distribution.png">
        </div>
        <h2>
            HC Ladder top 1K Fun Facts
        </h2>
        {kfun_facts_html}
        <h3>HOME PAGE (THIS PAGE) STATS AND DATA ARE FROM THE TOP 1,000 LADDER CHARACTERS OVER LVL 60</h3>
        <h3>OTHER PAGE STATS AND DATA ARE FROM THE TOP 200 CHARACTERS OVER LVL 60 OF THAT CLASS</h3>
    <hr>
        <h3>Class and special pages have taken character data and separated it into probable builds. As such, the groupings and associated data
            will change over time to reflect what is currently accurate.
            <br><br>
            Looking at class and build pages, what you see and what it means:</h3>
        <div>
            <img src="charts/build-pages-legend.png">
        </div>
        <h3>Looking at skills you can assume that:</h3>
        <ul style="padding-left:20px">
         <li>If the first number is 50%, then half of the characters fall into that "build"</li>
         <li>If the percent bar following a skill is 100% then every character in that group has points in that skill</li>
         <li>If the percent is 100% and the total points is high that skill is likely a main skill or synergy </li>
         <li>If the percent is 100% but the total is low that skill is likely one-point-wonder like Hydra and Whirlwind or just a prerequisite </li>
         </ul>
         </h3>
        
        <!-- Moved the Plotly scatter plot to the bottom -->
        <button onclick="topFunction()" id="backToTopBtn" class="back-to-top"></button>
        <hr> 
        <h1>Mercenary reporting</h1>
<h3 id="merc-equipment">
    Mercenary counts and Most Used Runewords, Uniques, and Set items equipped
    <a href="#merc-equipment" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h3>

        <button type="button" class="collapsible">
            <img src="icons/Merc_click.png" alt="Merc Details Open" class="icon open-icon hidden">
            <img src="icons/Merc.png" alt="Merc Details Close" class="icon close-icon">
<!--            <strong>Mercenary Details</strong> -->
        </button>
        <div class="content">
        <div id="mercequips">
            {html_output}
        </div>
        </div>
        <br>
        <hr>        
<h1>Item And Equipment Stats And Data</h1>
{loadouthtml} 
<hr>
<h2 id="runeword-usage">
    Most and Least Used Runewords, Uniques, and Set items currently equipped by characters
    <a href="#runeword-usage" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>

<button type="button" class="collapsible runewords-button">
    <img src="icons/Runewords_click.png" alt="Runewords Open" class="icon open-icon hidden">
    <img src="icons/Runewords.png" alt="Runewords Close" class="icon close-icon">
<!--    <strong>Runewords</strong> -->
</button>
<div class="content">
    <div id="runewords" class="container">
        <div class="column">
            <h3>Most Used Runewords:</h3>
            <ul id="most-popular-runewords">
                {most_popular_runewords}
            </ul>
        </div>
        <div class="column">
            <h3>Least Used Runewords:</h3>
            <ul id="least-popular-runewords">
                {least_popular_runewords}
            </ul>
        </div>
    </div>


    <button type="button" class="collapsible small-collapsible">
        <img src="icons/open.png" alt="All Runewords Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Runewords Close" class="icon-small close-icon">
        <strong>ALL Runewords</strong>
    </button>

    <div class="content">
        <div id="allrunewords">
            {all_runewords}
        </div>
    </div>
</div>

<br>
<button type="button" class="collapsible uniques-button">
    <img src="icons/Uniques_click.png" alt="Uniques Open" class="icon open-icon hidden">
    <img src="icons/Uniques.png" alt="Uniques Close" class="icon close-icon">
<!--    <strong>Uniques</strong>-->
</button>    
<div class="content">   
    <div id="uniques" class="container">
        <div class="column">
            <h3>Most Used Uniques:</h3>
            <ul id="most-popular-uniques">
                {most_popular_uniques}
            </ul>
        </div>
        <div class="column">
            <h3>Least Used Uniques:</h3>
            <ul id="least_popular_uniques">
                {least_popular_uniques}
            </ul>
        </div>
    </div>
    <button type="button" class="collapsible small-collapsible">
        <img src="icons/open.png" alt="All Uniques Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Uniques Close" class="icon-small close-icon">
        <strong>ALL Uniques</strong>
    </button>

    <div class="content">
        <div id="alluniques">
            {all_uniques_all}
        </div>
    </div>

</div>

<br>
<button type="button" class="collapsible sets-button">
    <img src="icons/Sets_click.png" alt="Sets Open" class="icon open-icon hidden">
    <img src="icons/Sets.png" alt="Sets Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
    <div id="sets" class="container">
        <div class="column">
            <h3>Most Used Set Items:</h3>
            <ul id="most-popular-set-items">
                {most_popular_set_items}
            </ul>
        </div>
        <div class="column">
            <h3>Least Used Set Items:</h3>
            <ul id="least_popular_set_items">
                {least_popular_set_items}
            </ul>
        </div>
    </div>
    <button type="button" class="collapsible small-collapsible">
        <img src="icons/open.png" alt="All Set Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Set Close" class="icon-small close-icon">
        <strong>ALL Set</strong>
    </button>

    <div class="content">
        <div id="allset">
            {all_set}
        </div>
    </div>
</div>
<br>
<hr>

        <br>

        <h2>Synth reporting</h2>
<h2 id="synth-items">
    {synth_user_count} Characters with Synthesized items equipped
    <a href="#synth-items" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
        <h3>This is base synthesized items</h3>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <div id="special">
            {all_synth}
        </div>
    </div>

<h2 id="synth-from">
    {synth_source_user_count} Synthesized FROM listings
    <a href="#synth-from" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
        <h3>This shows where propertied an item are showing up in other items. If you wanted to see where the slow from Kelpie or the Ball light from Ondal's had popped up, this is where to look </h3>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <div id="special">
            {synth_source_data}
        </div>
    </div>


        <br>

<h2 id="craft-reporting">Craft reporting
    <a href="#craft-reporting" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>       
        <h3>{craft_user_count} Characters with crafted items equipped</h3>

<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <div id="special">
            {all_crafted}
        </div>
    </div>

<br>

<h2 id="magic-reporting">Magic reporting
    <a href="#magic-reporting" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
        <h3>{magic_user_count} Characters with Magic items equipped</h3>

<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <div id="special">
            {all_magic}
        </div>
    </div>

<br>

<h2 id="rare-reporting">Rare reporting
    <a href="#rare-reporting" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
        <h3>{rare_user_count} Characters with rare items equipped</h3>

<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <div id="special">
            {all_rare}
        </div>
    </div>

<br>

<h2 id="socketable-reporting">Socketable reporting
    <a href="#socketable-reporting" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
        <h3>What are people puting in sockets</h3>

<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">  
        <h2>Socketed Runes Count</h2>
        <h3>Includes Only Character Data, No Mercs</h3>
    <div id="special"  class="container">
<br>
        <div class="column">
            <!-- Left Column -->
                <h2>Most Common Runes <br>(Including Runewords)</h2>
            <ul id="sorted_just_socketed_runes"
                {sorted_just_socketed_runes}
            </ul>
            </div>

            <!-- Right Column -->
            <div class="column">
                <h2>Most Common Runes <br>(Excluding Runewords)</h2>
            <ul id="sorted_just_socketed_excluding_runewords_runes">
                {sorted_just_socketed_excluding_runewords_runes}
            </ul>
            </div>
        </div>

        <div>
            <h2>Other Items Found in Sockets</h2>
        <h3>Includes Only Character Data, No Mercs</h3>
            {all_other_items}
        </div>
    </div>
<br>
<h2 id="unused-items">Unused Items
    <a href="#unused-items" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
            <h3>Some items get no love at the top of the ladder *</h3>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
<!--    <strong>Sets</strong>-->
</button>  
<div class="content">
    <!-- Runewords -->
    <button class="collapsible"> 
        <img src="icons/open.png" alt="Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Close" class="icon-small close-icon">
        <strong>Unused Runewords</strong>
    </button>
    <div class="content">{unused_runewords}</div>

    <!-- Uniques -->
    <button class="collapsible"> 
        <img src="icons/open.png" alt="Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Close" class="icon-small close-icon">
        <strong>Unused Unique Items</strong>
    </button>
    <div class="content">{unused_uniques}</div>

    <!-- Set Items -->
    <button class="collapsible"> 
        <img src="icons/open.png" alt="Open" class="icon-small open-icon hidden">
        <img src="icons/closed.png" alt="Close" class="icon-small close-icon">
        <strong>Unused Set Items</strong>
    </button>
    <div class="content">{unused_set_items}</div>
</div>
<br>
<em>*Reference list used for <a href="https://github.com/GreenDude120/builds_data/blob/main/items_list.py">all runewords, uniques, and set items</a> can be found here</em>
<br>
<br>
<h2 id="one-two-handed">Characters Weilding 2-Handed Swords
    <a href="#one-two-handed" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
</button>  
<div class="content">
{one_or_two_html}
</div>

<br>
<h2 id="two-handed">Melee Weapons That Require Two Hands
    <a href="#two-handed" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
</button>  
<div class="content">
{runewordbasehtml_output}
</div>
<br>
<h2 id="all-bows">Bows and Crossbows
    <a href="#all-bows" class="anchor-link">
        <img src="icons/anchor.png" alt="🔗" class="anchor-icon">
    </a>
</h2>
<button type="button" class="collapsible sets-button">
    <img src="icons/Special_click.png" alt="Synth Open" class="icon open-icon hidden">
    <img src="icons/Special.png" alt="Synth Close" class="icon close-icon">
</button>  
<div class="content">
{bowbasehtml_output}
</div>
<br>
<hr>
        <h1>Specialty Searches, Character Builds</h1>
        <h2>Special builds and custom querries that don't fit in class specific pages</h2>
<!--        <h2>Iron Jang Bong & Warpspear</h2>
        <a href="hcBong_and_Warpspear"> <img src="icons/Special.png" alt="Iron Jang Bong & Warpspear" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br> -->
        <h2>Unique Arrows & Bolts</h2>
        <a href="hcUnique_Bolts_and_Arrows"> <img src="icons/Special.png" alt="Unique Arrows & Bolts" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br>
        <h2>Non-Amazon Bow Users</h2>
        <a href="hcNotazons"> <img src="icons/Special.png" alt="Non-Amazon Bow Users" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br>
        <h2>Dual Offensive Aura Items Equipped</h2>
        <a href="hc2AuraItems"> <img src="icons/Special.png" alt="Dual Offensive Aura Items Equipped" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br>
<!--        <h2>Dashing Strikers</h2>
        <a href="hcDashadin"> <img src="icons/Special.png" alt="Dashing Strikers" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br> -->
<!--        <h2>Possibly Chargers</h2>
        <a href="hcCharge"> <img src="icons/Special.png" alt="Possibly Chargers" style="width:300px;height:50px;" class="collapsible icon"></a>
        <br> -->
        <br>
        <hr>
{fun_facts_html}
<br>
<br>
        <br><br><br><br>


        </div>
        <div class="footer">
        <p>PoD data current as of {timeStamp}</p>
        </div>





<script>
// Collapsible elemets
var coll = document.getElementsByClassName("collapsible");
for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        var openIcon = this.querySelector("img.icon[alt='Open']");
        var closeIcon = this.querySelector("img.icon[alt='Close']");

        if (content.style.display === "block") {
            content.style.display = "none";
            openIcon.classList.remove("hidden");
            closeIcon.classList.add("hidden");
        } else {
            content.style.display = "block";
            openIcon.classList.add("hidden");
            closeIcon.classList.remove("hidden");
        }
    });
}


//Back to top button
var backToTopBtn = document.getElementById("backToTopBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
backToTopBtn.style.display = "block";
} else {
backToTopBtn.style.display = "none";
}
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
document.body.scrollTop = 0; // For Safari
document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

//Trends toolbar
// Trends toolbar
// Trends toolbar
function toggleMenu() {
    const navMenu = document.querySelector('.top-buttons');
    navMenu.classList.toggle('show');
}

document.addEventListener("DOMContentLoaded", function () {
    const scHcButton = document.getElementById("SC_HC");
    const currentUrl = window.location.href;
    const filename = currentUrl.split("/").pop(); // Get the last part of the URL

    // Check if the current page is Hardcore or Softcore
    const isHardcore = filename.startsWith("hc");

    // Update button appearance based on current mode
    if (isHardcore) {
        scHcButton.classList.add("hardcore");
        scHcButton.classList.remove("softcore");
    } else {
        scHcButton.classList.add("softcore");
        scHcButton.classList.remove("hardcore");
    }

    // Update background image based on mode
    updateButtonImage(isHardcore);

    // Add click event to toggle between SC and HC pages
    scHcButton.addEventListener("click", function () {
        let newUrl;

        if (isHardcore) {
            // Convert HC -> SC (remove "hc" from filename)
            newUrl = currentUrl.replace(/hc(\w+)$/, "$1"); // Remove "hc"
        } else {
            // Convert SC -> HC (prepend "hc" to the filename)
            newUrl = currentUrl.replace(/\/(\w+)$/, "/hc$1"); // Prepend "hc"
        }

        // Redirect to the new page
        if (newUrl !== currentUrl) {
            window.location.href = newUrl;
        }
    });

    // Function to update button background image
    function updateButtonImage(isHardcore) {
        if (isHardcore) {
            scHcButton.style.backgroundImage = "url('icons/Hardcore_click.png')";
        } else {
            scHcButton.style.backgroundImage = "url('icons/Softcore_click.png')";
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const currentPage = window.location.pathname.split("/").pop(); // Get current page filename
    const menuItems = document.querySelectorAll(".top-button");

    menuItems.forEach(item => {
        const itemPage = item.getAttribute("href");
        if (itemPage && currentPage === itemPage) {
            item.classList.add("active");
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const currentPage = window.location.pathname.split("/").pop(); // Get current page filename
    const menuItems = document.querySelectorAll(".top-button");

    menuItems.forEach(item => {
        const itemPage = item.getAttribute("href");
        if (itemPage && currentPage === itemPage) {
            item.classList.add("active");
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
const currentPage = window.location.pathname.split("/").pop(); // Get current page filename
const menuItems = document.querySelectorAll(".top-button");

menuItems.forEach(item => {
const itemPage = item.getAttribute("href");
if (itemPage && currentPage === itemPage) {
item.classList.add("active");
}
});
});

//Armory pop up
document.addEventListener("DOMContentLoaded", function () {
let activePopup = null;

document.querySelectorAll(".hover-trigger").forEach(trigger => {
trigger.addEventListener("click", function (event) {
event.stopPropagation();
const characterName = this.getAttribute("data-character-name");

// Close any open popup first
if (activePopup) {
activePopup.classList.remove("active");
activePopup.innerHTML = ""; // Remove iframe for memory efficiency
activePopup = null;
}

// Find the associated popup container
const popup = this.closest(".character-info").nextElementSibling.querySelector(".popup");

// If this popup was already active, just close it
if (popup === activePopup) {
return;
}

// Create an iframe and set its src
const iframe = document.createElement("iframe");
iframe.src = `./armory/video_component.html?charName=${encodeURIComponent(characterName)}`;
iframe.setAttribute("id", "popupFrame");

// Add iframe to the popup
popup.appendChild(iframe);
popup.classList.add("active");

// Set this popup as the active one
activePopup = popup;
});
});

// Close the popup when clicking anywhere outside
document.addEventListener("click", function (event) {
if (activePopup && !activePopup.contains(event.target)) {
activePopup.classList.remove("active");
activePopup.innerHTML = ""; // Remove iframe to free memory
activePopup = null;
}
});
});


//PoD nav buttons
document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.navbar-burger');
    const menu = document.querySelector('.navbar-menu');

    burger.addEventListener('click', () => {
        menu.classList.toggle('is-active');
        burger.classList.toggle('is-active');
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const dropdownButton = document.querySelector('.dropdown2-button');
    const dropdownContent = document.querySelector('.dropdown2-content');

    dropdownButton.addEventListener('click', (event) => {
        event.stopPropagation(); // Prevents clicks from propagating to other elements
        dropdownContent.classList.toggle('is-active'); // Toggles the dropdown visibility
    });

    // Close the dropdown if you click anywhere outside it
    document.addEventListener('click', () => {
        if (dropdownContent.classList.contains('is-active')) {
            dropdownContent.classList.remove('is-active');
        }
    });
});


//Anchor in place fix
// Expand collapsibles and scroll to anchor
function scrollWithOffset(el, offset = -50) {
    const y = el.getBoundingClientRect().top + window.pageYOffset + offset;
    window.scrollTo({ top: y, behavior: 'smooth' });
}

function expandToAnchor(anchorId) {
    console.log("expandToAnchor called with:", anchorId);
    const target = document.getElementById(anchorId);
    if (!target) return;

    // Step 1: Collect all parent .content elements that need expanding
    const stack = [];
    let el = target;
    while (el) {
        if (el.classList?.contains('content')) {
            stack.unshift(el); // add to beginning to expand outermost first
        }
        el = el.parentElement;
    }

    // Step 2: Expand each .content section in order
    for (const content of stack) {
        const button = content.previousElementSibling;
        if (button?.classList.contains('collapsible')) {
            button.classList.add('active');
            content.style.display = "block";

            const openIcon = button.querySelector("img.open-icon");
            const closeIcon = button.querySelector("img.close-icon");
            if (openIcon) openIcon.classList.add("hidden");
            if (closeIcon) closeIcon.classList.remove("hidden");
        }
    }

    // Step 3: Delay scroll until DOM has reflowed
    setTimeout(() => {
        console.log("scrolling to:", target.id);
        scrollWithOffset(target);
    }, 250); // Adjust if necessary
}

// Handle clicks on .anchor-link elements
document.addEventListener('DOMContentLoaded', () => {
    // Handle clicks on .anchor-link elements
    document.querySelectorAll('.anchor-link, a[href^="#"]').forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default anchor behavior
            const anchorId = this.getAttribute('href').substring(1);
            const fullUrl = `${window.location.origin}${window.location.pathname}#${anchorId}`;

            navigator.clipboard.writeText(fullUrl); // Copy full link to clipboard
            history.pushState(null, '', `#${anchorId}`); // Update URL without page reload
            expandToAnchor(anchorId); // Expand and scroll
        });
    });

    // On initial load with hash
    if (window.location.hash) {
        const anchorId = window.location.hash.substring(1);
        // Wait a bit for collapsibles/content to render
        setTimeout(() => {
            expandToAnchor(anchorId);
        }, 200);
    }
});



</script>


    </body>
    </html>
    """

    socketed_runes_html, socketed_excluding_runes_html, other_items_html = socket_html(
        sorted_just_socketed_runes, 
        sorted_just_socketed_excluding_runewords_runes, 
        all_other_items
    )

    two_handed_counter, _ = count_two_handed_weapons(all_equipped_items, all_the_items["two_handed_bases"])
    html_result = generate_two_handed_weapon_html(two_handed_counter)

    bow_bases = all_the_items["bow_bows"] + all_the_items["zon_bows"] + all_the_items["cross_bows"]
    bow_counter, _ = count_two_handed_weapons(all_equipped_items, bow_bases)
    html_result += generate_two_handed_weapon_htmlbow(bow_counter)

    one_or_two_html = analyze_one_or_two_handed_usage(all_characters, items_list.all_the_items["one_or_two_hand"])

    loadout_counts, total_loadouts, empty_loadout_count, partially_empty_set_count = categorize_weapon_loadouts(all_characters)

#    for line in loadout_counts:
#        print(line)

    loadouthtml = generate_loadout_summary_html(loadout_counts, total_loadouts, empty_loadout_count, partially_empty_set_count)
#    with open("loadout_summary.html", "w") as f:
#        f.write(loadouthtml)

    filled_html_content = f"""{html_content}""".replace(
        "{most_popular_runewords}", generate_list_items(most_common_runewords)
    ).replace(
        "{most_popular_uniques}", generate_list_items(most_common_uniques)
    ).replace(
        "{most_popular_set_items}", generate_list_items(most_common_set_items)
    ).replace(
        "{least_popular_runewords}", generate_list_items(least_common_runewords)
    ).replace(
        "{least_popular_uniques}", generate_list_items(least_common_uniques)
    ).replace(
        "{least_popular_set_items}", generate_list_items(least_common_set_items)
    ).replace( 
        "{all_runewords}", generate_all_list_items(all_runewords, runeword_users)
    ).replace(
        "{all_uniques}", generate_all_list_items(all_uniques, all_characters)
    ).replace(
        "{all_uniques_all}", generate_all_list_items(all_uniques_all, unique_users)
    ).replace(
        "{all_set}", generate_all_list_items(all_set, all_characters)
    ).replace(
        "{all_synth}", generate_synth_list_items(synth_counter, synth_users)
    ).replace(
        "{timeStamp}", timeStamp
    ).replace(
        "{synth_user_count}", str(synth_user_count)
    ).replace(
        "{all_crafted}", generate_crafted_list_items(crafted_counters, crafted_users)
    ).replace(
        "{craft_user_count}", str(craft_user_count)
    ).replace(
        "{synth_source_data}", generate_synth_source_list(synth_sources)
    ).replace(
        "{synth_source_user_count}", str(synth_source_user_count)
    ).replace(
        "{all_magic}", generate_magic_list_items(magic_counters, magic_users)
    ).replace(
        "{magic_user_count}", str(magic_user_count)
    ).replace(
        "{all_rare}", generate_rare_list_items(rare_counters, rare_users)
    ).replace(
        "{rare_user_count}", str(rare_user_count)
    ).replace(
        "{sorted_just_socketed_runes}", socketed_runes_html  # ✅ Correctly insert formatted HTML
    ).replace(
        "{sorted_just_socketed_excluding_runewords_runes}", socketed_excluding_runes_html
    ).replace(
        "{all_other_items}", other_items_html
    ).replace(
        "{fun_facts_html}", fun_facts_html
    ).replace(
        "{unused_runewords}", unused_runewords_html
    ).replace(
        "{unused_uniques}", unused_uniques_html
    ).replace(
        "{unused_set_items}", unused_set_items_html
    ).replace(
        "{kfun_facts_html}", kfun_facts_html
    ).replace(
        "{runewordbasehtml_output}", generate_two_handed_weapon_html(two_handed_counter)
    ).replace(
        "{bowbasehtml_output}", generate_two_handed_weapon_htmlbow(bow_counter)
    ).replace(
         "{one_or_two_html}", analyze_one_or_two_handed_usage_with_characters(all_characters, items_list.all_the_items["one_or_two_hand"])
    ).replace(
         "{loadouthtml}", generate_loadout_summary_html(loadout_counts, total_loadouts, empty_loadout_count, partially_empty_set_count)
    ).replace(
        "{html_output}", html_output
    )


    print("Runewords:", sum(runeword_counter.values()))
    print("Uniques:", sum(unique_counter.values()))
    print("Set items:", sum(set_counter.values()))
#    print("Synth:", sum(synth_counter[worn_category][title] for worn_category in synth_counter for title in synth_counter[worn_category]))
 #   print("Crafted:", sum(crafted_counters[worn_category][title] for worn_category in crafted_counters for title in crafted_counters[worn_category]))
 #   print("Magic:", sum(magic_counters[worn_category][title] for worn_category in magic_counters for title in magic_counters[worn_category]))
 #   print("Rare:", sum(rare_counters[worn_category][title] for worn_category in rare_counters for title in rare_counters[worn_category]))

#    template = Template(html_content)
#    html_content = template.render(html_output=html_output)  # Pass sorted clusters to the template

    # Write the filled HTML content to a file
    with open('hcHome.html', 'w') as file:
        file.write(filled_html_content)

    print("HTML file generated successfully.")



def main():
    MakeHome()
    MakehcHome()


if __name__ == "__main__":
    main()
