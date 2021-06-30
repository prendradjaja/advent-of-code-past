const input = require('./input').input;

let total = 0;

function traverse(node) {
  if (typeof node === 'string') {
  } else if (typeof node === 'number') {
    total += node;
  } else if (Array.isArray(node)) {
    for (let child of node) {
      traverse(child);
    }
  } else { // object
    let red = false;
    for (let key in node) {
      if (node[key] === 'red') {
        red = true;
        break;
      }
    }
    if (!red) {
      for (let key in node) {
        traverse(node[key]);
      }
    }
  }
}

traverse(input);
console.log(total);
