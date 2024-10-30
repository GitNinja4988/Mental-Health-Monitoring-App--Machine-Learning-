document.addEventListener('DOMContentLoaded', function () {
    const predictionForm = document.getElementById("prediction-form");
    const loadingMessage = document.getElementById("loading");
    const predictionResult = document.getElementById("prediction-result");
    const sentimentOutput = document.getElementById("sentiment-output");
    const activityOutput = document.getElementById("activity-output");
    const emojiOutput = document.getElementById("emoji-output");
    const analyzingMessage = document.getElementById("analyzing"); // Element to display analyzing message

    predictionForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent page reload
        showLoading(); // Show loading message and hide form

        // Get the input value
        const inputField = this.input_field.value;

        // Show analyzing message
        analyzingMessage.style.display = 'block'; // Show analyzing text
        gsap.from(analyzingMessage, { opacity: 0, y: -20, duration: 0.5 }); // Fade in analyzing message

        // Send AJAX request
        fetch('/mental_health', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input_field: inputField }) // Send input data
        })
        .then(response => response.json()) // Expect JSON response
        .then(data => {
            // Hide loading message and analyzing message
            loadingMessage.style.display = 'none';
            analyzingMessage.style.display = 'none'; // Hide analyzing message

            // Check if sentiment data is returned
            if (data && data.sentiment) {
                sentimentOutput.innerText = data.sentiment;
                activityOutput.innerText = data.activity;
                predictionResult.style.display = 'block'; // Show prediction result

                // Animate based on sentiment
                if (data.sentiment.includes("Positive")) {
                    // Fireworks effect for positive sentiment
                    showFireworks();
                    fallEmojis('happy'); // Trigger happy emoji fall
                } else if (data.sentiment.includes("Negative")) {
                    // Cheer up effect for negative sentiment
                    cheerUpEffect();
                    fallEmojis('sad'); // Trigger sad emoji fall
                }

                // Animate the output display
                animateOutputDisplay();

                // Reset for next input after 10 seconds
                setTimeout(() => {
                    predictionResult.style.display = 'none'; // Hide prediction result
                    predictionForm.reset(); // Reset the form
                    showInputForm(); // Show the input form after a 10-second gap
                }, 10000); // 10 seconds
            } else {
                console.error('No sentiment returned from the server.');
                loadingMessage.innerText = "Error analyzing input. Please try again."; // Display error
            }
        })
        .catch(error => {
            console.error('Error:', error);
            loadingMessage.style.display = 'none'; // Hide loading message on error
        });
    });

    // Function to show loading message
    function showLoading() {
        loadingMessage.style.display = 'block';
        loadingMessage.style.opacity = 0;
        gsap.to(loadingMessage, { opacity: 1, duration: 0.5 }); // Fade in effect
        predictionResult.style.display = 'none'; // Hide prediction result
        predictionForm.style.display = 'none'; // Hide the input form
    }

    // Fireworks effect function
    function showFireworks() {
        // Example of using a fireworks library
        const fireworks = new Fireworks({
            selector: '#fireworks', // Make sure to have an element with this ID in your HTML
        });
        fireworks.start();
        emojiOutput.innerHTML = '🎉🎉🎉'; // Example positive emojis
    }

    // Cheer up effect function
    function cheerUpEffect() {
        emojiOutput.innerHTML = '😊😊😊'; // Cheerful emojis
        gsap.from(predictionResult, {
            scale: 0.5,
            duration: 0.5,
            ease: "elastic.out(1, 0.3)",
            onComplete: () => {
                gsap.to(predictionResult, {
                    x: 10,
                    duration: 0.1,
                    yoyo: true,
                    repeat: 5
                });
            }
        });
    }

    // Function to animate the output display
    function animateOutputDisplay() {
        // Animate sentiment output
        gsap.from(sentimentOutput, {
            opacity: 0,
            y: -20,
            duration: 0.5,
            ease: "power2.out",
        });
        // Animate activity output
        gsap.from(activityOutput, {
            opacity: 0,
            y: -20,
            duration: 0.5,
            ease: "power2.out",
            delay: 0.2 // Delay to show activity output after sentiment output
        });
        // Animate emoji output
        gsap.from(emojiOutput, {
            opacity: 0,
            scale: 0.5,
            duration: 0.5,
            ease: "back.out(1.7)",
            delay: 0.4 // Delay to show emojis after the other outputs
        });
    }

    // Function to show the input form after a delay
    function showInputForm() {
        predictionForm.style.display = 'block'; // Show the input form
        gsap.from(predictionForm, {
            opacity: 0,
            y: -20,
            duration: 0.5,
            ease: "power2.out",
        });
        document.getElementsByName('input_field')[0].focus(); // Focus on input field
    }

    // Function to make emojis fall
    function fallEmojis(type) {
        const emoji = type === 'happy' ? '🎉' : '😞'; // Choose emoji based on sentiment
        const emojiCount = 10; // Number of emojis to fall
        for (let i = 0; i < emojiCount; i++) {
            const fallingEmoji = document.createElement('div');
            fallingEmoji.innerText = emoji;
            fallingEmoji.className = 'falling-emoji'; // Add class for styling
            document.body.appendChild(fallingEmoji); // Append emoji to the body

            // Set a random position for the emoji
            fallingEmoji.style.left = Math.random() * window.innerWidth + 'px';
            fallingEmoji.style.opacity = 1;

            // Animate the emoji falling
            gsap.to(fallingEmoji, {
                y: window.innerHeight,
                duration: 2 + Math.random() * 3, // Random duration for falling
                ease: "linear",
                onComplete: () => {
                    fallingEmoji.remove(); // Remove emoji after falling
                }
            });
        }
    }
});
