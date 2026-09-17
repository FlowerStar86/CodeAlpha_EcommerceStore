document.addEventListener("DOMContentLoaded", function () {

    // =================================
    // REMOVE / QUANTITY CONFIRMATION
    // =================================

    const removeButtons =
        document.querySelectorAll(".remove-button");

    const quantityButtons =
        document.querySelectorAll(".quantity-button");

    const removeModal =
        document.getElementById("remove-modal");

    const cancelRemove =
        document.getElementById("cancel-remove");

    const confirmRemove =
        document.getElementById("confirm-remove");

    let removeLink = null;


    // =================================
    // REMOVE BUTTON
    // =================================

    removeButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            event.preventDefault();

            removeLink = button;

            if (removeModal) {
                removeModal.classList.add("show");
            }

        });

    });


    // =================================
    // CART QUANTITY BUTTONS
    // =================================

    quantityButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            const cartItem =
                button.closest(".cart-item");

            if (!cartItem) {
                return;
            }

            const quantityElement =
                cartItem.querySelector(".quantity-number");

            if (!quantityElement) {
                return;
            }

            const quantity =
                parseInt(quantityElement.textContent.trim());

            const isMinus =
                button.textContent.trim() === "−";


            // Quantity 1 + minus = remove item

            if (isMinus && quantity === 1) {

                event.preventDefault();

                removeLink =
                    cartItem.querySelector(".remove-button");

                if (removeModal) {
                    removeModal.classList.add("show");
                }

                return;
            }


            // Small button animation

            button.style.transform = "scale(0.85)";

            setTimeout(function () {

                button.style.transform = "";

            }, 120);

        });

    });


    // =================================
    // CANCEL REMOVE
    // =================================

    if (cancelRemove) {

        cancelRemove.addEventListener("click", function () {

            if (removeModal) {
                removeModal.classList.remove("show");
            }

            removeLink = null;

        });

    }


    // =================================
    // CONFIRM REMOVE
    // =================================

    if (confirmRemove) {

        confirmRemove.addEventListener("click", function () {

            if (removeLink) {
                window.location.href = removeLink.href;
            }

        });

    }


    // =================================
    // ADD TO CART FEEDBACK
    // =================================

    const addToCartLinks =
        document.querySelectorAll(".add-to-cart");

    addToCartLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            link.textContent = "Added to Cart!";

            link.style.pointerEvents = "none";

            setTimeout(function () {

                link.textContent = "Add to Cart";

                link.style.pointerEvents = "auto";

            }, 1500);

        });

    });


    // =================================
    // SEARCH
    // =================================

    const searchForm =
        document.querySelector('form[action="/products/"]');

    const searchInput =
        document.querySelector('input[name="search"]');

    if (searchForm && searchInput) {

        searchForm.addEventListener("submit", function () {

            if (searchInput.value.trim() === "") {

                searchInput.focus();

            }

        });

    }


    // =================================
    // BUTTON PRESS EFFECT
    // =================================

    const buttons =
        document.querySelectorAll("button");

    buttons.forEach(function (button) {

        button.addEventListener("click", function () {

            button.style.transform = "scale(0.97)";

            setTimeout(function () {

                button.style.transform = "";

            }, 100);

        });

    });


    // =================================
    // LOGIN PASSWORD SHOW / HIDE
    // =================================

    const passwordInput =
        document.getElementById("password");

    const passwordToggle =
        document.getElementById("password-toggle");

    if (passwordInput && passwordToggle) {

        passwordToggle.addEventListener("click", function () {

            if (passwordInput.type === "password") {

                passwordInput.type = "text";

                passwordToggle.textContent =
                    "Hide password";

            } else {

                passwordInput.type = "password";

                passwordToggle.textContent =
                    "Show password";

            }

        });

    }


    // =================================
    // REGISTER PASSWORD SHOW / HIDE
    // =================================

    const passwordToggles =
        document.querySelectorAll(".password-toggle");

    passwordToggles.forEach(function (toggle) {

        toggle.addEventListener("click", function () {

            const targetId =
                toggle.getAttribute("data-target");

            const passwordField =
                document.getElementById(targetId);

            if (!passwordField) {
                return;
            }

            if (passwordField.type === "password") {

                passwordField.type = "text";

                toggle.textContent =
                    "Hide password";

            } else {

                passwordField.type = "password";

                toggle.textContent =
                    "Show password";

            }

        });

    });


    // =================================
    // LIVE PASSWORD VALIDATION
    // =================================

    const registerPassword =
        document.getElementById("id_password");

    const registerConfirmPassword =
        document.getElementById("id_confirm_password");

    const passwordMessage =
        document.getElementById("password-message");

    const confirmPasswordMessage =
        document.getElementById("confirm-password-message");

    if (
        registerPassword &&
        registerConfirmPassword &&
        passwordMessage &&
        confirmPasswordMessage
    ) {

        registerPassword.addEventListener("input", function () {

            const password =
                registerPassword.value;

            if (password.length === 0) {

                passwordMessage.textContent = "";

            } else if (password.length < 8) {

                passwordMessage.textContent =
                    "Password should be at least 8 characters.";

            } else {

                passwordMessage.textContent =
                    "Password looks good!";

            }

            checkPasswords();

        });


        registerConfirmPassword.addEventListener(
            "input",
            function () {

                checkPasswords();

            }
        );


        function checkPasswords() {

            const password =
                registerPassword.value;

            const confirmPassword =
                registerConfirmPassword.value;

            if (confirmPassword.length === 0) {

                confirmPasswordMessage.textContent = "";

            } else if (password === confirmPassword) {

                confirmPasswordMessage.textContent =
                    "Passwords match!";

            } else {

                confirmPasswordMessage.textContent =
                    "Passwords do not match";

            }

        }

    }


    // =================================
    // PRODUCT DETAILS QUANTITY
    // =================================

    const productQuantity =
        document.getElementById("product-quantity");

    const productMinus =
        document.querySelector(".product-minus");

    const productPlus =
        document.querySelector(".product-plus");

    const addToCartButton =
        document.querySelector(".add-to-cart");

    if (
        productQuantity &&
        productMinus &&
        productPlus &&
        addToCartButton
    ) {

        let quantity = 1;


        // PLUS

        productPlus.addEventListener("click", function () {

            quantity++;

            productQuantity.textContent =
                quantity;

            addToCartButton.href =
                "/cart/add/" +
                addToCartButton.getAttribute("data-product-id") +
                "/?quantity=" +
                quantity;

        });


        // MINUS

        productMinus.addEventListener("click", function () {

            if (quantity > 1) {

                quantity--;

                productQuantity.textContent =
                    quantity;

                addToCartButton.href =
                    "/cart/add/" +
                    addToCartButton.getAttribute("data-product-id") +
                    "/?quantity=" +
                    quantity;

            }

        });

    }
   
});