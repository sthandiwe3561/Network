document.addEventListener("DOMContentLoaded", function () {
  //fetch the dropdown button and add event listener
  const dropdown = document.querySelectorAll(".options-btn");
  const dropMenu = document.querySelectorAll(".dropdown-menu");

  function dropDown(event) {
    // Get the corresponding dropdown menu for the clicked button
    const clickedMenu = event.target.nextElementSibling;
    const isAlreadyVisible = clickedMenu.style.display === "block";

    // Hide all dropdown menus
    dropMenu.forEach((menu) => {
      menu.style.display = "none";
    });

    // Show the clicked one only if it was not already visible
    if (!isAlreadyVisible) {
      clickedMenu.style.display = "block";
    }
  }

  //select all dropdown buttons
  dropdown.forEach((dropdowns) => {
    dropdowns.addEventListener("click", dropDown);
  });

  //getting post id so when user like it returns to the liked post
  const urlParams = new URLSearchParams(window.location.search);
  const postId = urlParams.get("post_id");

  if (postId) {
    const postElement = document.getElementById(`post-${postId}`);
    if (postElement) {
      postElement.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }
});
