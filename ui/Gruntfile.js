'use strict';
var path = require('path');

var folderMount = function folderMount(connect, point) {
    return connect.static(path.resolve(point));
};

module.exports = function (grunt) {
    // Project configuration.
    grunt.initConfig({
        connect: {
            main: {
                options: {
                    port: 9001,
                    middleware: function (connect, options) {
                        return [folderMount(connect, options.base)]
                    }
                }
            }
        },
        watch: {
            main: {
                options: {
                    livereload: true
                },
                files: ['js/**/*', 'css/**/*', 'img/**/*', 'partial/**/*', 'service/**/*', 'filter/**/*', 'directive/**/*', 'index.html'],
                tasks: ['jshint']
            }
        },
        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            files: ['js/**/*.js', 'partial/**/*.js', 'service/**/*.js', 'filter/**/*.js', 'directive/**/*.js']
        },
        clean: {
            before: {
                src: ['dist', 'temp']
            },
            after: {
                src: ['temp']
            }
        },
        less: {
            production: {
                options: {
                },
                files: {
                    "temp/app.css": "css/app.less"
                }
            }
        },
        ngtemplates: {
            main: {
                options: {
                    module: 'geniedb'
                },
                src: [ 'partial/**/*.html', 'directive/**/*.html' ],
                dest: 'temp/templates.js'
            }
        },
        copy: {
            main: {
                files: [
                    {src: ['index.html'], dest: 'dist/'},
                    {src: ['favicon.ico'], dest: 'dist/'},
                    {src: ['img/**'], dest: 'dist/'},
                    {src: ['bower_components/angular-ui/build/angular-ui-ieshiv.js'], dest: 'dist/'},
                    {src: ['bower_components/font-awesome/font/**'], dest: 'dist/font/', flatten: true, filter: 'isFile', expand: true},
                ]
            }
        },
        dom_munger: {
            readscripts: {
                options: {
                    read: {selector: 'script[data-build!="exclude"]', attribute: 'src', writeto: 'appjs'}
                },
                src: 'index.html'
            },
            readcss: {
                options: {
                    read: {selector: 'link[rel="stylesheet"]', attribute: 'href', writeto: 'appcss'}
                },
                src: 'index.html'
            },
            removescripts: {
                options: {
                    remove: 'script[data-remove!="exclude"]',
                    append: {selector: 'head', html: '<script src="app.full.min.js"></script>'}
                },
                src: 'dist/index.html'
            },
            addscript: {
                options: {
                    callback: function ($) {
                        $("#jQueryScript").after('<script src="app.full.min.js"></script>');
                    }
                },
                src: 'dist/index.html'
            },
            removecss: {
                options: {
                    remove: 'link[rel="stylesheet/less"]'
                },
                src: 'dist/index.html'
            },
            addcss: {
                options: {
                    append: {selector: 'head', html: '<link rel="stylesheet" href="css/app.full.min.css">'}
                },
                src: 'dist/index.html'
            },
            cdn: {
                options: {
                    callback: function ($) {
                        $("script[data-cdn]").attr('src', function () {
                            return this.attr("data-cdn");
                        });
                        $("link[data-cdn]").attr('href', function () {
                            return this.attr("data-cdn");
                        });
                    }
                },
                src: 'dist/index.html'
            },
            clean: {
                options: {
                    callback: function ($) {
                        $("script[data-cdn]").attr('data-cdn', null);

                    }
                },
                src: 'dist/index.html'
            }
        },
        cssmin: {
            main: {
                src: ['temp/app.css'],
                dest: 'dist/css/app.full.min.css'
            }
        },
        concat: {
            main: {
                src: ['<%= dom_munger.data.appjs %>', '<%= ngtemplates.main.dest %>'],
                dest: 'temp/app.full.js'
            }
        },
        ngmin: {
            main: {
                src: 'temp/app.full.js',
                dest: 'dist/app.full.min.js'
            }
        },
        uglify: {
            main: {
                src: 'temp/app.full.js',
                dest: 'dist/app.full.min.js'
            }
        },
        htmlmin: {
            main: {
                options: {
                    removeComments: true,
                    collapseWhitespace: true
                },
                files: {
                    'dist/index.html': 'dist/index.html'
                }
            }
        },
        imagemin: {
            main: {
                files: [
                    {
                        expand: true, cwd: 'dist/',
                        src: ['**/{*.png,*.jpg}'],
                        dest: 'dist/'
                    }
                ]
            }
        },
        jasmine: {
            unit: {
                src: ['<%= dom_munger.data.appjs %>', 'bower_components/angular-mocks/angular-mocks.js'],
                options: {
                    specs: 'test/unit/**/*.js'
                }
            }
        },
        sed: {
            serviceUrl: {
                pattern: new RegExp("//BEGINSERVICEURL[\\s\\S]*ENDSERVICEURL"),
                replacement: 'var serviceUrl = "<%= grunt.option("serviceurl") %>";',
                path: 'js/config.js'
            },
            buildDate: {
                pattern: '%BUILDDATE%',
                replacement: '<%= grunt.template.today("dddd, mmmm dS, yyyy, h:MM:ss TT Z") %>',
                path: 'js/config.js'
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-connect');
    grunt.loadNpmTasks('grunt-angular-templates');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-dom-munger');
    grunt.loadNpmTasks('grunt-contrib-htmlmin');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-jasmine');
    grunt.loadNpmTasks('grunt-ngmin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-sed');


    grunt.registerTask('configure', 'Apply environment settings', function () {
        if (grunt.option('serviceurl')) {
            grunt.task.run(['sed']);
        } else {
            grunt.warn("serviceurl not specified");
        }
    });

    // Original flow
//  grunt.registerTask('build',['jshint','clean:before','less','dom_munger:readcss','dom_munger:readscripts','ngtemplates','cssmin','concat','ngmin','uglify','copy','dom_munger:removecss','dom_munger:addcss','dom_munger:removescripts','dom_munger:addscript','htmlmin','imagemin','clean:after']);
    grunt.registerTask('build', ['jshint', 'clean:before', 'less', 'dom_munger:readscripts', 'ngtemplates', 'cssmin', 'configure', 'concat', 'ngmin', 'copy', 'dom_munger:removecss', 'dom_munger:addcss', 'dom_munger:removescripts', 'dom_munger:addscript', 'dom_munger:cdn', 'dom_munger:clean', 'htmlmin', 'imagemin', 'clean:after']);
    grunt.registerTask('server', ['jshint', 'connect', 'watch']);
    grunt.registerTask('test', ['dom_munger:readscripts', 'jasmine'])

    // grunt build --serviceurl="//dbaas-test.geniedb.com:4000"
};
