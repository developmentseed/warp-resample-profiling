earthaccess_args = {
    "mursst": dict(
        concept_id="C1996881146-POCLOUD",
        bucket="podaac-ops-cumulus-protected",
        folder="MUR-JPL-L4-GLOB-v4.1",
        filename="20020601090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc",
        variable="analysed_sst",
        mask_and_scale=True,
        a_ullr="-179.995,89.995,180.005,-89.995",
    ),
    "gpm_imerg": dict(
        concept_id="C2723754850-GES_DISC",
        bucket="gesdisc-cumulus-prod-protected",
        folder="GPM_L3/GPM_3IMERGDE.07/2002/06",
        filename="3B-DAY-E.MS.MRG.3IMERG.20020601-S000000-E235959.V07B.nc4",
        variable="precipitation",
        mask_and_scale=False,
        a_ullr="-180,90,180,-90",
    ),
}
