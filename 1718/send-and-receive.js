async function main() {

  // Example 1
  async function x() {
    const mySend = value => send('y', value);
    const myReceive = () => receive('x');
    mySend('Hello!');
  }
  async function y() {
    const mySend = value => send('x', value);
    const myReceive = () => receive('y');
    console.log(await myReceive());
  }
  x();
  y();
  // Output: Hello!

  // // Example 2 (comment out example 1 and uncomment me!)
  // async function x() {
  //   const mySend = value => send('y', value);
  //   const myReceive = () => receive('x');
  //   mySend('a');
  //   mySend('b');
  //   console.log(await myReceive());
  // }
  // async function y() {
  //   const mySend = value => send('x', value);
  //   const myReceive = () => receive('y');
  //   console.log(await myReceive());
  //   console.log(await myReceive());
  //   mySend('c');
  // }
  // x();
  // y();
  // // Output: a b c

  // // Example 3
  // async function x() {
  //   const mySend = value => send('y', value);
  //   const myReceive = () => receive('x');
  //   mySend('a');
  //   mySend('b');
  //   console.log(await myReceive());
  // }
  // async function y() {
  //   const mySend = value => send('x', value);
  //   const myReceive = () => receive('y');
  //   console.log(await myReceive());
  //   console.log(await myReceive());
  //   mySend('c');
  // }
  // y();
  // x(); // Order of x() and y() was reversed -- but messages still come through in the same order!
  // // Output: a b c

  // // Example 4: Just more messages in various combinations
  // async function x() {
  //   const mySend = value => send('y', value);
  //   const myReceive = () => receive('x');
  //   mySend('a');
  //   mySend('b');
  //   console.log(await myReceive());
  //   mySend('d');
  //   console.log(await myReceive());
  //   console.log(await myReceive());
  //   mySend('g');
  //   mySend('h');
  //   mySend('i');
  // }
  // async function y() {
  //   const mySend = value => send('x', value);
  //   const myReceive = () => receive('y');
  //   console.log(await myReceive());
  //   console.log(await myReceive());
  //   mySend('c');
  //   console.log(await myReceive());
  //   mySend('e');
  //   mySend('f');
  //   console.log(await myReceive());
  //   console.log(await myReceive());
  //   console.log(await myReceive());
  // }
  // y();
  // x();
  // // Output: a b c d e f g h i

  // // Example 5: Deadlock! Looks like Node is smart enough to notice and exit
  // async function x() {
  //   const mySend = value => send('y', value);
  //   const myReceive = () => receive('x');
  //   await myReceive();
  //   console.log('This message will not be printed');
  // }
  // async function y() {
  //   const mySend = value => send('x', value);
  //   const myReceive = () => receive('y');
  //   await myReceive();
  //   console.log('This message will not be printed');
  // }
  // y();
  // x();
  // // Output: [nothing]

}

const waitingForReceive = {
  x: [],
  y: [],
};

const waitingForSend = {
  x: [],
  y: [],
}

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

function myPromise() {
  let resolve;
  const result = new Promise((_resolve) => {
    resolve = _resolve;
  });
  result.resolve = resolve;
  return result;
}

main();
