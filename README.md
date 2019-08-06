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

Should any information be missing from a notification, it will either be replaced by a default value (as is the case with the button labels), or simply omitted (as is the case with type, requirements, start/end date).

Note, to implement a custom function, change the `open_link` function in Orange's `__main__.py`, such that a link with the `orange` scheme (starting with 'orange://') defines custom behavior.

### Notification Template

```
start: YYYY-MM-DD
end: YYYY-MM-DD
type: (announcement|blog|new-features)
requirements:
    installed:
        - [package-name][operation][value]
    local_config
        - [config-option][operation][value]
icon: [path-string]  # relative to Orange directory
title: [string]
text: [string]  # can contain hrefs
link: [string]  # implement custom actions with orange:// scheme
accept_button_label: [string]
reject_button_label: [string]
```

### Example notification

```
start: 2019-06-02
end: 2019-06-05
type: events
requirements:
    installed:
        - Orange3>=3.20
        - Orange3-Bioinformatics<3.5
        - Orange3-Educational==0.2.1
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
