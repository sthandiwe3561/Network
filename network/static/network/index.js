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
                </div>
                <div class="post-content">${post.content}</div>
                <div class="post-image"><img src="${imageUrl}" alt="Post Image"></div>
                <div class="post-action"><button class="like-btn">like</button>
                 <span class="comment"><a href="#">comments</a></span>
                 </div>
                 </div>`;

        //append it on my html div forallpost
        document.getElementById("allpost").appendChild(postDiv);
      });
    })
    .catch((error) => {
      console.error("Error fetching posts:", error);
    });
}
