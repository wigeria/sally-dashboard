# Plugins

This directory should contain all of your custom SeleniumYAML Steps/Plugins.

There should also be an `__init__.py` file containing imports for all of those steps in the following syntax:

```python
# __init__.py

import plugins.custom_step_package
...
```

Where `custom_step_package` would be the name of your step's package.