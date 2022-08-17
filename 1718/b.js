const fs = require('fs');


const waitingForReceive = {
  0: [],
  1: [],
};

const waitingForSend = {
  0: [],
  1: [],
}

let answer = 0;

async function main() {
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

  run(program, 0, 1);
  run(program, 1, 0);
}

async function run(program, programId, otherProgramId) {
  function get(valueOrRegister) {
    const x = valueOrRegister;
    if (+x === x) { // i.e. is a number
      return x;
    } else {
      return registers[x];
    }
  }

  let ip = 0;
  const registers = Object.fromEntries(
    Array.from('abcdefghijklmnopqrstuvwxyz')
      .map(letter => [letter, 0])
  );
  registers.p = programId;

  while (0 <= ip && ip < program.length) {
    const { command, x, y } = program[ip];
    if (command === 'snd') {
      if (programId === 1) {
        answer += 1;
        console.log(`Program 1 sent its ${answer}th value`);
      }
      send(otherProgramId, get(x));
    } else if (command === 'set') {
      registers[x] = get(y);
    } else if (command === 'add') {
      registers[x] += get(y);
    } else if (command === 'mul') {
      registers[x] *= get(y);
    } else if (command === 'mod') {
      registers[x] %= get(y);
    } else if (command === 'rcv') {
      registers[x] = await receive(programId);
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

// See send-and-receive.js to see that machinery in isolation
function receive(receiverName) {
  const items = waitingForReceive[receiverName];
  if (items.length) {
    const result = items.shift();
    return Promise.resolve(result);
  } else {
    const promise = myPromise();
    waitingForSend[receiverName].push(promise);
    return promise;
  }
}

function send(receiverName, value) {
  const promises = waitingForSend[receiverName];
  if (promises.length) {
    const promise = promises.shift();
    promise.resolve(value);
  } else {
    waitingForReceive[receiverName].push(value);
  }
}

// Just a Promise that exposes its resolve function as a method
function myPromise() {
  let resolve;
  const result = new Promise((_resolve) => {
    resolve = _resolve;
  });
  result.resolve = resolve;
  return result;
}

main();
