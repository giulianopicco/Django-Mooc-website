var generate = require('generate-source-map');
var fs = require('fs');
 
var file = {
  source: fs.readFileSync('django-formset.js'),
  sourceFile: 'django-formset.js'
};
 
var map = generate(file);
 
console.log(map.toString());
