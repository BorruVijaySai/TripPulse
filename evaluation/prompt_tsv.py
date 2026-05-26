import os
import json
import random
import argparse
import pandas as pd


# ============================================================
# CLEAN TEXT
# ============================================================

def sanitize_text(text):

    if text is None:
        return ""

    text = str(text)

    # Remove newlines/tabs
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")

    # Collapse spaces
    text = " ".join(text.split())

    return text


# ============================================================
# REMOVE CITY NAME
# ============================================================

def remove_city(entity):

    entity = sanitize_text(entity)

    if "," in entity:
        entity = entity.rsplit(",", 1)[0].strip()

    return entity


# ============================================================
# LOAD REVIEW DATABASE
# ============================================================

def load_review_database(db_dir):

    reviews_db = {}

    files = [
        os.path.join(
            db_dir,
            "review_pro_cons",
            "accomodation_review_pro_cons.csv"
        ),

        os.path.join(
            db_dir,
            "review_pro_cons",
            "restaurant_review_pro_cons_clean.csv"
        ),

        os.path.join(
            db_dir,
            "review_pro_cons",
            "attraction_review_pro_cons_fixed.csv"
        )
    ]

    for file_path in files:

        if not os.path.exists(file_path):
            continue

        df = pd.read_csv(file_path)

        for _, row in df.iterrows():

            city = sanitize_text(
                row.get("City", row.get("city", ""))
            ).lower()

            name = sanitize_text(
                row.get("name", row.get("Name", ""))
            ).lower()

            pros = sanitize_text(
                row.get("pros", row.get("Pros", ""))
            )

            cons = sanitize_text(
                row.get("cons", row.get("Cons", ""))
            )

            if pd.isna(pros):
                pros = ""

            if pd.isna(cons):
                cons = ""

            reviews_db[(city, name)] = {
                "pros": pros.replace("|", ". "),
                "cons": cons.replace("|", ". ")
            }

    return reviews_db


# ============================================================
# EXTRACT ENTITIES
# ============================================================

def extract_entities(plan):

    entities = []

    for day in plan.get("plan", []):

        for key in [
            "accommodation",
            "breakfast",
            "lunch",
            "dinner"
        ]:

            val = sanitize_text(day.get(key, ""))

            if val and val != "-" and "," in val:

                name, city = val.rsplit(",", 1)

                entities.append((
                    city.strip().lower(),
                    name.strip().lower()
                ))

        attractions = sanitize_text(
            day.get("attraction", "")
        )

        if attractions and attractions != "-":

            for attr in attractions.split(";"):

                attr = sanitize_text(attr)

                if "," in attr:

                    name, city = attr.rsplit(",", 1)

                    entities.append((
                        city.strip().lower(),
                        name.strip().lower()
                    ))

    return entities


# ============================================================
# CLEAN REVIEW TEXT
# ============================================================

def clean_review_points(text):

    if not text:
        return []

    points = [
        sanitize_text(x)
        for x in text.split(".")
        if sanitize_text(x)
    ]

    points = list(dict.fromkeys(points))

    return points


# ============================================================
# BUILD REVIEW TEXT
# ============================================================

def build_review_text(entities, reviews_db):

    visited = set()

    outputs = []

    for city, name in entities:

        key = (city, name)

        if key in visited:
            continue

        visited.add(key)

        if key not in reviews_db:
            continue

        data = reviews_db[key]

        pros = clean_review_points(
            data["pros"]
        )

        cons = clean_review_points(
            data["cons"]
        )

        pros_text = " || ".join(
            [f"- {x}" for x in pros]
        )

        cons_text = " || ".join(
            [f"- {x}" for x in cons]
        )

        if not pros_text:
            pros_text = "- None"

        if not cons_text:
            cons_text = "- None"

        outputs.append(
            f"{name.title()} || "
            f"Pros: {pros_text} || "
            f"Cons: {cons_text}"
        )

    return " || ".join(outputs)


# ============================================================
# FORMAT ITINERARY
# ============================================================

def format_itinerary(plan):

    sections = {
        "Accommodation": set(),
        "Restaurants": set(),
        "Attractions": set()
    }

    for day in plan.get("plan", []):

        # ----------------------------------------------------
        # Accommodation
        # ----------------------------------------------------

        acc = sanitize_text(
            day.get("accommodation", "-")
        )

        if acc != "-":
            sections["Accommodation"].add(
                remove_city(acc)
            )

        # ----------------------------------------------------
        # Meals
        # ----------------------------------------------------

        for meal in [
            "breakfast",
            "lunch",
            "dinner"
        ]:

            val = sanitize_text(
                day.get(meal, "-")
            )

            if val != "-":
                sections["Restaurants"].add(
                    remove_city(val)
                )

        # ----------------------------------------------------
        # Attractions
        # ----------------------------------------------------

        attrs = sanitize_text(
            day.get("attraction", "-")
        )

        if attrs != "-":

            for attr in attrs.split(";"):

                attr = sanitize_text(attr)

                if attr:

                    sections["Attractions"].add(
                        remove_city(attr)
                    )

    lines = []

    for section, values in sections.items():

        lines.append(f"{section}:")

        for v in sorted(values):

            lines.append(f"- {v}")

    return " || ".join(lines)


# ============================================================
# VALIDATE PLAN
# ============================================================

def is_valid_plan(plan):

    if not isinstance(plan, dict):
        return False

    if "plan" not in plan:
        return False

    if not isinstance(plan["plan"], list):
        return False

    if len(plan["plan"]) == 0:
        return False

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--without_review_file",
        type=str,
        required=True
    )

    parser.add_argument(
        "--with_review_file",
        type=str,
        required=True
    )

    parser.add_argument(
        "--db_dir",
        type=str,
        required=True
    )

    parser.add_argument(
        "--output_tsv",
        type=str,
        required=True
    )

    args = parser.parse_args()

    # ========================================================
    # LOAD REVIEW DATABASE
    # ========================================================

    print("[*] Loading review database...")

    reviews_db = load_review_database(
        args.db_dir
    )

    # ========================================================
    # LOAD JSONL FILES
    # ========================================================

    print("[*] Loading itineraries...")

    with open(
        args.without_review_file,
        "r",
        encoding="utf-8"
    ) as f:

        without_review_lines = [
            json.loads(x)
            for x in f
        ]

    with open(
        args.with_review_file,
        "r",
        encoding="utf-8"
    ) as f:

        with_review_lines = [
            json.loads(x)
            for x in f
        ]

    # ========================================================
    # BUILD IDX MAPS
    # ========================================================

    without_review_dict = {}

    for sample in without_review_lines:

        if "idx" not in sample:
            continue

        if not is_valid_plan(sample):
            continue

        without_review_dict[sanitize_text(sample["idx"])] = sample

    with_review_dict = {}

    for sample in with_review_lines:

        if "idx" not in sample:
            continue

        if not is_valid_plan(sample):
            continue

        with_review_dict[sanitize_text(sample["idx"])] = sample

    # ========================================================
    # COMMON INDICES
    # ========================================================

    common_indices = sorted(
        set(without_review_dict.keys()) &
        set(with_review_dict.keys()),
        key=lambda x: int(x)
    )

    print(f"[*] Common valid indices: {len(common_indices)}")
    # ========================================================
    # PRINT MISSING INDICES
    # ========================================================

    without_only = sorted(
        set(without_review_dict.keys()) -
        set(with_review_dict.keys()),
        key=lambda x: int(x)
    )

    with_only = sorted(
        set(with_review_dict.keys()) -
        set(without_review_dict.keys()),
        key=lambda x: int(x)
    )

    print("\n" + "=" * 60)
    print("MISSING INDEX REPORT")
    print("=" * 60)

    print(f"\nIndices only in WITHOUT_REVIEW file ({len(without_only)}):")
    print(without_only)

    print(f"\nIndices only in WITH_REVIEW file ({len(with_only)}):")
    print(with_only)

    print("=" * 60 + "\n")

    # ========================================================
    # BUILD TSV ROWS
    # ========================================================

    rows = []

    for idx in common_indices:

        without_review_plan = without_review_dict[idx]

        with_review_plan = with_review_dict[idx]

        persona = sanitize_text(
            without_review_plan
            .get("JSON", {})
            .get("persona", "")
        )

        query = sanitize_text(
            without_review_plan
            .get("JSON", {})
            .get("query", "")
        )

        # ====================================================
        # RANDOMIZE A/B
        # ====================================================

        swap = random.random() < 0.5

        if swap:

            itinerary_a_plan = with_review_plan
            itinerary_b_plan = without_review_plan

            a_label = "with_review"
            b_label = "without_review"

        else:

            itinerary_a_plan = without_review_plan
            itinerary_b_plan = with_review_plan

            a_label = "without_review"
            b_label = "with_review"

        # ====================================================
        # FORMAT ITINERARIES
        # ====================================================

        itinerary_a = format_itinerary(
            itinerary_a_plan
        )

        itinerary_b = format_itinerary(
            itinerary_b_plan
        )

        # ====================================================
        # REVIEW TEXT
        # ====================================================

        entities_a = extract_entities(
            itinerary_a_plan
        )

        entities_b = extract_entities(
            itinerary_b_plan
        )

        reviews_a = build_review_text(
            entities_a,
            reviews_db
        )

        reviews_b = build_review_text(
            entities_b,
            reviews_db
        )

        # ====================================================
        # APPEND ROW
        # ====================================================

        rows.append({
            "index": idx,
            "persona": persona,
            "query": query,
            "itinerary_a": itinerary_a,
            "reviews_a": reviews_a,
            "a_label": a_label,
            "itinerary_b": itinerary_b,
            "reviews_b": reviews_b,
            "b_label": b_label,
            "gpt_response": ""
        })

    # ========================================================
    # SAVE TSV
    # ========================================================

    df = pd.DataFrame(rows)

    df.to_csv(
        args.output_tsv,
        sep="\t",
        index=False
    )

    print(f"\n[✓] TSV saved to: {args.output_tsv}")
    print(f"[✓] Total rows: {len(df)}")


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    main()