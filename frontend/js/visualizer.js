// Floor Plan Visualizer using HTML5 Canvas
class FloorPlanVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.floorData = null;
        this.currentPath = [];
        this.animationId = null;
        this.dashOffset = 0;
        
        // Set canvas size
        this.canvas.width = CONFIG.CANVAS_WIDTH;
        this.canvas.height = CONFIG.CANVAS_HEIGHT;
        
        // Bind methods
        this.render = this.render.bind(this);
        this.animatePath = this.animatePath.bind(this);
    }

    // Load floor data and render
    loadFloorData(floorData) {
        this.floorData = floorData;
        this.currentPath = [];
        this.render();
    }

    // Main render function
    render() {
        if (!this.floorData) return;

        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw background
        this.drawBackground();
        
        // Draw rooms
        this.drawRooms();
        
        // Draw doors
        this.drawDoors();
        
        // Draw corridors
        this.drawCorridors();
        
        // Draw path if exists
        if (this.currentPath.length > 0) {
            this.drawPath();
        }
    }

    // Draw background and grid
    drawBackground() {
        this.ctx.fillStyle = CONFIG.COLORS.BACKGROUND;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw subtle grid
        this.ctx.strokeStyle = CONFIG.COLORS.GRID;
        this.ctx.lineWidth = 0.5;
        this.ctx.setLineDash([5, 5]);
        
        for (let x = 0; x <= this.canvas.width; x += 50) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y <= this.canvas.height; y += 50) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
        
        this.ctx.setLineDash([]);
    }

    // Draw all rooms
    drawRooms() {
        if (!this.floorData.rooms) return;

        this.floorData.rooms.forEach(room => {
            this.drawRoom(room);
        });
    }

    // Draw individual room
    drawRoom(room) {
        const { x, y, width, height } = room.bounds;
        const isInPath = this.currentPath.includes(room.id);
        const isStart = this.currentPath.length > 0 && this.currentPath[0] === room.id;
        const isEnd = this.currentPath.length > 0 && this.currentPath[this.currentPath.length - 1] === room.id;

        // Set room color based on state
        if (isStart) {
            this.ctx.fillStyle = CONFIG.COLORS.ROOM_SELECTED;
        } else if (isInPath) {
            this.ctx.fillStyle = CONFIG.COLORS.ROOM_PATH;
        } else {
            this.ctx.fillStyle = CONFIG.COLORS.ROOM;
        }

        // Draw room rectangle with rounded corners
        this.ctx.beginPath();
        this.ctx.roundRect(x, y, width, height, CONFIG.ROOM.CORNER_RADIUS);
        this.ctx.fill();

        // Draw room border
        this.ctx.strokeStyle = CONFIG.COLORS.TEXT;
        this.ctx.lineWidth = CONFIG.ROOM.BORDER_WIDTH;
        this.ctx.stroke();

        // Draw room label
        this.ctx.fillStyle = CONFIG.COLORS.TEXT;
        this.ctx.font = 'bold 12px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(room.id, room.center.x, room.center.y - 10);
        this.ctx.fillText(room.name, room.center.x, room.center.y + 10);

        // Draw START/END labels
        if (isStart) {
            this.ctx.fillStyle = CONFIG.COLORS.ROOM_SELECTED;
            this.ctx.font = 'bold 10px Arial';
            this.ctx.fillText('START', room.center.x, room.center.y + 25);
        } else if (isEnd) {
            this.ctx.fillStyle = CONFIG.COLORS.ROOM_SELECTED;
            this.ctx.font = 'bold 10px Arial';
            this.ctx.fillText('END', room.center.x, room.center.y + 25);
        }
    }

    // Draw all doors
    drawDoors() {
        if (!this.floorData.doors) return;

        this.floorData.doors.forEach(door => {
            this.drawDoor(door);
        });
    }

    // Draw individual door
    drawDoor(door) {
        const { x, y } = door.position;
        
        this.ctx.fillStyle = CONFIG.COLORS.DOOR;
        this.ctx.fillRect(
            x - CONFIG.DOOR.WIDTH / 2,
            y - CONFIG.DOOR.HEIGHT / 2,
            CONFIG.DOOR.WIDTH,
            CONFIG.DOOR.HEIGHT
        );
    }

    // Draw corridors (connections between rooms)
    drawCorridors() {
        if (!this.floorData.doors) return;

        this.ctx.strokeStyle = CONFIG.COLORS.CORRIDOR;
        this.ctx.lineWidth = 2;
        this.ctx.setLineDash([5, 5]);

        this.floorData.doors.forEach(door => {
            if (door.connects && door.connects.length === 2) {
                const room1 = this.floorData.rooms.find(r => r.id === door.connects[0]);
                const room2 = this.floorData.rooms.find(r => r.id === door.connects[1]);
                
                if (room1 && room2) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(room1.center.x, room1.center.y);
                    this.ctx.lineTo(room2.center.x, room2.center.y);
                    this.ctx.stroke();
                }
            }
        });

        this.ctx.setLineDash([]);
    }

    // Draw path between rooms
    drawPath() {
        if (this.currentPath.length < 2) return;

        this.ctx.strokeStyle = CONFIG.COLORS.PATH;
        this.ctx.lineWidth = CONFIG.PATH.WIDTH;
        this.ctx.setLineDash([CONFIG.PATH.DASH_LENGTH, CONFIG.PATH.DASH_GAP]);
        this.ctx.lineDashOffset = -this.dashOffset;

        this.ctx.beginPath();
        
        for (let i = 0; i < this.currentPath.length; i++) {
            const roomId = this.currentPath[i];
            const room = this.floorData.rooms.find(r => r.id === roomId);
            
            if (room) {
                if (i === 0) {
                    this.ctx.moveTo(room.center.x, room.center.y);
                } else {
                    this.ctx.lineTo(room.center.x, room.center.y);
                }
            }
        }
        
        this.ctx.stroke();
        this.ctx.setLineDash([]);
    }

    // Set path and start animation
    setPath(path) {
        this.currentPath = path;
        this.dashOffset = 0;
        
        if (path.length > 1) {
            this.startPathAnimation();
        }
        
        this.render();
    }

    // Start path animation
    startPathAnimation() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        this.animatePath();
    }

    // Animate path drawing
    animatePath() {
        this.dashOffset += CONFIG.PATH.ANIMATION_SPEED;
        this.render();
        
        if (this.dashOffset < 1000) { // Continue animation
            this.animationId = requestAnimationFrame(this.animatePath);
        }
    }

    // Clear current path
    clearPath() {
        this.currentPath = [];
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        this.render();
    }

    // Get room at coordinates (for click detection)
    getRoomAt(x, y) {
        if (!this.floorData || !this.floorData.rooms) return null;

        return this.floorData.rooms.find(room => {
            const { x: roomX, y: roomY, width, height } = room.bounds;
            return x >= roomX && x <= roomX + width && y >= roomY && y <= roomY + height;
        });
    }

    // Handle canvas click
    handleClick(event) {
        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        const room = this.getRoomAt(x, y);
        if (room) {
            // Dispatch custom event for room selection
            const event = new CustomEvent('roomSelected', { detail: { room } });
            this.canvas.dispatchEvent(event);
        }
    }
}

// Add click handler to canvas
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('floor-plan-canvas');
    if (canvas) {
        canvas.addEventListener('click', (event) => {
            // This will be handled by the visualizer instance
        });
    }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FloorPlanVisualizer };
}
