
// Preloader js
function preloader() {
	'use strict';
	$('.preloader').delay(100).fadeOut(10);
}
$(preloader);

(function ($) {
	'use strict';
	// tab
	$('.tab-content').find('.tab-pane').each(function (idx, item) {
		var navTabs = $(this).closest('.code-tabs').find('.nav-tabs'),
			title = $(this).attr('title');
		navTabs.append('<li class="nav-item"><a class="nav-link" href="#">' + title + '</a></li>');
	});

	$('.code-tabs ul.nav-tabs').each(function () {
		$(this).find('li:first').addClass('active');
	});

	$('.code-tabs .tab-content').each(function () {
		$(this).find('div:first').addClass('active');
	});

	$('.nav-tabs a').click(function (e) {
		e.preventDefault();
		var tab = $(this).parent(),
			tabIndex = tab.index(),
			tabPanel = $(this).closest('.code-tabs'),
			tabPane = tabPanel.find('.tab-pane').eq(tabIndex);
		tabPanel.find('.active').removeClass('active');
		tab.addClass('active');
		tabPane.addClass('active');
	});

	// Accordions
	$('.collapse').on('shown.bs.collapse', function () {
		$(this).parent().find('.ti-plus').removeClass('ti-plus').addClass('ti-minus');
	}).on('hidden.bs.collapse', function () {
		$(this).parent().find('.ti-minus').removeClass('ti-minus').addClass('ti-plus');
	});


})(jQuery);


let lastScrollTop = 0;
const navbar = document.querySelector('.navigation');
const navbarHeight = navbar.offsetHeight;

window.addEventListener('scroll', function () {
	let currentScroll = window.scrollY || document.documentElement.scrollTop;

	if (currentScroll > lastScrollTop && currentScroll > navbarHeight) {
		// Scrolling down - hide navbar
		navbar.classList.remove('show');
		navbar.classList.add('hide');
	} else if (currentScroll < lastScrollTop) {
		// Scrolling up - show navbar
		navbar.classList.remove('hide');
		navbar.classList.add('show');
	}

	// Prevent negative values (useful if you are at the top of the page)
	lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});






//  pagination

// Function to handle page changes
let currentPage = 1;

// Total number of pages
const totalPages = 2;

// Get all page links and previous/next buttons
const pageLinks = document.querySelectorAll('.page-link');
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');

// Function to update the active page
function updatePagination() {
	// Remove the 'active' class from all pages
	pageLinks.forEach(link => link.parentElement.classList.remove('active'));

	// Add the 'active' class to the current page
	document.getElementById('page-' + currentPage).classList.add('active');

	// Enable/disable previous/next buttons based on the current page
	prevButton.classList.toggle('disabled', currentPage === 1);
	nextButton.classList.toggle('disabled', currentPage === totalPages);
}

// Event listeners for page links
document.getElementById('page-1').addEventListener('click', function (e) {
	e.preventDefault();
	currentPage = 1;
	updatePagination();
});

document.getElementById('page-2').addEventListener('click', function (e) {
	e.preventDefault();
	currentPage = 2;
	updatePagination();
});

// Event listeners for previous/next buttons
prevButton.addEventListener('click', function (e) {
	e.preventDefault();
	if (currentPage > 1) {
		currentPage--;
		updatePagination();
	}
});

nextButton.addEventListener('click', function (e) {
	e.preventDefault();
	if (currentPage < totalPages) {
		currentPage++;
		updatePagination();
	}
});

updatePagination();


// like dislike

document.querySelectorAll('.reaction-btn').forEach(function (button) {
	button.addEventListener('click', function () {
		const reactionType = this.dataset.reaction;

		fetch("{% url 'react_to_post' slug=post.slug reaction_type='REACT_TYPE' %}".replace('REACT_TYPE', reactionType), {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': '{{ csrf_token }}'
			},
		})
			.then(response => response.json())
			.then(data => {
				document.getElementById('like-count').textContent = data.like_count;
				document.getElementById('dislike-count').textContent = data.dislike_count;
				document.getElementById('love-count').textContent = data.love_count;

				document.querySelectorAll('.reaction-btn').forEach(btn => {
					btn.classList.remove('active');
				});
				if (reactionType === data.current_reaction) {
					document.getElementById(`${reactionType}-btn`).classList.add('active');
				}
			});
	});
});
