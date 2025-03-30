document.addEventListener("DOMContentLoaded", function () {
  //fetch the dropdown button and add event listener
  const dropdown = document.querySelectorAll(".options-btn");
  const dropMenu = document.querySelectorAll(".dropdown-menu");

  function dropDown(event) {
    dropMenu.forEach((dropMenus) => {
      dropMenus.style.display = "none";
    });
    // Get the corresponding dropdown menu for the clicked button
    const clickedMenu = event.target.nextElementSibling;

    // Toggle the visibility of the clicked menu
    if (clickedMenu.style.display === "block") {
      clickedMenu.style.display = "none"; // Hide if already visible
    } else {
      clickedMenu.style.display = "block"; // Show if hidden
    }
  }

  //select all dropdown buttons
  dropdown.forEach((dropdowns) => {
    dropdowns.addEventListener("click", dropDown);
  });
});
