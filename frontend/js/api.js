// API client for communicating with the backend
class API {
    constructor(baseURL = API_CONFIG.BASE_URL) {
        this.baseURL = baseURL;
        this.isOnline = false;
    }

    // Check if backend is online
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/health`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                signal: AbortSignal.timeout(API_CONFIG.TIMEOUT)
            });
            
            if (response.ok) {
                this.isOnline = true;
                return { status: 'online', data: await response.json() };
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.warn('Backend health check failed:', error.message);
            this.isOnline = false;
            return { status: 'offline', error: error.message };
        }
    }

    // Get list of available floors
    async getFloors() {
        if (!this.isOnline) {
            console.log('Using mock data - backend offline');
            return { status: 'offline', data: [{ id: 'building_a_floor_1', name: 'Building A - Floor 1' }] };
        }

        try {
            const response = await fetch(`${this.baseURL}/floors`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                signal: AbortSignal.timeout(API_CONFIG.TIMEOUT)
            });

            if (response.ok) {
                const data = await response.json();
                return { status: 'online', data };
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.error('Failed to fetch floors:', error.message);
            return { status: 'error', error: error.message };
        }
    }

    // Get floor data by ID
    async getFloorData(floorId) {
        if (!this.isOnline) {
            console.log('Using mock floor data - backend offline');
            return { status: 'offline', data: MOCK_FLOOR_DATA };
        }

        try {
            const response = await fetch(`${this.baseURL}/floor/${floorId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                signal: AbortSignal.timeout(API_CONFIG.TIMEOUT)
            });

            if (response.ok) {
                const data = await response.json();
                return { status: 'online', data };
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.error('Failed to fetch floor data:', error.message);
            return { status: 'error', error: error.message };
        }
    }

    // Find path between two rooms
    async findPath(fromRoom, toRoom, floorId = 'building_a_floor_1') {
        if (!this.isOnline) {
            console.log('Using mock path data - backend offline');
            return { status: 'offline', data: MOCK_PATH_DATA };
        }

        try {
            const response = await fetch(`${this.baseURL}/navigate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    from_room: fromRoom,
                    to_room: toRoom,
                    floor_id: floorId
                }),
                signal: AbortSignal.timeout(API_CONFIG.TIMEOUT)
            });

            if (response.ok) {
                const data = await response.json();
                return { status: 'online', data };
            } else {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || `HTTP ${response.status}`);
            }
        } catch (error) {
            console.error('Failed to find path:', error.message);
            return { status: 'error', error: error.message };
        }
    }

    // Retry mechanism for failed requests
    async retryRequest(requestFn, maxAttempts = API_CONFIG.RETRY_ATTEMPTS) {
        for (let attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                const result = await requestFn();
                if (result.status === 'online') {
                    return result;
                }
            } catch (error) {
                console.warn(`Attempt ${attempt} failed:`, error.message);
                if (attempt === maxAttempts) {
                    throw error;
                }
                // Wait before retry (exponential backoff)
                await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
            }
        }
    }

    // Update online status
    updateStatus(isOnline) {
        this.isOnline = isOnline;
    }
}

// Create global API instance
const api = new API();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API, api };
}
