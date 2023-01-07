function initialize() {
	  var myLatlng = new google.maps.LatLng(19.28537333483182,-98.91085725277662); //coordenadas de ubicación
	  var mapOptions = {
	  zoom: 18, //zoom de tu mapa
	  center: myLatlng, //centrar tu mapa
	  scrollwheel: false, //si colocas true en vez de false el usuario podrá hacer scroll dentro del mapa
	  draggable: true, //esta opción es la manito que aparece y es usado para desplazarse en el mapa
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	  };
	  var map = new google.maps.Map(document.getElementById('mapita'), mapOptions);
	  var contentString = '<img src="img/vallelogo.png" width="80" style="display:block;margin:auto;"><p>Valle de Loyola, A.C.</p>';//imagen y dirección
	  var infowindow = new google.maps.InfoWindow({content: contentString});
	  var marker = new google.maps.Marker({
	  position: myLatlng,
	  animation:google.maps.Animation.DROP,
	  icon: 'icono-mapa.png', //icono de mapa
	  map: map
	  });
	  infowindow.open(map,marker);
	  google.maps.event.addListener(marker, 'click', function() {
	  infowindow.open(map,marker);
	  });
}
google.maps.event.addDomListener(window, 'load', initialize);