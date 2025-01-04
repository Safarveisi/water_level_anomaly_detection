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

    # Absolute path to the parent directory of the current directory
    par_dir_path = os.path.dirname(os.path.dirname(__file__))
    parser.add_argument(
        "--output",
        default=os.path.join(par_dir_path, "kubeconfig.yml"),
        help="Absolute path to output YAML file",
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

    with open(args.output, "w") as yaml_file:
        yaml.safe_dump(yaml_content, yaml_file, default_flow_style=False)

    print(f"Kubeconfig has been written to {args.output}")
