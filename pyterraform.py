import subprocess
import os

def run_terraform_command(command, working_dir):
    """Run a Terraform command in the specified working directory and capture the output."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=working_dir)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print(f"Error running command: {' '.join(command)}")
        print(f"STDERR: {stderr}")
    else:
        print(f"Command ran successfully: {' '.join(command)}")
        print(f"STDOUT: {stdout}")

    return stdout, stderr, process.returncode

def terraform_init(working_dir):
    """Run 'terraform init' in the specified directory."""
    command = ['terraform', 'init']
    return run_terraform_command(command, working_dir)

def terraform_apply(working_dir, auto_approve=True):
    """Run 'terraform apply' in the specified directory with optional auto-approve."""
    command = ['terraform', 'apply']
    if auto_approve:
        command.append('-auto-approve')
    return run_terraform_command(command, working_dir)

def terraform_destroy(working_dir, auto_approve=True):
    """Run 'terraform destroy' in the specified directory with optional auto-approve."""
    command = ['terraform', 'destroy']
    if auto_approve:
        command.append('-auto-approve')
    return run_terraform_command(command, working_dir)

def main():
    """Main function to run Terraform commands."""
    terraform_dir = os.path.join(os.getcwd(), 'tf-codes')

    print("Initializing Terraform...")
    terraform_init(terraform_dir)

    print("Applying Terraform configuration...")
    terraform_apply(terraform_dir)

    # Optional: Destroy the resources after applying
    # print("Destroying Terraform-managed infrastructure...")
    # terraform_destroy(terraform_dir)

if __name__ == "__main__":
    main()
