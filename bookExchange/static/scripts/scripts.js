document.addEventListener("DOMContentLoaded", () => {
	const circle = document.querySelector(".mouse-circle");
	const formElements = document.querySelectorAll(
		".form-container input, .form-container textarea, .form-container select, .form input, .login-form textarea, .login-form select, .custom-image-button "
	);

	document.addEventListener("mousemove", (e) => {
		const mouseX = e.clientX;
		const mouseY = e.clientY;

		circle.style.left = `${mouseX - circle.offsetWidth / 2}px`;
		circle.style.top = `${mouseY - circle.offsetHeight / 2}px`;
	});

	document.addEventListener("mousedown", () => {
		circle.style.backgroundColor = "rgb(101, 101, 247)";
	});

	document.addEventListener("mouseup", () => {
		circle.style.backgroundColor = "rgb(157, 217, 247)";
	});

	formElements.forEach((element) => {
		element.addEventListener("mouseenter", () => {
			circle.style.opacity = "0";
		});

		element.addEventListener("mouseleave", () => {
			circle.style.opacity = "1";
		});
	});

	const loader = document.querySelector(".container");
	const mainContent = document.getElementById("main-content");

	// Hide loader and show content when page is fully loaded
	window.addEventListener("load", () => {
		setTimeout(() => {
			loader.style.display = "none";
			mainContent.style.display = "block";
		}, 1800);
	});
});
