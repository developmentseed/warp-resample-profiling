earthaccess_args = {
    "mursst": dict(
        concept_id="C1996881146-POCLOUD",
        bucket="podaac-ops-cumulus-protected",
        folder="MUR-JPL-L4-GLOB-v4.1",
        filename="20020601090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc",
        variable="analysed_sst",
        scale=True,
        a_ullr="-179.995,89.995,180.005,-89.995",
        daac="PODAAC",
    ),
    "gpm_imerg": dict(
        concept_id="C2723754850-GES_DISC",
        bucket="gesdisc-cumulus-prod-protected",
        folder="GPM_L3/GPM_3IMERGDE.07/2002/06",
        filename="3B-DAY-E.MS.MRG.3IMERG.20020601-S000000-E235959.V07B.nc4",
        variable="precipitation",
        scale=False,
        a_ullr="-180,90,180,-90",
        daac="GES_DISC",
    ),
}

target_extent = {
    0: [
        -20037508.342789244,
        -20037508.342789244,
        20037508.342789244,
        20037508.342789244,
    ],
    1: [
        -20037508.342789244,
        2.2351741790771484e-08,
        -2.2351741790771484e-08,
        20037508.342789244,
    ],
    2: [
        -20037508.342789244,
        10018754.171394633,
        -10018754.171394633,
        20037508.342789244,
    ],
    3: [-20037508.342789244, 15028131.25709194, -15028131.25709194, 20037508.342789244],
    4: [
        -20037508.342789244,
        17532819.79994059,
        -17532819.79994059,
        20037508.342789244,
    ],
    5: [
        -20037508.342789244,
        18785164.071364917,
        -18785164.071364917,
        20037508.342789244,
    ],
    6: [-20037508.342789244, 19411336.20707708, -19411336.20707708, 20037508.342789244],
}
