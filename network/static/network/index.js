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
