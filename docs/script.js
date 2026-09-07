document.addEventListener("DOMContentLoaded", () => {
    
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
                const response = await fetch('http://127.0.0.1:8000/sign-in', {
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
                const response = await fetch('http://127.0.0.1:8000/sign-up', {
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


    const clockElement = document.getElementById(".live-clock");
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