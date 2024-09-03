import earthaccess

earthaccess.login()

results = earthaccess.search_data(
    concept_id="C1996881146-POCLOUD", count=1, temporal=("2002-06-01", "2002-06-01")
)
earthaccess.download(results, "earthaccess_data")
