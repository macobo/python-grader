import os
from os.path import join
import json

CURRENT_FOLDER = os.path.abspath(os.path.dirname(__file__))


def process_file(task_file_contents, folder_path):
    task_data = json.loads(task_file_contents)
    result = []
    for task in task_data["tasks"]:
        assert all(x in task for x in ("name", "tester", "solution"))
        t_result = dict(task)  # copy
        # join paths that are needed
        t_result["tester"] = join(folder_path, t_result["tester"])
        t_result["solution"] = join(folder_path, t_result["solution"])
        if "assets" in t_result:
            t_result["assets"] = [join(folder_path, x) for x in t_result["assets"]]
        result.append(t_result)
    return result


def find_files_with_name(searched_name, path):
    for filename in os.listdir(path):
        full_path = join(path, filename)
        if os.path.isdir(full_path):
            yield from find_files_with_name(searched_name, full_path)
        elif filename == searched_name:
            yield full_path, path


def extend_nameset(collection, nameset):
    for c in collection:
        assert c["name"] not in nameset
        nameset.add(c["name"])


def find_all_tasks(path=CURRENT_FOLDER):
    tasks = []
    seen_names = set()

    for file_path, folder in find_files_with_name("tasks.json", path):
        result = process_file(open(file_path).read(), folder)
        extend_nameset(result, seen_names)
        tasks.extend(result)

    return tasks

if __name__ == "__main__":
    print(json.dumps(find_all_tasks(), indent=4))
