# Orange Notification Feed

When the master branch is updated, travis collects all yml files in the notifications directory, generates a `feed.yaml` file, and pushes it to the `generated-feed` branch. Orange reads this file on startup.

## Adding a notification

Put new notifications in the `notifications` folder.
The notification's id, used to discern whether the user has already seen the notification, is its filename. Generally, notifications should adhere to the following naming approach:

```
[date]-[name].yaml
```

For example:

```
20190729-survey.yaml
```

Should any information be missing from a notification, it will either be replaced by a default value (as is the case with the button labels -- an "Ok" accept label is added if nor an accept nor reject label are present), or simply omitted (as is the case with type, requirements, start/end date).

Note, to implement a custom function, change the `open_link` function in Orange's `__main__.py`, such that a link with the `orange` scheme (starting with 'orange://') defines custom behavior.

### Notification Template and Specifics

```
start: YYYY-MM-DD
end: YYYY-MM-DD
type: (announcement|blog|new-features)
requirements:
    installed:
        - [package-name][operator][value]  # check package version
        - [package-name]  # check if package is installed
        - ~[package-name]  # check if package is not installed
    local_config  
        - [config-option][operator][value]
icon: [path-string]  # relative to Orange directory
title: [string]
text: [string]  # can contain hrefs
link: [url-string]  # implement custom actions with orange:// scheme
accept_button_label: [string]
reject_button_label: [string]
```

The start and end dates are **inclusive**.

Supported operators: `<`, `>`, `<=`, `>=`, `==`

In an installed requirement:
- `[package-name]` is syntactic sugar for `[package-name]>=0` (package is installed).
- `~[package-name]` is syntactic sugar for `[package-name]==-1` (package is not installed).

When requiring a local configuration value, the required value is cast from string to the configuration's value before comparison, with the exception of booleans: `True`, `true`, `1`, `False`, `false`, `0` correctly map to a boolean value when compared against a boolean local configuration value.

### Example notification

```
start: 2019-06-02
end: 2019-06-05
type: announcement
requirements:
    installed:
        - Orange3>=3.20
        - Orange3-Bioinformatics
        - ~Orange3-Educational
    local_config:
        - startup/launch-count>5
        - error-reporting/send-statistics==true 
icon: "widgets/icons/Dlg_down3.png" 
title: "Questionnaire"
text: "Would you care to fill in a survey?"
link: "https://orange.biolab.si/"
accept_button_label: 'Ok'
reject_button_label: 'No'
```
