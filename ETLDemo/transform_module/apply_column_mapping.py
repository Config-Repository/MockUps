class ApplyColumnMappingModule:

    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, df, context):
        if df is None:
            raise ValueError("Input DataFrame is None")

        mapping = self.rules.get("columns")
        indexes = self.rules.get("indexes")

        if not mapping:
            raise ValueError("Missing 'columns' in mapping rules")

        # If indexes ARE provided -> use index-based selection
        if indexes:
            if len(indexes) != len(mapping):
                raise ValueError("Indexes and columns length mismatch")

            df = df.iloc[:, indexes].copy()

        # If indexes NOT provided -> fallback to old logic
        else:
            if len(df.columns) < len(mapping):
                raise ValueError(
                    f"DataFrame has fewer columns ({len(df.columns)}) "
                    f"than mapping ({len(mapping)})"
                )

            df = df.iloc[:, :len(mapping)].copy()

        # Apply column names
        df.columns = mapping

        return df
