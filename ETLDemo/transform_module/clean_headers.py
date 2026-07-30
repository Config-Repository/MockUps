class CleanHeadersModule:

    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, df, context):
        """
        Standardize column names.

        - Trim whitespace
        - Replace spaces with underscores
        - Lowercase everything
        """

        if df is None:
            raise ValueError("Input DataFrame is None")

        df.columns = (
            df.columns
            .str.strip()          # remove leading/trailing spaces
            .str.replace(" ", "_")  # replace spaces with underscore
            .str.lower()          # normalize casing
        )

        return df
