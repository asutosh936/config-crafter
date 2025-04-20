from ruamel.yaml import YAML
import sys
import os

def update_bogiefile_with_ruamel(yaml_file, backup=True):
    # Create backup if requested
    if backup:
        backup_file = f"{yaml_file}.bak"
        with open(yaml_file, 'r') as src, open(backup_file, 'w') as dst:
            dst.write(src.read())
        print(f"Backup created: {backup_file}")
    
    # Initialize YAML parser to preserve comments and formatting exactly
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096  # Prevent line wrapping
    # Don't set any indent parameters - let it maintain existing indentation
    
    # Read the existing YAML file
    with open(yaml_file, 'r') as file:
        data = yaml.load(file)
    
    # Make your changes here - this is where you'd add the missing configurations
    
    # Example: Add new variable to vars section
    data['vars']['OTEL_custom_opts'] = '&OTEL_custom_opts -Dotel.resource.attributes=asv=ASVREBEL,ba=BAREBEL -Dotel.exporter.otlp.endpoint=http://localhost:4318 -Dotel.exporter.otlp.protocol=http/protobuf -Dotel.exporter_oltp_metrics_temporality_preference=delta'
    data['vars']['OTEL_east_otel_collector'] = '&OTEL_EAST_COLLECTOR otelservices-fs-dealer'
    data['vars']['OTEL_west_otel_collector'] = '&OTEL_WEST_COLLECTOR otelservices-fs-dealer-w'
    data['vars']['OTEL_east_app_name'] = '&OTEL_WEST_COLLECTOR dealer-insights-bff-fargate-east'
    data['vars']['OTEL_west_app_name'] = '&OTEL_WEST_COLLECTOR dealer-insights-bff-fargate-west'
    
    print('Updating Dev configurations')
    for environment in data['environments']:
        if environment['name'] == 'dev-ecs-fargate':
            for service in environment['inputs']['service']:
                for container in service['containers']:
                        print(container['env'])
                        container['env']['SPRING_PROFILES_ACTIVE'] = 'dev, vault_aws_iam'
                        container['env']['OTEL_CUSTOM_OPTS'] = '*OTEL_custom_opts'

    print('Updating QA configurations')                    
    for environment in data['environments']:
        if environment['name'] == 'qa-ecs-fargate':
            for service in environment['inputs']['service']:
                for container in service['containers']:
                        print(container['env'])
                        container['env']['SPRING_PROFILES_ACTIVE'] = 'qa, vault_aws_iam'
                        container['env']['OTEL_CUSTOM_OPTS'] = '*OTEL_custom_opts'
    
    

    # Write back to file with exact preservation of style
    with open(yaml_file, 'w') as file:
        yaml.dump(data, file)
    
    return True

if __name__ == "__main__":
    # Path to your YAML file
    yaml_file = "bogiefile.yaml"
    
    if len(sys.argv) > 1:
        yaml_file = sys.argv[1]
    
    if not os.path.exists(yaml_file):
        print(f"Error: File {yaml_file} does not exist")
        sys.exit(1)
    
    # Update the YAML file
    if update_bogiefile_with_ruamel(yaml_file):
        print(f"Successfully updated {yaml_file} with new configurations.")
    else:
        print(f"Failed to update {yaml_file}.")