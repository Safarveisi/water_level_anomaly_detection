import os
import argparse
import requests
import yaml


def get_ionos_k8s_kubeconfig(k8s_cluster_id: str, target_dir_path: str) -> None:
    """Calls IONOS cloud API to get the k8s cluster's kubeconfig.yml
    file and saves it in target_dir_path.

    Parameters
    ==========
    k8s_cluster_id: str
        K8s cluster id. The id is generated after creating the
        cluster using e.g. Terraform.
    target_dir_path: str
        The directory in which the kubeconfig.yml will live.
    """
    try:
        ionos_token = os.environ.get(
            "TF_VAR_ionos_token", os.environ["IONOS_CLOUD_TOKEN"]
        )
    except KeyError:
        print(
            "Please set either TF_VAR_ionos_token or IONOS_CLOUD_TOKEN "
            "env variable first."
        )

    response = requests.get(
        f"https://api.ionos.com/cloudapi/v6/k8s/{k8s_cluster_id}/kubeconfig",
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

    file_path = os.path.join(target_dir_path, "kubeconfig.yml")
    with open(file_path, "w") as yaml_file:
        yaml.safe_dump(yaml_content, yaml_file, default_flow_style=False)

    print(f"Kubeconfig has been written to {file_path}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Managed Kubernetes cluster id")
    parser.add_argument(
        "--output",
        default=os.path.dirname(os.path.dirname(__file__)),
        help="Absolute path to the directory where output YAML file will live",
    )
    args = parser.parse_args()

    get_ionos_k8s_kubeconfig(k8s_cluster_id=args.id, target_dir_path=args.output)