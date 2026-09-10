const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    loadFriends();
    const signInForm = document.querySelector('.sign-in-form');

    if (signInForm) {
        signInForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const emailValue = document.getElementById('user-email').value;
            const passwordValue = document.getElementById('user-password').value;

            const userData = {
                email: emailValue,
                password: passwordValue
            };

            try {
                const response = await fetch(`${API_BASE_URL}/sign-in`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(userData)
                });

                const result = await response.json();

                if (response.ok) {
                    localStorage.setItem("sereniq_token", result.access_token);
                    alert("Successfully signed in as " + result.email + "!");
                    window.location.href = "sereniq_main1.html";
                } else {
                    alert("Login Failed: " + result.detail);
                }
            } catch (error) {
                alert("Could not connect to the server. Is Uvicorn running?");
            }
        });
    }

    const signUpForm = document.querySelector('.sign-up-form');

    if (signUpForm) {
        signUpForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const firstName = document.getElementById('user-first-name').value;
            const lastName = document.getElementById('user-last-name').value;
            const email = document.getElementById('user-email').value;
            const password = document.getElementById('password').value;
            const address = document.getElementById('user-address').value;
            const country = document.getElementById('user-country').value;
            const state = document.getElementById('user-state').value;
            const city = document.getElementById('user-city').value;
            const pincode = parseInt(document.getElementById('user-pincode').value, 10);

            const signUpData = {
                first_name: firstName,
                last_name: lastName,
                email: email,
                password: password,
                address: address,
                country: country,
                state: state,
                city: city,
                pincode: pincode
            };

            try {
                const response = await fetch(`${API_BASE_URL}/sign-up`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(signUpData)
                });

                const result = await response.json();

                if (response.ok) {
                    localStorage.setItem("sereniq_token", result.access_token);
                    alert("Account successfully created for " + result.email + "!");
                    window.location.href = "sereniq_main1.html";
                } else {
                    alert("Sign Up Failed: " + result.detail);
                }
            } catch (error) {
                alert("Could not connect to the server. Is Uvicorn running?");
            }
        });
    }


    const clockElement = document.querySelector(".live-clock");
    
    if (clockElement) {
        function updateClock() {
            const now = new Date();
            
            let hours = now.getHours();
            let minutes = now.getMinutes();
            let seconds = now.getSeconds();
    
            hours = hours < 10 ? "0" + hours : hours;
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            clockElement.innerText = `${hours}:${minutes}:${seconds}`;
        }

        updateClock();

        setInterval(updateClock, 1000);
    }
    
});

window.logoutUser = function() {
    localStorage.removeItem("sereniq_token");
    console.log("Token successfully cleared from local storage.");
};


document.addEventListener("DOMContentLoaded", () => {
    const searchTrigger = document.getElementById('search-trigger');
    const searchInput = document.getElementById('friend-search-input');
    const resultsPopup = document.getElementById('search-results-popup');

    if (searchTrigger) {
        searchTrigger.addEventListener('click', () => {
            searchInput.classList.toggle('active');
            if (searchInput.classList.contains('active')) {
                searchInput.focus();
            } else {
                resultsPopup.style.display = 'none';
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', async (e) => {
            const query = e.target.value;
            if (query.length < 2) {
                resultsPopup.style.display = 'none';
                return;
            }

            try {
                
                const response = await fetch(`${API_BASE_URL}/search-users?name=${query}`);
                const users = await response.json();

                resultsPopup.innerHTML = ''; 
                
                if (users.length > 0) {
                    resultsPopup.style.display = 'block';
                    
                    users.forEach(user => {
                        const li = document.createElement('li');
                        
                        
                        const infoGroup = document.createElement('div');
                        infoGroup.className = 'user-info-group';
                        
                        const nameSpan = document.createElement('span');
                        nameSpan.className = 'user-name-text';
                        nameSpan.innerText = `${user.first_name} ${user.last_name}`;
                        
                        const detailsSpan = document.createElement('span');
                        detailsSpan.className = 'user-details-text';
                        detailsSpan.innerText = `${user.state}, ${user.country} • ${user.email}`;
                        
                        infoGroup.appendChild(nameSpan);
                        infoGroup.appendChild(detailsSpan);
                        
                        const addBtn = document.createElement('button');
                        addBtn.innerText = '+ Add';
                        addBtn.className = 'popup-add-btn';
                        
                        addBtn.onclick = async (event) => {
                            event.stopPropagation(); 
                            
                            
                            const token = localStorage.getItem("sereniq_token");
                            
                            if (!token) {
                                alert("You must be logged in to add friends!");
                                return;
                            }

                            try {
                                const addResponse = await fetch(`${API_BASE_URL}/add-friend`, {
                                    method: 'POST',
                                    headers: { 
                                        'Content-Type': 'application/json',
                                        'Authorization': `Bearer ${token}` 
                                    },
                                    body: JSON.stringify({ friend_email: user.email })
                                });
                                
                                const result = await addResponse.json();
                                
                                if (addResponse.ok) {
                                    alert(result.message);
                                    addBtn.innerText = 'Added';
                                    addBtn.style.background = '#d7eedb';
                                    addBtn.style.color = '#4A5D4B';
                                    addBtn.disabled = true;
                                    if(typeof loadFriends === "function") loadFriends();
                                } else {
                                    alert("Could not add friend: " + result.detail); 
                                }
                                
                            } catch (error) {
                                console.error("Error adding friend:", error);
                            }
                        };

                        li.appendChild(infoGroup);
                        li.appendChild(addBtn);
                        
                        resultsPopup.appendChild(li);
                    });
                } else {
                    resultsPopup.style.display = 'none';
                }
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        });
    }
});


async function loadFriends() {
    const token = localStorage.getItem("sereniq_token");
    if (!token) return; 

    try {
        const response = await fetch(`${API_BASE_URL}/my-friends`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const friends = await response.json();
            const container = document.getElementById('dynamic-friends-container');
            container.innerHTML = ''; 

            friends.forEach(friend => {
                const cardHtml = `
                    <div class="friend-container">
                        <svg viewBox="0 0 120 120" class="profile-pic-svg">
                            <circle cx="60" cy="60" r="58" fill="#d7eedb"/>
                            <circle cx="60" cy="45" r="22" fill="#8fc9a2"/>
                            <path d="M18 108 Q60 68 102 108 L102 120 L18 120 Z" fill="#8fc9a2"/>
                        </svg>
                        
                        <p>${friend.first_name} ${friend.last_name}</p>
                        ${friend.is_online ? '<span class="online-dot"></span>' : ''}

                        <div class="friend-actions">
                            <svg viewBox="0 0 24 24" class="video-call-svg" xmlns="http://www.w3.org/2000/svg">
                                <rect x="2" y="6" width="14" height="12" rx="3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M16 10.5L22 7.5V16.5L16 13.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            <svg viewBox="0 0 24 24" class="send-message-svg" xmlns="http://www.w3.org/2000/svg">
                                <path d="M22 2L11 13M22 2L15 22L11 13L2 9L22 2Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', cardHtml);
            });
        }
    } catch (error) {
        console.error("Error loading friends:", error);
    }
}