def calculate_score(row):
    score = 0

    title = str(row.get("title", "")).lower()
    stage = str(row.get("funding_stage", "")).lower()
    uses_invitro = str(row.get("uses_invitro", "")).lower()
    hub = str(row.get("company_in_hub", "")).lower()

    # Publication logic
    pub_year = row.get("publication_year", "")
    try:
        pub_year = int(pub_year)
        if pub_year >= 2023:
            score += 30
    except:
        pass

    # Seniority scoring
    if any(k in title for k in ["director", "head", "vp"]):
        score += 30
    elif "scientist" in title:
        score += 10

    # Funding stage scoring
    if stage in ["series a", "series b"]:
        score += 20
    elif stage == "seed":
        score += 10

    # Tech fit
    if uses_invitro == "yes":
        score += 15

    # Hub bonus
    if hub == "yes":
        score += 10

    return min(score, 100)
