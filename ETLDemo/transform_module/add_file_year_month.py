import os
from datetime import datetime


class AddFileYearMonthModule:

    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, df, context):
        """
        Add FileYearMonth column using:
        - staging.output_file (base name)
        - current YYYYMM
        """

        if df is None:
            raise ValueError("Input DataFrame is None")

        # Get output file from staging section
        staging = context.get("staging", {})
        output_file = staging.get("output_file")

        if not output_file:
            raise ValueError("Missing 'output_file' in staging config")

        # Build FileYearMonth
        current_yyyymm = datetime.now().strftime("%Y%m")
        filename = os.path.basename(output_file)
        base_filename = os.path.splitext(filename)[0]

        df["FileYearMonth"] = f"{base_filename}_{current_yyyymm}"

        return df
