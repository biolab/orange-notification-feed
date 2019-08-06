#!/usr/bin/env python3

import sys
import os
import glob
import yaml
from pathlib import Path


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
        reject_button_label=None
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
        reject_button_label
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
        return GeneratedYAMLNotification(
            None,
            notif.type,
            notif.start,
            notif.end,
            notif.requirements,
            notif.icon,
            notif.title,
            notif.text,
            notif.link,
            notif.accept_button_label,
            notif.reject_button_label
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
        except:
            print("Failed to load " + path)
            continue
        generated.id = Path(path).stem
        out.append(generated)

    return out


def main():
    print("Parsing yaml files...", flush=True)
    out = parse_yamls()

    # write feed to file
    print("Writing notification feed to file...", flush=True)
    yaml_string = yaml.dump(out)
    with open("tmpfeed.yaml", "w") as f:
        f.write(yaml_string)


if __name__ == "__main__":
    main()
