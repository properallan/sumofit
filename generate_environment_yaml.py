import os
import subprocess
import yaml

def generate_environment_yaml(env_name="myenv", output_path="environment.yml"):
    """Gera o arquivo environment.yml a partir do ambiente Conda/Mamba atual."""
    
    # Obtem a versão do Python usada no ambiente
    python_version = subprocess.check_output(["python", "--version"], stderr=subprocess.STDOUT)
    python_version = python_version.decode("utf-8").strip().split()[1]
    
    # Obtem as dependências do ambiente ativo usando `conda list`
    result = subprocess.run(["conda", "list", "--export"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError("Erro ao obter lista de dependências do ambiente Conda.")
    
    # Processa a saída e separa as dependências
    dependencies = []
    for line in result.stdout.decode().splitlines():
        if line.startswith("#"):
            continue
        package = line.split("=")[0]  # Nome do pacote
        dependencies.append(package)

    # Gera o arquivo environment.yml
    environment_data = {
        "name": env_name,
        "channels": ["conda-forge", "defaults"],
        "dependencies": [
            f"python={python_version}",  # Inclui a versão do Python
            *dependencies  # Adiciona as dependências extraídas
        ]
    }
    
    with open(output_path, 'w') as f:
        yaml.dump(environment_data, f, default_flow_style=False)
    
    print(f"environment.yml gerado com sucesso em {os.path.abspath(output_path)}")

if __name__ == "__main__":
    # Gera o environment.yml
    generate_environment_yaml()
