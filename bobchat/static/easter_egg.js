document.addEventListener('DOMContentLoaded', () => {
    const konamiCode = [
        'arrowup', 'arrowup', 'arrowdown', 'arrowdown',
        'arrowleft', 'arrowright', 'arrowleft', 'arrowright',
        'b', 'a'
    ];
    let cursor = 0;

    document.addEventListener('keydown', (e) => {
        const key = e.key.toLowerCase();

        if (key === konamiCode[cursor]) {
             cursor++;
             if (cursor === konamiCode.length) {
                 toggleDarkMode();
                 cursor = 0;
             }
        } else {
             cursor = 0;
             // If the mismatch key is actually the start of the sequence, start tracking
             if (key === konamiCode[0]) {
                 cursor = 1;
             }
        }
    });

    function toggleDarkMode() {
        document.documentElement.classList.toggle('dark-mode');
        const isDark = document.documentElement.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
    }

    // Check initial state
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.documentElement.classList.add('dark-mode');
    }
});
