document.addEventListener("DOMContentLoaded", () => {
	const circle = document.querySelector(".mouse-circle");
	const formElements = document.querySelectorAll(
		".form-container input, .form-container textarea, .form-container select"
	);

	document.addEventListener("mousemove", (e) => {
		const mouseX = e.clientX;
		const mouseY = e.clientY;

		circle.style.left = `${mouseX - circle.offsetWidth / 2}px`;
		circle.style.top = `${mouseY - circle.offsetHeight / 2}px`;
	});

	formElements.forEach((element) => {
		element.addEventListener("mouseenter", () => {
			circle.style.opacity = "0";
		});

		element.addEventListener("mouseleave", () => {
			circle.style.opacity = "1";
		});
	});
});
