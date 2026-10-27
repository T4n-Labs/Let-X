#!/usr/bin/env python3
from letx.src.config import BASE_URL, DB_DIR, JSON_FILES, CONFIG_DIR
from letx.src.utility import ensure_dirs, fetch_url, load_json, find_package, parse_template, format_dependencies

def cmd_update_db():
    """Function: letx update (Updates the JSON database)"""
    print("🗘 Updating VUR database...")
    ensure_dirs()
    for filename in JSON_FILES:
        url = f"{BASE_URL}/{filename}"
        print(f"   ⤓ Downloading {filename}...")
        content = fetch_url(url)
        with open(DB_DIR / filename, 'w', encoding='utf-8') as f:
            f.write(content)
    print("✔ Database successfully updated!")

def cmd_update_pkg(pkg_name):
    """Function: letx update <pkg_name> (Update template package)"""
    pkg = find_package(pkg_name)
    if not pkg:
        print(f"✗ Package '{pkg_name}' not found in the database")
        return
    
    path = pkg.get("path")
    template_url = f"{BASE_URL}/{path}/template"
    local_path = CONFIG_DIR / path / "template"
    
    local_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"🗘 Updating template for '{pkg_name}'...")
    content = fetch_url(template_url)
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✔ Template '{pkg_name}' has been successfully updated at: {local_path}")

def cmd_get(pkg_name):
    """Function: letx get <pkg_name> (Retrieves a package template)"""
    cmd_update_pkg(pkg_name)

def cmd_search(query):
    """Function: letx search <query> (Searches by name, description, or category)"""
    packages = load_json("packages.json")
    query = query.lower()
    results = []
    
    for pkg in packages:
        name = pkg.get("name", "").lower()
        desc = pkg.get("description", "").lower()
        cat = pkg.get("category", "").lower()
        if query in name or query in desc or query in cat:
            results.append(pkg)
            
    if not results:
        print(f"🔍︎ No packages match '{query}'.")
        return
        
    print(f"🔍︎ Found {len(results)} package(s) for '{query}':\n")
    print(f"{'PACKAGE NAME':<30} | {'CATEGORY':<10} | {'DESCRIPTION'}")
    print("-" * 80)
    for pkg in results[:20]:
        name = pkg.get("name")
        cat = pkg.get("category")
        desc = pkg.get("description")
        desc = desc[:45] + "..." if len(desc) > 45 else desc
        print(f"{name:<30} | {cat:<10} | {desc}")
        
    if len(results) > 20:
        print(f"\n... and {len(results) - 20} other packages.")

def cmd_info(pkg_name):
    """Function: letx info <pkg_name> (Displays detailed package information)"""
    pkg = find_package(pkg_name)
    if not pkg:
        print(f"✗ Package '{pkg_name}' not found in database.")
        return
        
    path = pkg.get("path")
    local_template = CONFIG_DIR / path / "template"
    
    if not local_template.exists():
        print(f" Local template not found. Downloading template '{pkg_name}' first...")
        cmd_get(pkg_name)
        
    try:
        with open(local_template, 'r', encoding='utf-8') as f:
            template_data = parse_template(f.read())
    except FileNotFoundError:
        print(f"✗ Failed to read template at {local_template}")
        return
        
    archs = ", ".join(pkg.get("archs", []))
    
    print(f"Name Package    : {pkg.get('name')}")
    print(f"Version         : {pkg.get('version')}")
    print(f"Revision        : {template_data.get('revision', 'N/A')}")
    print(f"Archs           : {archs}")
    print(f"Description     : {pkg.get('description')}")
    print(f"Maintainer      : {pkg.get('maintainer')}")
    print(f"Distributor     : {pkg.get('distributor')}")
    print(f"License         : {template_data.get('license')}")
    print(f"Homepage        : {pkg.get('homepage')}")
    print(f"Build Style     : {template_data.get('build_style', 'N/A')}")
    print("Hostmakedepends :")
    print(format_dependencies(template_data.get('hostmakedepends', '')))
    print("Makedepends     :")
    print(format_dependencies(template_data.get('makedepends', '')))
    print("Depends         :")
    print(format_dependencies(template_data.get('depends', '')))