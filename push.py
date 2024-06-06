# a push.py file in this project could be responsible for
# pushing data or configurations to a remote repository,
# handling tasks like uploading the Docker images to Amazon ECR,
# or pushing dbt models to database

# here is a basic example, this would be tailored to the actual project and
# necessary use case

# assumes images are stored in ECR

import subprocess
import sys

ECR_REPOSITORY = "123456789012.dkr.ecr.us-west-2.amazonaws.com/my-repo"


def run_command(command):
    """Run a shell command."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
        sys.exit(process.returncode)
    print(stdout.decode('utf-8'))


def login_to_ecr():
    """Log in to Amazon ECR."""
    login_command = (
        "aws ecr get-login-password --region us-west-2 | "
        "docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com"
    )
    run_command(login_command)


def build_and_push_image(image_name):
    """Build and push Docker image to ECR."""
    build_command = f"docker build -t {image_name} ."
    tag_command = f"docker tag {image_name}:latest {ECR_REPOSITORY}/{image_name}:latest"
    push_command = f"docker push {ECR_REPOSITORY}/{image_name}:latest"

    run_command(build_command)
    run_command(tag_command)
    run_command(push_command)


if __name__ == "__main__":
    login_to_ecr()
    build_and_push_image("my-airflow-webserver")
    build_and_push_image("my-airflow-scheduler")
    build_and_push_image("my-dbt")

