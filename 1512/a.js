const input = require('./input').input;

let total = 0;

function traverse(node) {
  if (typeof node === 'string') {
  } else if (typeof node === 'number') {
    total += node;
  } else { // array or object
    for (let key in node) {
      traverse(node[key]);
    }
  }
}

traverse(input);
console.log(total);
