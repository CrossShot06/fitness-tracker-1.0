document.addEventListener("DOMContentLoaded", function () {
    const gender = document.getElementById("id_gender");

    document.getElementById("id_role").disabled = true;
    
    if (gender) {
      const defaultOption = document.createElement("option");
      defaultOption.text = "Gender";
      defaultOption.disabled = true;
      defaultOption.selected = true;
      gender.insertBefore(defaultOption, gender.firstChild);
    }
  });