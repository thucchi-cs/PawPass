tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '#2563eb', // elegant blue
            accent: '#1e40af'
          }
        }
      }
    }

function flashMsg(msg) {
    let flash = document.querySelector("#flash-msg")
    flash.hidden = false;
    flash.querySelector("#msg").innerHTML = msg
}

document.querySelector(".btn-close").addEventListener("click", () => {
    document.querySelector("#flash-msg").hidden = true;
})

if ((window.location.pathname == "/create-pet") || ((window.location.pathname == "/edit-pet") && (window.location.search))){
    // Get form to check validation
    let addPet = document.querySelector("#addPet")
    addPet.querySelector("#btn").addEventListener("click", function() {
        // Get inputs
        let petName = addPet.querySelector("#id1").value;
        let petType = addPet.querySelector("#id2").value;
        let favoriteFood = addPet.querySelector("#id5").value;
        let OwnerName = addPet.querySelector("#id7").value;
        let OwnerContact = addPet.querySelector("#id8").value;
        let petAge = addPet.querySelector("#id4").value;
        let password = addPet.querySelector("#id11");
        password = password ? password.value : "password!";

        // Flash error if not all fields are filled out
        if (!petName || !petType || !favoriteFood || !OwnerName || !OwnerContact || !password) {
            flashMsg("All required fields must be filled out!");
            console.log(petName + petType + favoriteFood + OwnerName + OwnerContact + password)
            return;
        }
    
        // Flash error for invalid date
        const passwordRight = password.match(/[^a-zA-Z]/g) || [];
        console.log(passwordRight)
        if(password.length < 8 || passwordRight.length == 0){
            flashMsg("Your password does not meet the requirements. You must have a password 8 characters or longer, and it must have at least 1 number or 1 special character")
            return;
        }

        // Submit form if all inputs are valid
        addPet.submit()
})}