var fs = require('fs');
var path = require('path');

function readFiles(dirname) {
  fs.readdir(dirname, function(err, filenames) {
 
    filenames.forEach(function(filename) {
      fs.readFile(path.join(dirname, filename), 'utf-8', function(err, content) {
        if (filename === 'kelli.html' || filename === 'example.html') {
          return 
        }
        let match = content.match(/<img src="(.*)\.*(gif|jpg|png|.)*" /)
        if (match) {
          let res = {filename, img: match[1]}
          console.log(JSON.stringify(res))
        } else {
          console.log(filename)
        }
      });
    });
  });
}

readFiles('./submission')
