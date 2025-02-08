document.addEventListener("DOMContentLoaded", () => {
	const circle = document.querySelector(".mouse-circle");
	const formElements = document.querySelectorAll(
		".form-container input, .form-container textarea, .form-container select, .login-form input, .login-form textarea, .login-form select"
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

//fetch books
async function fetchAllBooks() {
	let books = [];
	let startIndex = 0;
	const maxResults = 20;
	const totalLimit = 50;
	const query = "book OR novel OR literature OR fiction";
	const lang = "en";

	try {
		while (startIndex < totalLimit) {
			const apiUrl = `https://www.googleapis.com/books/v1/volumes?q=${query}&langRestrict=${lang}&startIndex=${startIndex}&maxResults=${maxResults}`;

			const response = await fetch(apiUrl);
			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}

			const data = await response.json();
			if (data.items) {
				books = books.concat(data.items);
			} else {
				break;
			}

			startIndex += maxResults;
		}

		console.log(`Fetched ${books.length} books`);
		console.log(books);
		return books;
	} catch (error) {
		console.error("Error fetching books:", error);
	}
}

fetchAllBooks();
