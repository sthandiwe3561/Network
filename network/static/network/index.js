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
        postDiv.setAttribute("style", "border: 1px solid black:");
        // Set the image source
        const imageUrl = post.image ? post.image : "default-profile.png"; // Fallback image

        //posts layout
        postDiv.innerHTML = `<div><img
                src=""
                alt="Profile Picture"
                class="profile_img">
                </div>
                <span>${post.user.first_name}</span>
                <span>${post.user.last_name}</span>`;

        //append it on my html div forallpost
        document.getElementById("allpost").appendChild(postDiv);
      });
    })
    .catch((error) => {
      console.error("Error fetching posts:", error);
    });
}
