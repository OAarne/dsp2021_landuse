import sys
import os
import pandas as pd


def xlsx_to_df(sheet_path: str) -> pd.DataFrame:
    sheet = pd.read_excel(
        sheet_path,
        sheet_name=0,  # Gets first sheet or tab in the file
        engine="openpyxl",
    )
    return sheet


def standardize_df(df: pd.DataFrame, country: str) -> pd.DataFrame:
    # Remove known anomalous data
    if "email" in df.columns:
        df = df.loc[df["email"] != "sfernandez@abt.gob.bo", :]

    # Define dict to translate values from Spanish
    spanish_to_english = {
        " Otras Tierras": "Other Land",
        "Otras Tierras Boscosas": "Other Wooded Land",
        "Bosque": "Forest",
        "Agua": "Water",
        " Bosque Regenerado de Forma Natural": "Naturally regenerated forest",
        " Bosque Plantado": "Planted Forest",
        "Bosque con árboles": "Stocked forest",
        "Bosque temporalmente desprovisto de árboles": "Temporarily unstocked forest",
        "Bosque plantado con árboles": "Stocked planted forest",
        "Bosque plantado temporalmente desprovisto de árboles": "Temporarily unstocked planted forest",
        "Suelo desnudo": "Bare soil",
        "Cultivos": "Cropland",
        "Pastizales": "Grassland",
        "Asentamientos": "Settlement",
        "Con árboles": "With Trees",
        "Sin árboles": "Without Trees",
        "No bosque estable": "Stable Non Forest",
        "Bosque estable": "Stable Forest",
        " Pérdida de bosque": "Forest Loss",
        "Ganancia de bosque": "Forest Gain",
        "Estable con árboles": "Stable Stocked",
        "Con árboles a Sin árboles": "Stocked to Unstocked",
        "De bosque natural a plantación": "Natural forest to plantation",
        "Sin árboles a Con árboles": "Unstocked to Stocked",
        "Estable sin árboles": "Stable Unstocked",
    }
    # Translate value of relevant columns from Spanish
    if "Uso del Suelo 2018 - Centroide" in df.columns:
        cols_to_be_translated = [
            "Uso del Suelo 2018 - Centroide",
            "Subcategorías de Bosque",
            "Sub-categorías si es Bosque regenerado de forma natural",
            "Sub-categorías si es Bosque Plantado",
            "Subcategorías OT",
            "Cultivo - Con o sin árboles",
            "Pastizal - Con o sin árboles",
            "Asentamiento - Con o sin árboles",
            "Cambios para el periodo 2000-2010",
            "Subcategorías de Bosque Estable 00 - 10",
            "Cambios para el periodo 2010-2018",
            "Subcategorías de Bosque Estable 10 - 18",
        ]
        for col in cols_to_be_translated:
            df.loc[:, col] = df.loc[:, col].map(spanish_to_english)

    df = df.rename(
        columns={
            "PLOT_ID": "plot_id",
            "SAMPLE_ID": "sample_id",
            "LON": "lon",
            "LAT": "lat",
            "PL_PLOTID": "pl_plotid",
            "pl_stratum": "stratum",
            # "PL_STRATUM": "stratum",
            "SMPL_STRATUM": "stratum",
            "LAND USE 2018 - CENTROID": "Land Use 2018 - Centroid",
            "LAND.USE.2018...CENTROID": "Land Use 2018 - Centroid",
            "Uso del Suelo 2018 - Centroide": "Land Use 2018 - Centroid",
            "FOREST SUB-CATEGORIES": "Forest Sub-Categories",
            "FOREST.SUB.CATEGORIES": "Forest Sub-Categories",
            "Subcategorías de Bosque": "Forest Sub-Categories",
            "Sub-categorías si es Bosque regenerado de forma natural": "Sub-Categories if Naturally regenerated forest",
            "SUB-CATEGORIES IF NATURALLY REGENERATED FOREST": "Sub-Categories if Naturally regenerated forest",
            "SUB.CATEGORIES.IF.NATURALLY.REGENERATED.FOREST": "Sub-Categories if Naturally regenerated forest",
            "Sub-categorías si es Bosque Plantado": "Sub-Categories if Planted forest",
            "SUB-CATEGORIES IF PLANTED FOREST": "Sub-Categories if Planted forest",
            "SUB.CATEGORIES.IF.PLANTED.FOREST": "Sub-Categories if Planted forest",
            "OL Sub-Categories": "Other Land Sub-Categories",
            "Subcategorías OT": "Other Land Sub-Categories",
            "OL SUB-CATEGORIES": "Other Land Sub-Categories",
            "OL.SUB.CATEGORIES": "Other Land Sub-Categories",
            "Cultivo - Con o sin árboles": "Cropland - With or without trees",
            "CROPLAND - WITH OR WITHOUT TREES": "Cropland - With or without trees",
            "CROPLAND...WITH.OR.WITHOUT.TREES": "Cropland - With or without trees",
            "Pastizal - Con o sin árboles": "Grassland - With or without trees",
            "GRASSLAND - WITH OR WITHOUT TREES": "Grassland - With or without trees",
            "GRASSLAND...WITH.OR.WITHOUT.TREES": "Grassland - With or without trees",
            "Asentamiento - Con o sin árboles": "Settlement - With or without trees",
            "SETTLEMENT - WITH OR WITHOUT TREES": "Settlement - With or without trees",
            "SETTLEMENT...WITH.OR.WITHOUT.TREES": "Settlement - With or without trees",
            "Changes for period 2000 - 2010": "Centroid - Changes 2000-2010",
            "Cambios para el periodo 2000-2010": "Centroid - Changes 2000-2010",
            "CHANGES FOR PERIOD 2000 - 2010": "Centroid - Changes 2000-2010",
            "CHANGES.FOR.PERIOD.2000...2010": "Centroid - Changes 2000-2010",
            "Subcategory of Stable forest 00 - 10": "Centroid - Subcategory of Stable forest 2000-2010",
            "Subcategorías de Bosque Estable 00 - 10": "Centroid - Subcategory of Stable forest 2000-2010",
            "SUBCATEGORY OF STABLE FOREST 00 - 10": "Centroid - Subcategory of Stable forest 2000-2010",
            "SUBCATEGORY.OF.STABLE.FOREST.00...10": "Centroid - Subcategory of Stable forest 2000-2010",
            "Changes for period 2010 - 2018": "Centroid - Changes 2010-2018",
            "Cambios para el periodo 2010-2018": "Centroid - Changes 2010-2018",
            "CHANGES FOR PERIOD 2010 - 2018": "Centroid - Changes 2010-2018",
            "CHANGES.FOR.PERIOD.2010...2018": "Centroid - Changes 2010-2018",
            "Subcategory of Stable forest 10 - 18": "Centroid - Subcategory of Stable forest 2010-2018",
            "Subcategorías de Bosque Estable 10 - 18": "Centroid - Subcategory of Stable forest 2010-2018",
            "SUBCATEGORY OF STABLE FOREST 10 - 18": "Centroid - Subcategory of Stable forest 2010-2018",
            "SUBCATEGORY.OF.STABLE.FOREST.10...18": "Centroid - Subcategory of Stable forest 2010-2018",
            "% OF FOREST": "% of Forest",
            "X..OF.FOREST": "% of Forest",
            "% de Bosque": "% of Forest",
            "% OF OTHER WOODED LAND": "% of Other Wooded Land",
            "X..OF.OTHER.WOODED.LAND": "% of Other Wooded Land",
            "% de Otras Tierras Boscosas": "% of Other Wooded Land",
            "% OF OTHER LAND": "% of Other Land",
            "% de Otras Tierras": "% of Other Land",
            "X..OF.OTHER.LAND": "% of Other Land",
            "% OF WATER": "% of Water",
            "X..OF.WATER": "% of Water",
            "% de Agua": "% of Water",
            "% FOREST LOSS 2000-2010": "% Forest Loss 2000-2010",
            "X..FOREST.LOSS.2000.2010": "% Forest Loss 2000-2010",
            "% Pérdida de bosque 2000-2010": "% Forest Loss 2000-2010",
            "% FOREST GAIN 2000-2010": "% Forest Gain 2000-2010",
            "X..FOREST.GAIN.2000.2010": "% Forest Gain 2000-2010",
            "% Ganancia de bosque 2000-2010": "% Forest Gain 2000-2010",
            "% STABLE FOREST 2000-2010": "% Stable Forest 2000-2010",
            "X..STABLE.FOREST.2000.2010": "% Stable Forest 2000-2010",
            " % Bosque estable 2000-2010": "% Stable Forest 2000-2010",
            "% STABLE NON FOREST 2000-2010": "% Stable Non Forest 2000-2010",
            "X..STABLE.NON.FOREST.2000.2010": "% Stable Non Forest 2000-2010",
            "% No bosque estable 2000-2010": "% Stable Non Forest 2000-2010",
            "% FOREST LOSS 2010-2018": "% Forest Loss 2010-2018",
            "X..FOREST.LOSS.2010.2018": "% Forest Loss 2010-2018",
            "% Pérdida de bosque 2010-2018": "% Forest Loss 2010-2018",
            "% FOREST GAIN 2010-2018": "% Forest Gain 2010-2018",
            "X..FOREST.GAIN.2010.2018": "% Forest Gain 2010-2018",
            "% Ganancia de bosque 2010-2018": "% Forest Gain 2010-2018",
            "% STABLE FOREST 2010-2018": "% Stable Forest 2010-2018",
            "X..STABLE.FOREST.2010.2018": "% Stable Forest 2010-2018",
            "% Bosque estable 2010-2018": "% Stable Forest 2010-2018",
            "% STABLE NON FOREST 2010-2018": "% Stable Non Forest 2010-2018",
            "X..STABLE.NON.FOREST.2010.2018": "% Stable Non Forest 2010-2018",
            "% No bosque estable 2010-2018": "% Stable Non Forest 2010-2018",
        }
    )
    strata_map = {
        "nochangeforest": "No Change, Forest",
        "nochangenoforest": "No Change, No Forest",
        "smallchange": "Small Change",
        "Change": "Big Change",
        "change": "Big Change",
    }
    df["stratum"] = df["stratum"].map(strata_map)
    df = df[
        [
            "plot_id",
            "sample_id",
            "lon",
            "lat",
            # "sample_geom", # This is missing from some of the data for some reason?
            "stratum",
            "pl_plotid",
            "Land Use 2018 - Centroid",
            "Forest Sub-Categories",
            "Sub-Categories if Naturally regenerated forest",
            "Sub-Categories if Planted forest",
            "Other Land Sub-Categories",
            "Cropland - With or without trees",
            "Grassland - With or without trees",
            "Settlement - With or without trees",
            "Centroid - Changes 2000-2010",
            "Centroid - Subcategory of Stable forest 2000-2010",
            "Centroid - Changes 2010-2018",
            "Centroid - Subcategory of Stable forest 2010-2018",
            "% of Forest",
            "% of Other Wooded Land",
            "% of Other Land",
            "% of Water",
            "% Forest Loss 2000-2010",
            "% Forest Gain 2000-2010",
            "% Stable Forest 2000-2010",
            "% Stable Non Forest 2000-2010",
            "% Forest Loss 2010-2018",
            "% Forest Gain 2010-2018",
            "% Stable Forest 2010-2018",
            "% Stable Non Forest 2010-2018",
        ]
    ]
    df["Country"] = [country] * df.shape[0]
    return df


def main():
    dir_path = "_Avoin_U_Result_Matrix_"
    target_dir = "label_CSVs"
    complete_df = None
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    for filename in os.listdir(dir_path):
        if filename.endswith(".xlsx"):
            country = filename.split("_")[0]
            if country == "Results":
                country = "Indonesia"
            print("Processing: " + country)
            df = xlsx_to_df(os.path.join(dir_path, filename))
            df = standardize_df(df, country)
            df.to_csv(os.path.join(target_dir, filename[:-5] + ".csv"), index=False)
            if complete_df is None:
                complete_df = df
            else:
                complete_df = complete_df.append(df)
    complete_df.to_csv(os.path.join(target_dir, "complete.csv"), index=False)


if __name__ == "__main__":
    main()
