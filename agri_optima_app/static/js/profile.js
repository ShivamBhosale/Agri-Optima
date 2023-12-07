document.addEventListener("DOMContentLoaded", function () {
  // Get all the profile-nav items
  const profileNavItems = document.querySelectorAll(".profile-nav");

  // Get all the content divs in main-content-sub
  const contentDivs = document.querySelectorAll("#main-content-sub > div");

  // Function to show the corresponding content div
  function showContent(target) {
      contentDivs.forEach((div) => {
          div.style.display = "none";
      });

      const correspondingDiv = document.getElementById(target);
      if (correspondingDiv) {
          correspondingDiv.style.display = "block";
      }

      // Reset the color of all profile-nav items to the normal color
      profileNavItems.forEach((navItem) => {
          navItem.style.color = "black"; // Set the normal color here
      });

      // Find the corresponding profile-nav item and change its color to white
      const correspondingNavItem = document.querySelector(`[data-target="${target}"]`);
      if (correspondingNavItem) {
          correspondingNavItem.style.color = "white";
      }
  }

  // Add click event listeners to the profile-nav items
  profileNavItems.forEach((item) => {
      item.addEventListener("click", () => {
          const target = item.getAttribute("data-target");
          showContent(target);

          // Store the active state in local storage
          localStorage.setItem("activeContent", target);
      });
  });

  // Check if there is an activeContent in local storage
  const activeContent = localStorage.getItem("activeContent");
  if (activeContent) {
      showContent(activeContent);
  }
});



// document.addEventListener("DOMContentLoaded", function () {
//     // Get all the profile-nav items
//     const profileNavItems = document.querySelectorAll(".profile-nav");
  
//     // Get all the content divs in main-content-sub
//     const contentDivs = document.querySelectorAll("#main-content-sub > div");
  
//     // Add click event listeners to the profile-nav items
//     profileNavItems.forEach((item, index) => {
//       item.addEventListener("click", () => {
//         // Hide all content divs
//         contentDivs.forEach((div) => {
//           div.style.display = "none";
//         });
  
//         // Show the corresponding content div based on the data-target attribute
//         const target = item.getAttribute("data-target");
//         const correspondingDiv = document.getElementById(target);
//         if (correspondingDiv) {
//           correspondingDiv.style.display = "block";
//         }
//         // Reset the color of all profile-nav items to the normal color
//         profileNavItems.forEach((navItem) => {
//           navItem.style.color = "black"; // Set the normal color here
//         });
  
//         // Change the color of the clicked profile-nav item to white
//         item.style.color = "white";
//       });
//     });
//   });



