import pandas as pd
from datetime import datetime

def export_to_excel(aggregation_results):
    current_date = datetime.now().strftime('%Y-%m-%d')
    excel_filepath = f"/home/fazan123/MW/Duplicate_ref_Id/duplicate_records_summary_{current_date}.xlsx"

    with pd.ExcelWriter(excel_filepath) as writer:
        for collection_name, duplicate_groups in aggregation_results.items():
            df = pd.DataFrame([group['_id'] for group in duplicate_groups], columns=["Duplicate referenceId"])
            df.to_excel(writer, sheet_name=collection_name, index=False)

    print(f"Duplicate referenceIds have been exported to '{excel_filepath}'.")
    return excel_filepath
