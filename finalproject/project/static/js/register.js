var usernameField = document.querySelector('#usernameField');
var feedBackArea = document.querySelector('.invalid-feedback');
var emailField =document.querySelector('#emailField');
var emailInvalidarea = document.querySelector('.emailFeedBackArea');
var passwordInvalidarea = document.querySelector('.passwordInvalidarea');
var passwordField = document.querySelector('#passwordField');
var passwordField1 = document.querySelector('#passwordField1');
var showPasswordToggle = document.querySelector('.showPasswordToggle');
var confirmshowPasswordToggle = document.querySelector('.showPasswordToggles');
var submit_btn = document.querySelector('.submit-btn');


const ShowToogleInput = (e)=>{
    if(showPasswordToggle.textContent == 'SHOW'){
        showPasswordToggle.innerHTML ='HIDE';
        passwordField.setAttribute('type','text');
    }else{
        showPasswordToggle.innerHTML = "SHOW";
        passwordField.setAttribute('type','password');
    }
}
showPasswordToggle.addEventListener('click',ShowToogleInput);






const ShowTooglePassword = (e)=>{
    if(confirmshowPasswordToggle.textContent == 'SHOW'){
        confirmshowPasswordToggle.innerHTML ='HIDE';
        passwordField1.setAttribute('type','text');
    }else{
        confirmshowPasswordToggle.innerHTML = "SHOW";
        passwordField1.setAttribute('type','password');
    }
}


confirmshowPasswordToggle.addEventListener('click',ShowTooglePassword);



emailField.addEventListener('keyup',(e)=>{
    const emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    emailInvalidarea.style.display = "none";


    if (emailVal.length > 0){
        fetch('/authentication/validation-email/',{
            method: 'POST',
            body: JSON.stringify({'email': emailVal}),
        })
        .then((response) => response.json())
        .then((data) => {
            if(data.email_error){
                emailField.classList.add("is-invalid");
                emailInvalidarea.style.display = "block";
                emailInvalidarea.innerHTML = `<p>${data.email_error}</p>`;
                submit_btn.disabled = true ;
            }else{
                submit_btn.removeAttribute("disabled");
            }
        })
    }
})
usernameField.addEventListener('keyup', (e) =>{
    const usernameVal =e.target.value;

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";

    if (usernameVal.length > 0) {
        fetch("/authentication/validation-username/", {
          body: JSON.stringify({ username: usernameVal }),
          method: "POST",
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                submit_btn.disabled = true ;
            }else{
                submit_btn.removeAttribute('disabled');
            }
        });
    }
});


passwordField1.addEventListener('keyup', (e) =>{
    const passwordVal1 =e.target.value;
    const passwordVal = passwordField.value;

    passwordField1.classList.remove("is-invalid");
    passwordInvalidarea.style.display = "none";

    if (passwordVal1.length > 0) {
        fetch("/authentication/validation-password/", { 
          body: JSON.stringify({ password1: passwordVal1 , password : passwordVal}),
          method: "POST",
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.password_error) {
                passwordField1.classList.add("is-invalid");
                passwordInvalidarea.style.display = "block";
                passwordInvalidarea.innerHTML = `<p>${data.password_error}</p>`;
                submit_btn.disabled = true ;
            }else{
                submit_btn.removeAttribute('disabled');
            }
        });
    }
});
