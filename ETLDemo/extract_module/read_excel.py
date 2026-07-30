import pandas as pd


class ReadExcelModule:

    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, data, context):
        """
        Read Excel file defined in the YAML 'source' section.
        """

        source = context.get("source", {})

        file_path = source.get("file")
        sheet_name = source.get("sheet")
        skiprows = source.get("skiprows", 0)

        if not file_path:
            raise ValueError("Missing 'file' in source config")
        if not sheet_name:
            raise ValueError("Missing 'sheet' in source config")

        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            skiprows=skiprows
        )

        return df
