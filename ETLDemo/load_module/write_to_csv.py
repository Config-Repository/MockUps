import os


class WriteToCsvModule:

    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, df, context):
        if df is None:
            raise ValueError("Input DataFrame is None")

        staging = context.get("staging", {})
        output_file = staging.get("output_file")

        if not output_file:
            raise ValueError("Missing 'output_file' in staging config")

        output_dir = os.path.dirname(output_file)

        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        df = df.replace("nan", "")

        df.to_csv(
            output_file,
            sep="|",
            index=False,
            encoding="utf-8"
        )

        print(f"Wrote staging file: {output_file}")

        return df
