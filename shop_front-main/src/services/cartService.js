import api from './AxiosService'

export const cartService = {
    async getCart() {
        return api.get('/cart/')
    },

    async addToCart(productId, quantity = 1) {
        return api.post('/cart/', { product_id: productId, quantity })
    },

    async updateCartItem(itemId, quantity) {
        return api.patch(`/cart/${itemId}`, { quantity })
    },

    async removeFromCart(itemId) {
        return api.delete(`/cart/${itemId}`)
    },

    async clearCart() {
        return api.delete('/cart/clear')
    }
}
