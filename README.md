# QGIS Plugin: Show Random Changelog Entry on Launch

Pops up a window showing a random entry from the QGIS version's visual changelog.

It might take a while for the window to appear because all images etc. are loaded.
In other words the behaviour is a *bit* annoying...

Just meant as a small prototype for myself to be reminded of new QGIS features.

![screenshot](https://github.com/kannes/show-random-changelog-entry/assets/7661092/f8ba9f4c-a98f-4292-aa68-f78a591574c9)

# TODO
- Also consider the last n versions (maybe up to latest LTR) and random pick one
- Add information to the user how to disable the plugin again
- Show some indication that at some point the future THERE WILL BE A WINDOW IN YO FACE
- Instead of scrolling, extract just the section and make a new HTML document from it?
- Properly clear the message from the messagebar when done instead of using an arbitrary duration
- Handle changelog fetching failures :D
- Do use QtWebKit anymore
