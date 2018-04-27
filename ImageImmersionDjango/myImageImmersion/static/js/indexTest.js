var scene, camera, renderer, allCubes, mouseVector, raycaster;
var click, texture;
 var cssRenderer, cssScene, element, cssObject;
var meshFloor;
var sceneCubes = [];
var keyboard = {};
var player = { height:0.5, speed:0.2, turnSpeed:Math.PI*0.02 };


function init() {
  texture = new THREE.TextureLoader().load( "bg1.jpg" );

  scene = new THREE.Scene();
  mouseVector = new THREE.Vector3();
  // var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
  // camera = new THREE.PerspectiveCamera( 90, window.innerWidth / window.innerHeight, 0.1, 1000 );
  camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 10000);
   camera.position.set(0, 0, -1000);

  container = document.getElementById( 'container' );
	renderer = new THREE.WebGLRenderer();
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	container.appendChild( renderer.domElement );

  camera.position.set(0, player.height, -5);
	camera.lookAt(new THREE.Vector3(0,player.height,0));
  setLighting();
  setSkybox();

  // geometry = new THREE.BoxGeometry( 10, 10, 10 );
	// // Create a MeshBasicMaterial with a loaded texture
	// material = new THREE.MeshBasicMaterial( { map: texture} );
  // material.map.needsUpdate = true;
	// // Combine the geometry and material into a mesh
	// mesh = new THREE.Mesh( geometry, material );
	// // Add the mesh to the scene
	// scene.add( mesh );

  meshFloor = new THREE.Mesh(
    new THREE.PlaneGeometry(10,10, 10,10),
    new THREE.MeshBasicMaterial({color:0xffffff, wireframe:true})
    // material
  );

  meshFloor.rotation.x -= Math.PI / 2; // Rotate the floor 90 degrees
  scene.add(meshFloor);

  // allCubes = [
  //    { name: 'code', position: new THREE.Vector3(-6, 3, 3), url: 'http://gracehuang.net/code.html'},
  //    { name: 'videos', position: new THREE.Vector3( -6, 5, 1), url: 'http://gracehuang.net/me.html'},
  //    { name: 'art', position: new THREE.Vector3(6, 3, 3), url: 'http://gracehuang.net/art.html'},
  //    { name: 'contact', position: new THREE.Vector3( 6, 5, 1), url: 'http://gracehuang.net/photography.html'}
 // 	];

  // console.log("texture:" + JSON.stringify(texture));

  // createClickableBoxes();
  // createMoreBoxes(10);
  // createText();
  createHTMLElem();
  animate();
//  rotate_div();

}

function setSkybox() {
  cubeMap = new THREE.CubeTexture( [] );
  cubeMap.format = THREE.RGBFormat;
  var loader = new THREE.ImageLoader();
  loader.load( 'images/bg1.jpg', function ( image ) {
    var getSide = function ( x, y ) {
      var size = 350;
      var canvas = document.createElement( 'canvas' );
      canvas.width = size;
      canvas.height = size;
      var context = canvas.getContext( '2d' );
      context.drawImage( image, - x * size, - y * size );
      return canvas;
    };
    cubeMap.images[ 0 ] = getSide( 2, 1 ); // px
    cubeMap.images[ 1 ] = getSide( 0, 1 ); // nx
    cubeMap.images[ 2 ] = getSide( 1, 0 ); // py
    cubeMap.images[ 3 ] = getSide( 1, 2 ); // ny
    cubeMap.images[ 4 ] = getSide( 1, 1 ); // pz
    cubeMap.images[ 5 ] = getSide( 3, 1 ); // nz
    cubeMap.needsUpdate = true;
  } );
  console.log("LOADED");
  var cubeShader = THREE.ShaderLib[ 'cube' ];
  cubeShader.uniforms[ 'tCube' ].value = cubeMap;
  var skyBoxMaterial = new THREE.ShaderMaterial( {
    fragmentShader: cubeShader.fragmentShader,
    vertexShader: cubeShader.vertexShader,
    uniforms: cubeShader.uniforms,
    side: THREE.BackSide
  } );
  var material = new THREE.MeshBasicMaterial( {color: 0x00ff00} );
  var skyBox = new THREE.Mesh(
    new THREE.BoxGeometry( 2000 * 5 + 100, 1000 * 5 + 100, 1000 * 5 + 100 ),
    material
  );
  scene.add( skyBox );
}

function setLighting() {
  renderer.shadowMap.enabled = true;
  light = new THREE.DirectionalLight( 0xffffbb, 1 );
  light.position.set( - 30, 30, - 30 );
  light.castShadow = true;
  light.shadow.camera.top = 45;
  light.shadow.camera.right = 40;
  light.shadow.camera.left = light.shadow.camera.bottom = -40;
  light.shadow.camera.near = 1;
  light.shadow.camera.far = 200;
  scene.add( light, new THREE.AmbientLight( 0x888888 ) );
}


function createHTMLElem(){
  console.log("createHTML");
  cssScene = new THREE.Scene();
}


function createText(){
  var text2 = document.createElement('p');
  text2.style.position = 'absolute';
  //text2.style.zIndex = 1;    // if you still don't see the label, try uncommenting this
  text2.style.width = 100;
  text2.style.height = 100;
  text2.style.color = "white";
  // text2.innerHTML = "Hi There! <br> I'm Grace. This is a project I am working on right now. <br>"
  // + " Click on a spinning box to learn more about my work. <br> You can navigate using W, A, S, and D keys, and the left and right arrows.";

  document.body.appendChild(text2);
}

function createClickableBoxes(){
  for (i = 0; i < allCubes.length; i ++) {
    var box =  new THREE.BoxGeometry(1,1,1);
    var wireframe = new THREE.MeshBasicMaterial({color:0xff9999, wireframe:true});
    sceneCubes[i] = new THREE.Mesh(box, wireframe);
    sceneCubes[i].position.x = allCubes[i].position.x;
    sceneCubes[i].position.y = allCubes[i].position.y;
    sceneCubes[i].position.z = allCubes[i].position.z;
    sceneCubes[i].userData = { url: allCubes[i].url };
    scene.add(sceneCubes[i]);
  }
}

function createMoreBoxes(n){
  for (i = 0; i < n; i ++) {
    var box =  new THREE.BoxGeometry(1,1,1);
    var wireframe = new THREE.MeshBasicMaterial({color:0xffffff, wireframe:true});
    var dummyCube = new THREE.Mesh(box, wireframe);
    if (i % 2 == 0) {
      dummyCube.position.x = 6;
    }
    else {
      dummyCube.position.x = -6;
    }
    dummyCube.position.y = Math.random() * 5;
    if (i == 3 || i == 1) {
      dummyCube.position.z = i + n;
    }
    else dummyCube.position.z = (i - 2) * 1.2;
    scene.add(dummyCube);
  }

}

function toXYCoords (pos) {
      var vector = projector.projectVector(pos.clone(), camera);
      vector.x = (vector.x + 1)/2 * window.innerWidth;
      vector.y = -(vector.y - 1)/2 * window.innerHeight;
      return vector;
}


function raycast(){
  raycaster = new THREE.Raycaster();
  raycaster.setFromCamera( mouseVector.clone(), camera ),
  intersects = raycaster.intersectObjects(sceneCubes);

  for ( var i = 0; i < intersects.length; i++ ) {
    intersects[ i ].object.material.color.set( 0xff0000 );

  }
  if (intersects.length > 0) {
        window.open(intersects[0].object.userData.url);
        keyboard[65] = false;
    }
}

function render() {
  requestAnimationFrame( render );
}

function animate(){
  requestAnimationFrame(animate);
  sceneCubes.forEach(function(cube) {
    cube.rotation.x += 0.005;
    cube.rotation.y += 0.006;
  });

  if(keyboard[87]){ // W key
    camera.position.x -= Math.sin(camera.rotation.y) * 0.2;
    camera.position.z -= -Math.cos(camera.rotation.y) * 0.2;
  }
  if(keyboard[83]){ // S key
		camera.position.x += Math.sin(camera.rotation.y) * 0.2;
		camera.position.z += -Math.cos(camera.rotation.y) * 0.2;
	}
  if(keyboard[65]){ // A key
		// Redirect motion by 90 degrees
		camera.position.x += Math.sin(camera.rotation.y + Math.PI/2) * 0.2;
		camera.position.z += -Math.cos(camera.rotation.y + Math.PI/2) * 0.2;
	}
	if(keyboard[68]){ // D key
		camera.position.x += Math.sin(camera.rotation.y - Math.PI/2) * 0.2;
		camera.position.z += -Math.cos(camera.rotation.y - Math.PI/2) * 0.2;
	}

  if(keyboard[37]){ // left arrow key
    camera.rotation.y -= 0.05;
  }
  if(keyboard[39]){ // right arrow key
    camera.rotation.y += 0.05;
  }
  if(keyboard[38]){ // left arrow key
    camera.rotation.x += 0.05;
  }
  if(keyboard[40]){ // right arrow key
    camera.rotation.x -= 0.05;
  }
  if(click) {
    raycast();
    click = false;
  }
  // cssRenderer.render(cssScene, camera);
  renderer.render( scene, camera );

}

function rotate_div(){
  setTimeout(function(){
    var modified_y = (cssObject.rotation.y > 0) ? 0 : Math.PI * 3;
    createjs.Tween.get(cssObject.rotation).to(
      {y: modified_y},
      2000,
      createjs.Ease.backInOut
    ).call(function(){rotate_div();});
  }, 1000);
}


function onMouseMove(event){
  mouseVector.x = 2 * (event.clientX /  window.innerWidth) - 1;
  mouseVector.y = 1 - 2 * ( event.clientY / window.innerHeight);

}
function onClick(event){
  click = true;
}

function keyDown(event){
	keyboard[event.keyCode] = true;
}

function keyUp(event){
	keyboard[event.keyCode] = false;
}
window.addEventListener('click', onClick);
window.addEventListener('mousemove', onMouseMove, false );
window.addEventListener('keydown', keyDown);
window.addEventListener('keyup', keyUp);
window.onload = init;
