import xml.etree.ElementTree as ET
import json

filename = 'input/0934fdb1-9078-8011-8004-1a424dd879c9/0934fdb1-9078-8011-8004-1a424dd879ca.svg'  # Pfad zur Penpot-Datei

def read_penpot_interactions(filename):
    """ Liest eine Penpot-SVG-Datei und extrahiert Shapes mit Interaktionen. """
    try:
        # Lade und parse die XML-Datei
        tree = ET.parse(filename)
        root = tree.getroot()

        # Definiere den Namespace für Penpot-SVG-Dateien
        ns = {'penpot': 'https://penpot.app/xmlns'}

        # Finde alle Shape-Elemente, die ein Interactions-Element enthalten
        shapes_with_interactions = root.findall('.//penpot:shape[penpot:interactions]', ns)
        interactions_info = []

        for shape in shapes_with_interactions:
            shape_name = shape.attrib['{https://penpot.app/xmlns}name']
            interactions = []
            for interaction in shape.findall('.//penpot:interaction', ns):
                event_type = interaction.attrib['{https://penpot.app/xmlns}event-type']
                destination = interaction.attrib['{https://penpot.app/xmlns}destination']
                action_type = interaction.attrib['{https://penpot.app/xmlns}action-type']
                interactions.append((event_type, destination, action_type))
            interactions_info.append((shape_name, interactions))

        return interactions_info
    except Exception as e:
        print(f"Fehler bei read_penpot_interactions: {e}")
        return []

def find_forms_and_fields(filename):
    """
    Liest eine SVG-Datei und extrahiert alle <g> Elemente, die direkt untergeordnete <penpot:shape> Elemente mit penpot:type='group' enthalten.
    Innerhalb dieser <g>-Elemente sucht das Skript nach <penpot:shape> Elementen mit penpot:type='text', um Felder zu identifizieren.
    """
    try:
        # Lade und parse die XML-Datei
        tree = ET.parse(filename)
        root = tree.getroot()

        # Definiere den Namespace für Standard-SVG und Penpot
        ns = {'svg': 'http://www.w3.org/2000/svg', 'penpot': 'https://penpot.app/xmlns'}

        # Finde alle <g>-Elemente
        root_groups = root.findall('svg:g', {'svg': 'http://www.w3.org/2000/svg'})
        views_with_forms = []
        for root_group in root_groups:
            view_id = root_group.get('id')
            subgroups = root_group.findall('.//svg:g', ns)
            for subgroup in subgroups:
                forms_in_view = []
                # Suche nach Formularen in der Gruppe
                form_header = subgroup.find("penpot:shape[@penpot:type='group']", ns)

                if form_header is not None:
                    form_fields = subgroup.findall(".//penpot:shape[@penpot:type='text']", ns)
                    if len(form_fields) > 0:
                        # Sammle alle Detail-Felder (Text-Shapes) innerhalb dieses Formulars
                        view_form_fields = []
                        for form_field in form_fields:
                            if "{https://penpot.app/xmlns}name" in form_field.attrib:
                                form_field_name = form_field.get("{https://penpot.app/xmlns}name")
                                view_form_fields.append(form_field_name)
                        # Füge die Formularinformationen hinzu
                        if view_form_fields is not None and len(view_form_fields) > 0:
                            forms_in_view.append((form_header.get("{https://penpot.app/xmlns}name"), view_form_fields))
                    views_with_forms.append((view_id, forms_in_view))
        return views_with_forms

    except Exception as e:
        print(f"Fehler bei find_forms_and_fields: {e}")
        return []

# Funktionen aufrufen und Ergebnisse in einer JSON-Struktur speichern
interactions_info = read_penpot_interactions(filename)
forms_and_fields = find_forms_and_fields(filename)
print(forms_and_fields)

# Gesamte Datenstruktur als JSON ausgeben
data_structure = {
    'interactions': interactions_info,
    'views': forms_and_fields
}

print(json.dumps(data_structure, indent=2))
