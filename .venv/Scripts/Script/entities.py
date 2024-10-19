import re
import os

# Názov súboru
file_name = 'output_vmware_esx_esximsg.xml'

# Načítanie obsahu súboru
with open(file_name, 'r', encoding='utf-8') as file:
    content = file.read()

# Regulárny výraz na nájdenie všetkých entít v zátvorkách <>
entities = re.findall(r'<(.*?)>', content)

# Výpis unikátnych entít
unique_entities = set(entities)

# Odstránenie zátvoriek a medzier z entít
cleaned_entities = {re.sub(r'[<>{}\[\]\(\)\s]', '', entity) for entity in unique_entities}

# Vytvorenie názvu pre nový súbor
new_file_name = f"entities_{os.path.basename(file_name)}"

# Zápis upravených unikátnych entít do nového súboru
with open(new_file_name, 'w', encoding='utf-8') as new_file:
    for entity in cleaned_entities:
        new_file.write(entity + '\n')

print(f"Upravené unikátne entity boli uložené do súboru: {new_file_name}")
