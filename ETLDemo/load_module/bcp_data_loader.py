import subprocess
import os


class BcpDataLoaderModule:

    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, data, context):
        connection = context.get("target_connection", {})

        server = connection.get("server")
        database = connection.get("database")
        schema = connection.get("schema")
        table = connection.get("table")

        template_path = self.rules.get("data_loader_template")
        output_path = self.rules.get("data_loader")
        datafile = self.rules.get("datafile")
        formatfile = self.rules.get("formatfile")
        delimiter = self.rules.get("delimiter")
        firstrow = self.rules.get("firstrow")
        encoding = self.rules.get("encoding")
        batchsize = self.rules.get("batchsize")
        packetsize = self.rules.get("packetsize")

        # Strict validation
        if not server:
            raise ValueError("Missing 'server' in connection config")
        if not database:
            raise ValueError("Missing 'database' in connection config")
        if not schema:
            raise ValueError("Missing 'schema' in connection config")
        if not table:
            raise ValueError("Missing 'table' in connection config")
        if not template_path:
            raise ValueError("Missing 'data_loader_template' in load rules")
        if not output_path:
            raise ValueError("Missing 'data_loader' in load rules")
        if not datafile:
            raise ValueError("Missing 'datafile' in load rules")
        if not formatfile:
            raise ValueError("Missing 'formatfile' in load rules")
        if delimiter is None:
            raise ValueError("Missing 'delimiter' in load rules")
        if firstrow is None:
            raise ValueError("Missing 'firstrow' in load rules")
        if encoding is None:
            raise ValueError("Missing 'encoding' in load rules")
        if batchsize is None:
            raise ValueError("Missing 'batchsize' in load rules")
        if packetsize is None:
            raise ValueError("Missing 'packetsize' in load rules")

        # Read template
        with open(template_path, "r") as f:
            template = f.read()

        # Replace placeholders
        output = (
            template
            .replace("{{SERVER}}", server)
            .replace("{{DATABASE}}", database)
            .replace("{{SCHEMA}}", schema)
            .replace("{{TABLE}}", table)
            .replace("{{DATAFILE}}", datafile)
            .replace("{{FMTFILE}}", formatfile)
            .replace("{{DELIMITER}}", delimiter)
            .replace("{{FIRSTROW}}", str(firstrow))
            .replace("{{ENCODING}}", str(encoding))
            .replace("{{BATCHSIZE}}", str(batchsize))
            .replace("{{PACKETSIZE}}", str(packetsize))
        )

        # Write batch file
        with open(output_path, "w") as f:
            f.write(output)

        print("Generated batch file")

        # Execute batch file
        output_path = os.path.abspath(self.rules.get("data_loader"))

        result = subprocess.run(
            output_path,
            shell=True,
            text=True
        )

        print(f"Batch execution completed. Return code: {result.returncode}")

        if result.returncode != 0:
            raise RuntimeError("BCP load failed")

        return data
