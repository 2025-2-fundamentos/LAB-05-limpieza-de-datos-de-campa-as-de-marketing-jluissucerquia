"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
from zipfile import ZipFile
from pathlib import Path
def clean_campaign_data():
    input_path = Path("files/input/")
    output_path = Path("files/output/")
    output_path.mkdir(parents=True, exist_ok=True)

    # 1. Cargar todos los CSV dentro de los ZIP
    df_list = []
    for zip_file in input_path.glob("*.csv.zip"):
        with ZipFile(zip_file) as z:
            for file in z.namelist():
                if file.endswith(".csv"):
                    df_list.append(pd.read_csv(z.open(file)))

    df = pd.concat(df_list, ignore_index=True)

    # CLIENT.CSV

    client = df[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage"
        ]
    ].copy()


    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # education: "." → "_" ; "unknown" → NA
    client["education"] = (
        client["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", pd.NA)
    )

    # credit_default y mortgage: yes → 1 ; otro → 0
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    client.to_csv(output_path / "client.csv", index=False)

    # CAMPAIGN.CSV
    campaign = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",   # correcto
            "previous_outcome",
            "campaign_outcome",
            "day",
            "month"
        ]
    ].copy()

    # previous_outcome: success → 1 ; otro → 0
    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)

    # campaign_outcome: yes → 1 ; otro → 0
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    # last_contact_date: YYYY-MM-DD (año 2022)  
    campaign["last_contact_date"] = pd.to_datetime(
        "2022-" + campaign["month"].astype(str) + "-" + campaign["day"].astype(str),
        format="%Y-%b-%d",
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # columnas finales según pytest
    campaign = campaign[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "last_contact_date"
        ]
    ]

    campaign.to_csv(output_path / "campaign.csv", index=False)

    
    # ECONOMICS.CSV
    economics = df[
        [
            "client_id",
            "cons_price_idx",
            "euribor_three_months"
        ]
    ].copy()

    economics.to_csv(output_path / "economics.csv", index=False)

    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    return


if __name__ == "__main__":
    clean_campaign_data()