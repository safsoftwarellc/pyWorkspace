Open Command Pallete
    Shift +Command+P

1) Color Theme
    Predawn Theme Kit
2) File Icon
    vscode-Icon
3) To Open Default Settings
    to show JSON settings side by side
    Open Command Pallete-->Default Settings (JSON)
    a) Find Workbench Settings (workbench.settings with this prefix)
        "workbench.settings.editor": "json",
        "workbench.settings.openDefaultSettings": true,
        "workbench.settings.useSplitJSON": true
    b) update Python settings
        "python.pythonPath": "/Library/Frameworks/Python.framework/Versions/3.9/bin/python3"
    c) Update properties for some editor related
4) Python formatting tools
    Shift+Option+F (formatting keyboard shortcut)
    autopip8
5) Lintting
    helps you o find issues in code and gives you erros and warnings at bottm
    Install Pylint, Enable Lintting and Run Lintting from Command Pallete
6) Code Runner Package
    In Settings(JOSN)-->"code-runner.executorMap":{
        "python": "$pythonPath -u $fullFileName",
    }
    To clear Output window for every run add following settings
        "code-runner.showExecutionMessage": false,
        "code-runner.clearPreviousOutput": true

7) Add Files to Git
8) Understanding Debugger
9) Unit Testing using 'unittest.TestCase'
    Select Pattern of Test Cases like test_*.py or *_test.py etc.
    TestTab opens in left side of Code window
10) Close side bar (Cmd+b)


