document.addEventListener("DOMContentLoaded", function () {
  allpost();
  const form = document.querySelector("#createpostform");
  if (form) {
    form.addEventListener("submit", handlesubmit);
  } else {
    console.log("Create post form not found!");
  }

  document.querySelector("#post").addEventListener("click", () => createpost());
  document
    .querySelector("#Following")
    .addEventListener("click", () => FollowPost());
});

function getCSRFToken() {
  return (
    document.querySelector("[name=csrfmiddlewaretoken]").value ||
    document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1]
  );
}

let editingPostId = null; // This will store the post ID when editing a post

function createpost(postId = null) {
  //show cratepost and hide other views
  document.querySelector("#createpost").style.display = "block";
  document.querySelector("#allpost").style.display = "none";
  document.querySelector("#profile").style.display = "none";
  document.querySelector("#following").style.display = "none";

  if (postId) {
    // If editing a post, set the editingPostId to the postId
    editingPostId = postId;

    // Fetch the post data to populate the form
    fetch(`/post/${postId}/`)
      .then((response) => response.json())
      .then((post) => {
        // Fill the form with the post data
        document.querySelector("#texterea").value = post.content;
        // For the image, you can add a preview (optional)
        document.querySelector("#image").value = ""; // Reset the file input
        // You can show the existing image if needed, or use a preview
        console.log(post); // For debugging
      })
      .catch((error) => {
        console.error("Error fetching post:", error);
      });
  } else {
    // Reset the form if creating a new post
    document.querySelector("#texterea").value = "";
    document.querySelector("#image").value = ""; // Reset the file input
    editingPostId = null; // Reset the editing post ID
  }
}

function handlesubmit(event) {
  event.preventDefault(); // Prevent page reload

  //getting data from the inputs
  const content = document.querySelector("#texterea").value;
  console.log(content);
  const image = document.querySelector("#image");
  const file = image.files[0];

  const formData = new FormData();
  formData.append("content", content);

  if (file) {
    formData.append("image", file); // Append the image if it exists
    console.log(" file selected");
  } else {
    console.log("No file selected");
  }

  // If editing a post, use PUT, otherwise use POST
  const method = editingPostId ? "PUT" : "POST"; // PUT for editing, POST for creating
  const url = editingPostId ? `/post/${editingPostId}/` : "/post/";

  fetch(url, {
    // ✅ Ensure the correct endpoint with a trailing slash
    method: method,
    headers: { "X-CSRFToken": getCSRFToken() }, // CSRF token required
    body: formData, // ✅ Don't set Content-Type manually, it's handled by FormData
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("HTTP error! Status: " + response.status);
      }
      return response.json();
    })
    .then((result) => {
      console.log(result);
      allpost(); // ✅ Ensure `allpost()` is defined and working
      editingPostId = null; // Reset editingPostId after successful submission
    })
    .catch((error) => {
      console.error("Error while creating post:", error);
    });
}

function Delete(postId) {
  fetch(`/post/${postId}/`, {
    method: "DELETE",
    headers: { "X-CSRFToken": getCSRFToken() },
  })
    .then((response) => {
      if (!response.ok) throw new Error("Failed to delete post");
      console.log("Post deleted successfully");
      allpost(); // Refresh post list
    })
    .catch((error) => console.error("Error:", error));
}

function hide(postid, isHide) {
  // this fetch is for updating
  fetch(`/post/${postid}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(), // Ensure CSRF token is included
    },
    body: JSON.stringify({
      hide: isHide,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(() => {
      console.log(`Post ${postid} is now ${isHide ? "hidden" : "visible"}`);
      allpost(); // Refresh posts
    })
    .catch((error) => {
      console.error("Error updating post:", error);
    });
}

//Follow button function
function followbutton(follower_id, following_id, button) {
  console.log(follower_id);
  console.log(following_id);

  // Get all follow buttons for the same user
  const followButtons = document.querySelectorAll(
    `.follow-btn[data-user-id='${following_id}']`
  );

  if (button.textContent === "Follow") {
    // Send a request to follow the user
    fetch("/follow/", {
      method: "POST",
      credentials: "include", // Ensures cookies (like sessionid) are sent
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(), // Ensure CSRF token is included
      },
      body: JSON.stringify({
        follower: follower_id,
        following: following_id,
        follow_status: true,
      }),
    })
      .then((response) => response.json())
      .then(() => {
        // Change button text for all buttons related to this user
        followButtons.forEach((button) => {
          button.textContent = "Unfollow";
          button.setAttribute(
            "onclick",
            `followbutton('${follower_id}', '${following_id}', this)`
          );
        });
        button.textContent = "Unfollow"; // Update button text
      })
      .catch((error) => console.error("Error following user:", error));
  } else {
    // Send a request to unfollow the user
    fetch(`/follow/unfollow/${follower_id}/${following_id}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(), // Ensure CSRF token is included
      },
      body: JSON.stringify({
        follower_status: false,
      }),
    })
      .then(() => {
        // Change button text for all buttons related to this user
        followButtons.forEach((button) => {
          button.textContent = "Follow";
          button.setAttribute(
            "onclick",
            `followbutton('${follower_id}', '${following_id}', this)`
          );
        });
        button.textContent = "Follow"; // Update button text
      })
      .catch((error) => console.error("Error unfollowing user:", error));
  }
}

function PostDisplay(
  filter = "",
  onlyFollowing = false,
  containerId = "allpost"
) {
  let url;

  if (onlyFollowing) {
    url = `/follow/following-posts/${currentUserId}/`; // Fetch only posts from followed users
  } else {
    url = filter ? `/post/${filter}` : "/post/";
  }

  fetch(url)
    .then((response) => response.json())
    .then((eachpost) => {
      // Ensure `eachpost` is always an array
      if (!Array.isArray(eachpost)) {
        eachpost = [eachpost]; // Convert single post into an array
      }

      const postContainer = document.getElementById(containerId);
      postContainer.innerHTML = ""; // Clear previous posts (optional)

      eachpost.forEach((post) => {
        console.log(post);
        console.log(eachpost);

        // Ensure the post.user is defined before accessing post.user.id
        if (post.user) {
          const userId = post.user.id; // Safe access to user.id
          console.log(userId); // Check if userId exists
        } else {
          console.log("User object is missing in post:", post);
        }

        const postDiv = document.createElement("div");

        //const profileImageUrl = post.user.profile?.profile_picture || "/media/default.jpg";

        // Ensure post.user is defined before accessing profile
        const profileImageUrl =
          post.user && post.user.profile
            ? post.user.profile.profile_picture
            : "/media/default.jpg";

        const firstName = post.user ? post.user.first_name : "Unknown";
        const lastName = post.user ? post.user.last_name : "User";

        const imageUrl = post.image ? post.image : `/media/default.jpg`;

        postDiv.innerHTML = `
          <div class="post-container">
            <div class="post-header">
              <div class="user-info">
                <img src="${profileImageUrl}" alt="Profile Picture" class="profile_img">
                <span class="user-name">${firstName} ${lastName}</span>
              </div>
              ${
                post.user.id != currentUserId
                  ? `<button class="follow-btn" data-user-id="${post.user.id}" onclick="followbutton('${currentUserId}', '${post.user.id}',this)">Checking...</button>`
                  : ""
              }
              <div class="post-options">
                <button class="options-btn">⋮</button>
                <div class="dropdown-menu">
                  <ul>
                    ${
                      post.user.id == currentUserId
                        ? `<li><a href="#" onclick="createpost(${post.id})">Edit</a></li>`
                        : ""
                    }
                    ${
                      post.user.id == currentUserId
                        ? `<li><a href="#" onclick="Delete(${post.id})">Delete</a></li>`
                        : ""
                    }
                    <li><a href="#" onclick="hide(${
                      post.id
                    }, true)">Hide</a></li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="post-content">${post.content}</div>
            <div class="post-image"><img src="${imageUrl}" alt="Post Image"></div>
            <div class="post-action">
              <button class="like-btn">Like</button>
              <span class="comment"><a href="#">Comments</a></span>
            </div>
          </div>`;

        postContainer.appendChild(postDiv);

        // Fetch follow status
        fetch(`/follow/follow-status/${currentUserId}/${post.user.id}/`)
          .then((response) => response.json())
          .then((statusData) => {
            const followButtons = document.querySelectorAll(
              `[data-user-id="${post.user.id}"]`
            );

            followButtons.forEach((button) => {
              button.textContent = statusData.follow_status
                ? "Unfollow"
                : "Follow";
            });
          })
          .catch((error) => {
            console.error("Error fetching follow status:", error);
          });

        // Dropdown Toggle (inside post)
        postDiv
          .querySelector(".options-btn")
          .addEventListener("click", (event) => {
            event.stopPropagation(); // Prevents event bubbling
            let dropdown = postDiv.querySelector(".dropdown-menu");
            dropdown.style.display =
              dropdown.style.display === "block" ? "none" : "block";
          });
      });
    })
    .catch((error) => {
      console.error("Error fetching posts:", error);
    });

  // Close dropdown when clicking outside (Added only once)
  document.addEventListener(
    "click",
    () => {
      document.querySelectorAll(".dropdown-menu").forEach((menu) => {
        menu.style.display = "none";
      });
    },
    { once: true }
  );
}

function allpost() {
  //show All post and hide other views
  document.querySelector("#createpost").style.display = "none";
  document.querySelector("#allpost").style.display = "block";
  document.querySelector("#profile").style.display = "none";
  document.querySelector("#following").style.display = "none";

  //call postdisplay
  PostDisplay("", false, "allpost");
}

function FollowPost() {
  //show following and hide other views
  document.querySelector("#createpost").style.display = "none";
  document.querySelector("#allpost").style.display = "none";
  document.querySelector("#profile").style.display = "none";
  document.querySelector("#following").style.display = "block";

  PostDisplay("", true, "following");

  console.log("following");
}
