document.addEventListener("DOMContentLoaded", function () {
    const gender = document.getElementById("id_gender");

    document.getElementById("id_role").disabled = true;
    
    if (gender && !gender.value) {
        const defaultOption = document.createElement("option");
        defaultOption.text = "Select gender";
        defaultOption.value = "";  // Important: empty value
        defaultOption.disabled = true;
        defaultOption.selected = true;

        gender.insertBefore(defaultOption, gender.firstChild);
    }

  });