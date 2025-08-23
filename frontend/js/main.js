const loginForm = document.querySelector("#userFormLogin form");
const regForm = document.querySelector('#userFormReg form');

const userMgmtInterface = document.getElementById('userMgmt');
const showReg = document.getElementById('showReg');
const showLogin = document.getElementById('showLogin');
const logout = document.getElementById('userlogout');

const taskCotainer = document.getElementById('tasksbox');
const taskForm = document.querySelector('#tasksform form');

function fmtTime(timestamp) {
    // remove microseconds if present, because JS Date can't parse them reliably
    const cleanTs = timestamp.split('.')[0] + 'Z'; // ensures UTC format
    const d = new Date(cleanTs);

    // Format to "Aug 21 2025 11:58:19 PM"
    const options = {
        year: 'numeric',
        month: 'short',
        day: '2-digit',
        hour: 'numeric',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
    };

    return new Intl.DateTimeFormat('en-US', options).format(d);
}



    /* INITIAL STATE */

    // show only login page initially
    document.getElementById("loginHeader").style.display = "block";
    document.getElementById("userFormLogin").style.display = "block";
    document.getElementById("registrationHeader").style.display = "none";
    document.getElementById("userFormReg").style.display = "none";
    taskCotainer.style.display = "none";


    // show registration hide login
    showReg.addEventListener('click', (e) => {

        document.getElementById("loginHeader").style.display = "none";
        document.getElementById("userFormLogin").style.display = "none";
        document.getElementById("registrationHeader").style.display = "block";
        document.getElementById("userFormReg").style.display = "block";
        logout.style.display = "none";
        taskCotainer.style.display = "none";
    });

    // show login hide registration
    showLogin.addEventListener('click', (e) => {

        document.getElementById("loginHeader").style.display = "block";
        document.getElementById("userFormLogin").style.display = "block";
        document.getElementById("registrationHeader").style.display = "none";
        document.getElementById("userFormReg").style.display = "none";
        logout.style.display = "none";
        taskCotainer.style.display = "none";
    });



// login interface
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
        userMgmtInterface.style.display = 'none';

        // show logout option
        // logout.style.display = "block";
        taskCotainer.style.display = "block";
        loadTasksList(); // load user's task list

        alert(`Welcome! ${loginData.username}`);
    }
    else 
    {
        alert(loginData.message);
    }
});

// registration interface
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
        // logout.style.display = "none";
        taskCotainer.style.display = "none";

        alert(regData.message);
    }
    else 
    {
        alert(regData.message);
    }
});

// logout button interaction
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
        userMgmtInterface.style.display = "block";
        document.getElementById("loginHeader").style.display = "block";
        document.getElementById("userFormLogin").style.display = "block";
        document.getElementById("registrationHeader").style.display = "none";
        document.getElementById("userFormReg").style.display = "none";
        // logout.style.display = "none";
        taskCotainer.style.display = "none";
    }
    else 
    {
        alert(logoutData.message);
    }
});

// task creation interface
taskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    // values from form
    const taskTitle = document.getElementById('id_tasksTitle').value;
    const taskDesc = document.getElementById('id_tasksDescrp').value;

    // JWT from localstorage (login)
    const accessToken = localStorage.getItem('access');

    const taskResponse = await fetch("http://localhost:8000/api/tasks/", {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Authorization': `Bearer ${accessToken}`, // attach JWT for auth
        },
        body: JSON.stringify({
            tasksTitle: taskTitle,
            tasksDescrp: taskDesc
        })
    });

    const taskResponseData = await taskResponse.json();

    if(taskResponseData.status == 'success')
    {
        const task = taskResponseData.task;
        // Optionally, clear form
        taskForm.reset();

        // Dynamically add task to the list on page
        const taskList = document.getElementById('tasklist');
        const li = document.createElement("li");
        li.innerHTML = 
                    `<p>
                        <span class="taskTitle"><strong>${task.taskTitle}</strong></span>
                        <span class="taskCreationTime">${fmtTime(task.creationTime)}</span>
                        <input type="checkbox" class="taskDoneChckBox" ${task.isDone ? "checked" : ""} />
                        <button class="deleteTaskBtn" data-id="${task.taskID}">Delete</button>
                    </p>`;
        taskList.appendChild(li);
    }
    else 
    {
        alert(taskResponseData.message || 'Failed to create task');
    }
});

// task deletion interface

function checkNoTasks() {
    const taskList = document.getElementById('tasklist');
    const noTaskMsg = document.getElementById('noTasktoView');
    if (taskList.children.length === 0) {
        noTaskMsg.style.display = 'block';
    } else {
        noTaskMsg.style.display = 'none';
    }
}

document.getElementById('tasklist').addEventListener('click', async (e) => {
    if (e.target.classList.contains('deleteTaskBtn')) {
        const taskId = e.target.dataset.id;
        const accessToken = localStorage.getItem('access');

        const response = await fetch('http://localhost:8000/api/tasks/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ task_id: taskId })
        });

        const data = await response.json();

        if (data.status === 'success') {
            // Remove the task from DOM
            e.target.closest('li').remove();
            checkNoTasks(); // update "no tasks" message
        } else {
            alert(data.message || 'Failed to delete task');
        }
    }
});

// task update interface
document.addEventListener('change', async (e) => {
    if(e.target.classList.contains('taskDoneChckBox'))
    {
        const checkbox = e.target;
        const li = checkbox.closest('li');
        const isDone = checkbox.checked;

        // Toggle CSS class for strikethrough
        const titleSpan = li.querySelector('.taskTitle');
        if (isDone) 
        {
            titleSpan.classList.add('completedTask');
        } 
        else 
        {
            titleSpan.classList.remove('completedTask');
        }
    }
});


// task show interface 
async function loadTasksList() 
{
    const accessToken = localStorage.getItem('access');
    const taskList = document.getElementById('tasklist');
    // taskList.innerHTML = ""; // clear existing list

    try 
    {
        const response = await fetch("http://localhost:8000/api/tasks/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`
            }
        });   

        const data = await response.json();

        if(data.status == 'success')
        {
            if(data.tasks.length == 0)
            {
                taskList.innerHTML = "<p id='noTasktoView'>No tasks to do</p>";
            }
            else 
            {
                data.tasks.forEach(task => {
                    const li = document.createElement("li");
                    li.innerHTML = 
                    `<p>
                        <span class="taskTitle"><strong>${task.title}</strong></span>
                        <span class="taskCreationTime">${fmtTime(task.creationTime)}</span>
                        <input type="checkbox" class="taskDoneChckBox" ${task.completed ? "checked" : ""} />
                        <button class="deleteTaskBtn" data-id="${task.id}">Delete</button>
                    </p>`;
                    taskList.appendChild(li);

                    li.addEventListener('click', (e) => {
                        if (e.target.classList.contains("taskDoneChckBox") || e.target.classList.contains("deleteTaskBtn")) 
                        {
                            return; // don’t trigger popup on checkbox or delete
                        }

                        // Fill popup with task data
                        document.getElementById("popupTitle").innerText = task.title;
                        document.getElementById("popupCreationTime").innerText = fmtTime(task.creationTime);
                        document.getElementById("popupDetail").value = task.taskDesc || "No details provided";

                        // Show popup
                        document.getElementById("taskPopup").classList.remove("hidden");
                    });
                    // Close button handler
                    document.getElementById("popupCloseBtn").addEventListener("click", () => {
                        document.getElementById("taskPopup").classList.add("hidden");
                    });
                });
            }
        }
        else
        {
            alert(data.message || "Failed to load tasks");
        }
    } 
    catch (error) 
    {
        console.error("Error loading tasks: ", error);
        alert("Something went wrong while fetching tasks");   
    }
}

// Select all buttons with class 'googleRegBtn'
const googleButtons = document.querySelectorAll('.googleRegBtn');

googleButtons.forEach(button => {
  button.addEventListener('click', async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/auth/google/login/');
      const data = await res.json();
      window.location.href = data.auth_url;  // SPA redirect to Google
    } catch (err) {
      console.error('Google login failed:', err);
    }
  });
});
