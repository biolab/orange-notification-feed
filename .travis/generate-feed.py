#!/usr/bin/env python3

import sys
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
        priority=None
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
        self.priority = priority

    def __lt__(o1, o2):
        p1 = o1.priority or 1
        p2 = o2.priority or 1

        return p1 < p2


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

        if not notif.reject_button_label and not notif.accept_button_label:
            notif.accept_button_label = "Ok"

        return GeneratedYAMLNotification(
            None,
            notif.type,
            notif.start,
            notif.end,
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
    specified_yamls = []
    for path in yaml_paths:
        try:
            f = open(path)
            loaded = yaml.safe_load(f)
            y = SpecifiedYAMLNotification(**loaded)
            specified_yamls.append(y)
        except:
            print("Failed to load " + path)
            continue

    # sort by priority 
    specified_yamls.sort(reverse=True)
    
    generated_yamls = []
    for spec in specified_yamls:
        g = GeneratedYAMLNotification.from_specified(spec)
        g.id = Path(path).stem
        generated_yamls.append(g)
    
    return generated_yamls


def main():
    print("Parsing yaml files...", flush=True)
    out = parse_yamls()

    os.mkdir("out")

    # write feed to file
    print("Writing notification feed to file...", flush=True)
    yaml_string = yaml.dump(out)
    with open("out/feed.yaml", "w") as f:
        f.write(yaml_string)


if __name__ == "__main__":
    main()
