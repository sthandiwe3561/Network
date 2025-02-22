document.addEventListener("DOMContentLoaded", function () {
  allpost();
  document.querySelector("#post").addEventListener("click", () => createpost());
});

function createpost() {
  //show cratepost and hide other views
  document.querySelector("#createpost").style.display = "block";
  document.querySelector("#allpost").style.display = "none";
  document.querySelector("#profile").style.display = "none";
  document.querySelector("#notifications").style.display = "none";
}

function allpost() {
  //show cratepost and hide other views
  document.querySelector("#createpost").style.display = "none";
  document.querySelector("#allpost").style.display = "block";
  document.querySelector("#profile").style.display = "none";
  document.querySelector("#notifications").style.display = "none";
}
