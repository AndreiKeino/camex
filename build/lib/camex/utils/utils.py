import os
import sys


class AddonGroupPaths:
    def __init__(self, group_path):
        self.group_path = group_path
        self.addon_paths = []

    def __repr__(self):
        return ("<AddonGroupPaths group_path: %s addon_paths: %s>"
                % (self.group_path, self.addon_paths))


def get_exe_folder():
    """
    get the executable folder path
    """
    path = ''
    if getattr(sys, 'frozen', False):  # frozen
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.dirname(sys.argv[0])
    return path


def get_addons_group_folder():
    exe_folder = get_exe_folder()
    path = os.path.join(exe_folder, 'addon_groups')
    return path


def get_addon_groups():
    addon_groups = []
    try:
        addons_folder = get_addons_group_folder()
        for item in os.listdir(addons_folder):
            group_path = os.path.join(addons_folder, item)
            if os.path.isdir(group_path):
                group = AddonGroupPaths(group_path)
                addon_groups.append(group)
                for it in os.listdir(group_path):
                    addon_path = os.path.join(group_path, it)
                    if os.path.isdir(addon_path):
                        group.addon_paths.append(addon_path)

        return addon_groups, ''

    except Exception as e:
        return [], str(e)


def basename(filename: str):
    return os.path.basename(filename)


if __name__ == '__main__':
    print('get_addon_groups = ', get_addon_groups())
