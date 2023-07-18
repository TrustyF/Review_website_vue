export const eventThrottle = function (callback, interval) {
    let enableCall = true;

    return function (...args) {
        if (!enableCall) return;

        enableCall = false;
        callback.apply(args);
        setTimeout(() => enableCall = true, interval);
    }
}