// Function to animate cards on load
function animateCards() {
    const cards = document.querySelectorAll('.moving-in');
    gsap.from(cards, {
        duration: 1,
        opacity: 0,
        y: 50,
        stagger: 0.3, // Stagger the animations for each card
        ease: 'power2.out',
    });
}

// Function to animate button on hover
function animateButton() {
    const buttons = document.querySelectorAll('.gradient-button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            gsap.to(button, {
                scale: 1.1,
                duration: 0.3,
                ease: 'power2.out',
            });
        });
        button.addEventListener('mouseleave', () => {
            gsap.to(button, {
                scale: 1,
                duration: 0.3,
                ease: 'power2.out',
            });
        });
    });
}

// Function to animate elements on scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('#page2 .elem1');

    const scrollAnimation = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                gsap.to(entry.target, {
                    opacity: 1,
                    y: 0,
                    duration: 1,
                    ease: 'power2.out',
                });
            } else {
                gsap.to(entry.target, {
                    opacity: 0,
                    y: 50,
                    duration: 1,
                    ease: 'power2.out',
                });
            }
        });
    };

    const observer = new IntersectionObserver(scrollAnimation, {
        threshold: 0.1, // Trigger animation when 10% of the element is visible
    });

    elements.forEach(element => {
        observer.observe(element);
        // Initially hide elements offscreen
        gsap.set(element, { opacity: 0, y: 50 });
    });
}

function startEmotionDetection() {
    console.log("Starting real-time facial emotion detection...");

    // Assuming you have access to a video element
    const videoElement = document.getElementById('video'); // Replace with your actual video element
    const constraints = { video: true }; // Constraints for the video stream

    navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
            videoElement.srcObject = stream; // Show the video stream
            // Implement your face detection logic here
        })
        .catch(error => {
            console.error("Error accessing the camera:", error);
            alert("Could not access the camera. Please check your device settings.");
        });
}


// Run animations after DOM content is loaded
document.addEventListener('DOMContentLoaded', () => {
    animateCards(); // Call to animate the cards when the page loads
    animateButton(); // Call to animate buttons
    animateOnScroll(); // Trigger animations when elements are in view

    // Live Detection Event Listener
    document.getElementById('liveButton').addEventListener('click', function() {
        fetch('/face_recognition', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: 'live' }),
        })
        .then(response => response.json())
        .then(data => {
            // Display live recognition result
            document.getElementById('liveResult').innerText = 
                data.error ? `Error: ${data.error}` : `Live Detection Result: ${JSON.stringify(data)}`;
        })
        .catch(error => console.error('Error:', error));
    });

    // Captured Expressions Event Listener (No image upload required)
    document.getElementById('captureButton').addEventListener('click', function() {
        fetch('/face_recognition', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: 'captured' }),
        })
        .then(response => response.json())
        .then(data => {
            // Display captured recognition result
            document.getElementById('captureResult').innerText = 
                data.error ? `Error: ${data.error}` : `Captured Expressions Result: ${JSON.stringify(data)}`;
        })
        .catch(error => console.error('Error:', error));
    });
});

function animateCards() {
    const cards = document.querySelectorAll('.face-models-content > div');
    cards.forEach(card => {
        card.style.transform = 'scale(1.05)';
        card.style.transition = 'transform 0.3s';
        card.addEventListener('mouseover', () => card.style.transform = 'scale(1.1)');
        card.addEventListener('mouseout', () => card.style.transform = 'scale(1.05)');
    });
}

function animateButton() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.style.transition = 'background-color 0.3s';
        button.addEventListener('mouseover', () => button.style.backgroundColor = '#45a049');
        button.addEventListener('mouseout', () => button.style.backgroundColor = '#4CAF50');
    });
}

function animateOnScroll() {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.face-models-content > div').forEach(div => observer.observe(div));
}

// Select the respective elements
const liveModel = document.querySelector('.live-model');
const capturedModel = document.querySelector('.captured-model');

// Function to create the sticky note effect on hover
function addStickyNoteEffect(card) {
    card.addEventListener('mouseenter', () => {
        gsap.to(card, {
            x: 10, // Move slightly to the right
            duration: 0.3,
            ease: "power1.inOut"
        });
    });

    card.addEventListener('mouseleave', () => {
        gsap.to(card, {
            x: 0, // Return to original position
            duration: 0.3,
            ease: "power1.inOut"
        });
    });
}

// Apply the sticky note effect to each card
addStickyNoteEffect(liveModel);
addStickyNoteEffect(capturedModel);
