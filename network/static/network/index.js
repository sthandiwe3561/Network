document.addEventListener("DOMContentLoaded", function () {
  allpost();
  const form = document.querySelector("#createpostform");
  if (form) {
    form.addEventListener("submit", handlesubmit);
  } else {
    console.log("Create post form not found!");
  }

  document.querySelector("#post").addEventListener("click", () => createpost());
});

function createpost() {
  //show cratepost and hide other views
  document.querySelector("#createpost").style.display = "block";
  document.querySelector("#allpost").style.display = "none";
  document.querySelector("#profile").style.display = "none";
  document.querySelector("#notifications").style.display = "none";
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

  fetch("/post/", {
    // ✅ Ensure the correct endpoint with a trailing slash
    method: "POST",
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
      console.log("helloit working");
      allpost(); // ✅ Ensure `allpost()` is defined and working
    })
    .catch((error) => {
      console.error("Error while creating post:", error);
    });
}

function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
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

function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

function allpost() {
  //show cratepost and hide other views
  document.querySelector("#createpost").style.display = "none";
  document.querySelector("#allpost").style.display = "block";
  document.querySelector("#profile").style.display = "none";
  document.querySelector("#notifications").style.display = "none";

  //fecth and display post
  fetch("/post/")
    .then((response) => response.json())
    .then((eachpost) => {
      //foreach post
      eachpost.forEach((post) => {
        console.log(post);
        //create a div for each post
        const postDiv = document.createElement("div");

        // Access profile picture correctly
        const profileImageUrl =
          post.user.profile?.profile_picture || "/media/default.jpg";

        const imageUrl = post.image ? post.image : `/media/default.jpg`;

        //posts layout
        postDiv.innerHTML = `
              <div class="post-container">
               <div class="post-header">
               <div class="user-info">
               <img
                src="${profileImageUrl}"
                alt="Profile Picture"
                class="profile_img">
                <span class="user-name">${post.user.first_name} ${post.user.last_name}</span>
                </div>
                <button class="follow-btn">Follow</button>
                    <div class="post-options">
                <button class="options-btn">⋮</button>
                <div class="dropdown-menu">
                 <ul>
                    <li><a href="#">Edit</a></li>
                   <li><a href="#">Delete</a></li>
                   <li><a href="#" onclick="hide(${post.id},true)">Hide</a></li>
                 </ul>
               </div>
              </div>
              </div>
                <div class="post-content">${post.content}</div>
                <div class="post-image"><img src="${imageUrl}" alt="Post Image"></div>
                <div class="post-action"><button class="like-btn">like</button>
                 <span class="comment"><a href="#">comments</a></span>
                 </div>`;

        //dropdown
        postDiv
          .querySelector(".options-btn")
          .addEventListener("click", (event) => {
            event.stopPropagation(); // Prevents the click from bubbling up
            let dropdown = postDiv.querySelector(".dropdown-menu");
            dropdown.style.display =
              dropdown.style.display === "block" ? "none" : "block";
          });

        // Close the dropdown when clicking anywhere else
        document.addEventListener("click", () => {
          document.querySelectorAll(".dropdown-menu").forEach((menu) => {
            menu.style.display = "none";
          });
        });

        //append it on my html div forallpost
        document.getElementById("allpost").appendChild(postDiv);
      });
    })
    .catch((error) => {
      console.error("Error fetching posts:", error);
    });
}
