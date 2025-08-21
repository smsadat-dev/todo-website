const loginForm = document.querySelector("#userFormLogin form");
const regForm = document.querySelector('#userFormReg form');

const showReg = document.getElementById('showReg');
const showLogin = document.getElementById('showLogin');
const logout = document.getElementById('userlogout');

    /* INITIAL STATE */

    // show only login page initially
    document.getElementById("loginHeader").style.display = "block";
    document.getElementById("userFormLogin").style.display = "block";
    document.getElementById("registrationHeader").style.display = "none";
    document.getElementById("userFormReg").style.display = "none";
    logout.style.display = "none";


    // show registration hide login
    showReg.addEventListener('click', (e) => {

        document.getElementById("loginHeader").style.display = "none";
        document.getElementById("userFormLogin").style.display = "none";
        document.getElementById("registrationHeader").style.display = "block";
        document.getElementById("userFormReg").style.display = "block";
        logout.style.display = "none";
    });

    // show login hide registration
    showLogin.addEventListener('click', (e) => {

        document.getElementById("loginHeader").style.display = "block";
        document.getElementById("userFormLogin").style.display = "block";
        document.getElementById("registrationHeader").style.display = "none";
        document.getElementById("userFormReg").style.display = "none";
        logout.style.display = "none";
    });



loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const loginFormData = new FormData(loginForm);
    
    const loginResponse = await fetch("http://localhost:8000/api/login/", {
        method: 'POST',
        credentials: 'include', // very important for cookies across origins
        body: loginFormData,
    });

    const loginData = await loginResponse.json();

    if(loginData.status == 'success')
    {
        // store tokens for JWT logout
        localStorage.setItem("access", loginData.access);
        localStorage.setItem("refresh", loginData.refresh);

        // hide both login and registration interface
        document.getElementById("loginHeader").style.display = "none";
        document.getElementById("userFormLogin").style.display = "none";
        document.getElementById("registrationHeader").style.display = "none";
        document.getElementById("userFormReg").style.display = "none";

        // show logout option
        logout.style.display = "block";

        alert(`Welcome! ${loginData.username}`);
    }
    else 
    {
        alert(loginData.message);
    }
});


regForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const regFormData = new FormData(regForm);

    const regResponse = await fetch("http://localhost:8000/api/registration/", {
        method: 'POST',
        credentials: 'include', // very important for cookies across origins
        body: regFormData,
    });

    const regData = await regResponse.json();

    if(regData.status == 'success')
    {
        // back to login interface
        document.getElementById("loginHeader").style.display = "block";
        document.getElementById("userFormLogin").style.display = "block";
        document.getElementById("registrationHeader").style.display = "none";
        document.getElementById("userFormReg").style.display = "none";

        // show logout option
        logout.style.display = "none";

        alert(regData.message);
    }
    else 
    {
        alert(regData.message);
    }
});

logout.addEventListener('click', async (e) => {

    const refresh = localStorage.getItem("refresh"); 
    
    const logoutResponse = await fetch("http://localhost:8000/api/logout/", {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
    });

    const logoutData = await logoutResponse.json();

    if(logoutData.status == 'success')
    {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");

        // back to initial state
        document.getElementById("loginHeader").style.display = "block";
        document.getElementById("userFormLogin").style.display = "block";
        document.getElementById("registrationHeader").style.display = "none";
        document.getElementById("userFormReg").style.display = "none";
        logout.style.display = "none";

        alert(logoutData.message);
    }
    else 
    {
        alert(logoutData.message);
    }
});


