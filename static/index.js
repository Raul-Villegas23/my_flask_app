console.log('Hello from index.js!');

// Set up the scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setClearColor(0xFFFFFF, 0);
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('threejs-container').appendChild(renderer.domElement);

const numberOfSpheres = 20;
const spheres = [];
const boundary = 10; // Define the boundary for the movement of the spheres

// Function to create a sphere with random velocity
function createSphere() {
    const geometry = new THREE.SphereGeometry(1, 32, 32, 0, Math.PI * 2, 0, Math.PI );
    const material = new THREE.MeshBasicMaterial({ color: Math.random() * 0xffffff });
    const sphere = new THREE.Mesh(geometry, material);

    // Random position within the boundary
    sphere.position.x = (Math.random() - 0.5) * 2 * boundary;
    sphere.position.y = (Math.random() - 0.5) * 2 * boundary;
    sphere.position.z = (Math.random() - 0.5) * 2 * boundary;

    // Add random velocity
    sphere.velocity = new THREE.Vector3(
        (Math.random() - 0.5) * 0.2,
        (Math.random() - 0.5) * 0.2,
        (Math.random() - 0.5) * 0.2
    );

    return sphere;
}

// Create and add spheres to the scene
for (let i = 0; i < numberOfSpheres; i++) {
    const sphere = createSphere();
    spheres.push(sphere);
    scene.add(sphere);
}

camera.position.z = 30;

// Function to update sphere position and check boundaries
function updateSpherePosition(sphere) {
    sphere.position.add(sphere.velocity);

    // Check boundaries
    ['x', 'y', 'z'].forEach(axis => {
        if (Math.abs(sphere.position[axis]) > boundary) {
            sphere.velocity[axis] *= -1; // Reverse direction
        }
    });
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    // Update position of each sphere and check for boundaries
    spheres.forEach(updateSpherePosition);

    // Render the scene
    renderer.render(scene, camera);
}

animate();

// Handle window resize
window.addEventListener('resize', () => {
    const width = window.innerWidth;
    const height = window.innerHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
});
