"""
Interactive 3D Globe WebGL Component for Dashboard Footer
Renders Three.js globe with Earth texture, atmosphere, and worldwide creator markers.
"""

def get_3d_globe_html() -> str:
    return """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      margin: 0;
      padding: 0;
      overflow: hidden;
      background: transparent;
      font-family: 'Bricolage Grotesque', -apple-system, sans-serif;
    }
    #globe-container {
      width: 100%;
      height: 480px;
      position: relative;
    }
    .marker-label {
      position: absolute;
      background: rgba(255, 255, 255, 0.9);
      border: 1px solid #DCE1EC;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      color: #2D3142;
      pointer-events: none;
      transform: translate(-50%, -100%);
      white-space: nowrap;
      display: none;
    }
    .globe-overlay-tag {
      position: absolute;
      top: 16px;
      left: 20px;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(10px);
      border: 1px solid #DEE3EE;
      border-radius: 9999px;
      padding: 4px 14px;
      font-size: 12px;
      font-weight: 600;
      color: #4E5370;
      display: flex;
      align-items: center;
      gap: 6px;
      pointer-events: none;
    }
    .dot-live {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #48BB78;
    }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
  <div id="globe-container">
    <div class="globe-overlay-tag">
      <div class="dot-live"></div>
      Global Micro-Influencer Discovery Network
    </div>
    <div id="tooltip" class="marker-label"></div>
  </div>

  <script>
    const container = document.getElementById('globe-container');
    const tooltip = document.getElementById('tooltip');
    const width = container.clientWidth || 800;
    const height = 480;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 0, 8);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio || 1);
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enablePan = false;
    controls.enableZoom = false;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.6;
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(10, 10, 10);
    scene.add(dirLight);

    const backLight = new THREE.DirectionalLight(0x88ccff, 0.5);
    backLight.position.set(-10, -5, -10);
    scene.add(backLight);

    // Globe Group
    const globeGroup = new THREE.Group();
    scene.add(globeGroup);

    const radius = 2.4;
    const sphereGeometry = new THREE.SphereGeometry(radius, 64, 64);

    // Load Earth Texture
    const textureLoader = new THREE.TextureLoader();
    const earthTexture = textureLoader.load(
      'https://unpkg.com/three-globe@2.31.0/example/img/earth-blue-marble.jpg',
      function() { renderer.render(scene, camera); }
    );
    const bumpTexture = textureLoader.load(
      'https://unpkg.com/three-globe@2.31.0/example/img/earth-topology.png'
    );

    const sphereMaterial = new THREE.MeshStandardMaterial({
      map: earthTexture,
      bumpMap: bumpTexture,
      bumpScale: 0.05,
      roughness: 0.65,
      metalness: 0.05
    });

    const globe = new THREE.Mesh(sphereGeometry, sphereMaterial);
    globeGroup.add(globe);

    // Atmosphere Glow
    const atmosGeometry = new THREE.SphereGeometry(radius * 1.05, 32, 32);
    const atmosMaterial = new THREE.MeshBasicMaterial({
      color: 0x4da6ff,
      transparent: true,
      opacity: 0.12,
      side: THREE.BackSide
    });
    const atmosphere = new THREE.Mesh(atmosGeometry, atmosMaterial);
    scene.add(atmosphere);

    // Sample Markers
    const markers = [
      { lat: 40.7128, lng: -74.006, label: "New York" },
      { lat: 51.5074, lng: -0.1278, label: "London" },
      { lat: 35.6762, lng: 139.6503, label: "Tokyo" },
      { lat: -33.8688, lng: 151.2093, label: "Sydney" },
      { lat: 48.8566, lng: 2.3522, label: "Paris" },
      { lat: 28.6139, lng: 77.209, label: "New Delhi" },
      { lat: 55.7558, lng: 37.6173, label: "Moscow" },
      { lat: -22.9068, lng: -43.1729, label: "Rio de Janeiro" },
      { lat: 31.2304, lng: 121.4737, label: "Shanghai" },
      { lat: 25.2048, lng: 55.2708, label: "Dubai" },
      { lat: -34.6037, lng: -58.3816, label: "Buenos Aires" },
      { lat: 1.3521, lng: 103.8198, label: "Singapore" },
      { lat: 37.5665, lng: 126.978, label: "Seoul" }
    ];

    function latLngToVector3(lat, lng, r) {
      const phi = (90 - lat) * (Math.PI / 180);
      const theta = (lng + 180) * (Math.PI / 180);
      return new THREE.Vector3(
        -(r * Math.sin(phi) * Math.cos(theta)),
        r * Math.cos(phi),
        r * Math.sin(phi) * Math.sin(theta)
      );
    }

    // Add marker pins to rotating globe group
    markers.forEach(m => {
      const pos = latLngToVector3(m.lat, m.lng, radius * 1.01);
      const pinGeom = new THREE.SphereGeometry(0.045, 16, 16);
      const pinMat = new THREE.MeshBasicMaterial({ color: 0x5B638A });
      const pinMesh = new THREE.Mesh(pinGeom, pinMat);
      pinMesh.position.copy(pos);
      globeGroup.add(pinMesh);

      // Pulse ring
      const ringGeom = new THREE.RingGeometry(0.05, 0.08, 16);
      const ringMat = new THREE.MeshBasicMaterial({ color: 0x6C8CA5, side: THREE.DoubleSide });
      const ringMesh = new THREE.Mesh(ringGeom, ringMat);
      ringMesh.position.copy(pos.clone().multiplyScalar(1.002));
      ringMesh.lookAt(0, 0, 0);
      globeGroup.add(ringMesh);
    });

    // Animation Loop
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      const w = container.clientWidth;
      camera.aspect = w / height;
      camera.updateProjectionMatrix();
      renderer.setSize(w, height);
    });
  </script>
</body>
</html>
"""
