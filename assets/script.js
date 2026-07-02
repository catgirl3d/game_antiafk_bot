let isRunning = false;
let countdownInterval = null;
let currentSeconds = 0;
let totalInterval = 0;
let countdownState = null;

const toggleBtn = document.getElementById('toggleBtn');
const keysInput = document.getElementById('keysInput');
const keyChips = document.getElementById('keyChips');
const keyTagsContainer = document.getElementById('keyTagsContainer');
const randomizeEnabled = document.getElementById('randomizeEnabled');
const intervalMin = document.getElementById('intervalMin');
const intervalMax = document.getElementById('intervalMax');
const pressDurationMin = document.getElementById('pressDurationMin');
const pressDurationMax = document.getElementById('pressDurationMax');
const cursorMovePixels = document.getElementById('cursorMovePixels');
const microMovements = document.getElementById('microMovements');
const randomClicks = document.getElementById('randomClicks');
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
const advancedBtn = document.getElementById('advancedBtn');
const advancedModal = document.getElementById('advancedModal');
const modalClose = document.getElementById('modalClose');
const modalCloseBtn = document.getElementById('modalCloseBtn');

let pressCount = 0;
let sessionStartTime = 0;
let activeInterval = null;
let isRecording = false;
let selectedKeys = new Set(); // Initialized from backend defaults

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

function parseCursorMovePixels() {
    const value = Number.parseInt(cursorMovePixels.value, 10);
    if (!Number.isFinite(value) || value <= 0) {
        return null;
    }
    return value;
}

function buildSettingsObject() {
    return {
        keys: Array.from(selectedKeys).join(','),
        interval_min: parseFloat(intervalMin.value),
        interval_max: parseFloat(intervalMax.value),
        randomize_enabled: randomizeEnabled.checked,
        press_duration_min: parseInt(pressDurationMin.value),
        press_duration_max: parseInt(pressDurationMax.value),
        micro_movements: microMovements.checked,
        random_clicks: randomClicks.checked,
        cursor_move_pixels: parseCursorMovePixels() ?? 15,
        always_on_top: alwaysOnTop.checked
    };
}

function saveAllSettings() {
    if (!checkPywebview()) return;
    window.pywebview.api.save_settings(buildSettingsObject());
}

function renderChips() {
    keyChips.innerHTML = '';
    selectedKeys.forEach(key => {
        const chip = document.createElement('div');
        chip.className = 'key-chip';
        chip.textContent = key;
        chip.onclick = () => {
            if (isRunning) return;
            selectedKeys.delete(key);
            renderChips();
            saveAllSettings();
        };
        keyChips.appendChild(chip);
    });
}

function addKey(key) {
    if (!key) return;
    selectedKeys.add(key);
    renderChips();
    saveAllSettings();
}

// Modal controls
advancedBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    advancedModal.classList.add('active');
});

modalClose.addEventListener('click', () => {
    advancedModal.classList.remove('active');
    saveAllSettings();
});

modalCloseBtn.addEventListener('click', () => {
    advancedModal.classList.remove('active');
    saveAllSettings();
});

// Close modal when clicking backdrop
advancedModal.addEventListener('click', (e) => {
    if (e.target === advancedModal) {
        advancedModal.classList.remove('active');
        saveAllSettings();
    }
});

keysInput.addEventListener('focus', () => {
    if (isRunning) return;
    isRecording = true;
    keysInput.classList.add('recording');
});

keysInput.addEventListener('blur', () => {
    isRecording = false;
    keysInput.classList.remove('recording');
});

keysInput.addEventListener('keydown', (e) => {
    if (!isRecording) return;
    
    e.preventDefault();
    e.stopPropagation();

    let keyName = e.key;

    // Use mapping for special keys
    if (keyMap[keyName]) {
        keyName = keyMap[keyName];
    } else {
        keyName = keyName.toLowerCase();
    }

    addKey(keyName);
    keysInput.value = ''; // Keep input empty so user can keep typing
});

randomizeEnabled.addEventListener('change', () => {
    saveAllSettings();
});

microMovements.addEventListener('change', () => {
    saveAllSettings();
});

randomClicks.addEventListener('change', () => {
    saveAllSettings();
});

alwaysOnTop.addEventListener('change', (e) => {
    if (checkPywebview()) {
        window.pywebview.api.set_always_on_top(e.target.checked);
        saveAllSettings();
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
    window.pywebview.api.get_settings().then(settings => {
        if (settings) {
            const savedKeys = settings.keys || 'space';
            selectedKeys = new Set(savedKeys.split(',').map(s => s.trim()).filter(s => s));
            renderChips();
            
            randomizeEnabled.checked = settings.randomize_enabled || false;
            intervalMin.value = settings.interval_min || 4.5;
            intervalMax.value = settings.interval_max || 7.0;
            pressDurationMin.value = settings.press_duration_min || 50;
            pressDurationMax.value = settings.press_duration_max || 150;
            cursorMovePixels.value = settings.cursor_move_pixels || 15;
            microMovements.checked = settings.micro_movements || false;
            randomClicks.checked = settings.random_clicks || false;
            alwaysOnTop.checked = settings.always_on_top || false;
            
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
    const keysArray = Array.from(selectedKeys);
    const minInterval = parseFloat(intervalMin.value);
    const maxInterval = parseFloat(intervalMax.value);

    if (keysArray.length === 0) {
        showError("Please add at least one key!");
        return;
    }

    if (isNaN(minInterval) || minInterval <= 0) {
        showError("Please enter a valid min interval!");
        return;
    }

    if (isNaN(maxInterval) || maxInterval <= 0) {
        showError("Please enter a valid max interval!");
        return;
    }

    if (minInterval > maxInterval) {
        showError("Min interval must be <= max interval!");
        return;
    }

    if (parseCursorMovePixels() === null) {
        showError("Please enter a valid cursor move range!");
        return;
    }

    // Collect all settings
    const settings = buildSettingsObject();

    statusText.textContent = "Connecting...";
    
    if (checkPywebview()) {
        toggleBtn.blur();
        window.pywebview.api.start_bot(settings).then(response => {
            if (response.status === "success") {
                setTimeout(() => updateUIState(true, minInterval, maxInterval), 100);
            } else {
                showError("Backend error: " + response.message);
            }
        }).catch(err => {
            console.error("API Call failed:", err);
            showError("API Call failed.");
        });
    } else {
        console.log(`[MOCK] Start bot with settings:`, settings);
        updateUIState(true, minInterval, maxInterval);
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

function updateUIState(running, minInterval = 5.0, maxInterval = 5.0) {
    isRunning = running;
    if (running) {
        toggleBtn.textContent = "Stop Bot";
        toggleBtn.classList.remove('btn-start');
        toggleBtn.classList.add('btn-stop');
        
        statusIndicator.classList.add('active');
        statusText.textContent = "Working...";
        statusText.style.color = "var(--success-color)";
        
        // Disable all inputs
        keyTagsContainer.classList.add('disabled');
        keysInput.disabled = true;
        randomizeEnabled.disabled = true;
        intervalMin.disabled = true;
        intervalMax.disabled = true;
        pressDurationMin.disabled = true;
        pressDurationMax.disabled = true;
        cursorMovePixels.disabled = true;
        microMovements.disabled = true;
        randomClicks.disabled = true;

        totalInterval = randomizeEnabled.checked ? (minInterval + maxInterval) / 2 : minInterval;
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
        
        // Enable all inputs
        keyTagsContainer.classList.remove('disabled');
        keysInput.disabled = false;
        randomizeEnabled.disabled = false;
        intervalMin.disabled = false;
        intervalMax.disabled = false;
        pressDurationMin.disabled = false;
        pressDurationMax.disabled = false;
        cursorMovePixels.disabled = false;
        microMovements.disabled = false;
        randomClicks.disabled = false;
        
        stopCountdown();
        stopActiveTimer();
    }
}

function startActiveTimer() {
    stopActiveTimer();

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
    countdownState = window.CountdownTimer.createCountdownState(totalInterval);
    
    if (countdownInterval) clearInterval(countdownInterval);
    
    syncCountdown();
    
    countdownInterval = setInterval(() => {
        syncCountdown();
    }, 100);
}

function syncCountdown() {
    if (!countdownState) {
        currentSeconds = 0;
        updateTimerUI();
        return;
    }

    const snapshot = window.CountdownTimer.advanceCountdown(countdownState);
    countdownState.nextTriggerAt = snapshot.nextTriggerAt;
    currentSeconds = snapshot.remainingSeconds;

    if (snapshot.completedCycles > 0) {
        triggerFlash(snapshot.completedCycles);
    }

    updateTimerUI();
}

function triggerFlash(increment = 1) {
    pressCount += increment;
    pressCountEl.textContent = pressCount;
    pressCountEl.classList.add('pulse-success');
    statusIndicator.classList.add('active');
    
    setTimeout(() => {
        pressCountEl.classList.remove('pulse-success');
    }, 500);
}

function stopCountdown() {
    timerContainer.style.display = 'none';
    countdownState = null;
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

// Resize Logic for Frameless Window
let isResizing = false;
let resizeType = ''; // 'r', 'b', or 'rb'
let startX, startY, startWidth, startHeight;

function initResizer(id, type) {
    const el = document.getElementById(id);
    if (!el) return;

    el.addEventListener('mousedown', (e) => {
        isResizing = true;
        resizeType = type;
        startX = e.screenX;
        startY = e.screenY;
        startWidth = window.innerWidth;
        startHeight = window.innerHeight;
        e.preventDefault();
        e.stopPropagation();
    });
}

initResizer('resizer-r', 'r');
initResizer('resizer-b', 'b');
initResizer('resizer-rb', 'rb');

window.addEventListener('mousemove', (e) => {
    if (!isResizing || !checkPywebview()) return;

    const diffX = e.screenX - startX;
    const diffY = e.screenY - startY;
    
    let newWidth = startWidth;
    let newHeight = startHeight;

    if (resizeType === 'r' || resizeType === 'rb') {
        newWidth = Math.max(300, startWidth + diffX);
    }
    if (resizeType === 'b' || resizeType === 'rb') {
        newHeight = Math.max(200, startHeight + diffY);
    }

    window.pywebview.api.resize_window(newWidth, newHeight);
});

window.addEventListener('mouseup', () => {
    isResizing = false;
});
