def calculate_score(row):
    """
    Calculate a probability score for a lead based on title, company stage,
    in-vitro usage, hub status, and recent publication.
    Returns a score between 0 and 100.
    """
    score = 0

    # Safely read row values and normalize
    title = str(row.get("title", "")).strip().lower()
    stage = str(row.get("company_stage", "")).strip().lower()
    uses_invitro = str(row.get("uses_invitro", "")).strip().lower()
    hub = str(row.get("hub", "")).strip().lower()
    published = str(row.get("published_recent", "")).strip().lower()

    # ----------------------------
    # Title-based scoring
    # ----------------------------
    if any(k in title for k in ["director", "head", "vp"]):
        score += 30
    elif "senior scientist" in title:
        score += 20
    elif "scientist" in title:
        score += 10
    elif "junior scientist" in title:
        score += 5

    # ----------------------------
    # Company stage scoring
    # ----------------------------
    if stage in ["series b", "series c"]:
        score += 20
    elif stage == "series a":
        score += 15
    elif stage == "seed":
        score += 10
    elif stage in ["pre-seed", "angel"]:
        score += 5

    # ----------------------------
    # In-vitro usage
    # ----------------------------
    if uses_invitro == "yes":
        score += 15

    # ----------------------------
    # Hub affiliation
    # ----------------------------
    if hub == "yes":
        score += 10

    # ----------------------------
    # Recent publications
    # ----------------------------
    if published == "yes":
        score += 10

    # Introduce slight random variation for better spread
    import random
    score += random.randint(-5, 5)

    # Ensure score is between 0 and 100
    score = max(0, min(score, 100))

    return score
