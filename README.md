# Malicious Page Builder
## About
Malicious Page Builder is a framework built for making advance phishing pages.
It has a variety of modules which you can find useful for generating a good phishing page.
You can also make your own module easily and load it inside the framework.

## Contributing Instructions

First of all, if you can optimize the **base code** then you are more than welcome.
Now before you start doing anything, read this document to the end.

### Modules
* About
  Modules are just HTML files which are written in a way so that they can be merged with other HTML files easily.
* Instructions for writing
  There are few things you must do while writing a module:
    * Specify the name and description of your module
    * Mark the beginning and the end of your main code
    * Mark the `src` that need to be included
    * If the <body> is necessary, you need to Mark it as well.
    * Mark all the function names
#### 1. Specifying Name and Description
  Write these inside a HTML comment: `<!--
MLBname=your_module_name_using_underscore_instead_of_space
MLBdesc=your module description
-->`
#### 2. Marking START and END
  Suppose your code looks like this:
  ```
  function function() {
        console.log('1st');
			}
  function anotherfunction() {
        console.log('2nd');
      }
  function();
  ```
  You have to mark it like this:
  ```
  //MLB-START
  function function() {
        console.log('1st');
			}
  function anotherfunction() {
        console.log('2nd');
      }
  //MLB-END
  function();
  ```
  Everything between `//MLB-START` and `MLB-END` will get collected by the main script.
#### 3. Marking which `src` to include
  Write `<!--MLB_SRC-->` just above the line:
```
<html>
<head>
<title>test</title>
</head>
<!--MLB_SRC-->
<script type="text/javascript" src="https://requirejs.org/docs/release/2.3.5/minified/require.js"></script>

<script language="javascript">
	'use strict';
	const fs = require('fs');
	......
```
#### 4. Marking the `<body>`
Write `<!--MLB-BODY-->` just above `<body>`:
```
<html>
<head>
<title>test</title>
</head>
<!--MLB-BODY-->
<body>
<h1>test</h1>
</body>
</html>
```
#### 5. Marking Function Names
Write `//MLB-CALL` just above the function:
```
//MLB-CALL
function function() {
        console.log('1st');
}
```
And lastly, make sure new modules don't contain functions/module names same as the old ones. To check if your new module is clean, run the `module_checker.py <path_to_your_module.html>`.

**Make sure to check out the `demo_template` inside `templates/`**
