#!/usr/bin/env python3
import datetime
import shutil
import os
import glob
import yaml
from pathlib import Path


OPERATORS = {"<", ">", "<=", ">=", "=="}


class SpecifiedYAMLNotification:
    """
    Class used for safe loading of yaml files.
    """

    def __init__(
        self,
        type=None,
        start=None,
        end=None,
        requirements=None,
        icon=None,
        title=None,
        text=None,
        link=None,
        accept_button_label=None,
        reject_button_label=None,
    ):
        self.type = type
        self.start = start
        self.end = end
        self.requirements = requirements
        self.icon = icon
        self.title = title
        self.text = text
        self.link = link
        self.accept_button_label = accept_button_label
        self.reject_button_label = reject_button_label


def translate_installed_requirements(installed: [str]):
    # if an installed requirements has no operator, it's syntactic sugar for either installed
    # or not installed, denoted by >= 0 and == -1 respectively
    without_operator = [s for s in installed if not any(op in s for op in OPERATORS)]
    for req in without_operator:
        installed.remove(req)
        if req[0] == "~":
            installed.append(req[1:] + "==-1")
        else:
            installed.append(req + ">=0")

    # as not installed is represented by version -1, if < or <= check, add >= 0 check
    less_operator = [s for s in installed if any(op in s for op in ["<", "<="])]
    for req in less_operator:
        split = req.split("<")
        installed.append(split[0] + ">=0")

    return installed


class GeneratedYAMLNotification(yaml.YAMLObject):
    """
    YAMLObject class used for generating yaml feed.
    """

    yaml_tag = u"!Notification"

    def __init__(
        self,
        id,
        type,
        start,
        end,
        requirements,
        icon,
        title,
        text,
        link,
        accept_button_label,
        reject_button_label,
    ):
        self.id = id
        self.type = type
        self.start = start
        self.end = end
        self.requirements = requirements
        self.icon = icon
        self.title = title
        self.text = text
        self.link = link
        self.accept_button_label = accept_button_label
        self.reject_button_label = reject_button_label

    @staticmethod
    def from_specified(notif: SpecifiedYAMLNotification):
        # translate requirements syntactic sugar
        requirements = notif.requirements
        if requirements and "installed" in requirements:
            requirements["installed"] = translate_installed_requirements(
                requirements["installed"]
            )

        # move up start date, move back end date
        # in Orange, start and end are specified exclusively as opposed to inclusively
        start = notif.start - datetime.timedelta(days=1) if notif.start else None
        end = notif.end + datetime.timedelta(days=1) if notif.end else None

        # set accept button to Ok if no buttons are specified
        if not notif.reject_button_label and not notif.accept_button_label:
            notif.accept_button_label = "Ok"

        return GeneratedYAMLNotification(
            None,
            notif.type,
            start,
            end,
            requirements,
            notif.icon,
            notif.title,
            notif.text,
            notif.link,
            notif.accept_button_label,
            notif.reject_button_label,
        )


def parse_yamls():
    # collect yaml files
    yaml_paths = glob.glob("notifications/*.yml") + glob.glob("notifications/*.yaml")

    # add id and tag to notifications, concat into list
    out = []
    for path in yaml_paths:
        try:
            f = open(path)
            loaded = yaml.safe_load(f)
            y = SpecifiedYAMLNotification(**loaded)
            generated = GeneratedYAMLNotification.from_specified(y)
        except Exception as e:
            print("Failed to load " + path)
            print(e)
            continue
        generated.id = Path(path).stem
        out.append(generated)

    return out


def main():
    print("Parsing yaml files...", flush=True)
    out = parse_yamls()

    if os.path.exists("out"):
        shutil.rmtree("out")
    os.mkdir("out")

    # write feed to file
    print("Writing notification feed to file...", flush=True)
    yaml_string = yaml.dump(out)
    with open("out/feed.yaml", "w") as f:
        f.write(yaml_string)


if __name__ == "__main__":
    main()
