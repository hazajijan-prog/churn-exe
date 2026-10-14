import sys
import pandas as pd
import pandera.pandas as pa

SCHEMA = pa.DataFrameSchema(
    {
        "kund_id": pa.Column(int, unique=True),
        "alder": pa.Column(int, pa.Check.in_range(18, 110)),
        "region": pa.Column(str),
        "abonnemang": pa.Column(str),
        "manader_som_kund": pa.Column(int, pa.Check.ge(0)),
        "manadskostnad": pa.Column(float, pa.Check.gt(0)),
        "data_gb_per_manad": pa.Column(float, pa.Check.ge(0)),
        "supportarenden_12m": pa.Column(int, pa.Check.ge(0)),
        "avslutat": pa.Column(int, pa.Check.isin([0, 1])),
    },
    strict=True,
)

df = pd.read_csv(sys.argv[1])

try:
    SCHEMA.validate(df, lazy=True)
    print("GRÖN: Datavalidering godkänd!")

except pa.errors.SchemaErrors as fel:
    print("RÖD: Datavalidering misslyckades!")
    print(fel.failure_cases)
    raise SystemExit(1)