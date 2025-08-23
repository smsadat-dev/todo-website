const notifBox = document.getElementById('customNotif');
const notifMsg = document.getElementById('notification');
const okbtn = document.getElementById('OKbtn');

let notifTimeout;

function showNotif(message, duration = 3000)
{
    notifMsg.textContent = message;
    notifBox.classList.remove('hidden');
    notifBox.classList.add('show');

    clearTimeout(notifTimeout);
    notifTimeout = setTimeout(() => {
        hideNotif();
    }, duration);
}

function hideNotif()
{
    notifBox.classList.remove('show');
    notifBox.classList.remove('hidden');
}


// Dismiss immediately if OK is clicked
okbtn.addEventListener("click", hideNotif);
