```
deepdiy
│   README.md
│   main.py         # Entrence of the program   
│
└───assets          # Resource files for deepdiy.net and desktop
|                    client to fetch
│   widget_list.json
│   model_list.json
│   ...
│   
└───core            # Core modules of DeepDIY
|
|   plugin_mgr.py   # Collect/Load/Manage Plugins
|   widget_mgr.py   # Put widgets generated by plugins
|                     into window
|   display_mgr.py  # Update content in widget when user select
|                    something to show
|   data_mgr.py     # Manage Data Object which is share among
|                     plugins
|       
└───img             # Images for testing used in Plugins      
|
└───model_zoo       # Deep Learning Models.Including script for
|                    Predicting, Traing and Configuration
|
└───plugins         # Plugins
|   |
|   └───display     # plugins for displaying selected contents
|   |
|   └───processing  # plugins providing functions except for
|                     displaying selected content
|
└───test            # Only experimental snippets
|
└───ui              # UI files of core and plugin modules
|
└───utils           # Utility classes and functions    
```