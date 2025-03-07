import yaml
import toml
import os

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
    # Gera o requirements.txt a partir do environment.yml
    generate_requirements_from_envyml()
    
    # Atualiza o pyproject.toml com as dependências do environment.yml
    update_pyproject_toml_with_dependencies()
