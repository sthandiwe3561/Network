document.addEventListener("DOMContentLoaded", function () {
  //csrf function for post methods
  function getCSRFToken() {
    return (
      document.querySelector("[name=csrfmiddlewaretoken]").value ||
      document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1]
    );
  }

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

  //fetching the follow_status from backend to change the inner text of te follow button
  document.querySelectorAll(".follow-btn").forEach((button) => {
    const userId = button.dataset.userId;

    console.log("User ID to follow:", userId); // test output

    // Example: Fetch follow
    fetch(`/follow/follow-status/${currentUserId}/${userId}/`)
      .then((res) => res.json())
      .then((data) => {
        if (data.follow_status) {
          button.innerText = "Unfollow";
        } else {
          button.innerText = "Follow";
        }
      });
  });

  //follow button
  const followButtons = document.querySelectorAll(".follow-btn");

  followButtons.forEach((button) => {
    button.addEventListener("click", () => followButton(button));
  });

  function followButton(button) {
    const userId = button.dataset.userId;

    if (button.innerText === "Follow") {
      // Send a request to follow the user
      fetch("/follow/", {
        method: "POST",
        credentials: "include", // Ensures cookies (like sessionid) are sent
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(), // Ensure CSRF token is included
        },
        body: JSON.stringify({
          follower: currentUserId,
          following: userId,
          follow_status: true,
        }),
      })
        .then(() => {
          // Change button text for all buttons related to this user
          followButtons.forEach((button) => {
            button.textContent = "Unfollow";
          });
        })
        .catch((error) => console.error("Error unfollowing user:", error));
    } else {
      // Send a request to unfollow the user
      fetch(`/follow/unfollow/${currentUserId}/${userId}/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(), // Ensure CSRF token is included
        },
      })
        .then(() => {
          // Change button text for all buttons related to this user
          followButtons.forEach((button) => {
            button.textContent = "Follow";
          });
        })
        .catch((error) => console.error("Error unfollowing user:", error));
    }
  }
});
