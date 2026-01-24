let isRunning = false;
let countdownInterval = null;
let currentSeconds = 0;
let totalInterval = 0;

const toggleBtn = document.getElementById('toggleBtn');
const keyInput = document.getElementById('keyParams');
const intervalInput = document.getElementById('intervalParams');
const statusIndicator = document.querySelector('.status-indicator');
const statusText = document.getElementById('statusText');
const timerContainer = document.getElementById('timerContainer');
const progressBar = document.getElementById('progressBar');
const countdownText = document.getElementById('countdownText');
const alwaysOnTop = document.getElementById('alwaysOnTop');
const pressCountEl = document.getElementById('pressCount');
const activeTimeEl = document.getElementById('activeTime');
const statsContainer = document.getElementById('statsContainer');
const closeBtn = document.getElementById('closeBtn');
const minBtn = document.getElementById('minBtn');

let pressCount = 0;
let sessionStartTime = 0;
let activeInterval = null;

let isRecording = false;

// Key mapping for pyautogui compatibility
const keyMap = {
    ' ': 'space',
    'Control': 'ctrl',
    'Alt': 'alt',
    'Shift': 'shift',
    'Escape': 'esc',
    'ArrowUp': 'up',
    'ArrowDown': 'down',
    'ArrowLeft': 'left',
    'ArrowRight': 'right',
    'Enter': 'enter',
    'Backspace': 'backspace',
    'Tab': 'tab',
    'Delete': 'delete',
    'Insert': 'insert',
    'Home': 'home',
    'End': 'end',
    'PageUp': 'pageup',
    'PageDown': 'pagedown',
    'CapsLock': 'capslock',
    'NumLock': 'numlock',
    'ScrollLock': 'scrolllock'
};

keyInput.addEventListener('focus', () => {
    if (isRunning) return;
    isRecording = true;
    keyInput.value = '';
    keyInput.placeholder = 'Press any key...';
    keyInput.classList.add('recording');
});

keyInput.addEventListener('blur', () => {
    isRecording = false;
    keyInput.placeholder = 'e.g. F1, space, w';
    keyInput.classList.remove('recording');
});

keyInput.addEventListener('keydown', (e) => {
    if (!isRecording) return;
    
    e.preventDefault();
    e.stopPropagation();

    let keyName = e.key;

    // Use mapping or clean up the key name
    if (keyMap[keyName]) {
        keyName = keyMap[keyName];
    } else {
        keyName = keyName.toLowerCase();
    }

    keyInput.value = keyName;
    keyInput.blur();
});

alwaysOnTop.addEventListener('change', (e) => {
    if (checkPywebview()) {
        window.pywebview.api.set_always_on_top(e.target.checked);
    }
});

// Check if pywebview is available
function checkPywebview() {
    if (window.pywebview) {
        return true;
    }
    console.warn("pywebview API not found. Running in browser mode?");
    return false;
}

// Load settings from backend on startup
window.addEventListener('pywebviewready', () => {
    // Make title bar draggable
    const titleBar = document.getElementById('titleBar');
    titleBar.classList.add('pywebview-drag-region');

    window.pywebview.api.get_settings().then(settings => {
        if (settings) {
            keyInput.value = settings.key || 'space';
            intervalInput.value = settings.interval || 5;
            alwaysOnTop.checked = settings.always_on_top || false;
            
            // Apply always on top immediately if saved
            if (settings.always_on_top) {
                window.pywebview.api.set_always_on_top(true);
            }
        }
    });
});

closeBtn.addEventListener('click', () => {
    if (checkPywebview()) window.pywebview.api.close_window();
});

minBtn.addEventListener('click', () => {
    if (checkPywebview()) window.pywebview.api.minimize_window();
});

toggleBtn.addEventListener('click', () => {
    if (isRunning) {
        stopBot();
    } else {
        startBot();
    }
});

function startBot() {
    const key = keyInput.value.trim();
    const interval = parseFloat(intervalInput.value);

    if (!key) {
        showError("Please enter a key!");
        return;
    }

    if (isNaN(interval) || interval <= 0) {
        showError("Please enter a valid interval!");
        return;
    }

    statusText.textContent = "Connecting...";
    
    if (checkPywebview()) {
        toggleBtn.blur(); // Remove focus so 'space' key doesn't click it again
        
        window.pywebview.api.start_bot(key, interval).then(response => {
            console.log("Backend response:", response);
            if (response.status === "success") {
                // Small delay to ensure the click event is fully processed
                setTimeout(() => updateUIState(true), 100);
            } else {
                showError("Backend error: " + response.message);
            }
        }).catch(err => {
            console.error("API Call failed:", err);
            showError("API Call failed. Check console.");
        });
    } else {
        console.log(`[MOCK] Start bot: Key=${key}, Interval=${interval}`);
        updateUIState(true);
    }
}

function stopBot() {
    if (checkPywebview()) {
        window.pywebview.api.stop_bot().then(response => {
            if (response.status === "success") {
                updateUIState(false);
            } else {
                showError("Backend error: " + response.message);
            }
        }).catch(err => {
            console.error("API Call failed:", err);
            showError("Stop call failed.");
        });
    } else {
        console.log("[MOCK] Stop bot");
        updateUIState(false);
    }
}

function showError(msg) {
    statusText.textContent = msg;
    statusText.style.color = "var(--error-color)";
    console.error(msg);
}

function updateUIState(running) {
    isRunning = running;
    if (running) {
        toggleBtn.textContent = "Stop Bot";
        toggleBtn.classList.remove('btn-start');
        toggleBtn.classList.add('btn-stop');
        
        statusIndicator.classList.add('active');
        statusText.textContent = "Working...";
        statusText.style.color = "var(--success-color)";
        
        keyInput.disabled = true;
        intervalInput.disabled = true;

        totalInterval = parseFloat(intervalInput.value);
        pressCount = 0;
        pressCountEl.textContent = "0";
        sessionStartTime = Date.now();
        statsContainer.style.display = 'flex';
        
        startCountdown();
        startActiveTimer();
    } else {
        toggleBtn.textContent = "Start Bot";
        toggleBtn.classList.remove('btn-stop');
        toggleBtn.classList.add('btn-start');
        
        statusIndicator.classList.remove('active');
        statusText.textContent = "Stopped";
        statusText.style.color = "var(--text-secondary)";
        
        keyInput.disabled = false;
        intervalInput.disabled = false;
        
        stopCountdown();
        stopActiveTimer();
    }
}

function startActiveTimer() {
    activeInterval = setInterval(() => {
        const seconds = Math.floor((Date.now() - sessionStartTime) / 1000);
        activeTimeEl.textContent = formatTime(seconds);
    }, 1000);
}

function stopActiveTimer() {
    if (activeInterval) {
        clearInterval(activeInterval);
        activeInterval = null;
    }
}

function startCountdown() {
    timerContainer.style.display = 'flex';
    currentSeconds = totalInterval;
    
    if (countdownInterval) clearInterval(countdownInterval);
    
    updateTimerUI();
    
    countdownInterval = setInterval(() => {
        currentSeconds -= 0.1;
        if (currentSeconds <= 0) {
            currentSeconds = totalInterval;
            triggerFlash();
        }
        updateTimerUI();
    }, 100);
}

function triggerFlash() {
    pressCount++;
    pressCountEl.textContent = pressCount;
    pressCountEl.classList.add('pulse-success');
    statusIndicator.classList.add('active'); // Re-trigger glow
    
    setTimeout(() => {
        pressCountEl.classList.remove('pulse-success');
    }, 500);
}

function stopCountdown() {
    timerContainer.style.display = 'none';
    if (countdownInterval) {
        clearInterval(countdownInterval);
        countdownInterval = null;
    }
}

function formatTime(totalSeconds) {
    if (totalSeconds < 60) {
        return totalSeconds.toFixed(1) + 's';
    }
    
    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = Math.floor(totalSeconds % 60);
    
    const parts = [];
    if (h > 0) parts.push(h + 'h');
    if (m > 0 || h > 0) parts.push(m + 'm');
    parts.push(s + 's');
    
    return parts.join(' ');
}

function updateTimerUI() {
    const percentage = ((totalInterval - currentSeconds) / totalInterval) * 100;
    progressBar.style.width = `${percentage}%`;
    countdownText.textContent = formatTime(currentSeconds);
}
