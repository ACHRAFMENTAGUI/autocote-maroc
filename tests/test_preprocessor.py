import pandas as pd
from src.features.preprocessor import CleanInputTransformer

def test_clean_input_transformer_numeric_and_text():
    transformer = CleanInputTransformer()
    raw_df = pd.DataFrame([{
        "kilometrage": "100 000 - 120 000",
        "puissance": "6 cv",
        "Nombre_doors": "5",
        "year": 2018,
        "marke": "renault ",
        "model": "clio",
        "type_boit": "manuelle",
        "type_carburant": "diesel",
        "premiere_main": "oui",
        "city": "casablanca"
    }])
    transformed = transformer.transform(raw_df)

    assert transformed["kilometrage"].iloc[0] == 110000.0
    assert transformed["puissance"].iloc[0] == 6.0
    assert transformed["Nombre_doors"].iloc[0] == 5.0
    assert transformed["marke"].iloc[0] == "Renault"
    assert transformed["city"].iloc[0] == "Casablanca"
    assert transformed["type_carburant"].iloc[0] == "Diesel"
