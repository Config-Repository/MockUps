import os
import yaml
import importlib


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def resolve_module(module_path):
    module_name, class_name = module_path.split(":")
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls


def build_modules(module_configs, registry):
    modules = []

    for cfg in module_configs:
        name = cfg["name"]

        if name not in registry:
            raise ValueError(f"Module not in registry: {name}")

        module_path = registry[name]["module"]
        module_class = resolve_module(module_path)

        rules = cfg.get("rules", {})

        modules.append(module_class(rules))

    return modules


def run_modules(modules, data, context):
    for module in modules:
        print(f"Running: {module.__class__.__name__}")
        data = module.run(data, context)

    return data


def main():
    import_config_dir = "Config/Import"
    export_config_dir = "Config/Export"

    extract_registry = load_yaml(
        "Module_Registry/extract_module_registry.yaml"
    )
    transform_registry = load_yaml(
        "Module_Registry/transform_module_registry.yaml"
    )
    load_registry = load_yaml(
        "Module_Registry/load_module_registry.yaml"
    )
    export_registry = load_yaml(
        "Module_Registry/export_module_registry.yaml"
    )

    for filename in os.listdir(import_config_dir):
        if not filename.endswith(".yaml"):
            continue

        config_path = os.path.join(import_config_dir, filename)

        try:
            config = load_yaml(config_path)

            if config.get("load_file_flag", "N") != "Y":
                print(f"Skipping: {filename}")
                continue

            print(f"\nProcessing: {filename}")

            # Extract
            data = None
            extract_modules = build_modules(
                config.get("extract", {}).get("modules", []),
                extract_registry,
            )
            data = run_modules(extract_modules, data, config)

            # Transform
            transform_modules = build_modules(
                config.get("transform", {}).get("modules", []),
                transform_registry,
            )
            data = run_modules(transform_modules, data, config)

            # Load
            load_modules = build_modules(
                config.get("load", {}).get("modules", []),
                load_registry,
            )
            run_modules(load_modules, data, config)

            print(f"SUCCESS: {filename}")

        except Exception as e:
            print(f"FAILED: {filename}")
            print(f"Error: {str(e)}")
            continue

    for filename in os.listdir(export_config_dir):
        if not filename.endswith(".yaml"):
            continue

        config_path = os.path.join(export_config_dir, filename)

        try:
            config = load_yaml(config_path)

            if config.get("export_data_flag", "N") != "Y":
                print(f"Skipping: {filename}")
                continue

            print(f"\nProcessing Export: {filename}")

            export_modules = build_modules(
                config.get("export", {}).get("modules", []),
                export_registry,
            )

            run_modules(export_modules, None, config)

            print(f"SUCCESS: {filename}")

        except Exception as e:
            print(f"FAILED: {filename}")
            print(f"Error: {str(e)}")
            continue


if __name__ == "__main__":
    main()
