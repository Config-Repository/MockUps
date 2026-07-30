class RemoveSpacesModule:

    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, df, context):
        """
        Remove spaces from string values in selected columns.

        rules:
            columns: "all" OR list of column names
        """

        if df is None:
            raise ValueError("Input DataFrame is None")

        columns_rule = self.rules.get("columns", "all")

        # Determine target columns
        if columns_rule == "all":
            target_columns = df.columns
        else:
            target_columns = columns_rule

        # Apply transformation
        for col in target_columns:
            if col not in df.columns:
                continue

            # Only apply to string-like columns
            if df[col].dtype == "object":
                df[col] = df[col].astype(str).str.replace(" ", "")

        return df
