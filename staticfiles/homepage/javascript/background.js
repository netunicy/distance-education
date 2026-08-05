class BackgroundEngine {

    constructor(canvasId) {

        this.canvas = document.getElementById(canvasId);

        if (!this.canvas) {
            console.error("Background canvas not found.");
            return;
        }

        this.ctx = this.canvas.getContext("2d");

        this.icons = [];

        this.iconPaths = [

            "/static/images/background/books.png",

            "/static/images/background/greek.png",

            "/static/images/background/math.png",

            "/static/images/background/video.png"

        ];

        this.particles = [];

        this.mouse = {
            x: null,
            y: null
        };

        const isMobile = window.innerWidth <= 768;

        this.config = {

            particleCount: isMobile ? 10 : 50,

            maxDistance: isMobile ? 90 : 140,

            particleColor: "rgba(255,213,79,0.85)",

            lineColor: "rgba(59,94,168,0.10)",

            particleMinRadius: 1,

            particleMaxRadius: 2.5,

            speed: isMobile ? 0.18 : 0.25

        };

        this.resize();

        this.createParticles();

        this.loadIcons();

        this.events();

        this.animate();

    }

    resize() {

        this.canvas.width = window.innerWidth;

        this.canvas.height = window.innerHeight;

    }

    loadIcons() {

        this.icons = [];

        for (const path of this.iconPaths) {

            const img = new Image();

            img.src = path;

            this.icons.push(img);

        }

    }

    events() {

        window.addEventListener("resize", () => {

            this.resize();

        });

        window.addEventListener("mousemove", (e) => {

            this.mouse.x = e.clientX;

            this.mouse.y = e.clientY;

        });

    }

    createParticles() {

        this.particles = [];

        for (let i = 0; i < this.config.particleCount; i++) {

            this.particles.push({

                x: Math.random() * this.canvas.width,

                y: Math.random() * this.canvas.height,

                vx: (Math.random() - 0.5) * this.config.speed,

                vy: (Math.random() - 0.5) * this.config.speed,

                radius:
                    this.config.particleMinRadius +
                    Math.random() *
                    (this.config.particleMaxRadius - this.config.particleMinRadius),

                iconIndex: i % this.iconPaths.length

            });

        }

    }

    updateParticles() {

        for (const p of this.particles) {

            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) {
                p.x = this.canvas.width;
            }

            if (p.x > this.canvas.width) {
                p.x = 0;
            }

            if (p.y < 0) {
                p.y = this.canvas.height;
            }

            if (p.y > this.canvas.height) {
                p.y = 0;
            }

        }

    }

    drawParticles() {

        for (const p of this.particles) {

            this.ctx.beginPath();

            this.ctx.arc(
                p.x,
                p.y,
                p.radius,
                0,
                Math.PI * 2
            );

            // Glow
            this.ctx.shadowBlur = 8;
            this.ctx.shadowColor = "#FFD54F";

            // Χρώμα κουκκίδας
            this.ctx.fillStyle = this.config.particleColor;

            this.ctx.fill();

        }

        // Reset για να μην επηρεάζονται οι γραμμές
        this.ctx.shadowBlur = 0;

    }

    drawConnections() {

        for (let i = 0; i < this.particles.length; i++) {

            const p1 = this.particles[i];

            for (let j = i + 1; j < this.particles.length; j++) {

                const p2 = this.particles[j];

                const dx = p2.x - p1.x;
                const dy = p2.y - p1.y;

                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < this.config.maxDistance) {

                    const opacity =
                        1 - distance / this.config.maxDistance;

                    this.ctx.beginPath();

                    this.ctx.moveTo(p1.x, p1.y);

                    this.ctx.lineTo(p2.x, p2.y);

                    this.ctx.strokeStyle =
                        `rgba(255,213,79,${opacity * 0.15})`;

                    this.ctx.lineWidth = 1;

                    this.ctx.stroke();

                }

            }

        }

    }

    animate() {

        this.ctx.clearRect(

            0,
            0,
            this.canvas.width,
            this.canvas.height

        );

        this.updateParticles();

        this.drawConnections();

        this.drawParticles();

        requestAnimationFrame(() => this.animate());

    }

}

window.addEventListener("DOMContentLoaded", () => {

    new BackgroundEngine("background-canvas");

});