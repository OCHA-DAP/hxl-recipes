import io, json, os

_RECIPES = '../recipes'


def _write_to_file(data, filename):
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


def _read_from_file(filename):
    with open(filename) as f_in:
        orgs = (json.load(f_in))
    return orgs


def _list_folders(path="."):
    folders = []
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            folders.append(entry)
    return folders


def _build_recipe_file(folders_list: None):
    if folders_list:
        files = []
        for dir in folders_list:
            file = _read_from_file(dir.path + '/recipe.json')
            files.append(file)
        cookbook = {
            "name": "HDX curated cookbooks",
            "title": "HDX curated cookbooks",
            "type": "cookbook-library",
            "cookbooks": files
        }
        _write_to_file(cookbook, _RECIPES + "/cookbook-library.json")
        return cookbook
    return None


def main():
    _build_recipe_file(_list_folders(_RECIPES))


if __name__ == '__main__':
    main()
