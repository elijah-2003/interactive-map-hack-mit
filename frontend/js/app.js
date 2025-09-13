// Main application logic for Floor Plan Navigator
class FloorPlanApp {
    constructor() {
        this.visualizer = null;
        this.currentFloorData = null;
        this.isBackendOnline = false;
        
        // DOM elements
        this.fromRoomSelect = null;
        this.toRoomSelect = null;
        this.findPathBtn = null;
        this.clearPathBtn = null;
        this.backendStatus = null;
        this.directionsSection = null;
        this.directionsContent = null;
        
        this.init();
    }

    // Initialize the application
    async init() {
        this.setupDOM();
        this.setupEventListeners();
        this.setupKeyboardShortcuts();
        
        // Initialize visualizer
        this.visualizer = new FloorPlanVisualizer('floor-plan-canvas');
        
        // Check backend status and load data
        await this.checkBackendStatus();
        await this.loadFloorData();
    }

    // Setup DOM element references
    setupDOM() {
        this.fromRoomSelect = document.getElementById('from-room');
        this.toRoomSelect = document.getElementById('to-room');
        this.findPathBtn = document.getElementById('find-path');
        this.clearPathBtn = document.getElementById('clear-path');
        this.backendStatus = document.getElementById('backend-status');
        this.directionsSection = document.getElementById('directions');
        this.directionsContent = document.getElementById('directions-content');
    }

    // Setup event listeners
    setupEventListeners() {
        // Button events
        this.findPathBtn.addEventListener('click', () => this.findPath());
        this.clearPathBtn.addEventListener('click', () => this.clearPath());
        
        // Room selection events
        this.fromRoomSelect.addEventListener('change', () => this.onRoomSelectionChange());
        this.toRoomSelect.addEventListener('change', () => this.onRoomSelectionChange());
        
        // Canvas click events
        const canvas = document.getElementById('floor-plan-canvas');
        canvas.addEventListener('click', (event) => this.handleCanvasClick(event));
        
        // Room selection from canvas
        canvas.addEventListener('roomSelected', (event) => this.handleRoomSelection(event.detail.room));
    }

    // Setup keyboard shortcuts
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            // Escape key to clear path
            if (event.key === 'Escape') {
                this.clearPath();
            }
            
            // Ctrl+Enter to find path
            if (event.ctrlKey && event.key === 'Enter') {
                event.preventDefault();
                this.findPath();
            }
        });
    }

    // Check backend status
    async checkBackendStatus() {
        try {
            const result = await api.checkHealth();
            this.isBackendOnline = result.status === 'online';
            this.updateBackendStatus();
        } catch (error) {
            console.error('Failed to check backend status:', error);
            this.isBackendOnline = false;
            this.updateBackendStatus();
        }
    }

    // Update backend status indicator
    updateBackendStatus() {
        if (this.backendStatus) {
            if (this.isBackendOnline) {
                this.backendStatus.textContent = 'Backend Online';
                this.backendStatus.className = 'online';
            } else {
                this.backendStatus.textContent = 'Backend Offline';
                this.backendStatus.className = 'offline';
            }
        }
    }

    // Load floor data
    async loadFloorData() {
        try {
            const result = await api.getFloorData('building_a_floor_1');
            
            if (result.status === 'online' || result.status === 'offline') {
                this.currentFloorData = result.data;
                this.visualizer.loadFloorData(this.currentFloorData);
                this.populateRoomSelects();
            } else {
                throw new Error(result.error || 'Failed to load floor data');
            }
        } catch (error) {
            console.error('Failed to load floor data:', error);
            this.showError('Failed to load floor data. Please refresh the page.');
        }
    }

    // Populate room selection dropdowns
    populateRoomSelects() {
        if (!this.currentFloorData || !this.currentFloorData.rooms) return;

        const rooms = this.currentFloorData.rooms;
        
        // Clear existing options
        this.fromRoomSelect.innerHTML = '<option value="">Select starting room...</option>';
        this.toRoomSelect.innerHTML = '<option value="">Select destination room...</option>';
        
        // Add room options
        rooms.forEach(room => {
            const fromOption = document.createElement('option');
            fromOption.value = room.id;
            fromOption.textContent = `${room.id} - ${room.name}`;
            this.fromRoomSelect.appendChild(fromOption);
            
            const toOption = document.createElement('option');
            toOption.value = room.id;
            toOption.textContent = `${room.id} - ${room.name}`;
            this.toRoomSelect.appendChild(toOption);
        });
    }

    // Handle room selection change
    onRoomSelectionChange() {
        const fromRoom = this.fromRoomSelect.value;
        const toRoom = this.toRoomSelect.value;
        
        // Enable/disable find path button
        this.findPathBtn.disabled = !fromRoom || !toRoom || fromRoom === toRoom;
    }

    // Handle canvas click for room selection
    handleCanvasClick(event) {
        if (this.visualizer) {
            this.visualizer.handleClick(event);
        }
    }

    // Handle room selection from canvas
    handleRoomSelection(room) {
        // Auto-fill room selection if one is empty
        if (!this.fromRoomSelect.value) {
            this.fromRoomSelect.value = room.id;
        } else if (!this.toRoomSelect.value) {
            this.toRoomSelect.value = room.id;
        } else {
            // Cycle through: from -> to -> clear
            if (this.fromRoomSelect.value === room.id) {
                this.toRoomSelect.value = room.id;
                this.fromRoomSelect.value = '';
            } else if (this.toRoomSelect.value === room.id) {
                this.fromRoomSelect.value = '';
                this.toRoomSelect.value = '';
            } else {
                this.fromRoomSelect.value = room.id;
                this.toRoomSelect.value = '';
            }
        }
        
        this.onRoomSelectionChange();
    }

    // Find path between selected rooms
    async findPath() {
        const fromRoom = this.fromRoomSelect.value;
        const toRoom = this.toRoomSelect.value;
        
        if (!fromRoom || !toRoom) {
            this.showError('Please select both starting and destination rooms.');
            return;
        }
        
        if (fromRoom === toRoom) {
            this.showError('Starting and destination rooms cannot be the same.');
            return;
        }

        // Show loading state
        this.setLoadingState(true);
        
        try {
            const result = await api.findPath(fromRoom, toRoom);
            
            if (result.status === 'online' || result.status === 'offline') {
                const pathData = result.data;
                this.visualizer.setPath(pathData.path);
                this.displayDirections(pathData.directions);
                this.showSuccess(`Path found! Distance: ${pathData.distance || 'N/A'} units`);
            } else {
                throw new Error(result.error || 'Failed to find path');
            }
        } catch (error) {
            console.error('Failed to find path:', error);
            this.showError('Failed to find path. Please try again.');
        } finally {
            this.setLoadingState(false);
        }
    }

    // Display step-by-step directions
    displayDirections(directions) {
        if (!directions || directions.length === 0) {
            this.directionsSection.classList.add('hidden');
            return;
        }

        this.directionsContent.innerHTML = '';
        
        directions.forEach((direction, index) => {
            const stepDiv = document.createElement('div');
            stepDiv.className = 'directions-step';
            stepDiv.innerHTML = `
                <span class="step-number">${index + 1}.</span>
                ${direction}
            `;
            this.directionsContent.appendChild(stepDiv);
        });
        
        this.directionsSection.classList.remove('hidden');
    }

    // Clear current path
    clearPath() {
        this.visualizer.clearPath();
        this.directionsSection.classList.add('hidden');
        this.fromRoomSelect.value = '';
        this.toRoomSelect.value = '';
        this.onRoomSelectionChange();
    }

    // Set loading state
    setLoadingState(isLoading) {
        this.findPathBtn.disabled = isLoading;
        
        if (isLoading) {
            this.findPathBtn.innerHTML = '<span class="loading"></span> Finding Path...';
        } else {
            this.findPathBtn.innerHTML = 'Find Path';
        }
    }

    // Show error message
    showError(message) {
        console.error(message);
        // You could implement a toast notification system here
        alert(`Error: ${message}`);
    }

    // Show success message
    showSuccess(message) {
        console.log(message);
        // You could implement a toast notification system here
        console.log(`Success: ${message}`);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FloorPlanApp();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FloorPlanApp };
}
