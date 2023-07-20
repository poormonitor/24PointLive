function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateRandomNumbers() {
    const randomNumbers = [];
    const count = 4;
    for (let i = 0; i < count; i++) {
        randomNumbers.push(getRandomNumber(1, 13));
    }
    return randomNumbers;
}

export { generateRandomNumbers };
