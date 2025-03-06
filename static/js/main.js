/**
 * SAVDO - Asosiy JavaScript fayli
 */

// Import Bootstrap
import * as bootstrap from "bootstrap"

// DOM yuklangandan keyin ishga tushadi
document.addEventListener("DOMContentLoaded", () => {
  // Savatdagi maxsulotlar sonini yangilash
  updateCartCount()

  // Xabarlarni avtomatik yopish
  setTimeout(() => {
    const alerts = document.querySelectorAll(".alert")
    alerts.forEach((alert) => {
      const bsAlert = new bootstrap.Alert(alert)
      bsAlert.close()
    })
  }, 5000)

  // Rasmlarni kattalashtirish
  const productImages = document.querySelectorAll(".product-image-container img")
  productImages.forEach((img) => {
    img.addEventListener("click", () => {
      // Kattalashtirish logikasi
    })
  })
})

// Savatdagi maxsulotlar sonini yangilash
function updateCartCount() {
  // Bu funksiya server tomonidan yangilanadi
  // Har bir sahifada savat soni ko'rsatiladi
}

// CSRF token olish funksiyasi
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Savatga qo'shish funksiyasi
function addToCart(productId, quantity = 1) {
  fetch("/savatga-qoshish/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      maxsulot_id: productId,
      miqdor: quantity,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Savatdagi maxsulotlar sonini yangilash
        document.getElementById("savat-soni").textContent = data.savat_maxsulotlar_soni

        // Modal xabarini yangilash va ko'rsatish
        document.getElementById("cartModalMessage").textContent = `"${data.maxsulot_nomi}" savatga qo'shildi!`
        new bootstrap.Modal(document.getElementById("addToCartModal")).show()
      }
    })
    .catch((error) => console.error("Error:", error))
}

// Savatni yangilash funksiyasi
function updateCart(productId, quantity) {
  fetch("/savat-yangilash/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      maxsulot_id: productId,
      miqdor: quantity,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Savatdagi maxsulotlar sonini yangilash
        document.getElementById("savat-soni").textContent = data.maxsulotlar_soni

        // Jami narxni yangilash
        document.getElementById("cart-subtotal").textContent = data.jami_narx + " so'm"
        document.getElementById("cart-total").textContent = data.jami_narx + " so'm"
      }
    })
    .catch((error) => console.error("Error:", error))
}

// Savatni tozalash funksiyasi
function clearCart() {
  fetch("/savat-tozalash/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        location.reload()
      }
    })
    .catch((error) => console.error("Error:", error))
}

