const circle = document.querySelector(".mouse-circle");

document.addEventListener("mousemove", (e) => {
	const mouseX = e.clientX;
	const mouseY = e.clientY;

	circle.style.left = `${mouseX - circle.offsetWidth / 2}px`;
	circle.style.top = `${mouseY - circle.offsetHeight / 2}px`;
});
