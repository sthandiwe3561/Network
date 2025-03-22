//make sure the page is fully load before using any of the function
document.addEventListener("DOMContentLoaded", function () {
  //fecth form and allpost div
  const postForm = document.getElementById("form");
  const postList = document.getElementById("postList");

  // Detect which page the user is on
  const pageType = document.body.getAttribute("data-page");

  // Define API endpoints based on the page
  let apiURL = "/post/";
  if (pageType === "following") {
    apiURL = "/follow/following-posts/${currentUserId}/";
  } else if (pageType === "profile") {
    apiURL = `/post/${currentuserId}/`;
  }

  function attachDropdownEvents(postDiv) {
    const optionsButton = postDiv.querySelector(".options-btn");
    const dropdownMenu = postDiv.querySelector(".dropdown-menu");

    optionsButton.addEventListener("click", function (event) {
      event.stopPropagation(); // Prevent click from bubbling up
      closeAllDropdowns(); // Close other open dropdowns first
      dropdownMenu.classList.toggle("show"); // Toggle visibility
    });
  }

  // Function to close all open dropdowns
  function closeAllDropdowns() {
    document.querySelectorAll(".dropdown-menu").forEach((menu) => {
      menu.classList.remove("show");
    });
  }

  // Close dropdowns when clicking outside
  document.addEventListener("click", function () {
    closeAllDropdowns();
  });

  //getCSRFToken function for forms
  function getCSRFToken() {
    return (
      document.querySelector("[name=csrfmiddlewaretoken]").value ||
      document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1]
    );
  }

  // Function to fetch and display posts
  function loadPosts() {
    fetch(apiURL)
      .then((response) => response.json())
      .then((data) => {
        postList.innerHTML = ""; // Clear existing posts
        data.forEach((post) => {
          const postElement = createPostElement(post);
          postList.prepend(postElement);
        });
      })
      .catch((error) => console.error("Error loading posts:", error));
  }

  //displaying a post
  function createPostElement(post) {
    const postDiv = document.createElement("div");
    postDiv.classList.add("post");

    // Ensure post.user is defined before accessing profile
    const profileImageUrl = post.user
      ? post.user.profile.profile_picture
      : "/media/default.jpg";

    //post image
    const imageUrl = post.image ? post.image : `/media/default.jpg`;

    postDiv.innerHTML = `
               <div class="post-container">
            <div class="post-header">
              <div class="user-info">
                <img src="${profileImageUrl}" alt="Profile Picture" class="profile_img">
                <span class="user-name">${post.user.first_name} ${
      post.user.last_name
    }</span>
              </div>
              ${
                post.user.id != currentUserId
                  ? `<button class="follow-btn" data-user-id="${post.user.id}" onclick="followbutton('${currentUserId}', '${post.user.id}',this)">Checking...</button>`
                  : ""
              }
              <div class="post-options">
                <button class="options-btn">⋮</button>
                <div class="dropdown-menu hidden">
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
               <button class="like-btn"><span class="like-count">${
                 post.like_count
               }</span> likes
      </button>
              <span class="comment"><a href="#">Comments</a></span>
            </div>
          </div>`;

    attachDropdownEvents(postDiv); // Attach event to new post

    // Attach like button event listener
    postDiv.querySelector(".like-btn").addEventListener("click", function () {
      like(post.id, this);
    });

    return postDiv;
  }

  //craeting a post
  if (postForm) {
    postForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const content = document.getElementById("contant").value;
      const image = document.getElementById("image").files[0];

      const formData = new FormData();
      formData.append("content", content);
      if (image) formData.append("image", image);

      fetch("/post/", {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() }, // CSRF token required
        body: formData,
        credentials: "include",
      })
        .then((response) => response.json())
        .then((newPost) => {
          postList.prepend(createPostElement(newPost)); // Add new post to top
          postForm.reset(); // Clear form
        })
        .catch((error) => console.error("Error creating post:", error));
    });
  }

  //function for like
  function like(postId, button) {
    const method = button.classList.contains("liked") ? "DELETE" : "POST";

    fetch(`/post/${postId}/like/${currentUserId}/`, {
      // Ensure URL matches backend
      method: method,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.liked);

        // Update the like count displayed inside the button
        const likeCountSpan = button.querySelector(".like-count");
        if (data.liked) {
          button.classList.add("liked");
          likeCountSpan.textContent = data.like_count; // Update the like count
        } else {
          button.classList.remove("liked");
          likeCountSpan.textContent = data.like_count; // Update the like count
        }
      })
      .catch((error) => console.error("Error:", error));
  }
  loadPosts();
});
