const API_BASE = window.location.port === '5004' ? '' : 'http://127.0.0.1:5004';

let currentUser = null;
let cart = {};

document.addEventListener('DOMContentLoaded', function () {
    showSection('products');
    loadProducts();
    loadUsers();
});

function openUserModal() {
    document.getElementById('userModal').style.display = 'block';
    loadUsers();
}

function closeUserModal() {
    document.getElementById('userModal').style.display = 'none';
}

window.onclick = function (event) {
    const modal = document.getElementById('userModal');
    if (event.target == modal) {
        closeUserModal();
    }
}

function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');

    if (sectionId === 'products') {
        loadProducts();
    } else if (sectionId === 'cart') {
        loadCart();
    } else if (sectionId === 'orders') {
        loadOrders();
    }
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const content = document.querySelector('.content');
    content.insertBefore(alertDiv, content.firstChild);

    setTimeout(() => alertDiv.remove(), 5000);
}

async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE}/api/products`);
        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        const productsGrid = document.getElementById('productsGrid');
        productsGrid.innerHTML = '';

        data.products.forEach(product => {
            const card = document.createElement('div');
            card.className = 'product-card';

            const stockClass = product.stock < 5 ? 'low' : '';
            const stockText = product.stock === 0 ? 'Brak w magazynie' : `${product.stock} szt. dostępne`;

            card.innerHTML = `
                <h3>${product.name}</h3>
                <div class="price">$${product.price.toFixed(2)}</div>
                <div class="stock ${stockClass}">${stockText}</div>
                <div class="product-actions">
                    <input type="number" id="qty-${product.product_id}" value="1" min="1" max="${product.stock}">
                    <button class="btn-small" onclick="addToCart('${product.product_id}', '${product.name}', ${product.price}, ${product.stock})" ${product.stock === 0 ? 'disabled' : ''}>
                        Dodaj do koszyka
                    </button>
                </div>
            `;

            productsGrid.appendChild(card);
        });
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

async function addToCart(productId, productName, price, stock) {
    const qtyInput = document.getElementById(`qty-${productId}`);
    const quantity = parseInt(qtyInput.value);

    if (quantity <= 0 || quantity > stock) {
        showAlert('Nieprawidłowa ilość', 'error');
        return;
    }

    if (!currentUser) {
        showAlert('Musisz najpierw wybrać użytkownika', 'error');
        showSection('checkout');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/cart/${currentUser.user_id}/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity
            })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        cart[productId] = {
            name: productName,
            price: price,
            quantity: quantity
        };

        showAlert(`${productName} (x${quantity}) dodany do koszyka!`, 'success');
        qtyInput.value = '1';
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

async function loadCart() {
    if (!currentUser) {
        showAlert('Musisz najpierw wybrać użytkownika', 'error');
        showSection('checkout');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/cart/${currentUser.user_id}`);
        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        const cartItems = document.getElementById('cartItems');
        cartItems.innerHTML = '';

        if (!data.items || data.items.length === 0) {
            cartItems.innerHTML = '<div class="cart-empty">Koszyk jest pusty</div>';
            document.getElementById('cartSummary').innerHTML = '';
            return;
        }

        let total = 0;
        data.items.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;

            const itemDiv = document.createElement('div');
            itemDiv.className = 'cart-item';
            itemDiv.innerHTML = `
                <div class="cart-item-info">
                    <h3>${item.name}</h3>
                    <p>Cena: $${item.price.toFixed(2)} × ${item.quantity}</p>
                </div>
                <div style="display: flex; gap: 20px; align-items: center;">
                    <div class="cart-item-total">$${itemTotal.toFixed(2)}</div>
                    <button class="btn-small btn-danger" onclick="removeFromCart('${item.product_id}')">Usuń</button>
                </div>
            `;
            cartItems.appendChild(itemDiv);
        });

        const summaryDiv = document.getElementById('cartSummary');
        summaryDiv.innerHTML = `
            <div class="cart-summary">
                <h3>Podsumowanie</h3>
                <div class="summary-row">
                    <span>Liczba pozycji:</span>
                    <span>${data.items.length}</span>
                </div>
                <div class="summary-row total">
                    <span>Razem:</span>
                    <span>$${total.toFixed(2)}</span>
                </div>
                <button style="width: 100%; margin-top: 20px;" onclick="proceedToCheckout()">Przejdź do kasy</button>
            </div>
        `;
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

async function removeFromCart(productId) {
    if (!currentUser) return;

    try {
        const response = await fetch(`${API_BASE}/api/cart/${currentUser.user_id}/remove`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_id: productId
            })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        delete cart[productId];
        showAlert('Produkt usunięty z koszyka', 'success');
        loadCart();
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

function proceedToCheckout() {
    showSection('checkout');
}

async function selectUser(userId, username) {
    try {
        const response = await fetch(`${API_BASE}/api/users/${userId}`);
        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        currentUser = data.user;

        const display = document.getElementById('currentUserDisplay');
        display.innerHTML = `👤 ${currentUser.username}`;
        document.getElementById('userBadge').classList.add('selected');

        const checkoutDetails = document.getElementById('checkoutUserDetails');
        if (checkoutDetails) {
            checkoutDetails.innerHTML = `
                <div style="background: #f0f7ff; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>Zalogowany jako:</strong> ${currentUser.username} (${currentUser.email})
                    ${currentUser.address ? `<p style="margin-top: 5px;">📍 ${currentUser.address}</p>` : ''}
                </div>
            `;
        }

        showAlert(`Wybrany użytkownik: ${username}`, 'success');
        closeUserModal();

        if (document.getElementById('cart').classList.contains('active')) {
            loadCart();
        }
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE}/api/users`);
        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        const usersListModal = document.getElementById('usersListModal');
        if (usersListModal) {
            usersListModal.innerHTML = '';
            if (!data.users || data.users.length === 0) {
                usersListModal.innerHTML = '<p style="color: #999; text-align: center;">Brak użytkowników. Dodaj ich w panelu Admin.</p>';
            } else {
                data.users.forEach(user => {
                    const userCard = document.createElement('div');
                    userCard.className = 'user-selection-card';
                    if (currentUser && currentUser.user_id === user.user_id) {
                        userCard.classList.add('active');
                    }
                    userCard.onclick = () => selectUser(user.user_id, user.username);
                    userCard.innerHTML = `
                        <div class="user-info">
                            <strong>${user.username}</strong>
                            <span>${user.email}</span>
                        </div>
                        ${currentUser && currentUser.user_id === user.user_id ? '<span class="status-badge">Aktywny</span>' : ''}
                    `;
                    usersListModal.appendChild(userCard);
                });
            }
        }
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

async function createOrder() {
    if (!currentUser) {
        showAlert('Musisz wybrać użytkownika', 'error');
        return;
    }

    const address = document.getElementById('addressInput').value;

    try {
        let updateResponse = null;
        if (address) {
            updateResponse = await fetch(`${API_BASE}/api/users/${currentUser.user_id}/address`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ address: address })
            });

            if (!updateResponse.ok) {
                const errorData = await updateResponse.json();
                throw new Error(errorData.error);
            }
        }

        const response = await fetch(`${API_BASE}/api/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: currentUser.user_id
            })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        showAlert('✅ Zamówienie zostało złożone!', 'success');
        document.getElementById('addressInput').value = '';
        cart = {};

        setTimeout(() => {
            showSection('orders');
        }, 1500);
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

async function loadOrders() {
    if (!currentUser) {
        showAlert('Musisz wybrać użytkownika', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/users/${currentUser.user_id}/orders`);
        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        const ordersList = document.getElementById('ordersList');
        ordersList.innerHTML = '';

        if (!data.orders || data.orders.length === 0) {
            ordersList.innerHTML = '<div style="color: #999; text-align: center; padding: 40px;">Brak zamówień</div>';
            return;
        }

        data.orders.forEach(order => {
            const orderCard = document.createElement('div');
            orderCard.className = 'order-card';

            const statusMap = {
                'pending': 'pending',
                'confirmed': 'confirmed',
                'shipped': 'shipped',
                'delivered': 'delivered',
                'cancelled': 'cancelled'
            };

            const items = order.items.map(item =>
                `<div class="order-item">
                    <span>${item.name}</span>
                    <span>${item.quantity}× @ $${item.price.toFixed(2)} = $${(item.quantity * item.price).toFixed(2)}</span>
                </div>`
            ).join('');

            orderCard.innerHTML = `
                <h3>${order.order_id}</h3>
                <span class="order-status ${statusMap[order.status.toLowerCase()]}">${order.status.toUpperCase()}</span>
                <p style="color: #666; margin-top: 5px;">Data: ${new Date(order.creation_date).toLocaleString('pl-PL')}</p>
                <div class="order-items">
                    ${items}
                    <div class="order-total">Razem: $${order.total_price.toFixed(2)}</div>
                </div>
                <div style="margin-top: 15px;">
                    <select onchange="updateOrderStatus('${order.order_id}', this.value)" style="padding: 8px;">
                        <option value="">Zmień status...</option>
                        <option value="pending">Oczekujące</option>
                        <option value="confirmed">Potwierdzone</option>
                        <option value="shipped">Wysłane</option>
                        <option value="delivered">Dostarczone</option>
                        <option value="cancelled">Anulowane</option>
                    </select>
                    <button class="btn-small" onclick="downloadOrderXML('${order.order_id}')">Pobierz XML</button>
                </div>
            `;

            ordersList.appendChild(orderCard);
        });
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

async function updateOrderStatus(orderId, newStatus) {
    if (!newStatus) return;

    try {
        const response = await fetch(`${API_BASE}/api/orders/${orderId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: newStatus
            })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        showAlert('Status zamówienia zaktualizowany', 'success');
        loadOrders();
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

async function downloadOrderXML(orderId) {
    try {
        const response = await fetch(`${API_BASE}/api/orders/${orderId}/xml`);

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${orderId}.xml`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showAlert('Plik XML pobrany', 'success');
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

async function createProduct() {
    const productId = document.getElementById('productId').value;
    const productName = document.getElementById('productName').value;
    const productPrice = parseFloat(document.getElementById('productPrice').value);
    const productStock = parseInt(document.getElementById('productStock').value);

    if (!productId || !productName || !productPrice || !productStock) {
        showAlert('Uzupełnij wszystkie pola', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/products`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_id: productId,
                name: productName,
                price: productPrice,
                stock: productStock
            })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        showAlert('Produkt dodany pomyślnie!', 'success');
        document.getElementById('productId').value = '';
        document.getElementById('productName').value = '';
        document.getElementById('productPrice').value = '';
        document.getElementById('productStock').value = '';

        loadProducts();
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}

async function createUser() {
    const userId = document.getElementById('userId').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('userEmail').value;

    if (!userId || !username || !email) {
        showAlert('Uzupełnij wymagane pola', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                username: username,
                email: email
            })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        showAlert('Użytkownik utworzony pomyślnie!', 'success');
        document.getElementById('userId').value = '';
        document.getElementById('username').value = '';
        document.getElementById('userEmail').value = '';

        loadUsers();
    } catch (error) {
        showAlert(`Błąd: ${error.message}`, 'error');
    }
}
