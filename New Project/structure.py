import os

def generate_directory_tree(startpath, exclude_dirs=['.git', '__pycache__', '.vscode']):
    tree = []
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]  # Exclude unwanted directories
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level
        tree.append(f"{indent}├── {os.path.basename(root)}/")
        for file in files:
            if file != os.path.basename(__file__):  # Exclude this script itself
                tree.append(f"{indent}│   ├── {file}")
    return '\n'.join(tree)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Assumes this script is in the project root
    
    print("Project Structure:")
    print(f"{os.path.basename(project_root)}/")
    print(generate_directory_tree(project_root))