(function (global, factory) {
    const exports = factory();

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = exports;
    }

    global.CountdownTimer = exports;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    function createCountdownState(totalIntervalSeconds, nowMs = Date.now()) {
        const intervalMs = Math.max(totalIntervalSeconds, 0) * 1000;

        return {
            intervalMs,
            nextTriggerAt: nowMs + intervalMs
        };
    }

    function advanceCountdown(state, nowMs = Date.now()) {
        if (!state || state.intervalMs <= 0) {
            return {
                nextTriggerAt: nowMs,
                remainingSeconds: 0,
                completedCycles: 0
            };
        }

        let nextTriggerAt = state.nextTriggerAt;
        let completedCycles = 0;

        while (nextTriggerAt <= nowMs) {
            nextTriggerAt += state.intervalMs;
            completedCycles += 1;
        }

        return {
            nextTriggerAt,
            remainingSeconds: (nextTriggerAt - nowMs) / 1000,
            completedCycles
        };
    }

    return {
        createCountdownState,
        advanceCountdown
    };
});
