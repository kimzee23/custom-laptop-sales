const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

async function fetchJson<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
  const headers = new Headers(options.headers || {});
  
  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  const res = await fetch(url, {
    ...options,
    headers,
  });

  if (!res.ok) {
    let errorDetail = 'An unexpected error occurred';
    try {
      const errJson = await res.json();
      errorDetail = errJson.detail || errJson.message || JSON.stringify(errJson);
    } catch {
      errorDetail = await res.text() || res.statusText;
    }
    throw new Error(errorDetail);
  }

  return res.json() as Promise<T>;
}

export const api = {
  // -----------------
  // Products & Catalog
  // -----------------
  async getProducts(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null && val !== '') {
        query.append(key, String(val));
      }
    });
    const qs = query.toString();
    return fetchJson<any[]>(`/products${qs ? `?${qs}` : ''}`);
  },

  async getProduct(idOrSlug: string) {
    return fetchJson<any>(`/products/${idOrSlug}`);
  },

  async getCategories() {
    return fetchJson<any[]>('/categories');
  },

  async getBrands() {
    return fetchJson<any[]>('/brands');
  },

  async getPromotions() {
    return fetchJson<any[]>('/promotions');
  },

  // -----------------
  // Configurations & Pricing
  // -----------------
  async getConfigurations(productId: string) {
    return fetchJson<any[]>(`/products/${productId}/configurations`);
  },

  async calculatePrice(payload: {
    product_id: string;
    color_id?: string;
    ram_id?: string;
    storage_id?: string;
    cpu_id?: string;
    gpu_id?: string;
    display_id?: string;
    keyboard_id?: string;
    accessory_ids?: string[];
    artwork?: any;
  }) {
    return fetchJson<any>('/configurations/price', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async createConfiguration(payload: any) {
    return fetchJson<any>('/configurations', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async getSavedBuilds(userId?: string) {
    const qs = userId ? `?user_id=${encodeURIComponent(userId)}` : '';
    return fetchJson<any[]>(`/saved-builds${qs}`);
  },

  async saveBuild(payload: {
    title: string;
    product_id: string;
    total_price: number;
    configuration_snapshot: any;
    specs_summary?: any;
    image_url?: string;
    user_id?: string;
  }) {
    return fetchJson<any>('/saved-builds', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // -----------------
  // Shopping Cart
  // -----------------
  async getCart(sessionId?: string) {
    const headers: Record<string, string> = {};
    if (sessionId) headers['X-Session-ID'] = sessionId;
    return fetchJson<any>('/cart', { headers });
  },

  async addToCart(item: {
    product_id: string;
    quantity: number;
    unit_price?: number;
    configuration_data?: any;
  }, sessionId?: string) {
    const headers: Record<string, string> = {};
    if (sessionId) headers['X-Session-ID'] = sessionId;
    return fetchJson<any>('/cart/items', {
      method: 'POST',
      headers,
      body: JSON.stringify(item),
    });
  },

  async updateCartItem(itemId: string, quantity: number) {
    return fetchJson<any>(`/cart/items/${itemId}`, {
      method: 'PATCH',
      body: JSON.stringify({ quantity }),
    });
  },

  async deleteCartItem(itemId: string) {
    return fetchJson<any>(`/cart/items/${itemId}`, {
      method: 'DELETE',
    });
  },

  // -----------------
  // Orders & Checkout
  // -----------------
  async checkoutOrder(payload: any) {
    return fetchJson<any>('/orders', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async getOrders(params: { customer_email?: string; status?: string; page?: number; limit?: number } = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.append(k, String(v));
    });
    const qs = query.toString();
    return fetchJson<any[]>(`/orders${qs ? `?${qs}` : ''}`);
  },

  async getOrder(idOrNumber: string) {
    return fetchJson<any>(`/orders/${idOrNumber}`);
  },

  // -----------------
  // Payments
  // -----------------
  async getPaymentGateways() {
    return fetchJson<any[]>('/payments/gateways');
  },

  async initializePayment(payload: {
    order_number: string;
    provider: 'PAYSTACK' | 'FLUTTERWAVE' | 'OPAY';
    idempotency_key: string;
    callback_url?: string;
  }) {
    return fetchJson<any>('/payments/initialize', {
      method: 'POST',
      headers: {
        'Idempotency-Key': payload.idempotency_key,
      },
      body: JSON.stringify(payload),
    });
  },

  async verifyPayment(provider: string, reference: string) {
    return fetchJson<any>(`/payments/verify/${provider.toUpperCase()}/${reference}`);
  },

  async mockCompletePayment(reference: string) {
    return fetchJson<any>(`/payments/mock-complete/${reference}`, {
      method: 'POST',
    });
  },

  // -----------------
  // Custom Artwork Upload
  // -----------------
  async uploadArtwork(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return fetchJson<{ success: boolean; image_url: string; filename: string; file_size: number }>('/artwork/upload', {
      method: 'POST',
      body: formData,
    });
  },

  // -----------------
  // Reviews
  // -----------------
  async getReviews(productId?: string) {
    const qs = productId ? `?product_id=${encodeURIComponent(productId)}` : '';
    return fetchJson<any[]>(`/reviews${qs}`);
  },

  async submitReview(payload: { product_id: string; author_name: string; rating: number; comment: string }) {
    return fetchJson<any>('/reviews', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // -----------------
  // Authentication & Accounts
  // -----------------
  async register(data: { name: string; email: string; password: string; phone?: string }) {
    return fetchJson<any>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async login(credentials: { email: string; password: string }) {
    return fetchJson<any>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },

  async getMe(token: string) {
    return fetchJson<any>('/auth/me', {
      headers: { Authorization: `Bearer ${token}` },
    });
  },

  async updateProfile(data: { name?: string; phone?: string; avatar_url?: string }, token: string) {
    return fetchJson<any>('/auth/profile', {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(data),
    });
  },

  async adminLogin(credentials: { email: string; password: string }) {
    return fetchJson<any>('/auth/admin/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },

  // -----------------
  // Admin Portal
  // -----------------
  async getAdminProducts() {
    return fetchJson<any[]>('/admin/products');
  },

  async createAdminProduct(product: any) {
    return fetchJson<any>('/admin/products', {
      method: 'POST',
      body: JSON.stringify(product),
    });
  },

  async updateAdminProduct(id: string, updates: any) {
    return fetchJson<any>(`/admin/products/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
  },

  async getAdminConfigurations() {
    return fetchJson<any[]>('/admin/configurations');
  },

  async addAdminConfiguration(option: any) {
    return fetchJson<any>('/admin/configurations', {
      method: 'POST',
      body: JSON.stringify(option),
    });
  },

  async getAdminOrders(status?: string) {
    const qs = status ? `?status=${encodeURIComponent(status)}` : '';
    return fetchJson<any[]>(`/admin/orders${qs}`);
  },

  async updateAdminOrder(id: string, updates: { status: string; payment_reference?: string; payment_gateway?: string }) {
    return fetchJson<any>(`/admin/orders/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
  },

  async getAdminCustomers() {
    return fetchJson<any[]>('/admin/customers');
  },

  async getAdminAnalytics() {
    return fetchJson<any>('/admin/analytics');
  },
};
