import subprocess
import os


class BcpDataExporterModule:

    def __init__(self, rules=None):
        self.rules = rules or {}

    def run(self, data, context):

        connection = context.get("server_connection", {})

        server = connection.get("server")
        database = connection.get("database")
        schema = connection.get("schema")
        table = connection.get("table")

        template_path = self.rules.get("data_exporter_template")
        output_path = self.rules.get("data_exporter")

        datafile = self.rules.get("datafile")
        delimiter = self.rules.get("delimiter")
        rowterminator = self.rules.get("rowterminator")
        encoding = self.rules.get("encoding")
        packetsize = self.rules.get("packetsize")

        # Strict validation

        if not server:
            raise ValueError("Missing 'server' in server_connection config")

        if not database:
            raise ValueError("Missing 'database' in server_connection config")

        if not schema:
            raise ValueError("Missing 'schema' in server_connection config")

        if not table:
            raise ValueError("Missing 'table' in server_connection config")

        if not template_path:
            raise ValueError("Missing 'data_exporter_template' in export rules")

        if not output_path:
            raise ValueError("Missing 'data_exporter' in export rules")

        if not datafile:
            raise ValueError("Missing 'datafile' in export rules")

        if delimiter is None:
            raise ValueError("Missing 'delimiter' in export rules")

        if rowterminator is None:
            raise ValueError("Missing 'rowterminator' in export rules")

        if encoding is None:
            raise ValueError("Missing 'encoding' in export rules")

        if packetsize is None:
            raise ValueError("Missing 'packetsize' in export rules")

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
            .replace("{{DELIMITER}}", delimiter)
            .replace("{{ROWTERMINATOR}}", rowterminator)
            .replace("{{ENCODING}}", str(encoding))
            .replace("{{PACKETSIZE}}", str(packetsize))
        )

        # Write batch file

        with open(output_path, "w") as f:
            f.write(output)

        print("Generated export batch file")

        # Execute batch file

        output_path = os.path.abspath(output_path)

        result = subprocess.run(
            output_path,
            shell=True,
            text=True
        )

        print(
            f"Batch execution completed. Return code: {result.returncode}"
        )

        if result.returncode != 0:
            raise RuntimeError("BCP export failed")

        return data
