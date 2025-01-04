import os
import argparse
import requests
import yaml

if __name__ == "__main__":

    try:
        ionos_token = os.environ["TF_VAR_ionos_token"]
    except KeyError:
        print("Please set TF_VAR_ionos_token env variable first.")

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Managed Kubernetes cluster id")
    parser.add_argument(
        "--output",
        default=os.path.dirname(os.path.dirname(__file__)),
        help="Absolute path to the directory where output YAML file will live",
    )
    args = parser.parse_args()

    response = requests.get(
        f"https://api.ionos.com/cloudapi/v6/k8s/{args.id}/kubeconfig",
        headers={
            "Authorization": f"Bearer {ionos_token}",
            "content-type": "application/yaml",
        },
    )
    response.raise_for_status()

    try:
        yaml_content = yaml.safe_load(response.content)
    except yaml.YAMLError as e:
        print(f"Error processing YAML content: {e}")
        exit(1)

    target_path = os.path.join(args.output, "kubeconfig.yml")
    with open(target_path, "w") as yaml_file:
        yaml.safe_dump(yaml_content, yaml_file, default_flow_style=False)

    print(f"Kubeconfig has been written to {target_path}")
