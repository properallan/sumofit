import yaml
import toml
import subprocess
import os

def generate_environment_yaml(env_name="sumofit", output_path="environment.yml"):
    """Gera o arquivo environment.yml a partir do ambiente Conda/Mamba atual."""
    
    # Obtem a versão do Python usada no ambiente
    python_version = subprocess.check_output(["python", "--version"], stderr=subprocess.STDOUT)
    python_version = python_version.decode("utf-8").strip().split()[1]
    
    with open(output_path, 'w') as f: 
        # Obtem as dependências do ambiente ativo usando `conda list`
        result = subprocess.run(f"mamba env export --no-builds --from-history".split(), stdout=f, stderr=f)
        if result.returncode != 0:
            raise RuntimeError("Erro ao obter lista de dependências do ambiente Conda.")
    
    # # Processa a saída e separa as dependências
    # dependencies = []
    # for line in result.stdout.decode().splitlines():
    #     if line.startswith("#"):
    #         continue
    #     package = line.split("=")[0]  # Nome do pacote
    #     dependencies.append(package)

    # # Gera o arquivo environment.yml
    # environment_data = {
    #     "name": env_name,
    #     "channels": ["conda-forge", "defaults"],
    #     "dependencies": [
    #         f"python={python_version}",  # Inclui a versão do Python
    #         *dependencies  # Adiciona as dependências extraídas
    #     ]
    # }
    
    # with open(output_path, 'w') as f:
    #     yaml.dump(environment_data, f, default_flow_style=False)
    
    print(f"environment.yml gerado com sucesso em {os.path.abspath(output_path)}")

def generate_requirements_txt(output_path='requirements.txt'):
    """Cria arquivo de requirements instalados via pip"""
    
    with open(output_path, 'w') as f: 
        # Obtem as dependências do ambiente ativo usando `conda list`
        result = subprocess.run("pip list --not-required --format=freeze".split(), stdout=f, stderr=f)
        if result.returncode != 0:
            raise RuntimeError("Erro ao criar lista de requirements.txt.")

def generate_requirements_from_envyml(envyml_path='environment.yml', output_path='requirements.txt'):
    """Gera o arquivo requirements.txt a partir do environment.yml"""
    with open(envyml_path, 'r') as f:
        env_data = yaml.safe_load(f)
    
    # Extrai as dependências
    dependencies = []
    for dep in env_data['dependencies']:
        if isinstance(dep, str):  # Dependência diretamente do Conda
            dependencies.append(dep)
        elif isinstance(dep, dict):  # Dependência de pip
            if 'pip' in dep:
                dependencies.extend(dep['pip'])

    with open(output_path, 'w') as f:
        for dep in dependencies:
            f.write(dep + "\n")
    
    print(f"requirements.txt gerado em {os.path.abspath(output_path)}")

def update_pyproject_toml_with_dependencies(pyproject_path='pyproject.toml', envyml_path='environment.yml'):
    """Adiciona as dependências do environment.yml no pyproject.toml"""
    with open(envyml_path, 'r') as f:
        env_data = yaml.safe_load(f)
    
    # Extrai as dependências de 'dependencies' (tanto de Conda quanto de pip)
    dependencies = []
    for dep in env_data['dependencies']:
        if isinstance(dep, str):  # Dependência diretamente do Conda
            dependencies.append(dep)
        elif isinstance(dep, dict):  # Dependência de pip
            if 'pip' in dep:
                dependencies.extend(dep['pip'])
    
    # Atualiza o pyproject.toml
    with open(pyproject_path, 'r') as f:
        config = toml.load(f)

    # Adiciona as dependências na seção 'install_requires'
    install_requires = config.get('tool', {}).get('setuptools', {}).get('dependencies', {}).get('install_requires', [])
    
    # Adiciona as novas dependências
    install_requires.extend(dependencies)
    
    # Atualiza a seção no toml
    config.setdefault('tool', {}).setdefault('setuptools', {}).setdefault('dependencies', {})['install_requires'] = install_requires
    
    # Salva as alterações no pyproject.toml
    with open(pyproject_path, 'w') as f:
        toml.dump(config, f)
    
    print(f"pyproject.toml atualizado com as dependências do environment.yml.")

if __name__ == "__main__":
    # Gera o requirements.txt
    generate_requirements_txt()

    # Gera o environment.yml
    generate_environment_yaml()

    # Gera o requirements.txt a partir do environment.yml
    #generate_requirements_from_envyml()
    
    # Atualiza o pyproject.toml com as dependências do environment.yml
    update_pyproject_toml_with_dependencies()
