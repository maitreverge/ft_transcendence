// LOGIN LOGIC
function initPongAnimation(register) {
	// Clear any existing animation before reinitializing
	const container = document.getElementById('pong-background');
	if (!container) return; // Exit if container doesn't exist
	
	// Clear previous icons if any
	container.innerHTML = '';
	
	const cols = 12;
	const rows = 7;
	const spacingX = window.innerWidth / cols;
	const spacingY = window.innerHeight / rows;
	const speed = 0.5;
	
	const icons = [];
	
	for (let row = -1; row <= rows; row++) {
		for (let col = -1; col <= cols; col++) {
			const icon = document.createElement('div');
			icon.className = 'pong-icon';
			icon.style.left = `${col * spacingX}px`;
			icon.style.top = `${row * spacingY}px`;
			container.appendChild(icon);
			
			icons.push({
				el: icon,
				x: col * spacingX,
				y: row * spacingY,
			});
		}
	}
	
	function animate() {
		const w = window.innerWidth;
		const h = window.innerHeight;
		
		// !!!!!!!!!!!!!!!!! WORK NEEDLE !!!!!!!!!!!!!!!!!
		for (const icon of icons) {
			if (register == true){
				icon.x -= speed;
			}
			else{
				icon.x += speed;
			}
			icon.y += speed;
			
			if (register == true){
				if (icon.x < -50) icon.x += (cols + 2) * spacingX; // When too far left, jump to right
			}
			else{
				if (icon.x > w) icon.x -= (cols + 2) * spacingX;
			}
			if (icon.y > h) icon.y -= (rows + 2) * spacingY;

			icon.el.style.left = `${icon.x}px`;
			icon.el.style.top = `${icon.y}px`;
		}

		// Store animation ID so we can cancel it if needed
		window.pongAnimationId = requestAnimationFrame(animate);
	}

	// Cancel any existing animation before starting a new one
	if (window.pongAnimationId) {
		cancelAnimationFrame(window.pongAnimationId);
	}

	animate();
}
// ! NOPEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
// ! NOPEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
// ! NOPEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE




// // !2FA LOGIC 
// function initPongAnimation() {
// 	// Clear any existing animation before reinitializing
// 	const container = document.getElementById('pong-background');
// 	if (!container) return; // Exit if container doesn't exist

// 	// Clear previous icons if any
// 	container.innerHTML = '';

// 	const cols = 12;
// 	const rows = 7;
// 	const spacingX = window.innerWidth / cols;
// 	const spacingY = window.innerHeight / rows;
// 	const speed = 0.5;
	
// 	const icons = [];
	
// 	for (let row = -1; row <= rows; row++) {
// 		for (let col = -1; col <= cols; col++) {
// 			const icon = document.createElement('div');
// 			icon.className = 'pong-icon';
// 			icon.style.left = `${col * spacingX}px`;
// 			icon.style.top = `${row * spacingY}px`;
// 			container.appendChild(icon);

// 			icons.push({
// 				el: icon,
// 				x: col * spacingX,
// 				y: row * spacingY,
// 			});
// 		}
// 	}

// 	function animate() {
// 		const w = window.innerWidth;
// 		const h = window.innerHeight;

// 		for (const icon of icons) {
// 			icon.x += speed;
// 			icon.y += speed;

// 			if (icon.x > w) icon.x -= (cols + 2) * spacingX;
// 			if (icon.y > h) icon.y -= (rows + 2) * spacingY;
			
// 			icon.el.style.left = `${icon.x}px`;
// 			icon.el.style.top = `${icon.y}px`;
// 		}

// 		// Store animation ID so we can cancel it if needed
// 		window.pongAnimationId = requestAnimationFrame(animate);
// 	}

// 	// Cancel any existing animation before starting a new one
// 	if (window.pongAnimationId) {
// 		cancelAnimationFrame(window.pongAnimationId);
// 	}

// 	animate();
// }
// 	// !!!!!!!!!!!!! REGISTER LOGIC 
	
// 	function initPongAnimation() {
// 		// Clear any existing animation before reinitializing
// 		const container = document.getElementById('pong-background');
// 		if (!container) return; // Exit if container doesn't exist
	
// 		// Clear previous icons if any
// 		container.innerHTML = '';
	
// 		const cols = 12;
// 		const rows = 7;
// 		const spacingX = window.innerWidth / cols;
// 		const spacingY = window.innerHeight / rows;
// 		const speed = 0.5;
	
// 		const icons = [];
	
// 		for (let row = -1; row <= rows; row++) {
// 			for (let col = -1; col <= cols; col++) {
// 				const icon = document.createElement('div');
// 				icon.className = 'pong-icon';
// 				icon.style.left = `${col * spacingX}px`;
// 				icon.style.top = `${row * spacingY}px`;
// 				container.appendChild(icon);
	
// 				icons.push({
// 					el: icon,
// 					x: col * spacingX,
// 					y: row * spacingY,
// 				});
// 			}
// 		}
	
// 		function animate() {
// 			const w = window.innerWidth;
// 			const h = window.innerHeight;
		
// 			for (const icon of icons) {
				
// 				icon.x -= speed;
// 				icon.y += speed;
		
// 				// Update boundary logic to mirror login.html's approach but for opposite direction
// 				if (icon.x < -50) icon.x += (cols + 2) * spacingX; // When too far left, jump to right
// 				if (icon.y > h) icon.y -= (rows + 2) * spacingY; // When too far down, jump to top
		
// 				icon.el.style.left = `${icon.x}px`;
// 				icon.el.style.top = `${icon.y}px`;
// 			}
		
// 			// Store animation ID so we can cancel it if needed
// 			window.pongAnimationId = requestAnimationFrame(animate);
// 		}
	
// 		animate();
// 	}