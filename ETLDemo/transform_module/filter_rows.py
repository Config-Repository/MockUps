import pandas as pd


class FilterRowsModule:

    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, df, context):
        if df is None:
            raise ValueError("Input DataFrame is None")

        exclude_values = self.rules.get("exclude_values", [])
        exclude_contains = self.rules.get("exclude_contains", [])

        # Convert entire DataFrame to string for comparison
        df_str = df.astype(str)

        # Start with all rows included
        mask = pd.Series([True] * len(df))

        # Remove rows with exact value matches anywhere
        for val in exclude_values:
            mask &= ~(df_str == val).any(axis=1)

        # Remove rows with substring matches anywhere
        for pattern in exclude_contains:
            mask &= ~df_str.apply(
                lambda row: row.str.contains(pattern, na=False)
            ).any(axis=1)

        df = df[mask]

        return df
