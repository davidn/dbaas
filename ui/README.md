# GenieDB DBaaS UI Project


## Requirements

[node, npm](http://nodejs.org/),
[grunt](http://gruntjs.com/getting-started),
[bower](http://bower.io/)



## Setup Build Environment

```shell
npm install
bower install
```


### Special Build Bower Components (Don't know why this specifically does not play nice with bower packaging rules)

```shell
cd bower_components/sparkline
make
```

You can ignore any error from the make (requires uglifyjs - we do not require the min version for running)

