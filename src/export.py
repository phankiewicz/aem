import csv


def export_similarities(name, similarities):
    with open(name, 'w') as f:
        fieldnames = ['x', 'y']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        similarities_dict = [{'x': x, 'y': y} for x, y in similarities]
        writer.writerows(similarities_dict)
