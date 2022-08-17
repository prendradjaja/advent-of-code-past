const fs = require('fs');

function main() {
  function get(valueOrRegister) {
    const x = valueOrRegister;
    if (+x === x) { // i.e. is a number
      return x;
    } else {
      return registers[x];
    }
  }

  // Parse input file
  const program =
    fs.readFileSync('in', 'utf-8')
      .trim()
      .split('\n')
      .map(line => // e.g. "set i 31"
        line
          .split(' ')
          .map(word => // e.g. "set" or "i" or "31" (string)
            Number.isNaN(+word)
            ? word
            : +word
          )
      )
      .map(([command, x, y]) => // e.g. ["set", "i", 31]
        ({command, x, y}) // e.g. {command: "set", x: "i", y: 31}
      );

  // Run program
  let ip = 0;
  const registers = Object.fromEntries(
    Array.from('abcdefghijklmnopqrstuvwxyz')
      .map(letter => [letter, 0])
  );
  let lastSound;
  while (0 <= ip && ip < program.length) {
    const { command, x, y } = program[ip];
    if (command === 'snd') {
      lastSound = get(x);
    } else if (command === 'set') {
      registers[x] = get(y);
    } else if (command === 'add') {
      registers[x] += get(y);
    } else if (command === 'mul') {
      registers[x] *= get(y);
    } else if (command === 'mod') {
      registers[x] %= get(y);
    } else if (command === 'rcv') {
      if (get(x) !== 0) {
        console.log(lastSound);
        break;
      }
    } else if (command === 'jgz') {
      if (get(x) > 0) {
        ip += get(y);
        continue;
      }
    } else {
      throw new Error('Invalid command');
    }
    ip += 1;
  }
}

main();
