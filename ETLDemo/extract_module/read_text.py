import pandas as pd


class ReadTextModule:
    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, data, context):
        """
        Read a text file using the delimiter specified in the YAML source section.
        """

        source = context.get("source", {})

        file_path = source.get("file")
        delimiter = source.get("delimiter", "|")
        skiprows = source.get("skiprows", 0)

        if not file_path:
            raise ValueError("Missing 'file' in source config")

        # Handle common escaped delimiters from YAML
        if delimiter == r"\t":
            delimiter = "\t"

        df = pd.read_csv(
            file_path,
            sep=delimiter,
            skiprows=skiprows,
            dtype=str,
        )

        return df
