const test = require('node:test');
const assert = require('node:assert/strict');

const {
    createCountdownState,
    advanceCountdown
} = require('../assets/countdown.js');

test('createCountdownState stores interval and first deadline', () => {
    const state = createCountdownState(15, 1_000);

    assert.equal(state.intervalMs, 15_000);
    assert.equal(state.nextTriggerAt, 16_000);
});

test('advanceCountdown reports remaining time before deadline', () => {
    const state = createCountdownState(15, 1_000);
    const snapshot = advanceCountdown(state, 6_500);

    assert.equal(snapshot.completedCycles, 0);
    assert.equal(snapshot.nextTriggerAt, 16_000);
    assert.equal(snapshot.remainingSeconds, 9.5);
});

test('advanceCountdown keeps cadence when tick arrives late', () => {
    const state = createCountdownState(15, 1_000);
    const snapshot = advanceCountdown(state, 16_200);

    assert.equal(snapshot.completedCycles, 1);
    assert.equal(snapshot.nextTriggerAt, 31_000);
    assert.equal(snapshot.remainingSeconds, 14.8);
});

test('advanceCountdown counts multiple elapsed cycles', () => {
    const state = createCountdownState(5, 0);
    const snapshot = advanceCountdown(state, 12_500);

    assert.equal(snapshot.completedCycles, 2);
    assert.equal(snapshot.nextTriggerAt, 15_000);
    assert.equal(snapshot.remainingSeconds, 2.5);
});
